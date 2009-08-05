from abjad import *
from abjad.tools import construct


def test_iterate_chained_contents_01( ):
   '''Iterate toplevel contents with tie chains in place of leaves.'''

   t = Staff(construct.notes(0, [(5, 32)] * 4))
   t.insert(4, FixedDurationTuplet((2, 8), construct.run(3)))
   pitchtools.diatonicize(t)

   r'''
   \new Staff {
      c'8 ~
      c'32
      \times 2/3 {
         d'8
         e'8
         f'8
      }
      g'8 ~
      g'32
      a'8 ~
      a'32
      b'8 ~
      b'32
   }
   '''

   chained_contents = list(iterate.chained_contents(t))

   assert chained_contents[0] == t[0].tie.chain
   assert chained_contents[1] == t[2].tie.chain
   assert chained_contents[2] is t[4]
   assert chained_contents[3] == t[5].tie.chain
   assert chained_contents[4] == t[7].tie.chain
