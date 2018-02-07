# Copyright(c) Live2D Inc. All rights reserved.
# 
# Use of this source code is governed by the Live2D Open Software license
# that can be found at http://live2d.com/eula/live2d-open-software-license-agreement_en.html.


"""Provides interface for generating C# bindings."""

from __future__ import print_function
import os
from pylib.genbase import GenBase


class CSGen(GenBase):
    """Generates TypeScript bindings."""


    @classmethod
    def createfrom(cls, options):
        """Creates instance."""
        return cls(options)


    def __init__(self, options):
        """Initializes instance."""
        # Patch options.
        options.infiles.append(os.path.join('cs', 'Live2D', 'Cubism', 'Core', 'Unmanaged', 'ByteExtensionMethods.cs'))
        options.infiles.append(os.path.join('cs', 'Live2D', 'Cubism', 'Core', 'Unmanaged', 'CubismCoreDll.cs'))
        options.infiles.append(os.path.join('cs', 'Live2D', 'Cubism', 'Core', 'Unmanaged', 'CubismUnmanagedArrayView.cs'))
        options.infiles.append(os.path.join('cs', 'Live2D', 'Cubism', 'Core', 'Unmanaged', 'CubismUnmanagedDrawables.cs'))
        options.infiles.append(os.path.join('cs', 'Live2D', 'Cubism', 'Core', 'Unmanaged', 'CubismUnmanagedMemory.cs'))
        options.infiles.append(os.path.join('cs', 'Live2D', 'Cubism', 'Core', 'Unmanaged', 'CubismUnmanagedMoc.cs'))
        options.infiles.append(os.path.join('cs', 'Live2D', 'Cubism', 'Core', 'Unmanaged', 'CubismUnmanagedModel.cs'))
        options.infiles.append(os.path.join('cs', 'Live2D', 'Cubism', 'Core', 'Unmanaged', 'CubismUnmanagedCanvasInformation.cs'))
        options.infiles.append(os.path.join('cs', 'Live2D', 'Cubism', 'Core', 'Unmanaged', 'CubismUnmanagedParameters.cs'))
        options.infiles.append(os.path.join('cs', 'Live2D', 'Cubism', 'Core', 'Unmanaged', 'CubismUnmanagedParts.cs'))
        # Let base initialize.
        super(CSGen, self).__init__(options)
        # Patch functions
        for func in self.data['funcs']:
            func['funccsentry'] = 'CubismCoreDll.' + func['entry'].replace('csm', '')
            func['funccsreturntype'] = 'void' if not 'return' in func else _tocstype(func['return']['type'])
        # Assemble DLL entries
        dllentries = []
        for func in self.data['funcs']:
            dllentries.append(_todllentrydata(func))
        self.data['dllentries'] = dllentries
        # Assemble array views
        arrayviews = {}
        for func in self.data['funcs']:
            # Skip void functions
            if not 'return' in func:
                continue
            # Skip non-scalar 1D arrays
            if func['return']['type'] == 'StringArray':
                continue
            if not 'Array' in func['return']['type']:
                continue
            # Make sure array view types are unique
            if func['return']['type'].split('Array')[0] in arrayviews:
                continue
            arrayviews[func['return']['type'].split('Array')[0]] = _toarrayviewdata(func)
        self.data['arrayviews'] = []
        for view in arrayviews.itervalues():
            self.data['arrayviews'].append(view)
        # Patch props
        for cls in self.data['clsmap'].itervalues():
            for prop in cls['props']:
                prop['propcstype'] = _tocstype(prop['proptype'])
                prop['propget'] = prop['funccsentry']
                if 'propgetlength' in prop:
                    prop['propgetlength'] = 'CubismCoreDll.' + prop['propgetlength'].replace('csm', '')
                    if 'proplengthfactor' in prop:
                        prop['proplengthfactor'] = ' * ' + prop['proplengthfactor']
                if 'propgetlength2' in prop:
                    prop['propcstype1d'] = prop['propcstype'].replace('[]', '')
                    prop['propgetlength2'] = 'CubismCoreDll.' + prop['propgetlength2'].replace('csm', '')
                    if 'proplength2factor' in prop:
                        prop['proplength2factor'] = ' * ' + prop['proplength2factor']
        # Provide shorthands for parameters, parts, and drawables
        self.data['parameters'] = self.data['clsmap']['parameters']
        self.data['parts'] = self.data['clsmap']['parts']
        self.data['drawables'] = self.data['clsmap']['drawables']


def _todllentrydata(func):
    """Converts function to DLL entry data."""


    data = {
        'funcdoc': func['doc'],
        'entrypoint': func['entry'],
        'funcname': func['entry'].replace('csm', '')
    }
    if 'args' in func:
        args = ''
        for arg in func['args']:
            args += ('%s %s, ' % (_todllentrytype(arg['type']), arg['name']))
        data['args'] = args[:-2]
    else:
        data['args'] = ''
    data['returntype'] = _todllentrytype(func['return']['type']) if 'return' in func else 'void'
    # HACK Patch unsafe...
    if '*' in data['args'] or '*' in data['returntype']:
        data['returntype'] = 'unsafe ' + data['returntype']
    return data


# TODO Improve naive deduction if necessary
def _todllentrytype(type):
    """Converts type to DLL entry type."""


    if type == 'StringArray':
        return 'char **'
    elif type.endswith('Array2'):
        return ('%s*' % _todllentrytype(type[:-1]))
    elif type.endswith('Array'):
        return ('%s*' % _todllentrytype(type[:-(len('Array'))]))
    elif type in ['Moc', 'Model', 'Memory']:
        return 'IntPtr'
    elif type == 'Int32':
        return 'int'
    elif type == 'Uint8':
        return 'Byte'
    elif type == 'Uint16':
        return 'ushort'
    elif type == 'Uint32':
        return 'uint'
    elif type == 'Float32':
        return 'float'
    print(type)
    assert(False)


def _toarrayviewdata(func):
    """Converts func to array view data."""


    type = _todllentrytype(func['return']['type'].split('Array')[0])
    data = {
        'Name': type[0].upper() + type[1:],
        'type': type
    }
    return data


# TODO Improve naive deduction if necessary
def _tocstype(type):
    """Converts type to DLL entry type."""


    if type == 'StringArray':
        return 'string[]'
    elif type.endswith('Array2'):
        return ('%s[]' % _tocstype(type[:-1]))
    elif type.endswith('Array'):
        name = _todllentrytype(type[:-(len('Array'))])
        name = name[0].upper() + name[1:]
        return ('CubismUnmanaged%sArrayView' % (name))
    elif type in ['Moc', 'Model', 'Memory']:
        return 'IntPtr'
    elif type == 'Int32':
        return 'int'
    elif type == 'Uint8':
        return 'Byte'
    elif type == 'Uint16':
        return 'ushort'
    elif type == 'Uint32':
        return 'uint'
    elif type == 'Float32':
        return 'float'
    print(type)
    assert(False)