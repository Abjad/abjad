from abjad.helpers.copy_fractured import copy_fractured
from abjad.helpers.iterate import iterate


## TODO: Finish implementation ##

def measures_overdraw(expr, source_count = 1, total_reps = 2):
   '''Input parameters:

      source_count gives the number of measures to copy.
      total_reps gives the number of times source_count should repeat.

      Iterate expr. Copy the first source_count measures as 'source'.
      'Draw', or paste, source 'over' the following measures in expr
      a total of total_reps times.

      Return a Python list of multiplied source measures.

      Example:'''

   source = [ ]
   result = [ ]
   from abjad.measure.measure import _Measure
   for i, measure in enumerate(iterate(expr, _Measure)):
      if i < source_count:
         source.append(measure)   
      elif i == source_count:
         copy_fractured(source)
      else:
         pass
      
          
   
