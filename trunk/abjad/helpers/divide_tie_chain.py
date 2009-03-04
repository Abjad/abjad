from abjad.note.note import Note
from abjad.helpers.bequeath_multiple import bequeath_multiple
from abjad.helpers.prolated_to_written import _prolated_to_written
from abjad.helpers.untie_components import untie_components
from abjad.tuplet.fd.tuplet import FixedDurationTuplet


def divide_tie_chain(tie_chain, divisions = 2, prolation = 'diminution'):
   '''Generalization of divide_leaf.'''

   # find target duration of fixed-duration tuplet
   target_duration = tie_chain[0].tie.spanner.written

   # find prolated duration of each note in tuplet
   prolated_duration = target_duration / divisions

   # find written duration of each notes in tuplet
   written_duration = _prolated_to_written(prolated_duration, prolation)
   
   # make tuplet notes
   notes = Note(0, written_duration) * divisions

   # make tuplet
   tuplet = FixedDurationTuplet(target_duration, notes)

   # bequeath tie chain position in score structure to tuplet
   bequeath_multiple(list(tie_chain), [tuplet])

   # untie tuplet
   tuplet.tie.unspan( )

   # return tuplet
   return tuplet
