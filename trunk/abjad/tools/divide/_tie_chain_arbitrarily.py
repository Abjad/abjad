from abjad.exceptions import AssignabilityError
from abjad.note import Note
from abjad.rational import Rational
from abjad.tools import durtools
from abjad.tools import scoretools
from abjad.tools import tietools
from abjad.tuplet import FixedDurationTuplet


def _tie_chain_arbitrarily(chain, divisions, prolation, dotted):
   '''.. versionadded:: 1.1.2

   Generalized tie-chain division function.
   '''

   # find target duration of fixed-duration tuplet
   target_duration = tietools.get_duration_preprolated(chain[0].tie.chain)

   # find prolated duration of each note in tuplet
   prolated_duration = target_duration / sum(divisions)

   # find written duration of each notes in tuplet
   if prolation == 'diminution':
      if dotted:
         basic_written_duration = \
            durtools.prolated_to_written_not_less_than(prolated_duration)
      else:
         basic_written_duration = \
            durtools.naive_prolated_to_written_not_less_than(prolated_duration)
   elif prolation == 'augmentation':
      if dotted:
         basic_written_duration = \
            durtools.prolated_to_written_not_greater_than(prolated_duration)
      else:
         basic_written_duration = \
            durtools.naive_prolated_to_written_not_greater_than(
            prolated_duration)
   else:
      raise ValueError('must be diminution or augmentation.')
   
   ## find written duration of each note in tuplet
   written_durations = [x * basic_written_duration for x in divisions]

   ## make tuplet notes
   try:
      notes = [Note(0, x) for x in written_durations]
   except AssignabilityError:
      denominator = target_duration._denominator
      note_durations = [Rational(x, denominator) for x in divisions]
      notes = construct.notes(0, note_durations)

   # make tuplet
   tuplet = FixedDurationTuplet(target_duration, notes)

   # bequeath tie chain position in score structure to tuplet
   scoretools.bequeath(list(chain), [tuplet])

   # untie tuplet
   tuplet.tie.unspan( )

   # return tuplet
   return tuplet
