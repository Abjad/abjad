from abjad import *


def test_clef_copy_01( ):
   '''Explicit clefs copy.'''
   staff = Staff([Note(n, (1, 8)) for n in range(8)])
   staff[0].clef = 'treble'
   staff[4].clef = 'bass'
   staff.extend(staff.copy(0, 1))
   assert staff.tester.testAll(ret = True)
   assert staff.format == "\\new Staff {\n\t\\clef treble\n\tc'8\n\tcs'8\n\td'8\n\tef'8\n\t\\clef bass\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n\t\\clef treble\n\tc'8\n\tcs'8\n}"
   assert [str(note.clef) for note in staff] == [
      'treble', 'treble', 'treble', 'treble',
      'bass', 'bass', 'bass', 'bass',
      'treble', 'treble']
   '''
   \new Staff {
           \treble
           c'8
           cs'8
           d'8
           ef'8
           \bass
           e'8
           f'8
           fs'8
           g'8
           \treble
           c'8
           cs'8
   }
   '''


def test_clef_copy_02( ):
   '''Implicit clefs do not copy.'''
   staff = Staff([Note(n, (1, 8)) for n in range(8)])
   staff[0].clef = 'treble'
   staff[4].clef = 'bass'
   staff.extend(staff.copy(2, 3))
   assert staff.tester.testAll(ret = True)
   assert staff.format == "\\new Staff {\n\t\\clef treble\n\tc'8\n\tcs'8\n\td'8\n\tef'8\n\t\\clef bass\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n\td'8\n\tef'8\n}"
   assert [str(note.clef) for note in staff] == [
      'treble', 'treble', 'treble', 'treble',
      'bass', 'bass', 'bass', 'bass', 'bass', 'bass']
   '''
   \new Staff {
        \treble
        c'8
        cs'8
        d'8
        ef'8
        \bass
        e'8
        f'8
        fs'8
        g'8
        d'8
        ef'8
   }
   '''
