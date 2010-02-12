from abjad import *


def test_clef_interface_effective_01( ):
   '''Clef defaults to treble.'''
   t = Staff(construct.scale(8))
   for note in t:
      assert note.clef.effective == Clef('treble')
   

def test_clef_interface_effective_02( ):
   '''Clefs carry over to notes following.'''
   t = Staff(construct.scale(8))
   t[0].clef.forced = Clef('treble')
   for note in t:
      assert note.clef.effective == Clef('treble')


def test_clef_interface_effective_03( ):
   '''Clef defaults to treble;
      clefs carry over to notes following.'''
   t = Staff(construct.scale(8))
   t[4].clef.forced = Clef('bass')
   for i, note in enumerate(t):
      if i in (0, 1, 2, 3):
         note.clef.effective == Clef('treble')
      else:
         note.clef.effective == Clef('bass')


def test_clef_interface_effective_04( ):
   '''Clefs carry over to notes following.'''
   t = Staff(construct.scale(8))
   t[0].clef.forced = Clef('treble')
   t[4].clef.forced = Clef('bass')
   assert [note.clef.effective for note in t] == \
      [Clef(name) for name in ['treble', 'treble', 'treble', 'treble', 
      'bass', 'bass', 'bass', 'bass']]


def test_clef_interface_effective_05( ):
   '''None cancels an explicit clef.'''
   t = Staff(construct.scale(8))
   t[0].clef.forced = Clef('treble')
   t[4].clef.forced = Clef('bass')
   t[4].clef.forced = None
   for note in t:
      assert note.clef.effective == Clef('treble')
      

def test_clef_interface_effective_06( ):
   '''None has no effect on an unassigned clef.'''
   t = Staff(construct.scale(8))
   for note in t:
      note.clef.forced = None
   for note in t:
      assert note.clef.effective == Clef('treble')


def test_clef_interface_effective_07( ):
   '''Redudant clefs are allowed.'''

   t = Staff(construct.run(8))
   pitchtools.chromaticize(t)
   t[0].clef.forced = Clef('treble')
   t[4].clef.forced = Clef('treble')

   r'''Staff {
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
   }'''

   assert check.wf(t)
   assert t.format == '''\\new Staff {\n\t\\clef "treble"\n\tc'8\n\tcs'8\n\td'8\n\tef'8\n\t\\clef "treble"\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n}'''


def test_clef_interface_effective_08( ):
   '''Clefs with transposition are allowed and work as expected.'''

   t = Staff(construct.run(8))
   pitchtools.chromaticize(t)
   t[0].clef.forced = Clef('treble_8')
   t[4].clef.forced = Clef('treble')

   r'''\new Staff {
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
   }'''

   assert check.wf(t)
   assert t.format == '\\new Staff {\n\t\\clef "treble_8"\n\tc\'8\n\tcs\'8\n\td\'8\n\tef\'8\n\t\\clef "treble"\n\te\'8\n\tf\'8\n\tfs\'8\n\tg\'8\n}'


def test_clef_interface_effective_09( ):
   '''Setting and then clearing works as expected.'''

   t = Staff(construct.scale(4))
   t[0].clef.forced = Clef('alto')
   t[0].clef.forced = None

   for leaf in t:
      assert leaf.clef.effective == Clef('treble')


