# Copyright(c) Live2D Inc. All rights reserved.
# 
# Use of this source code is governed by the Live2D Open Software license
# that can be found at http://live2d.com/eula/live2d-open-software-license-agreement_en.html.


"""Provides interface for generating JavaScript bindings vie Emscripten and TypeScript"""


import os
from pylib.genbase import GenBase


class JSGen(GenBase):
    """Generates TypeScript bindings"""


    @classmethod
    def createfrom(cls, options):
        """Creates instance"""
        return cls(options)


    def __init__(self, options):
        """Initializes instance"""
        # Patch options.
        options.yamlfiles.append('Live2DCubismCoreEMSCRIPTEN.yaml')
        options.infiles.append(os.path.join('js', 'make.py'))
        options.infiles.append(os.path.join('js', '.in', 'live2dcubismcore.ts'))
        options.infiles.append(os.path.join('js', '.in', 'Live2DCubismCoreEMSCRIPTEN.c'))
        # Let base initialize.
        super(JSGen, self).__init__(options)
        # Assemble 'ccalls'
        ccallsreturn = []
        ccallsvoid = []
        for func in self.data['funcs']:
            ccall = _toccalldata(func)
            if 'returnType' in ccall:
                ccallsreturn.append(ccall)
            else:
                ccallsvoid.append(ccall)
        self.data['ccalls'] = {}
        self.data['ccalls']['return'] = ccallsreturn
        self.data['ccalls']['void'] = ccallsvoid
        # Patch props
        for clsname, cls in self.data['clsmap'].items():
            # Add TypeScript type and Emscripten heap info
            for prop in cls['props']:
                prop['proptstype'] = _totstype(prop['proptype'])
                # ... and patch getters
                prop['propget'] = _toccallfullname(prop['propget'])
                if 'propgetlength' in prop:
                    prop['propgetlength'] = _toccallfullname(prop['propgetlength'])
                if 'propgetlength2' in prop:
                    prop['propgetlength2'] = _toccallfullname(prop['propgetlength2'])
            for prop in cls['scalararrayprops']:
                prop['propemheapbuffer'] = _toemheapbuffer(prop['propscalartype'])
                if 'proplengthfactor' in prop:
                    prop['proplengthfactor'] = ' * ' + prop['proplengthfactor']
            for prop in cls['scalararray2props']:
                prop['proparray1tstype'] = _totstype(prop['proptype'][:-1])
                prop['propemheapbuffer'] = _toemheapbuffer(prop['propscalartype'])
                if 'proplengthfactor' in prop:
                    prop['proplengthfactor'] = ' * ' + prop['proplengthfactor']
                if 'proplength2factor' in prop:
                    prop['proplength2factor'] = ' * ' + prop['proplength2factor']
            # Patch functions
            for func in cls['funcs']:
                func['ccall'] = _toccallfullname(func['entry'])
            # Additionally patch parts, parameters, and drawables.
            if clsname in ['parameters', 'parts', 'drawables']:
                # Validate getter signatures
                for prop in cls['props']:
                    assert(len(prop['args']) == 1)
                    assert(prop['args'][0]['type'] == 'Model')
                for func in cls['funcs']:
                    assert(len(func['args']) == 1)
                    assert(func['args'][0]['type'] == 'Model')
        # Initialize 'getter' classes data.
        self.data['modelgetterclss'] = [
            self.data['clsmap']['parameters'],
            self.data['clsmap']['parts'],
            self.data['clsmap']['drawables']
        ]
        self.data['modelgetterclss'][0]['clsdoc'] = 'Cubism model parameters'
        self.data['modelgetterclss'][0]['clsname'] = 'Parameters'
        self.data['modelgetterclss'][1]['clsdoc'] = 'Cubism model parts'
        self.data['modelgetterclss'][1]['clsname'] = 'Parts'
        self.data['modelgetterclss'][2]['clsdoc'] = 'Cubism model drawables'
        self.data['modelgetterclss'][2]['clsname'] = 'Drawables'


def _toccallname(entry):
    """Converts entry name to ccall name"""
    assert(entry.startswith('csm'))
    return entry[3].lower() + entry[4:]


def _toccallfullname(entry):
    """Converts entry name to ccall name including namespace"""
    return '_csm.' + _toccallname(entry)


# TODO Improve 'naive' type-deduction if necessary
def _toccalltype(type):
    """Converts Core YAML type to TypeScript type"""
    return 'number'


def _toccalldata(func):
    """Returns ccall data dictionary"""
    data = {
        'doc': func['doc'],
        'name': _toccallname(func['entry']),
        'entry': func['entry']
    }
    # Prepare args data
    if 'args' in func:
        args = ''
        argTypes = ''
        argNames = ''
        for arg in func['args']:
            args += ('%s: %s, ' % (arg['name'], _toccalltype(arg['type'])))
            argTypes += ('"%s", ' % (_toccalltype(arg['type'])))
            argNames += ('%s, ' % (arg['name']))
        data['args'] = args[:-2]
        data['argTypes'] = argTypes[:-2]
        data['argNames'] = argNames[:-2]
    # Prepare return data
    if 'return' in func:
        data['returnType'] = _toccalltype(func['return']['type'])
    return data


# TODO Improve 'naive' type-deduction if necessary
def _toemheapbuffer(scalartype):
    """Gets Emscripten heap buffer view based on type."""
    if scalartype.startswith('Uint8'):
        return '_em.HEAPU8.buffer'
    elif scalartype.startswith('Uint16'):
        return '_em.HEAPU16.buffer'
    elif scalartype.startswith('Uint32'):
        return '_em.HEAPU32.buffer'
    elif scalartype.startswith('Int32'):
        return '_em.HEAP32.buffer'
    elif scalartype.startswith('Float32'):
        return '_em.HEAPF32.buffer'
    assert(False)


# TODO Improve 'naive' type-deduction if necessary
def _totstype(proptype):
    """Converts Core YAML type to TypeScript type"""
    if proptype.endswith('Array2'):
        return ('Array<%s>' % (_totstype(proptype[:-1])))
    if proptype.endswith('Array'):
        if proptype.startswith('String'):
            return 'Array<string>'
        else:
            return proptype
    return 'number'
