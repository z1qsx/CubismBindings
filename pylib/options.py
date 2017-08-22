# Copyright(c) Live2D Inc. All rights reserved.
# 
# Use of this source code is governed by the Live2D Open Software license
# that can be found at http://live2d.com/eula/live2d-open-software-license-agreement_en.html.


"""Provides convenience class for dealing with generator options"""


import os
import yaml


class Options(object):
    """"Provides convenience"""


    @classmethod
    def parse(cls, args = None):
        """Creates instance"""
        outdir = args[0] if args else None
        if not outdir:
            outdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'out')
        return Options(outdir)


    def __init__(self, outdir):
        """Initializes instance"""
        # Initialize directory shorthands.
        selfdir = os.path.dirname(os.path.realpath(__file__))
        self.datadir = os.path.join(selfdir, '..', 'data')
        self.templatesdir = os.path.join(self.datadir, 'templates')
        self.outdir = outdir
        # Initialize containers.
        self.yamlfiles = ['Live2DCubismCore.yaml']
        self.infiles = []
