from abjad.tools.componenttools.yield_topmost_components_grouped_by_type import yield_topmost_components_grouped_by_type


def yield_topmost_components_of_klass_grouped_by_type(expr, klass):
    '''.. versionadded:: 2.0

    Yield topmost components of `klass` in `expr` grouped by type::

        abjad> staff = Staff(leaftools.make_leaves([0, 2, 4, None, None, 5, 7], [(1, 8)]))
        abjad> for x in componenttools.yield_topmost_components_of_klass_grouped_by_type(staff, Note):
        ...     x
        ...
        (Note("c'8"), Note("d'8"), Note("e'8"))
        (Note("f'8"), Note("g'8"))

    Return generator.
    '''

    for group in yield_topmost_components_grouped_by_type(expr):
        if isinstance(group[0], klass):
            yield group
