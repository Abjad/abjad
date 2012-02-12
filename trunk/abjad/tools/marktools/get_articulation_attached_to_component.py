from abjad.tools.marktools.get_articulations_attached_to_component import get_articulations_attached_to_component


def get_articulation_attached_to_component(component):
    r'''.. versionadded:: 2.0

    Get exactly one articulation attached to `component`::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")
        abjad> marktools.Articulation('staccato')(staff[0])
        Articulation('staccato')(c'8)

    ::

        abjad> f(staff)
        \new Staff {
            c'8 -\staccato
            d'8
            e'8
            f'8
        }

    ::

        abjad> marktools.get_articulation_attached_to_component(staff[0])
        Articulation('staccato')(c'8)

    Return one articulation.

    Raise missing mark error when no articulation is attached.

    Raise extra mark error when more than one articulation is attached.
    '''

    articulations = get_articulations_attached_to_component(component)
    if not articulations:
        raise MissingMarkError
    elif 1 < len(articulations):
        raise ExtraMarkError
    else:
        return articulations[0]
