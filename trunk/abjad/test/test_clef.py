from abjad import *


def test_clef_01( ):
   '''Clef defaults to treble.'''
   staff = Staff([Note(n, (1, 8)) for n in range(8)])
   for note in staff:
      assert note.clef.name == 'treble'
   

def test_clef_02( ):
   '''Clefs carry over to notes following.'''
   staff = Staff([Note(n, (1, 8)) for n in range(8)])
   staff[0].clef = 'treble'
   for note in staff:
      assert note.clef.name == 'treble'


def test_clef_03( ):
   '''Clef defaults to treble;
      clefs carry over to notes following.'''
   staff = Staff([Note(n, (1, 8)) for n in range(8)])
   staff[4].clef = 'bass'
   for i, note in enumerate(staff):
      if i in (0, 1, 2, 3):
         note.clef.name == 'treble'
      else:
         note.clef.name == 'bass'


def test_clef_04( ):
   '''Clefs carry over to notes following.'''
   staff = Staff([Note(n, (1, 8)) for n in range(8)])
   staff[0].clef = 'treble'
   staff[4].clef = 'bass'
   assert [note.clef.name for note in staff] == \
      ['treble', 'treble', 'treble', 'treble', 
      'bass', 'bass', 'bass', 'bass']


def test_clef_05( ):
   '''None cancels an explicit clef.'''
   staff = Staff([Note(n, (1, 8)) for n in range(8)])
   staff[0].clef = 'treble'
   staff[4].clef = 'bass'
   staff[4].clef = None
   for note in staff:
      assert note.clef.name == 'treble'
      

def test_clef_06( ):
   '''None has no effect on an unassigned clef.'''
   staff = Staff([Note(n, (1, 8)) for n in range(8)])
   for note in staff:
      note.clef = None
   for note in staff:
      assert note.clef.name == 'treble'


def test_clef_07( ):
   '''Redudant clefs are allowed.'''
   staff = Staff([Note(n, (1, 8)) for n in range(8)])
   staff[0].clef = 'treble'
   staff[4].clef = 'treble'
   assert staff.format == "\\new Staff {\n\t\\clef treble\n\tc'8\n\tcs'8\n\td'8\n\tef'8\n\t\\clef treble\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n}"
   '''
   Staff {
           \clef treble
           c'8
           cs'8
           d'8
           ef'8
           \clef treble
           e'8
           f'8
           fs'8
           g'8
   }
   '''
