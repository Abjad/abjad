from abjad.exceptions import MissingSpannerError
from abjad.leaf import _Leaf
from abjad.spanners import Tie
from abjad.tools.tietools.are_in_same_spanner import are_in_same_spanner


def span_leaf_pair(left, right):
   r'''Apply tie spanner to `left` leaf and `right` leaf::

      abjad> staff = Staff(leaftools.make_repeated_notes(4))
      abjad> Tie(staff[:2])
      abjad> f(staff)
      \new Staff {
         c'8 ~
         c'8
         c'8
         c'8
      }
      
   ::
      
      abjad> tietools.span_leaf_pair(staff[1], staff[2]) 
      
   ::
      
      abjad> f(staff)
      \new Staff {
         c'8 ~
         c'8 ~
         c'8
         c'8
      }

   Handle existing tie spanners intelligently.

   Return none.
   '''

   assert isinstance(left, _Leaf)
   assert isinstance(right, _Leaf)

   if are_in_same_spanner([left, right]):
      return 

   try:
      left_tie_spanner = left.tie.spanner
   except MissingSpannerError:
      left_tie_spanner = None

   try:
      right_tie_spanner = right.tie.spanner
   except MissingSpannerError:
      right_tie_spanner = None

   if left_tie_spanner is not None and right_tie_spanner is not None:
      left_tie_spanner.fuse(right_tie_spanner)
   elif left_tie_spanner is not None and right_tie_spanner is None:
      left_tie_spanner.append(right)
   elif left_tie_spanner is None and right_tie_spanner is not None:
      right_tie_spanner.append_left(left)
   elif left_tie_spanner is None and right_tie_spanner is None:
      Tie([left, right])
