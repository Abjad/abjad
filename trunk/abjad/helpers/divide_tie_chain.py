from abjad.note.note import Note
from abjad.helpers.bequeath import bequeath
from abjad.tools import durtools
from abjad.tools import tietools
from abjad.tuplet.fd.tuplet import FixedDurationTuplet


def divide_tie_chain(tie_chain, divisions = 2, prolation = 'diminution'):
   '''Generalization of divide_leaf.'''

   # find target duration of fixed-duration tuplet
   target_duration = tietools.duration_written(tie_chain[0].tie.chain)

   # find prolated duration of each note in tuplet
   prolated_duration = target_duration / divisions

   # find written duration of each notes in tuplet
   written_duration = durtools.prolated_to_written(prolated_duration, prolation)
   
   # make tuplet notes
   notes = Note(0, written_duration) * divisions

   # make tuplet
   tuplet = FixedDurationTuplet(target_duration, notes)

   # bequeath tie chain position in score structure to tuplet
   bequeath(list(tie_chain), [tuplet])

   # untie tuplet
   tuplet.tie.unspan( )

   # return tuplet
   return tuplet
