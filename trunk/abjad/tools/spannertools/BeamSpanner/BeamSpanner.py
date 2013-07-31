# -*- encoding: utf-8 -*-
from abjad.tools.spannertools.DirectedSpanner.DirectedSpanner \
	import DirectedSpanner


class BeamSpanner(DirectedSpanner):
    r'''Abjad beam spanner:

    ::

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

        >>> show(staff) # doctest: +SKIP

    ::

        >>> spannertools.BeamSpanner(staff[:4])
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

    ::

        >>> show(staff) # doctest: +SKIP

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

    ### PUBLIC METHODS ###

    @staticmethod
    def is_beamable_component(expr):
        '''.. versionadded:: 1.1

        True when `expr` is a beamable component. Otherwise false:

        ::

            >>> staff = Staff(r"r32 a'32 ( [ gs'32 fs''32 \staccato f''8 ) ]")
            >>> staff.extend(r"r8 e''8 ( ef'2 )")

        ::

            >>> show(staff) # doctest: +SKIP

        ::

            >>> for leaf in staff.select_leaves():
            ...     result = spannertools.BeamSpanner.is_beamable_component(leaf)
            ...     print '{:<8}{}'.format(leaf, result)
            ...
            r32     False
            a'32    True
            gs'32   True
            fs''32  True
            f''8    True
            r8      False
            e''8    True
            ef'2    False

        Return boolean.
        '''
        from abjad.tools import chordtools
        from abjad.tools import notetools
        if isinstance(expr, (notetools.Note, chordtools.Chord)):
            if 0 < expr.written_duration.flag_count:
                return True
        return False
