from abjad import *
from abjad.helpers.give_dominant_spanners_to import \
   _give_dominant_spanners_to


def test_give_dominant_spanners_to_01( ):
   '''Find spanners that dominate donor_components.
      Apply dominant spanners to recipient_components.
      Withdraw donor_components from spanners.
      The operation can mangle spanners.
      Remove donor_components from parentage immediately after.'''

   t = Voice(scale(4))
   Crescendo(t[:])
   Beam(t[:2])
   Slur(t[1:3])

   r'''\new Voice {
      c'8 [ \<
      d'8 ] (
      e'8 )
      f'8 \!
   }'''

   recipient = Voice(run(3, Rational(1, 16)))
   Beam(recipient)

   r'''\new Voice {
      c'16 [
      c'16
      c'16 ]
   }'''

   _give_dominant_spanners_to(t[1:3], recipient[:])

   "Voice t is now ..."

   r'''\new Voice {
      c'8 [ \<
      d'8 ]
      e'8
      f'8 \!
   }'''

   "Both crescendo and beam are now discontiguous."

   assert not check(t)
   assert t.format == "\\new Voice {\n\tc'8 [ \\<\n\td'8 ]\n\te'8\n\tf'8 \\!\n}"
   
   "Recipient is now ..."

   r'''\new Voice {
      c'16 [ (
      c'16
      c'16 ] )
   }'''

   "Slur is contiguous but recipient participates in discont. cresc."

   assert not check(recipient)
   assert recipient.format == "\\new Voice {\n\tc'16 [ (\n\tc'16\n\tc'16 ] )\n}"
