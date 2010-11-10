'''Score manipulation tools.

   This package depends on:

      * tools/componenttools
      * tools/spannertools
'''


from abjad.tools.importtools._import_public_names_from_path_into_namespace import _import_public_names_from_path_into_namespace

_import_public_names_from_path_into_namespace(__path__[0], globals( ))

from GrandStaff import GrandStaff
from PianoStaff import PianoStaff
from StaffGroup import StaffGroup
