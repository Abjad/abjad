from abjad import *
import py.test


def test_InstrumentMark_format_01( ):

   staff = Staff("c'8 d'8 e'8 f'8")
   contexttools.InstrumentMark('Flute', 'Fl.')(staff)

   r'''
   \new Staff {
      \set Staff.instrumentName = \markup { Flute }
      \set Staff.shortInstrumentName = \markup { Fl. }
      c'8
      d'8
      e'8
      f'8
   }
   '''

   assert staff.format == "\\new Staff {\n\t\\set Staff.instrumentName = \\markup { Flute }\n\t\\set Staff.shortInstrumentName = \\markup { Fl. }\n\tc'8\n\td'8\n\te'8\n\tf'8\n}"


def test_InstrumentMark_format_02( ):
   py.test.skip('make work with container names.')

   flute_staff = Staff("c'8 d'8 e'8 f'8")
   #flute_staff.name = 'Flute'
   contexttools.InstrumentMark('Flute', 'Fl.')(flute_staff)
   violin_staff = Staff("c'8 d'8 e'8 f'8")
   #violin_staff.name = 'Violin'
   contexttools.InstrumentMark('Violin', 'Vn.')(violin_staff)
   staff_group = scoretools.StaffGroup([flute_staff, violin_staff])
   score = Score([staff_group])
