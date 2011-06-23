from collections import Iterable
from numbers import Number
from itertools import groupby


def group_timepoints_by_beatspan(timepoints, beatspan, subscript = None):
   '''This function is provided outside of the QGridQuantizer classes
   in order to provide an easier import for multiprocessing operations.'''

   assert isinstance(timepoints, Iterable) and len(timepoints) 
   assert isinstance(beatspan, Number)

   if subscript is None:
      timepoints = sorted(timepoints)
      g = groupby(timepoints, lambda x: divmod(x, beatspan)[0])
   else: # in case we are processing timepoint tuples or dicts
      timepoints = sorted(timepoints, key = lambda x: x[subscript])
      g = groupby(timepoints, lambda x: divmod(x[subscript], beatspan)[0])

   # unpack for easier processing
   groups = { }
   for value, group in g:
      if subscript is None:
         groups[value] = list(sorted(group))
      else:
         groups[value] = list(sorted(group, key = lambda x: x[subscript]))

   return groups
