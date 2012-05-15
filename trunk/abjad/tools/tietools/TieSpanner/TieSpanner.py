from abjad.tools.spannertools._DirectedSpanner._DirectedSpanner import _DirectedSpanner


class TieSpanner(_DirectedSpanner):
    r'''Abjad tie spanner::

        abjad> staff = Staff(notetools.make_repeated_notes(4))
        abjad> tietools.TieSpanner(staff[:])
        TieSpanner(c'8, c'8, c'8, c'8)
        abjad> f(staff)
        \new Staff {
            c'8 ~
            c'8 ~
            c'8 ~
            c'8
        }

    Return tie spanner.
    '''

    ### INITIALIZER ###

    def __init__(self, music=None, direction=None):
        _DirectedSpanner.__init__(self, music, direction)

    ### PRIVATE METHODS ###
    
    def _format_right_of_leaf(self, leaf):
        result = []
        if not self._is_my_last_leaf(leaf):
            if self.direction is not None:
                result.append('%s ~' % self.direction)
            else:
                result.append('~')
        return result
