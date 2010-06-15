from abjad.exceptions import AssignabilityError
from abjad.note import Note
from abjad.rational import Rational
from abjad.tools import durtools
from abjad.tools import scoretools
from abjad.tools.tietools.get_tie_chain_duration_preprolated import \
   get_tie_chain_duration_preprolated
from abjad.tuplet import FixedDurationTuplet


def _tie_chain_to_tuplet(chain, divisions, prolation, dotted):
   '''.. versionadded:: 1.1.2

   Generalized tie-chain division function.
   '''

   # find target duration of fixed-duration tuplet
   tie_chain = chain[0].tie.chain
   target_duration = get_tie_chain_duration_preprolated(tie_chain)

   # find prolated duration of each note in tuplet
   prolated_duration = target_duration / sum(divisions)

   # find written duration of each notes in tuplet
   if prolation == 'diminution':
      if dotted:
         basic_written_duration = \
            durtools.rational_to_equal_or_greater_assignable_rational(prolated_duration)
      else:
         basic_written_duration = \
            durtools.rational_to_equal_or_greater_binary_rational(prolated_duration)
   elif prolation == 'augmentation':
      if dotted:
         basic_written_duration = \
            durtools.rational_to_equal_or_lesser_assignable_rational(prolated_duration)
      else:
         basic_written_duration = \
            durtools.rational_to_equal_or_lesser_binary_rational(
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
      notes = leaftools.make_notes(0, note_durations)

   # make tuplet
   tuplet = FixedDurationTuplet(target_duration, notes)

   # bequeath tie chain position in score structure to tuplet
   scoretools.bequeath(list(chain), [tuplet])

   # untie tuplet
   tuplet.tie.unspan( )

   # return tuplet
   return tuplet
