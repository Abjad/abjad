from abjad import *


def test_LilyFile_format_01( ):
   '''Naked strings format correctly.
   '''

   staff = Staff(macros.scale(4))
   lily_file = lilyfiletools.make_basic_lily_file(staff)
   lily_file.insert(0, r'\include "external-settings-file.ly"')

   r'''
   \include "external-settings-file.ly"

   \header { }

   \layout { }

   \paper { }

   \new Staff {
      c'8
      d'8
      e'8
      f'8
   }
   '''

   assert lily_file.format == '\\include "external-settings-file.ly"\n\n\\header { }\n\n\\layout { }\n\n\\paper { }\n\n\\new Staff {\n\tc\'8\n\td\'8\n\te\'8\n\tf\'8\n}'
