from abjad.tools.spannertools.DirectedSpanner.DirectedSpanner import DirectedSpanner


class BeamSpanner(DirectedSpanner):
    r'''Abjad beam spanner::

        >>> staff = Staff("c'8 d'8 e'8 f'8 g'2")

    ::

        >>> f(staff)
        \new Staff {
            c'8
            d'8
            e'8
            f'8
            g'2
        }

    ::

        >>> beamtools.BeamSpanner(staff[:4])
        BeamSpanner(c'8, d'8, e'8, f'8)

    ::

        >>> f(staff)
        \new Staff {
            c'8 [
            d'8
            e'8
            f'8 ]
            g'2
        }

    Return beam spanner.
    '''

    ### INITIALIZER ###

    def __init__(self, components=None, direction=None):
        DirectedSpanner.__init__(self, components, direction)

    ### PRIVATE METHODS ###

    def _copy_keyword_args(self, new):
        DirectedSpanner._copy_keyword_args(self, new)

    def _format_right_of_leaf(self, leaf):
        result = []
        if self._is_my_first_leaf(leaf):
            if self.direction is not None:
                result.append('%s [' % self.direction)
            else:
                result.append('[')
        if self._is_my_last_leaf(leaf):
            result.append(']')
        return result
