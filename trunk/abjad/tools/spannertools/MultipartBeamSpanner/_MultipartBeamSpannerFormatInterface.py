from abjad.tools.spannertools.BeamSpanner._BeamSpannerFormatInterface import \
   _BeamSpannerFormatInterface


class _MultipartBeamSpannerFormatInterface(_BeamSpannerFormatInterface):

   def __init__(self, spanner):
      _BeamSpannerFormatInterface.__init__(self, spanner)

   ## PUBLIC METHODS ##

#   def _before(self, leaf):
#      '''Spanner format contribution before leaf.'''
#      result = [ ]
#      result.extend(_BeamSpannerFormatInterface._before(self, leaf))
#      return result

   def _right(self, leaf):
      '''Spanner format contribution right of leaf.'''
      from abjad.tools import componenttools
      from abjad.tools import leaftools
      result = [ ]
      spanner = self.spanner
      if componenttools.is_beamable_component(leaf):
         if 1 < len(spanner.leaves):   
            if spanner._is_my_first_leaf(leaf):
               result.append('[')
            else:
               prev = leaftools.get_nth_leaf_in_thread_from_leaf(leaf, -1)
               if prev is not None and not componenttools.is_beamable_component(prev):
                  result.append('[')
            if spanner._is_my_last_leaf(leaf):
               result.append(']')   
            else:
               next = leaftools.get_nth_leaf_in_thread_from_leaf(leaf, 1)
               if next is not None and not componenttools.is_beamable_component(next):
                  result.append(']')
      return result
