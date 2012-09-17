from abjad.tools import stringtools
from abjad.tools.spannertools.DirectedSpanner.DirectedSpanner import DirectedSpanner


class TieSpanner(DirectedSpanner):
    r'''Abjad tie spanner::

        >>> staff = Staff(notetools.make_repeated_notes(4))
        >>> tietools.TieSpanner(staff[:])
        TieSpanner(c'8, c'8, c'8, c'8)

    ::

        >>> f(staff)
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
        DirectedSpanner.__init__(self, music, direction)

    ### PRIVATE METHODS ###
    
    def _copy_keyword_args(self, new):
        DirectedSpanner._copy_keyword_args(self, new)

    def _format_right_of_leaf(self, leaf):
        result = []
        if not self._is_my_last_leaf(leaf):
            if self.direction is not None:
                result.append('{} ~'.format(stringtools.arg_to_tridirectional_lilypond_symbol(self.direction)))
            else:
                result.append('~')
        return result
