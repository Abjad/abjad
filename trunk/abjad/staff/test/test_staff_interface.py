from abjad import *


def test_staff_interface_01( ):
   '''Staff changes work on the first note of a staff.'''

   piano = PianoStaff(Staff(scale(4)) * 2)
   piano.parallel = True
   piano[0].name = 'RH'
   piano[1].name = 'LH'
   piano[0][0].staff.forced = piano[1]

   r'''\new PianoStaff <<
      \context Staff = "RH" {
         \change Staff = LH
         c'8
         \change Staff = RH
         d'8
         e'8
         f'8
      }
      \context Staff = "LH" {
         c'8
         d'8
         e'8
         f'8
      }
   >>'''

   assert piano.format == '\\new PianoStaff <<\n\t\\context Staff = "RH" {\n\t\t\\change Staff = LH\n\t\tc\'8\n\t\t\\change Staff = RH\n\t\td\'8\n\t\te\'8\n\t\tf\'8\n\t}\n\t\\context Staff = "LH" {\n\t\tc\'8\n\t\td\'8\n\t\te\'8\n\t\tf\'8\n\t}\n>>'


def test_staff_interface_02( ):
   '''Staff changes work on middle notes of a staff.'''

   piano = PianoStaff(Staff(scale(4)) * 2)
   piano.parallel = True
   piano[0].name = 'RH'
   piano[1].name = 'LH'
   piano[0][1].staff.forced = piano[1]

   r'''\new PianoStaff <<
      \context Staff = "RH" {
         c'8
         \change Staff = LH
         d'8
         \change Staff = RH
         e'8
         f'8
      }
      \context Staff = "LH" {
         c'8
         d'8
         e'8
         f'8
      }
   >>'''

   assert piano.format == '\\new PianoStaff <<\n\t\\context Staff = "RH" {\n\t\tc\'8\n\t\t\\change Staff = LH\n\t\td\'8\n\t\t\\change Staff = RH\n\t\te\'8\n\t\tf\'8\n\t}\n\t\\context Staff = "LH" {\n\t\tc\'8\n\t\td\'8\n\t\te\'8\n\t\tf\'8\n\t}\n>>'


def test_staff_interface_03( ):
   '''Staff changes work on the last note of a staff.'''

   piano = PianoStaff(Staff(scale(4)) * 2)
   piano.parallel = True
   piano[0].name = 'RH'
   piano[1].name = 'LH'
   piano[0][-1].staff.forced = piano[1]

   r'''\new PianoStaff <<
      \context Staff = "RH" {
         c'8
         d'8
         e'8
         \change Staff = LH
         f'8
         \change Staff = RH
      }
      \context Staff = "LH" {
         c'8
         d'8
         e'8
         f'8
      }
   >>'''

   assert piano.format == '\\new PianoStaff <<\n\t\\context Staff = "RH" {\n\t\tc\'8\n\t\td\'8\n\t\te\'8\n\t\t\\change Staff = LH\n\t\tf\'8\n\t\t\\change Staff = RH\n\t}\n\t\\context Staff = "LH" {\n\t\tc\'8\n\t\td\'8\n\t\te\'8\n\t\tf\'8\n\t}\n>>'


def test_staff_interface_04( ):
   '''Adjacent staff-changed notes format nicely.'''

   piano = PianoStaff(Staff(scale(4)) * 2)
   piano.parallel = True
   piano[0].name = 'RH'
   piano[1].name = 'LH'
   for note in piano[0][:2]:
      note.staff.forced = piano[1]

   r'''\new PianoStaff <<
      \context Staff = "RH" {
         \change Staff = LH
         c'8
         d'8
         \change Staff = RH
         e'8
         f'8
      }
      \context Staff = "LH" {
         c'8
         d'8
         e'8
         f'8
      }
   >>'''

   assert piano.format == '\\new PianoStaff <<\n\t\\context Staff = "RH" {\n\t\t\\change Staff = LH\n\t\tc\'8\n\t\td\'8\n\t\t\\change Staff = RH\n\t\te\'8\n\t\tf\'8\n\t}\n\t\\context Staff = "LH" {\n\t\tc\'8\n\t\td\'8\n\t\te\'8\n\t\tf\'8\n\t}\n>>'
