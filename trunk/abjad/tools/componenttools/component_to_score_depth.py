from abjad.tools.componenttools.get_proper_parentage_of_component import get_proper_parentage_of_component


def component_to_score_depth(component):
    '''.. versionadded:: 1.1

    Change `component` to score depth::

        abjad> tuplet = tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")
        abjad> staff = Staff([tuplet])
        abjad> componenttools.component_to_score_depth(staff.leaves[0])
        2

    Return nonnegative integer.
    '''

    return len(get_proper_parentage_of_component(component))
