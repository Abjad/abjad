from abjad.tools.componenttools.get_proper_parentage_of_component import get_proper_parentage_of_component


def component_to_tuplet_depth(component):
    '''.. versionadded:: 1.1

    Change `component` to tuplet depth::

        >>> tuplet = tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")
        >>> staff = Staff([tuplet])
        >>> note = staff.leaves[0]

    ::

        >>> componenttools.component_to_tuplet_depth(note)
        1

    ::

        >>> componenttools.component_to_tuplet_depth(tuplet)
        0

    ::

        >>> componenttools.component_to_tuplet_depth(staff)
        0

    Return nonnegative integer.
    '''
    from abjad.tools.tuplettools.Tuplet import Tuplet

    result = 0
    for parent in get_proper_parentage_of_component(component):
        if isinstance(parent, Tuplet):
            result += 1
    return result
