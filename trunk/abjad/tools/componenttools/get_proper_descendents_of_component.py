def get_proper_descendents_of_component(component):
    r'''.. versionadded:: 2.9

    Get proper descendents of `component`::

        >>> staff = Staff(r"c'4 \times 2/3 { d'8 e'8 f'8 }")

    ::

        >>> f(staff)
        \new Staff {
            c'4
            \times 2/3 {
                d'8
                e'8
                f'8
            }
        }

    ::

        >>> componenttools.get_proper_descendents_of_component(staff)
        [Note("c'4"), Tuplet(2/3, [d'8, e'8, f'8]), Note("d'8"), Note("e'8"), Note("f'8")]

    Return list of proper descendents of `component`.
    '''
    from abjad.tools import iterationtools

    # create list of component and all descendents of component
    result = list(iterationtools.iterate_components_in_expr(component))

    # remove component from list
    result.remove(component)

    # return result
    return result
