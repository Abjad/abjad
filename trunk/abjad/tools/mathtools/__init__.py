'''Abjad mathtools.

   Package imports no other Abjad modules, save rational.
   Add no modules to mathtools with intrapackage imports.
   Higher level modules with intrapackage imports should go elsewhere.'''

from abjad.tools.importtools._import_public_names_from_path_into_namespace import _import_public_names_from_path_into_namespace

_import_public_names_from_path_into_namespace(__path__[0], globals( ))


