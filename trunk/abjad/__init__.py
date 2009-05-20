from abjad.tools.imports.import_functions_in_package_to_namespace import \
   _import_functions_in_package_to_namespace

_skip = ['book', 'checks', 'demos', 'documentation', 'scr', 'svn', 'tools', 'test']
_import_functions_in_package_to_namespace(__path__[0], globals( ), _skip)

from abjad.tools.io import *
from abjad.tools import *
