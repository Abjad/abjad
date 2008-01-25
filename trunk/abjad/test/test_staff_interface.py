from abjad import *


def test_staff_interface_01( ):
   '''Staff changes work on the first note of a staff.'''
   piano = Staff(Staff([Note(n, (1, 8)) for n in range(8)]) * 2)
   piano.invocation = ('PianoStaff', 'piano')
   piano.brackets = 'double-angle'
   piano[0].invocation = ('Staff', 'RH')
   piano[1].invocation = ('Staff', 'LH')
   piano[0][0].staff = piano[1]
   assert piano.format == "\\new PianoStaff = piano <<\n\t\\new Staff = RH {\n\t\t\\change Staff = LH\n\t\tc'8\n\t\t\\change Staff = RH\n\t\tcs'8\n\t\td'8\n\t\tef'8\n\t\te'8\n\t\tf'8\n\t\tfs'8\n\t\tg'8\n\t}\n\t\\new Staff = LH {\n\t\tc'8\n\t\tcs'8\n\t\td'8\n\t\tef'8\n\t\te'8\n\t\tf'8\n\t\tfs'8\n\t\tg'8\n\t}\n>>"
   '''
   \new PianoStaff = piano <<
           \new Staff = RH {
                   \change Staff = LH
                   c'8
                   \change Staff = RH
                   cs'8
                   d'8
                   ef'8
                   e'8
                   f'8
                   fs'8
                   g'8
           }
           \new Staff = LH {
                   c'8
                   cs'8
                   d'8
                   ef'8
                   e'8
                   f'8
                   fs'8
                   g'8
           }
   >>
   '''


def test_staff_interface_02( ):
   '''Staff changes work on middle notes of a staff.'''
   piano = Staff(Staff([Note(n, (1, 8)) for n in range(8)]) * 2)
   piano.invocation = ('PianoStaff', 'piano')
   piano.brackets = 'double-angle'
   piano[0].invocation = ('Staff', 'RH')
   piano[1].invocation = ('Staff', 'LH')
   piano[0][1].staff = piano[1]
   assert piano.format == "\\new PianoStaff = piano <<\n\t\\new Staff = RH {\n\t\tc'8\n\t\t\\change Staff = LH\n\t\tcs'8\n\t\t\\change Staff = RH\n\t\td'8\n\t\tef'8\n\t\te'8\n\t\tf'8\n\t\tfs'8\n\t\tg'8\n\t}\n\t\\new Staff = LH {\n\t\tc'8\n\t\tcs'8\n\t\td'8\n\t\tef'8\n\t\te'8\n\t\tf'8\n\t\tfs'8\n\t\tg'8\n\t}\n>>"
   '''
   \new PianoStaff = piano <<
           \new Staff = RH {
                   c'8
                   \change Staff = LH
                   cs'8
                   \change Staff = RH
                   d'8
                   ef'8
                   e'8
                   f'8
                   fs'8
                   g'8
           }
           \new Staff = LH {
                   c'8
                   cs'8
                   d'8
                   ef'8
                   e'8
                   f'8
                   fs'8
                   g'8
           }
   >>
   '''


def test_staff_interface_03( ):
   '''Staff changes work on the last note of a staff.'''
   piano = Staff(Staff([Note(n, (1, 8)) for n in range(8)]) * 2)
   piano.invocation = ('PianoStaff', 'piano')
   piano.brackets = 'double-angle'
   piano[0].invocation = ('Staff', 'RH')
   piano[1].invocation = ('Staff', 'LH')
   piano[0][-1].staff = piano[1]
   assert piano.format == "\\new PianoStaff = piano <<\n\t\\new Staff = RH {\n\t\tc'8\n\t\tcs'8\n\t\td'8\n\t\tef'8\n\t\te'8\n\t\tf'8\n\t\tfs'8\n\t\t\\change Staff = LH\n\t\tg'8\n\t\t\\change Staff = RH\n\t}\n\t\\new Staff = LH {\n\t\tc'8\n\t\tcs'8\n\t\td'8\n\t\tef'8\n\t\te'8\n\t\tf'8\n\t\tfs'8\n\t\tg'8\n\t}\n>>"
   '''
   \new PianoStaff = piano <<
           \new Staff = RH {
                   c'8
                   cs'8
                   d'8
                   ef'8
                   e'8
                   f'8
                   fs'8
                   \change Staff = LH
                   g'8
                   \change Staff = RH
           }
           \new Staff = LH {
                   c'8
                   cs'8
                   d'8
                   ef'8
                   e'8
                   f'8
                   fs'8
                   g'8
           }
   >>
   '''


def test_staff_interface_04( ):
   '''Adjacent staff-changed notes format nicely.'''
   piano = Staff(Staff([Note(n, (1, 8)) for n in range(8)]) * 2)
   piano.invocation = ('PianoStaff', 'piano')
   piano.brackets = 'double-angle'
   piano[0].invocation = ('Staff', 'RH')
   piano[1].invocation = ('Staff', 'LH')
   for note in piano[0][ : 4]:
      note.staff = piano[1]
   assert piano.format == "\\new PianoStaff = piano <<\n\t\\new Staff = RH {\n\t\t\\change Staff = LH\n\t\tc'8\n\t\tcs'8\n\t\td'8\n\t\tef'8\n\t\t\\change Staff = RH\n\t\te'8\n\t\tf'8\n\t\tfs'8\n\t\tg'8\n\t}\n\t\\new Staff = LH {\n\t\tc'8\n\t\tcs'8\n\t\td'8\n\t\tef'8\n\t\te'8\n\t\tf'8\n\t\tfs'8\n\t\tg'8\n\t}\n>>"
   '''
   \new PianoStaff = piano <<
           \new Staff = RH {
                   \change Staff = LH
                   c'8
                   cs'8
                   d'8
                   ef'8
                   \change Staff = RH
                   e'8
                   f'8
                   fs'8
                   g'8
           }
           \new Staff = LH {
                   c'8
                   cs'8
                   d'8
                   ef'8
                   e'8
                   f'8
                   fs'8
                   g'8
           }
   >>
   '''
