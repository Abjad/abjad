from abjad.tools.marktools.Articulation import Articulation


def get_articulations_attached_to_component(component):
    r'''.. versionadded:: 2.0

    Get articulations attached to `component`::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")
        abjad> marktools.Articulation('staccato')(staff[0])
        Articulation('staccato')(c'8)
        abjad> marktools.Articulation('marcato')(staff[0])
        Articulation('marcato')(c'8)

    ::

        abjad> f(staff)
        \new Staff {
            c'8 -\marcato -\staccato
            d'8
            e'8
            f'8
        }

    ::

        abjad> marktools.get_articulations_attached_to_component(staff[0])
        (Articulation('staccato')(c'8), Articulation('marcato')(c'8))

    Return tuple of zero or more articulations.
    '''

    result = []
    for mark in component._marks_for_which_component_functions_as_start_component:
        if isinstance(mark, Articulation):
            result.append(mark)

    result = tuple(result)
    return result
