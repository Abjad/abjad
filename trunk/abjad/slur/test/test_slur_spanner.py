from abjad import *

def test_slur_spanner_01( ):
   '''Slur spanner can attach to a container.'''
   t = Voice(scale(4))
   s = Slur(t)
   assert t.spanners.attached == set([s])
   assert t.format == "\\new Voice {\n\tc'8 (\n\td'8\n\te'8\n\tf'8 )\n}"
   r'''
   \new Voice {
           c'8 (
           d'8
           e'8
           f'8 )
   }
   '''

def test_slur_spanner_02( ):
   '''Slur spanner can attach to leaves.'''
   t = Voice(scale(4))
   s = Slur(t[:])
   assert len(t.spanners.attached) == 0
   for leaf in t.leaves:
      assert leaf.spanners.attached == set([s])
   assert t.format == "\\new Voice {\n\tc'8 (\n\td'8\n\te'8\n\tf'8 )\n}"
