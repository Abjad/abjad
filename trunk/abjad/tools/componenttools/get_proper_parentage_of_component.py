from abjad.tools.componenttools.get_improper_parentage_of_component import get_improper_parentage_of_component


def get_proper_parentage_of_component(component):
    '''.. versionadded:: 1.1

    Get proper parentage of `component`::

        abjad> tuplet = tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")
        abjad> staff = Staff([tuplet])
        abjad> note = staff.leaves[0]
        abjad> componenttools.get_proper_parentage_of_component(note)
        (FixedDurationTuplet(1/4, [c'8, d'8, e'8]), Staff{1})

    Return tuple of zero or more components.
    '''

    return get_improper_parentage_of_component(component)[1:]
