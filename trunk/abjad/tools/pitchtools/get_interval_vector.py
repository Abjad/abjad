from abjad.pitch import Pitch
from abjad.tools import listtools


def get_interval_vector(pitches):
   '''Return the interval vector of *pitches* as a Python dictionary.

   The interval vector implemented here gives the number of ``i0, ..., i11``
   between the ``n**2 - n`` pairs of *pitches* taken without respect for order.

   ::

      abjad> chord = Chord([0, 2, 11], (1, 4))
      abjad> vector = pitchtools.get_interval_vector(chord.pitches)
      abjad> vector
      {0: 0, 1: 0, 2: 1, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 1, 10: 0, 11: 1}
      abjad> vector[9]
      1
      abjad> vector[10]
      0

   ::

      abjad> staff = Staff(construct.scale(4) + construct.scale(4) + construct.scale(4))
      abjad> pitches = pitchtools.get_pitches(staff)
      abjad> vector = pitchtools.get_interval_vector(pitches)
      abjad> vector
      {0: 12, 1: 9, 2: 18, 3: 9, 4: 9, 5: 9, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0}
      abjad> for i in range(12):
      ...     print i, vector[i]
      ... 
      0 12
      1 9
      2 18
      3 9
      4 9
      5 9
      6 0
      7 0
      8 0
      9 0
      10 0
      11 0
   '''

   numbers = [ ]

   for pitch in pitches:
      if not isinstance(pitch, Pitch):
         raise ValueError
      numbers.append(pitch.number)

   pairs = listtools.get_unordered_pairs(numbers)

   intervals = [ ]

   for pair in pairs:
      interval = max(pair) - min(pair)
      interval %= 12
      intervals.append(interval)

   vector = { }

   for i in range(12):
      vector[i] = intervals.count(i)

   return vector
