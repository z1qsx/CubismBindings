"""Triggers generation of C# bindings"""

import sys
from pylib.options import Options
from pylib.csgen import CSGen

if __name__ == '__main__':
    opts = Options.parse(sys.argv[1:])
    gen = CSGen.createfrom(opts)
    gen.run()
