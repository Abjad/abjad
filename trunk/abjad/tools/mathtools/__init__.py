'''Abjad mathtools.

   Package imports no other Abjad modules, save rational.
   Add no modules to mathtools with intrapackage imports.
   Higher level modules with intrapackage imports should go elsewhere.'''

from abjad.tools.importtools._package_import import _package_import

_package_import(__path__[0], globals( ))


