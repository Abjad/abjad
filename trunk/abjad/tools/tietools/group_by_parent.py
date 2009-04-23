from abjad.tools.tietools.is_chain import is_chain as tietools_is_chain
import itertools


def group_by_parent(tie_chain):

   ## check input
   if not tietools_is_chain(tie_chain):
      raise TypeError('must be tie chain.')
   
   ## create partition with itertools
   result = [ ]
   pairs_generator = itertools.groupby(tie_chain, lambda x: x.parentage.parent)
   for key, values_generator in pairs_generator:
      result.append(list(values_generator))

   ## return result
   return result
