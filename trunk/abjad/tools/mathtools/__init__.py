'''Abjad mathtools.

   Package imports no other Abjad modules, save rational.
   Add no modules to mathtools with intrapackage imports.
   Higher level modules with intrapackage imports should go elsewhere.
'''

from abjad.tools import importtools

importtools.import_structured_package(__path__[0], globals())

_documentation_section = 'manual'
