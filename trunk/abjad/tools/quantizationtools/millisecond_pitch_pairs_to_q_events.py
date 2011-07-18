from collections import Iterable
from itertools import groupby
from numbers import Number
from abjad.tools.durtools import Offset
from abjad.tools.mathtools import cumulative_sums_zero
from abjad.tools.quantizationtools.QEvent import QEvent


def millisecond_pitch_pairs_to_q_events(pairs):

   # validate input
   assert isinstance(pairs, Iterable)
   assert all([isinstance(x, Iterable) for x in pairs])
   assert all([len(x) == 2 for x in pairs])
   assert all([0 < x[0] for x in pairs])
   for pair in pairs:
      assert isinstance(pair[1], (Number, type(None), Iterable))
      if isinstance(pair[1], Iterable):
         assert 0 < len(pair[1])
         assert all([isinstance(x, Number) for x in pair[1]])

   # fuse silences
   g = groupby(pairs, lambda x: x[1] is not None)
   groups = [ ]
   for value, group in g:
      if value:
         groups.extend(list(group))
      else:
         duration = sum([x[0] for x in group])
         groups.append((duration, None))

   # find offsets
   offsets = cumulative_sums_zero([abs(x[0]) for x in groups])

   # build Q-events
   q_events = [ ]
   for pair in zip(offsets, groups):
      offset = Offset(pair[0])
      # duration = abs(pair[1][0])
      pitches = pair[1][1]
      if isinstance(pitches, Iterable):
         assert all([isinstance(x, Number) for x in pitches])
      else:
         assert isinstance(pitches, (int, type(None)))
      q_events.append(QEvent(offset, pitches))

   # add terminating silence
   q_events.append(QEvent(offsets[-1], None))

   return q_events
