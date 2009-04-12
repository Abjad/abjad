from abjad import *


def test_detach_subtree_01( ):
   '''Detach sequential from score tree.'''

   t = Voice(run(2))
   t.insert(1, Container(run(2)))
   pitchtools.diatonicize(t)
   Beam(t.leaves)
   Glissando(t.leaves)

   r'''\new Voice {
      c'8 [ \glissando
      {
         d'8 \glissando
         e'8 \glissando
      }
      f'8 ]
   }'''

   sequential = t[1]
   receipt = detach_subtree(t[1])

   r'''\new Voice {
      c'8 [ \glissando
      f'8 ]
   }'''

   assert check.wf(t)
   assert check.wf(sequential)
   assert t.format == "\\new Voice {\n\tc'8 [ \\glissando\n\tf'8 ]\n}"


def test_detach_subtree_02( ):
   '''Detach leaf from score tree.'''

   t = Voice(run(2))
   t.insert(1, Container(run(2)))
   pitchtools.diatonicize(t)
   Beam(t.leaves)
   Glissando(t.leaves)

   r'''\new Voice {
      c'8 [ \glissando
      {
         d'8 \glissando
         e'8 \glissando
      }
      f'8 ]
   }'''

   leaf = t.leaves[1]
   receipt = detach_subtree(leaf)

   r'''\new Voice {
      c'8 [ \glissando
      {
         e'8 \glissando
      }
      f'8 ]
   }'''

   assert check.wf(t)
   assert check.wf(leaf)
   assert t.format == "\\new Voice {\n\tc'8 [ \\glissando\n\t{\n\t\te'8 \\glissando\n\t}\n\tf'8 ]\n}"
