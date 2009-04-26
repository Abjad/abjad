from abjad.container.container import Container
from abjad.exceptions.exceptions import ContainmentError
from abjad.leaf.leaf import _Leaf
from abjad.measure.rigid.measure import RigidMeasure
from abjad.tie.spanner import Tie
from abjad.tools import componenttools
from abjad.tools import durtools
from abjad.tools import iterate
from abjad.tools import mathtools
from abjad.tools import measuretools
from abjad.tools import tietools
from abjad.tools.split._leaf_at_duration import _leaf_at_duration as \
   split__leaf_at_duration
from abjad.tools.split._at_index import _at_index as \
   split__at_index


def _at_duration(
   component, duration, spanners = 'unfractured', tie_after = False):
   '''General component duration split algorithm.
      Duration is interpreted as prolated duration.
      Works on leaves, tuplets, measures, context and unqualified containers.
      Keyword controls spanner behavior at split-time.'''

   from abjad.tools import fuse

   assert 0 <= duration

   ## if zero duration then return component
   if duration == 0:
      ## TODO: This one case should be ([ ], component) ##
      return (component, )

   ## get global position of duration split in score
   global_split_point = component.offset.prolated.start + duration

   ## get duration crossers, if any
   contents = componenttools.get_duration_crossers(component, duration) 

   print component, global_split_point, contents

   ## get duration crossing measures, if any
   measures = [x for x in contents if isinstance(x, RigidMeasure)]

   ## if we must split a binary measure at a nonbinary split point
   ## go ahead and transform the binary measure to nonbinary equiavlent now;
   ## code that crawls and splits later on will be happier
   if len(measures) == 1:
      measure = measures[0]
      split_point_in_measure = \
         global_split_point - measure.offset.prolated.start
      split_point_denominator = split_point_in_measure._d
      if measure.duration.nonbinary:
         measure_multiplier = measure.duration.multiplier
         split_point_multiplier = durtools.denominator_to_multiplier(
            split_point_denominator)
         if not measure_multiplier == split_point_multiplier:
            raise Exception(NotImplemented)
      elif not mathtools.is_power_of_two(split_point_denominator):
         print 'bar'
         nonbinary_factors = mathtools.factors(
            mathtools.remove_powers_of_two(split_point_denominator))
         nonbinary_product = 1
         for nonbinary_factor in nonbinary_factors:
            nonbinary_product *= nonbinary_factor
         measuretools.binary_to_nonbinary(measure, nonbinary_product)
         print measure
         print component, duration
         print component.format
         ## rederive duration crosses with possibly new measure contents
         contents = componenttools.get_duration_crossers(component, duration) 
         print contents
         print ''
   elif 1 < len(measures):
      raise ContainmentError('measures can not nest.')

   ## if leaf duration crosser, will be at end of list
   bottom = contents[-1]

   did_split_leaf = False

   ## if split point necessitates leaf split
   if isinstance(bottom, _Leaf):
      assert isinstance(bottom, _Leaf)
      did_split_leaf = True
      split_point_in_bottom = global_split_point - bottom.offset.prolated.start
      left_list, right_list = split__leaf_at_duration(bottom, 
         split_point_in_bottom, spanners = spanners, tie_after = tie_after)
      right = right_list[0]
      leaf_right_of_split = right
      leaf_left_of_split = left_list[-1]
      containers = contents[:-1]
      if not len(containers):
         return left_list, right_list
   ## if split point falls between leaves
   ## then find leaf to immediate right of split point
   ## in order to start upward crawl through containers
   else:
      containers = contents[:]
      for leaf in iterate.naive(bottom, _Leaf):
         if leaf.offset.prolated.start == global_split_point:
            right = leaf
            leaf_right_of_split = right
            leaf_left_of_split = right.prev
            break
      else:
         raise ContainmentError('can not split empty container.')
   
   ## fracture leaf spanners if requested
   if spanners == 'fractured':
      right.spanners.fracture(direction = 'left')

   ## crawl back up through container duration crossers
   ## split each container duration crosser
   for cur in reversed(containers):
      assert isinstance(cur, Container)
      prev = right
      i = cur.index(prev)
      left, right = split__at_index(cur, i, spanners = spanners)

   ## NOTE: If tie chain here is convenience, then fusing is good.
   ##       If tie chain here is user-given, then fusing is less good.
   ##       Maybe later model difference between user tie chains and not.
   fuse.leaves_in_tie_chain(leaf_left_of_split.tie.chain)
   fuse.leaves_in_tie_chain(leaf_right_of_split.tie.chain)
   
   ## crawl above will kill any tie applied to leaves
   ## reapply tie here if necessary
   ## TODO: Possibly replace this with tietools.span_leaf_pair( )? ##
   if did_split_leaf:
      if tie_after:
         leaves_at_split = [leaf_left_of_split, leaf_right_of_split]
         if not tietools.are_in_same_spanner(leaves_at_split):
            if all([x.tie.spanned for x in leaves_at_split]):
               leaf_left_of_split.tie.spanner.fuse(
                  leaf_right_of_split.tie.spanner)
            else:
               Tie(leaves_at_split)
         
   ## return pair of left and right list-wrapped halves of container
   return ([left], [right])
