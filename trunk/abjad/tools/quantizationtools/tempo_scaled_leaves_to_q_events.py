from itertools import groupby
from abjad import Note
from abjad import Rest
from abjad.tools.componenttools import all_are_contiguous_components_in_same_thread
from abjad.tools.contexttools import TempoMark
from abjad.tools.contexttools import get_effective_tempo
from abjad.tools.durtools import Offset
from abjad.tools.quantizationtools.QEvent import QEvent
from abjad.tools.quantizationtools.millisecond_pitch_pairs_to_q_events \
   import millisecond_pitch_pairs_to_q_events
from abjad.tools.quantizationtools.tempo_scaled_rational_to_milliseconds \
   import tempo_scaled_rational_to_milliseconds
from abjad.tools.skiptools import Skip
from abjad.tools.tietools import get_tie_chain


def tempo_scaled_leaves_to_q_events(leaves, tempo = None):
   assert all_are_contiguous_components_in_same_thread(leaves) and len(leaves)
   if tempo is None:
      assert get_effective_tempo(leaves[0]) is not None
   else:
      assert isinstance(tempo, TempoMark)

   # sort by silence and tied leaves
   groups = [ ]
   for rvalue, rgroup in groupby(leaves, lambda x: isinstance(x, (Rest, Skip))):
      if rvalue:
         groups.append(list(rgroup))
      else:
         for tvalue, tgroup in groupby(rgroup, lambda x: get_tie_chain(x)):
            groups.append(list(tgroup))

   # calculate lists of pitches and durations
   durations = [ ]
   pitches = [ ]
   for group in groups:

      # get millisecond cumulative duration
      if tempo is not None:
         duration = sum([tempo_scaled_rational_to_milliseconds(x.duration.prolated, tempo)
            for x in group])
      else:
         duration = sum([tempo_scaled_rational_to_milliseconds(x.duration.prolated,
            get_effective_tempo(x)) for x in group])
      durations.append(duration)

      # get pitch of first leaf in group
      if isinstance(group[0], (Rest, Skip)):
         pitch = None
      elif isinstance(group[0], Note):
         pitch = group[0].pitch.chromatic_pitch_number
      else: # chord
         pitch = [x.pitch.chromatic_pitch_number for x in group[0].note_heads]
      pitches.append(pitch)

   # convert durations and pitches to QEvents and return
   return millisecond_pitch_pairs_to_q_events(zip(durations, pitches))
