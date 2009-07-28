from abjad.tools.imports.import_functions_in_package_to_namespace import \
   _import_functions_in_package_to_namespace

_skip = [
   'book', 'checks', 'demos', 'documentation', 'scr', '.svn', 'test', 'tools']

_import_functions_in_package_to_namespace(__path__[0], globals( ), _skip)

## remove AccidentalInterface, BeamInterface, etc.
for _key in globals( ).keys( ):
   if _key.endswith('Interface'):
      del(globals( )[_key])

from abjad.tools.io import *
from abjad.tools import *
