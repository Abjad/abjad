import itertools


def yield_topmost_components_grouped_by_type(expr):
    '''.. versionadded:: 2.0

    Yield topmost components in `expr` grouped by type::

        abjad> staff = Staff(leaftools.make_leaves([0, 2, 4, None, None, 5, 7], [(1, 8)]))
        abjad> for x in componenttools.yield_topmost_components_grouped_by_type(staff):
        ...     x
        ...
        (Note("c'8"), Note("d'8"), Note("e'8"))
        (Rest('r8'), Rest('r8'))
        (Note("f'8"), Note("g'8"))

    Return generator.
    '''

    grouper = itertools.groupby(expr, type)
    for leaf_type, generator in grouper:
        yield tuple(generator)
