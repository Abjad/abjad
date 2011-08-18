from abjad.tools.componenttools.get_improper_parentage_of_component import get_improper_parentage_of_component


def component_to_score_root(component):
    '''.. versionadded:: 1.1

    Change `component` to score root::

        abjad> tuplet = tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")
        abjad> staff = Staff([tuplet])
        abjad> note = staff.leaves[0]
        abjad> componenttools.component_to_score_root(note)
        Staff{1}

    Return score root.
    '''

    return get_improper_parentage_of_component(component)[-1]
