# -*- encoding: utf-8 -*-
from abjad.tools import stringtools
from abjad.tools.spannertools.DirectedSpanner import DirectedSpanner


class SlurSpanner(DirectedSpanner):
    r'''A slur spanner.

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> slur = spannertools.SlurSpanner()
        >>> attach(slur, staff[:])
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> f(staff)
        \new Staff {
            c'8 (
            d'8
            e'8
            f'8 )
        }

    '''

    ### INITIALIZER ###

    def __init__(
        self, 
        components=None, 
        direction=None,
        overrides=None,
        ):
        DirectedSpanner.__init__(
            self, 
            components, 
            direction,
            overrides=overrides,
            )

    ### PRIVATE METHODS ###

    def _copy_keyword_args(self, new):
        DirectedSpanner._copy_keyword_args(self, new)

    def _format_right_of_leaf(self, leaf):
        result = []
        if self._is_my_first_leaf(leaf):
            direction = self.direction
            if direction is not None:
                result.append('{} ('.format(
                    stringtools.arg_to_tridirectional_lilypond_symbol(
                        direction)))
            else:
                result.append('(')
        if self._is_my_last_leaf(leaf):
            result.append(')')
        return result
