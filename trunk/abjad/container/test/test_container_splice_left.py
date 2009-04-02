from abjad import *


def test_container_splice_01( ):
   '''Splice tuplet left of tuplet.'''

   t = Voice([FixedDurationTuplet((2, 8), scale(3))])
   Beam(t[0])
   result = t[0].splice_left([FixedDurationTuplet((2, 8), scale(3))])

   r'''\new Voice {
      \times 2/3 {
         c'8 [
         d'8
         e'8
      }
      \times 2/3 {
         c'8
         d'8
         e'8 ]
      }
   }'''

   assert check(t)
   assert result == t[:]
   assert t.format == "\\new Voice {\n\t\\times 2/3 {\n\t\tc'8 [\n\t\td'8\n\t\te'8\n\t}\n\t\\times 2/3 {\n\t\tc'8\n\t\td'8\n\t\te'8 ]\n\t}\n}"


def test_container_splice_02( ):
   '''Splice left of container with underspanners.'''

   t = Voice(Container(run(2)) * 2)
   diatonicize(t)
   Beam(t.leaves)
   result = t[1].splice_left([Note(2.5, (1, 8))])

   r'''\new Voice {
           {
                   c'8 [
                   d'8
           }
           dqs'8
           {
                   e'8
                   f'8 ]
           }
   }'''

   assert check(t)
   assert t.format == "\\new Voice {\n\t{\n\t\tc'8 [\n\t\td'8\n\t}\n\tdqs'8\n\t{\n\t\te'8\n\t\tf'8 ]\n\t}\n}"
   assert result == t[1:]
