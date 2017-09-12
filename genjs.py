"""Triggers generation of TypeScript bindings"""

import sys
from pylib.options import Options
from pylib.jsgen import JSGen

if __name__ == '__main__':
    opts = Options.parse(sys.argv[1:])
    gen = JSGen.createfrom(opts)
    gen.run()
