from abjad.container.container import Container
from abjad.leaf.leaf import _Leaf
from abjad.tools import componenttools
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

   if duration == 0:
      return (component, )

   global_split_point = component.offset.score + duration

   ## get duration crossers, if any
   contents = componenttools.get_duration_crossers(component, duration) 

   ## if leaf duration crosser, will be at end of list
   bottom = contents[-1]
   assert isinstance(bottom, _Leaf)
   split_point_in_bottom = global_split_point - bottom.offset.score
   left_list, right_list = split__leaf_at_duration(
      bottom, split_point_in_bottom)
   right = right_list[0]
   
   ## if container duration crossers, will be front of list
   containers = contents[:-1]

   ## if no container duration crosses, return split leaf halves
   if not len(containers):
      return left_list, right_list

   ## crawl back up through container duration crossers and split each
   for cur in reversed(contents[:-1]):
      assert isinstance(cur, Container)
      prev = right
      i = cur.index(prev)
      left, right = split__at_index(cur, i, spanners = spanners)
         
   ## return split input component and split contents, if any
   return ([left], [right])
