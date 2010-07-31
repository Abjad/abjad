from abjad import *


def test_Container_splice_01( ):
   '''Splice tuplet after tuplet.'''

   t = Voice([FixedDurationTuplet((2, 8), macros.scale(3))])
   Beam(t[0])
   result = t[-1].splice([FixedDurationTuplet((2, 8), macros.scale(3))])

   r'''
   \new Voice {
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
   }
   '''

   assert componenttools.is_well_formed_component(t)
   assert result == t[:]
   assert t.format == "\\new Voice {\n\t\\times 2/3 {\n\t\tc'8 [\n\t\td'8\n\t\te'8\n\t}\n\t\\times 2/3 {\n\t\tc'8\n\t\td'8\n\t\te'8 ]\n\t}\n}"


def test_Container_splice_02( ):
   '''Splice after container with underspanners.'''

   t = Voice(Container(leaftools.make_repeated_notes(2)) * 2)
   Beam(t.leaves)
   result = t[0].splice([Note(2.5, (1, 8))])

   r'''
   \new Voice {
      {
         c'8 [
         c'8
      }
      dqs'8
      {
         c'8
         c'8 ]
      }
   }
   '''

   assert componenttools.is_well_formed_component(t)
   assert t.format == "\\new Voice {\n\t{\n\t\tc'8 [\n\t\tc'8\n\t}\n\tdqs'8\n\t{\n\t\tc'8\n\t\tc'8 ]\n\t}\n}"
   assert result == t[0:2]
