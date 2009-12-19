from abjad import *


def test_clef_interface_copy_01( ):
   '''Forced clefs copy.'''

   t = Staff(construct.run(8))
   pitchtools.chromaticize(t)
   t[0].clef.forced = Clef('treble')
   t[4].clef.forced = Clef('bass')
   t.extend(clonewp.with_parent(t[:2]))

   r'''\new Staff {
           \clef "treble"
           c'8
           cs'8
           d'8
           ef'8
           \clef "bass"
           e'8
           f'8
           fs'8
           g'8
           \clef "treble"
           c'8
           cs'8
   }'''

   assert check.wf(t)
   assert t[0].clef.effective == Clef('treble')
   assert t[1].clef.effective == Clef('treble')
   assert t[2].clef.effective == Clef('treble')
   assert t[3].clef.effective == Clef('treble')
   assert t[4].clef.effective == Clef('bass')
   assert t[5].clef.effective == Clef('bass')
   assert t[6].clef.effective == Clef('bass')
   assert t[7].clef.effective == Clef('bass')
   assert t[8].clef.effective == Clef('treble')
   assert t[9].clef.effective == Clef('treble')

   assert t.format == '''\\new Staff {\n\t\\clef "treble"\n\tc'8\n\tcs'8\n\td'8\n\tef'8\n\t\\clef "bass"\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n\t\\clef "treble"\n\tc'8\n\tcs'8\n}'''


def test_clef_interface_copy_02( ):
   '''Implicit clefs do not copy.'''

   t = Staff(construct.run(8))
   pitchtools.chromaticize(t)
   t[0].clef.forced = Clef('treble')
   t[4].clef.forced = Clef('bass')
   t.extend(clonewp.with_parent(t[2:4]))

   assert check.wf(t)
   assert t[0].clef.effective == Clef('treble')
   assert t[1].clef.effective == Clef('treble')
   assert t[2].clef.effective == Clef('treble')
   assert t[3].clef.effective == Clef('treble')
   assert t[4].clef.effective == Clef('bass')
   assert t[5].clef.effective == Clef('bass')
   assert t[6].clef.effective == Clef('bass')
   assert t[7].clef.effective == Clef('bass')
   assert t[8].clef.effective == Clef('bass')
   assert t[9].clef.effective == Clef('bass')

   assert t.format == '''\\new Staff {\n\t\\clef "treble"\n\tc'8\n\tcs'8\n\td'8\n\tef'8\n\t\\clef "bass"\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n\td'8\n\tef'8\n}'''
