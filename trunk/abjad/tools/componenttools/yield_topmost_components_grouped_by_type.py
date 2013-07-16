import itertools
import types


def yield_topmost_components_grouped_by_type(expr):
    r'''.. versionadded:: 2.0

    Example 1. Yield topmost components in `expr` grouped by type:

    ::

        >>> staff = Staff(r"\times 2/3 { c'8 d'8 r8 } \times 2/3 { r8 <e' g'>8 <f' a'>8 }")
        >>> staff.extend("g'8 a'8 r8 r8 <b' d''>8 <c'' e''>8")

    ::

        >>> f(staff)
        \new Staff {
            \times 2/3 {
                c'8
                d'8
                r8
            }
            \times 2/3 {
                r8
                <e' g'>8
                <f' a'>8
            }
            g'8
            a'8
            r8
            r8
            <b' d''>8
            <c'' e''>8
        }

    ::

        >>> for x in componenttools.yield_topmost_components_grouped_by_type(
        ...     staff[:]):
        ...     x
        (Tuplet(2/3, [c'8, d'8, r8]), Tuplet(2/3, [r8, <e' g'>8, <f' a'>8]))
        (Note("g'8"), Note("a'8"))
        (Rest('r8'), Rest('r8'))
        (Chord("<b' d''>8"), Chord("<c'' e''>8"))

    Example 2. Yield leaves at all score levels in `expr` grouped by type:

    ::

        >>> leaves = iterationtools.iterate_leaves_in_expr(staff)

    ::

        >>> for x in componenttools.yield_topmost_components_grouped_by_type(
        ...     leaves):
        ...     x
        (Note("c'8"), Note("d'8"))
        (Rest('r8'), Rest('r8'))
        (Chord("<e' g'>8"), Chord("<f' a'>8"))
        (Note("g'8"), Note("a'8"))
        (Rest('r8'), Rest('r8'))
        (Chord("<b' d''>8"), Chord("<c'' e''>8"))

    Return generator.
    '''
    from abjad.tools import containertools
    from abjad.tools import selectiontools

    assert isinstance(expr, (
        list,
        tuple,
        types.GeneratorType, 
        selectiontools.Selection)), repr(expr)

#    grouper = itertools.groupby(expr, type)
#    for leaf_type, generator in grouper:
#        yield tuple(generator)

    selection = selectiontools.Selection(expr)
    groups = selection.group_by(type)
    for group in groups:
        yield group
