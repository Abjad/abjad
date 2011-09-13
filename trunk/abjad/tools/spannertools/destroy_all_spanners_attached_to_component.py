from abjad.tools.spannertools.get_spanners_attached_to_component import get_spanners_attached_to_component


def destroy_all_spanners_attached_to_component(component, klass = None):
    r'''.. versionadded:: 1.1

    Destroy all spanners attached to `component`::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")
        abjad> beam = spannertools.BeamSpanner(staff.leaves)
        abjad> slur = spannertools.SlurSpanner(staff.leaves)
        abjad> trill = spannertools.TrillSpanner(staff)
        abjad> f(staff)
        \new Staff {
            c'8 [ ( \startTrillSpan
            d'8
            e'8
            f'8 ] ) \stopTrillSpan
        }

    ::

        abjad> spannertools.destroy_all_spanners_attached_to_component(staff[0])
        abjad> f(staff)
        \new Staff {
            c'8 \startTrillSpan
            d'8
            e'8
            f'8 \stopTrillSpan
        }

    Return none.
    '''

    for spanner in get_spanners_attached_to_component(component):
        if klass is None:
            spanner.clear()
        elif isinstance(spanner, klass):
            spanner.clear()
