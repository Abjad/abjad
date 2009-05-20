from abjad.tools import listtools


def registrate(pcs, pitches):
   '''Turn pitch-classes into pitches.
   
      Example::

         abjad> pitchtools.registrate(
               [10, 0, 2, 6, 8, 7, 5, 3, 1, 9, 4, 11],
               [10, 19, 20, 23, 24, 26, 27, 29, 30, 33, 37, 40]) 

         [10, 24, 26, 30, 20, 19, 29, 27, 37, 33, 40, 23]'''

   if isinstance(pcs, list):
      r = [[p for p in pitches if p % 12 == pc] for pc in [x % 12 for x in pcs]]
      r = listtools.flatten(r)
   elif isinstance(pcs, int):
      r = [p for p in pitches if p % 12 == pcs][0]
   else:
      raise TypeError

   return r
