from abjad import *
from abjad.tools.componenttools.give_music_to import _give_music_to
import py.test


def test_componenttools_give_music_to_01( ):
   '''Give spanned music from donor to recipient.
      Helper is not composer-safe and results here in bad spanners.'''

   t = Voice(Container(construct.run(2)) * 2)
   pitchtools.diatonicize(t)
   Beam(t.leaves)

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
   recipient = Voice([ ])
   _give_music_to([donor], recipient)

   "Container t is now ..."
   
   r'''\new Voice {
      {
      }
      {
         e'8
         f'8 ]
      }
   }'''

   "Container t carries discontiguous spanners."
 
   assert not check.wf(t)
   assert t.format == "\\new Voice {\n\t{\n\t}\n\t{\n\t\te'8\n\t\tf'8 ]\n\t}\n}"

   "Recipient container is now ..."

   r'''\new Voice {
      c'8 [
      d'8
   }'''

   "Recipient container carries discontiguous spanners."

   assert not check.wf(recipient)
   assert recipient.format == "\\new Voice {\n\tc'8 [\n\td'8\n}"


def test_componenttools_give_music_to_02( ):
   '''When donor is leaf, do nothing.'''

   donor = Note(0, (1, 8))
   recipient = Voice([ ])
  
   _give_music_to([donor], recipient)

   assert check.wf(donor)
   assert donor.format == "c'8"

   assert check.wf(recipient)
   assert recipient.format == '\\new Voice {\n}'


def test_componenttools_give_music_to_03( ):
   '''When recipient is unable to accept donated music,
      raise MusicContentsError.'''

   donor = Voice(construct.scale(4))
   recipient = Voice(construct.scale(4))

   assert py.test.raises(
      MusicContentsError, '_give_music_to([donor], recipient)')
