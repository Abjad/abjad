'''Fuse score objects.

   This package depends on:

      * core components
      * navigator/dfs.py
      * tools/check
      * tools/iterate
      * tools/construct
      * tools/containertools
      * tools/componenttools'''

from abjad.tools.imports.import_functions_in_package_to_namespace import \
   _import_functions_in_package_to_namespace

_import_functions_in_package_to_namespace(__path__[0], globals( ))
