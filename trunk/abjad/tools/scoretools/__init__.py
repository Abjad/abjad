'''Score manipulation tools.

   This package depends on:

      * tools/componenttools
      * tools/spannertools
'''


from abjad.tools.importtools._package_import import _package_import

_package_import(__path__[0], globals( ))

from StaffGroup import GrandStaff
from StaffGroup import PianoStaff
from StaffGroup import StaffGroup
