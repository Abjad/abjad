from abjad import *
from abjad.tools.componenttools._give_music_to import _give_music_to
import py.test


def test_componenttools_give_music_to_01( ):
   '''Give spanned music from donor to recipient.
      Helper is not composer-safe and results here in bad spanners.'''

   t = Voice(Container(notetools.make_repeated_notes(2)) * 2)
   macros.diatonicize(t)
   BeamSpanner(t.leaves)

   r'''
   \new Voice {
      {
         c'8 [
         d'8
      }
      {
         e'8
         f'8 ]
      }
   }
   '''

   donor = t[0]
   recipient = Voice([ ])
   _give_music_to([donor], recipient)

   "Container t is now ..."
   
   r'''
   \new Voice {
      {
      }
      {
         e'8
         f'8 ]
      }
   }
   '''

   "Container t carries discontiguous spanners."
 
   assert not componenttools.is_well_formed_component(t)
   assert t.format == "\\new Voice {\n\t{\n\t}\n\t{\n\t\te'8\n\t\tf'8 ]\n\t}\n}"

   "Recipient container is now ..."

   r'''
   \new Voice {
      c'8 [
      d'8
   }
   '''

   "Recipient container carries discontiguous spanners."

   assert not componenttools.is_well_formed_component(recipient)
   assert recipient.format == "\\new Voice {\n\tc'8 [\n\td'8\n}"


def test_componenttools_give_music_to_02( ):
   '''When donor is leaf, do nothing.'''

   donor = Note(0, (1, 8))
   recipient = Voice([ ])
  
   _give_music_to([donor], recipient)

   assert componenttools.is_well_formed_component(donor)
   assert donor.format == "c'8"

   assert componenttools.is_well_formed_component(recipient)
   assert recipient.format == '\\new Voice {\n}'


def test_componenttools_give_music_to_03( ):
   '''When recipient is unable to accept donated music,
      raise MusicContentsError.'''

   donor = Voice(macros.scale(4))
   recipient = Voice(macros.scale(4))

   assert py.test.raises(
      MusicContentsError, '_give_music_to([donor], recipient)')
