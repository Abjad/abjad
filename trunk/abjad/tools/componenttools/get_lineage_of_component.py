def get_lineage_of_component(component):
    r'''.. versionadded:: 2.9

    Get lineage of `component`::

        >>> staff = Staff(r"c'4 \times 2/3 { d'8 e'8 f'8 }")

    ::

        f(staff)
        \new Staff {
            c'4
            \times 2/3 {
                d'8
                e'8
                f'8
            }
        }

    ::

        componenttools.get_lineage_of_component(staff[1])
        [Staff{2}, Tuplet(2/3, [d'8, e'8, f'8]), Note("d'8"), Note("e'8"), Note("f'8")]

    Return list of parentage, component and descendents.
    '''
    from abjad.tools import componenttools

    # initialize result
    result = []

    # add parentage of component
    result.extend(reversed(componenttools.get_proper_parentage_of_component(component)))

    # add component
    result.append(component)

    # add descendents of component
    result.extend(componenttools.get_proper_descendents_of_component(component))

    # return result
    return result
