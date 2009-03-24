from abjad import *
from abjad.helpers.give_my_attached_spanners_to import \
   _give_my_attached_spanners_to


def test_give_my_attached_spanners_to_01( ):
   '''Not composer-safe.'''

   t = Voice(Sequential(run(2)) * 2)
   diatonicize(t)
   Beam(t[:])

   r'''\new Voice {
      {
         c'8 [
         d'8
      }
      {
         e'8
         f'8 ]
      }
   }'''

   donor = t[0]
   recipient = Voice(scale(4))
   _give_my_attached_spanners_to(donor, [recipient])
   
   "Container t is now ..."

   r'''\new Voice {
      {
         c'8
         d'8
      }
      {
         e'8
         f'8 ]
      }
   }'''

   assert t.format == "\\new Voice {\n\t{\n\t\tc'8\n\t\td'8\n\t}\n\t{\n\t\te'8\n\t\tf'8 ]\n\t}\n}"

   "Recipient container is now ..."

   r'''\new Voice {
      c'8 [
      d'8
      e'8
      f'8
   }'''

   assert recipient.format == "\\new Voice {\n\tc'8 [\n\td'8\n\te'8\n\tf'8\n}"

   "Both container t and recipient container carry discontiguous spanners."

   assert not check(t)
   assert not check(recipient)
