from abjad.tools.marktools.get_articulations_attached_to_component import get_articulations_attached_to_component


def detach_articulations_attached_to_component(component):
    r'''.. versionadded:: 2.0

    Detach articulations attached to `component`::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")
        abjad> slur = spannertools.SlurSpanner(staff.leaves)
        abjad> marktools.Articulation('^')(staff[0])
        Articulation('^')(c'8)
        abjad> marktools.Articulation('.')(staff[0])
        Articulation('.')(c'8)

    ::

        abjad> f(staff)
        \new Staff {
            c'8 -\marcato -\staccato (
            d'8
            e'8
            f'8 )
        }

    ::

        abjad> marktools.get_articulations_attached_to_component(staff[0])
        (Articulation('^')(c'8), Articulation('.')(c'8))

    ::

        abjad> marktools.detach_articulations_attached_to_component(staff[0])
        (Articulation('^'), Articulation('.'))

    ::

        abjad> marktools.get_articulations_attached_to_component(staff[0])
        ()

    Return tuple or zero or more articulations detached.
    '''

    articulations = []
    for articulation in get_articulations_attached_to_component(component):
        articulation.detach()
        articulations.append(articulation)

    return tuple(articulations)
