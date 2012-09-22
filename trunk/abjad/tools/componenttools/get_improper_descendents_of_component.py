def get_improper_descendents_of_component(component):
    r'''.. versionadded:: 2.9

    Get improper descendents of `component`::

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

        >>> for x in componenttools.get_improper_descendents_of_component(staff):
        ...     x
        ...
        Staff{2}
        Note("c'4")
        Tuplet(2/3, [d'8, e'8, f'8])
        Note("d'8")
        Note("e'8")
        Note("f'8")

    Function returns exactly the same components as 
    ``iterationtools.iterate_components_in_expr()``.

    Return list of `component` together with proper descendents of `component`.
    '''
    from abjad.tools import iterationtools

    # return list of component and all descendents of component
    return list(iterationtools.iterate_components_in_expr(component))
