from abjad.tools import containertools
from abjad.tools import chordtools
from abjad.tools import notetools
from abjad.tools import resttools
from abjad.tools import skiptools


def iterate_topmost_masked_tie_chains_rest_groups_and_containers_in_expr(expr):
    r'''Iterate topmost masked tie chains, rest groups and containers in
    `expr`, masked by `expr`:

    ::

        >>> input = "abj: | 2/4 c'4 d'4 ~ |"
        >>> input += "| 4/4 d'8. r16 r8. e'16 ~ 2/3 { e'8 ~ e'8 f'8 ~ } f'4 ~ |"
        >>> input += "| 4/4 f'8 g'8 ~ g'4 a'4 ~ a'8 b'8 ~ |"
        >>> input += "| 2/4 b'4 c''4 |"
        >>> staff = Staff(input)
        >>> f(staff)
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

        >>> for x in tietools.iterate_topmost_masked_tie_chains_rest_groups_and_containers_in_expr(
        ...     staff[0]): x
        ...
        TieChain(Note("c'4"),)
        TieChain(Note("d'4"),)

    ::

        >>> for x in tietools.iterate_topmost_masked_tie_chains_rest_groups_and_containers_in_expr(
        ...     staff[1]): x
        ...
        TieChain(Note("d'8."),)
        TieChain(Rest('r16'), Rest('r8.'))
        TieChain(Note("e'16"),)
        Tuplet(2/3, [e'8, e'8, f'8])
        TieChain(Note("f'4"),)

    ::

        >>> for x in tietools.iterate_topmost_masked_tie_chains_rest_groups_and_containers_in_expr(
        ...     staff[2]): x
        ...
        TieChain(Note("f'8"),)
        TieChain(Note("g'8"), Note("g'4"))
        TieChain(Note("a'4"), Note("a'8"))
        TieChain(Note("b'8"),)

    ::

        >>> for x in tietools.iterate_topmost_masked_tie_chains_rest_groups_and_containers_in_expr(
        ...     staff[3]): x
        ...
        TieChain(Note("b'4"),)
        TieChain(Note("c''4"),)

    Return generator.
    '''
    from abjad.tools import tietools

    last_tie_chain = None 
    current_leaf_group = None
    current_leaf_group_is_silent = False

    for x in expr:
        if isinstance(x, (notetools.Note, chordtools.Chord)):
            this_tie_chain = tietools.get_tie_chain(x)
            if current_leaf_group is None:
                current_leaf_group = []
            elif current_leaf_group_is_silent or \
                last_tie_chain != this_tie_chain:
                yield tietools.TieChain(current_leaf_group)
                current_leaf_group = []
            current_leaf_group_is_silent = False
            current_leaf_group.append(x)
            last_tie_chain = this_tie_chain

        elif isinstance(x, (resttools.Rest, skiptools.Skip)):
            if current_leaf_group is None:
                current_leaf_group = []
            elif not current_leaf_group_is_silent:
                yield tietools.TieChain(current_leaf_group)
                current_leaf_group = []
            current_leaf_group_is_silent = True
            current_leaf_group.append(x)
            last_tie_chain = None

        elif isinstance(x, containertools.Container):
            if current_leaf_group is not None:
                yield tietools.TieChain(current_leaf_group)
                current_leaf_group = None
                last_tie_chain = None
            yield x

        else:
            raise Exception('Unhandled component found {!r}', x) 

    if current_leaf_group is not None:
        yield tietools.TieChain(current_leaf_group)

