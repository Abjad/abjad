from abjad.container.container import Container
from abjad.leaf.leaf import _Leaf
from abjad.tools import componenttools
from abjad.tools.split.leaf_at_duration import leaf_at_duration as \
   split_leaf_at_duration
from abjad.tools.split._at_count import _at_count as \
   split__at_count


def _at_duration(component, duration, spanners = 'unfractured'):
   '''General component duration split algorithm.
      Duration is interpreted as prolated duration.
      Works on leaves, tuplets, measures, context and unqualified containers.
      Keyword controls spanner behavior at split-time.'''

   ## get duration crossers, if any
   contents = componenttools.get_duration_crossers(component, duration) 

   ## if leaf duration crosser, will be at end of list
   last = contents[-1]
   assert isinstance(last, _Leaf)
   split_point = duration - last.offset.score 
   left_list, right_list = split_leaf_at_duration(last, split_point)
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
      left, right = split__at_count(cur, i, spanners = spanners)
         
   ## return split input component and split contents, if any
   return ([left], [right])
