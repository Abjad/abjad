from abjad import *


def test_pitchtools_insert_transposed_pc_subruns_01( ):

   notes = [Note(p, (1, 4)) for p in [0, 2, 7, 9, 5, 11, 4]]
   subrun_indicators = [(0, [2, 4]), (4, [3, 1])]
   pitchtools.insert_transposed_pc_subruns(notes, subrun_indicators)

   "Inserts are shown in the innermost pairs of brackets below."

   t = [ ]
   for x in notes:
      try:
         t.append(x.pitch.number)
      except AttributeError:
         t.append([y.pitch.number for y in x])

   print t

   assert t == [0, [5, 7], 2, [4, 0, 6, 11], 7, 9, 5, [10, 6, 8], 11, [7], 4]
   
   t = listtools.flatten(t)

   assert t == [0, 5, 7, 2, 4, 0, 6, 11, 7, 9, 5, 10, 6, 8, 11, 7, 4]
