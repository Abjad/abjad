from abjad import *
import py.test


def test_ClefInterface_effective_01( ):
   '''Clef defaults to treble.'''
   t = Staff(macros.scale(8))
   for note in t:
      #assert note.clef.effective == stafftools.Clef('treble')
      assert note.clef.effective is None
   

def test_ClefInterface_effective_02( ):
   '''Clefs carry over to notes following.'''
   t = Staff(macros.scale(8))
   #t[0].clef.forced = stafftools.Clef('treble')
   marktools.ClefMark('treble')(t)
   for note in t:
      #assert note.clef.effective == stafftools.Clef('treble')
      assert marktools.get_effective_clef(note) == marktools.ClefMark('treble')


def test_ClefInterface_effective_03( ):
   '''Clef defaults to none.
   Clefs carry over to notes following.'''
   t = Staff(macros.scale(8))
   #t[4].clef.forced = stafftools.Clef('bass')
   marktools.ClefMark('bass')(t[4])
   for i, note in enumerate(t):
      if i in (0, 1, 2, 3):
         #note.clef.effective == stafftools.Clef('treble')
         note.clef.effective is None
      else:
         #note.clef.effective == stafftools.Clef('bass')
         note.clef.effective == marktools.ClefMark('bass')


def test_ClefInterface_effective_04( ):
   '''Clefs carry over to notes following.'''
   t = Staff(macros.scale(8))
   #t[0].clef.forced = stafftools.Clef('treble')
   #t[4].clef.forced = stafftools.Clef('bass')
   marktools.ClefMark('treble')(t[0])
   marktools.ClefMark('bass')(t[4])
   #assert [note.clef.effective for note in t] == \
   #   [stafftools.Clef(name) for name in ['treble', 'treble', 'treble', 'treble', 
   #   'bass', 'bass', 'bass', 'bass']]
   assert [note.clef.effective for note in t] == \
      [marktools.ClefMark(name) for name in ['treble', 'treble', 'treble', 'treble', 
      'bass', 'bass', 'bass', 'bass']]


def test_ClefInterface_effective_05( ):
   '''None cancels an explicit clef.'''
   t = Staff(macros.scale(8))
   #t[0].clef.forced = stafftools.Clef('treble')
   #t[4].clef.forced = stafftools.Clef('bass')
   #t[4].clef.forced = None
   marktools.ClefMark('treble')(t[0])
   marktools.ClefMark('bass')(t[4])
   clef = marktools.get_effective_clef(t[4])
   clef.detach_mark( )
   for note in t:
      #assert note.clef.effective == stafftools.Clef('treble')
      assert note.clef.effective == marktools.ClefMark('treble')
      

def test_ClefInterface_effective_06( ):
   '''None has no effect on an unassigned clef.'''
   py.test.skip('deprecated.')
   t = Staff(macros.scale(8))
   for note in t:
      note.clef.forced = None
   for note in t:
      assert note.clef.effective == stafftools.Clef('treble')


def test_ClefInterface_effective_07( ):
   '''Redudant clefs are allowed.'''

   t = Staff(notetools.make_repeated_notes(8))
   macros.chromaticize(t)
   #t[0].clef.forced = stafftools.Clef('treble')
   #t[4].clef.forced = stafftools.Clef('treble')
   marktools.ClefMark('treble')(t[0])
   marktools.ClefMark('treble')(t[4])

   r'''
   Staff {
           \clef "treble"
           c'8
           cs'8
           d'8
           ef'8
           \clef "treble"
           e'8
           f'8
           fs'8
           g'8
   }
   '''

   assert componenttools.is_well_formed_component(t)
   assert t.format == '''\\new Staff {\n\t\\clef "treble"\n\tc'8\n\tcs'8\n\td'8\n\tef'8\n\t\\clef "treble"\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n}'''


def test_ClefInterface_effective_08( ):
   '''Clefs with transposition are allowed and work as expected.'''

   t = Staff(notetools.make_repeated_notes(8))
   macros.chromaticize(t)
   #t[0].clef.forced = stafftools.Clef('treble_8')
   #t[4].clef.forced = stafftools.Clef('treble')
   marktools.ClefMark('treble_8')(t[0])
   marktools.ClefMark('treble')(t[4])

   r'''
   \new Staff {
           \clef "treble_8"
           c'8
           cs'8
           d'8
           ef'8
           \clef "treble"
           e'8
           f'8
           fs'8
           g'8
   }
   '''

   assert componenttools.is_well_formed_component(t)
   assert t.format == '\\new Staff {\n\t\\clef "treble_8"\n\tc\'8\n\tcs\'8\n\td\'8\n\tef\'8\n\t\\clef "treble"\n\te\'8\n\tf\'8\n\tfs\'8\n\tg\'8\n}'


def test_ClefInterface_effective_09( ):
   '''Setting and then clearing works as expected.'''

   t = Staff(macros.scale(4))
   #t[0].clef.forced = stafftools.Clef('alto')
   #t[0].clef.forced = None
   marktools.ClefMark('alto')(t[0])
   clef = marktools.get_effective_clef(t[0])
   clef.detach_mark( )

   for leaf in t:
      #assert leaf.clef.effective == stafftools.Clef('treble')
      assert leaf.clef.effective is None
