from abjad.container import Container
from abjad.exceptions import MusicContentsError
from abjad.leaf.leaf import _Leaf
from abjad.tools import check
from abjad.tools.parenttools.switch import _switch


def _give_music_to(donors, recipient):
   '''Give any music belong to donor components 'donors'
      to recipient component 'recipient'.
      Works great when 'recipient' is an empty container.
      Pass silently when recipient is a nonempty container 
      or a leaf and when donors have no music.
      Raises MusicContentsError when donors *do* have music
      to music but when recipient is unable to accept music
      (because recipient is nonempty container or leaf).

      Return donor components 'donors'.

      Helper is not composer-safe and may cause discontiguous spanners.'''

   check.assert_components(donors, contiguity = 'strict', share = 'parent')

   ## if recipient is leaf or nonempty container, 
   ## make sure there's no music in donor components to hand over
   if isinstance(recipient, _Leaf) or \
      (isinstance(recipient, Container) and len(recipient)):
      if all([len(x.music) == 0 for x in donors]):
         return donors
      else:
         raise MusicContentsError('can not give music to leaf.')
      
   ## otherwise recipient is empty container, so proceed
   ## collect music from all donor components
   donor_music = [ ]
   for donor in donors:
      donor_music.extend(donor.music)

   ## give music from donor components to recipient component
   recipient._music.extend(donor_music)
   _switch(recipient[:], recipient)

   ## return donor components
   return donors
