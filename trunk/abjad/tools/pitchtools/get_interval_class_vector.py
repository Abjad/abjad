from abjad.pitch import Pitch
from abjad.tools import listtools


def get_interval_class_vector(pitches):
   r'''Return the interval class vector of *pitches* as a Python dictionary.

   The interval vector implemented here gives the number of ``i0, ..., i6``
   between the ``n**2 - n`` pairs of *pitches* taken without respect for order.

   ::

      abjad> chord = Chord([0, 2, 11], (1, 4))
      abjad> vector = pitchtools.get_interval_class_vector(chord.pitches)
      abjad> for i in range(7):
      ...     print '\t%s\t%s' % (i, vector[i])
      ... 
         0  0
         1  1
         2  1
         3  1
         4  0
         5  0
         6  0

   ::

      abjad> staff = Staff(construct.scale(4) + construct.scale(4) + construct.scale(4))
      abjad> pitches = pitchtools.get_pitches(staff)
      abjad> vector = pitchtools.get_interval_class_vector(pitches)
      abjad> for i in range(7):
      ...     print '\t%s\t%s' % (i, vector[i])
      ... 
         0  12
         1  9
         2  18
         3  9
         4  9
         5  9
         6  0
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
      if 6 < interval:
         interval = 12 - interval
      intervals.append(interval)

   vector = { }

   for i in range(7):
      vector[i] = intervals.count(i)

   return vector
