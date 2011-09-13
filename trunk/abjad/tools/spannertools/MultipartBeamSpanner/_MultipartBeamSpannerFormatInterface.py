from abjad.tools.spannertools.BeamSpanner._BeamSpannerFormatInterface import _BeamSpannerFormatInterface


class _MultipartBeamSpannerFormatInterface(_BeamSpannerFormatInterface):

    def __init__(self, spanner):
        _BeamSpannerFormatInterface.__init__(self, spanner)

    ### PUBLIC METHODS ###

#   def _before(self, leaf):
#      '''Spanner format contribution before leaf.'''
#      result = []
#      result.extend(_BeamSpannerFormatInterface._before(self, leaf))
#      return result

    def _right(self, leaf):
        '''Spanner format contribution right of leaf.'''
        from abjad.tools import componenttools
        from abjad.tools import leaftools
        result = []
        spanner = self.spanner
        if componenttools.is_beamable_component(leaf):
            if 1 < len(spanner.leaves):
                prev = leaftools.get_nth_leaf_in_thread_from_leaf(leaf, -1)
                if id(prev) not in [id(x) for x in spanner.leaves]:
                    prev = None
                next = leaftools.get_nth_leaf_in_thread_from_leaf(leaf, 1)
                if id(next) not in [id(x) for x in spanner.leaves]:
                    next = None
                if spanner._is_my_first_leaf(leaf):
                    if next is not None:
                        if componenttools.is_beamable_component(next):
                            result.append('[')
                else:
                    if prev is not None:
                        if not componenttools.is_beamable_component(prev):
                            if next is not None:
                                result.append('[')
                if spanner._is_my_last_leaf(leaf):
                    if prev is not None:
                        if componenttools.is_beamable_component(prev):
                            result.append(']')
                else:
                    next = leaftools.get_nth_leaf_in_thread_from_leaf(leaf, 1)
                    if next is not None and not componenttools.is_beamable_component(next):
                        result.append(']')
        return result
