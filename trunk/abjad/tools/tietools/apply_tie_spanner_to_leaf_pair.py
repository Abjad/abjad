from abjad.exceptions import MissingSpannerError
from abjad.components._Leaf import _Leaf
from abjad.spanners import TieSpanner
from abjad.tools.tietools.are_components_in_same_tie_spanner import are_components_in_same_tie_spanner


def apply_tie_spanner_to_leaf_pair(left, right):
   r'''Apply tie spanner to `left` leaf and `right` leaf::

      abjad> staff = Staff(notetools.make_repeated_notes(4))
      abjad> TieSpanner(staff[:2])
      abjad> f(staff)
      \new Staff {
         c'8 ~
         c'8
         c'8
         c'8
      }
      
   ::
      
      abjad> tietools.apply_tie_spanner_to_leaf_pair(staff[1], staff[2]) 
      
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

   .. versionchanged:: 1.1.2
      renamed ``tietools.span_leaf_pair( )`` to
      ``tietools.apply_tie_spanner_to_leaf_pair( )``.
   '''

   assert isinstance(left, _Leaf)
   assert isinstance(right, _Leaf)

   if are_components_in_same_tie_spanner([left, right]):
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
      TieSpanner([left, right])
