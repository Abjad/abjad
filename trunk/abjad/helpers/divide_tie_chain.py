from abjad.note.note import Note
#from abjad.helpers.bequeath_multiple import bequeath_multiple
from abjad.helpers.get_covered_spanners import get_covered_spanners
from abjad.helpers.get_tie_chain_written import _get_tie_chain_written
from abjad.helpers.give_dominant_spanners_to import \
   _give_dominant_spanners_to
from abjad.helpers.prolated_to_written import _prolated_to_written
from abjad.tuplet.fd.tuplet import FixedDurationTuplet
from abjad.voice.voice import Voice


def divide_tie_chain(tie_chain, divisions = 2, prolation = 'diminution'):
   '''Generalization of divide_leaf.'''

   # find target duration of fixed-duration tuplet
   target_duration = _get_tie_chain_written(tie_chain[0].tie.chain)

   # find prolated duration of each note in tuplet
   prolated_duration = target_duration / divisions

   # find written duration of each notes in tuplet
   written_duration = _prolated_to_written(prolated_duration, prolation)
   
   # make tuplet notes
   notes = Note(0, written_duration) * divisions

   # make tuplet
   tuplet = FixedDurationTuplet(target_duration, notes)

   # bequeath tie chain position in score structure to tuplet
   #bequeath_multiple(list(tie_chain), [tuplet])
   parent = tie_chain[0].parentage.parent
   if parent is None:
      _give_dominant_spanners_to(list(tie_chain), [tuplet])
   else:
      first, last = tie_chain[0], tie_chain[-1]
      first_index, last_index = parent.index(first), parent.index(last)
      parent[first_index:last_index+1] = [tuplet]

   # untie tuplet
   tuplet.tie.unspan( )

   # return tuplet
   return tuplet
