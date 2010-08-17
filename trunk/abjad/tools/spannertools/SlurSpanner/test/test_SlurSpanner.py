from abjad import *

def test_SlurSpanner_01( ):
   '''Slur spanner can attach to a container.'''
   t = Voice(macros.scale(4))
   s = spannertools.SlurSpanner(t)
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

def test_SlurSpanner_02( ):
   '''Slur spanner can attach to leaves.'''
   t = Voice(macros.scale(4))
   s = spannertools.SlurSpanner(t[:])
   assert len(t.spanners.attached) == 0
   for leaf in t.leaves:
      assert leaf.spanners.attached == set([s])
   assert t.format == "\\new Voice {\n\tc'8 (\n\td'8\n\te'8\n\tf'8 )\n}"


def test_SlurSpanner_03( ):
   '''Position may be set to None, 'neutral', 'up' or 'down'. '''
   t = Staff(notetools.make_repeated_notes(4))
   p = spannertools.SlurSpanner(t[:])
   p.position = None
   assert t.format == "\\new Staff {\n\tc'8 (\n\tc'8\n\tc'8\n\tc'8 )\n}"
   p.misc.slur_up = None
   assert t.format == "\\new Staff {\n\t\\slurUp\n\tc'8 (\n\tc'8\n\tc'8\n\tc'8 )\n}"
   del(p.misc.slur_up)
   p.misc.slur_down = None
   assert t.format == "\\new Staff {\n\t\\slurDown\n\tc'8 (\n\tc'8\n\tc'8\n\tc'8 )\n}"
   del(p.misc.slur_down)
   p.misc.slur_neutral = None
   assert t.format == "\\new Staff {\n\t\\slurNeutral\n\tc'8 (\n\tc'8\n\tc'8\n\tc'8 )\n}"

   r'''
   \new Staff {
           \slurNeutral
           c'8 (
           c'8
           c'8
           c'8 )
   }
   '''
