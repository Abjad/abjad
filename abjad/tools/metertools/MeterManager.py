# -*- encoding: utf-8 -*-
from abjad.tools import abctools


class MeterManager(abctools.AbjadObject):
    r'''A meter manager.
    '''

    ### PUBLIC METHODS ###

    @staticmethod
    def iterate_rewrite_inputs(expr):
        r'''Iterate topmost masked logical ties, rest groups and containers in
        `expr`, masked by `expr`:

        ::

            >>> input = "abj: | 2/4 c'4 d'4 ~ |"
            >>> input += "| 4/4 d'8. r16 r8. e'16 ~ "
            >>> input += "2/3 { e'8 ~ e'8 f'8 ~ } f'4 ~ |"
            >>> input += "| 4/4 f'8 g'8 ~ g'4 a'4 ~ a'8 b'8 ~ |"
            >>> input += "| 2/4 b'4 c''4 |"
            >>> staff = Staff(input)

        ..  doctest::

            >>> print format(staff)
            \new Staff {
                {
                    \time 2/4
                    c'4
                    d'4 ~
                }
                {
                    \time 4/4
                    d'8.
                    r16
                    r8.
                    e'16 ~
                    \times 2/3 {
                        e'8 ~
                        e'8
                        f'8 ~
                    }
                    f'4 ~
                }
                {
                    f'8
                    g'8 ~
                    g'4
                    a'4 ~
                    a'8
                    b'8 ~
                }
                {
                    \time 2/4
                    b'4
                    c''4
                }
            }

        ::

            >>> for x in metertools.MeterManager.iterate_rewrite_inputs(
            ...     staff[0]): x
            ...
            LogicalTie(Note("c'4"),)
            LogicalTie(Note("d'4"),)

        ::

            >>> for x in metertools.MeterManager.iterate_rewrite_inputs(
            ...     staff[1]): x
            ...
            LogicalTie(Note("d'8."),)
            LogicalTie(Rest('r16'), Rest('r8.'))
            LogicalTie(Note("e'16"),)
            Tuplet(Multiplier(2, 3), "e'8 ~ e'8 f'8 ~")
            LogicalTie(Note("f'4"),)

        ::

            >>> for x in metertools.MeterManager.iterate_rewrite_inputs(
            ...     staff[2]): x
            ...
            LogicalTie(Note("f'8"),)
            LogicalTie(Note("g'8"), Note("g'4"))
            LogicalTie(Note("a'4"), Note("a'8"))
            LogicalTie(Note("b'8"),)

        ::

            >>> for x in metertools.MeterManager.iterate_rewrite_inputs(
            ...     staff[3]): x
            ...
            LogicalTie(Note("b'4"),)
            LogicalTie(Note("c''4"),)

        Returns generator.
        '''
        from abjad.tools import scoretools
        from abjad.tools import selectiontools
        from abjad.tools import spannertools

        last_tie_spanner = None
        current_leaf_group = None
        current_leaf_group_is_silent = False

        for x in expr:
            if isinstance(x, (scoretools.Note, scoretools.Chord)):
                this_tie_spanner = x._get_spanners(spannertools.Tie) or None
                if current_leaf_group is None:
                    current_leaf_group = []
                elif current_leaf_group_is_silent or \
                    this_tie_spanner is None or \
                    last_tie_spanner != this_tie_spanner:
                    yield selectiontools.LogicalTie(current_leaf_group)
                    current_leaf_group = []
                current_leaf_group_is_silent = False
                current_leaf_group.append(x)
                last_tie_spanner = this_tie_spanner
            elif isinstance(x, (scoretools.Rest, scoretools.Skip)):
                if current_leaf_group is None:
                    current_leaf_group = []
                elif not current_leaf_group_is_silent:
                    yield selectiontools.LogicalTie(current_leaf_group)
                    current_leaf_group = []
                current_leaf_group_is_silent = True
                current_leaf_group.append(x)
                last_tie_spanner = None
            elif isinstance(x, scoretools.Container):
                if current_leaf_group is not None:
                    yield selectiontools.LogicalTie(current_leaf_group)
                    current_leaf_group = None
                    last_tie_spanner = None
                yield x

            else:
                message = 'unhandled component: {!r}.'
                message = message.format(x)
                raise Exception(message)
        if current_leaf_group is not None:
            yield selectiontools.LogicalTie(current_leaf_group)
