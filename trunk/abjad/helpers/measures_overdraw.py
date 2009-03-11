from abjad.helpers.components_copy import components_copy
from abjad.helpers.iterate import iterate


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
   for i, measure in enumerate(iterate(expr, '_Measure')):
      if i < source_count:
         source.append(measure)   
      elif i == source_count:
         components_copy(source)
      else:
         pass
      
          
   
