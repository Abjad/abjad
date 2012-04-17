from abjad.tools.spannertools.get_spanners_attached_to_component import get_spanners_attached_to_component


def destroy_spanners_attached_to_component(component, klass=None):
    r'''.. versionadded:: 1.1

    Destroy spanners of `klass` attached to `component`::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")
        abjad> beam = spannertools.BeamSpanner(staff.leaves)
        abjad> slur = spannertools.SlurSpanner(staff.leaves)
        abjad> trill = spannertools.TrillSpanner(staff)

    ::

        abjad> f(staff)
        \new Staff {
            c'8 [ ( \startTrillSpan
            d'8
            e'8
            f'8 ] ) \stopTrillSpan
        }

    ::

        abjad> spanners = spannertools.destroy_spanners_attached_to_component(staff[0])

    ::

        abjad> f(staff)
        \new Staff {
            c'8 \startTrillSpan
            d'8
            e'8
            f'8 \stopTrillSpan
        }

    Destroy all spanners when `klass` is none.

    Return tuple of zero or more empty spanners.

    Order of spanners in return value can not be predicted.
    '''

    result = []
    for spanner in get_spanners_attached_to_component(component):
        if klass is None or isinstance(spanner, klass):
            spanner.clear()
            result.append(spanner)

    return tuple(result)
