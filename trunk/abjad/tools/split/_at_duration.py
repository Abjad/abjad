from abjad.container.container import Container
from abjad.exceptions.exceptions import ContainmentError
from abjad.leaf.leaf import _Leaf
from abjad.tools import componenttools
from abjad.tools import iterate
from abjad.tools.split._leaf_at_duration import _leaf_at_duration as \
   split__leaf_at_duration
from abjad.tools.split._at_index import _at_index as \
   split__at_index


def _at_duration(component, duration, spanners = 'unfractured'):
   '''General component duration split algorithm.
      Duration is interpreted as prolated duration.
      Works on leaves, tuplets, measures, context and unqualified containers.
      Keyword controls spanner behavior at split-time.'''

   assert 0 <= duration

   ## if zero duration then return component
   if duration == 0:
      return (component, )

   ## get global position of duration split in score
   global_split_point = component.offset.score + duration

   ## get duration crossers, if any
   contents = componenttools.get_duration_crossers(component, duration) 

   ## if leaf duration crosser, will be at end of list
   bottom = contents[-1]

   ## if split point necessitates leaf split
   if isinstance(bottom, _Leaf):
      assert isinstance(bottom, _Leaf)
      split_point_in_bottom = global_split_point - bottom.offset.score
      left_list, right_list = split__leaf_at_duration(
         bottom, split_point_in_bottom)
      right = right_list[0]
      containers = contents[:-1]
      if not len(containers):
         return left_list, right_list
   else:
      ## if split point falls between leaves
      ## then find leaf to immediate right of split point
      ## in order to start upward crawl through containers
      containers = contents[:]
      for leaf in iterate.naive(bottom, _Leaf):
         if leaf.offset.score == global_split_point:
            right = leaf
            break
      else:
         raise ContainmentError('can not split empty container.')
   
   ## crawl back up through container duration crossers
   ## split each container duration crosser
   for cur in reversed(containers):
      assert isinstance(cur, Container)
      prev = right
      i = cur.index(prev)
      left, right = split__at_index(cur, i, spanners = spanners)
         
   ## return pair of left and right list-wrapped halves of container
   return ([left], [right])
