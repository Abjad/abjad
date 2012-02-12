from abjad.tools.spannertools.get_spanners_attached_to_component import get_spanners_attached_to_component


def get_the_only_spanner_attached_to_component(component, klass = None):
    r'''.. versionadded:: 1.1

    Get the only spanner attached to `component`::

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

        abjad> print spannertools.get_the_only_spanner_attached_to_component(staff)
        TrillSpanner({c'8, d'8, e'8, f'8})

    Raise missing spanner error when no spanner attached to `component`.

    Raise extra spanner error when more than one spanner attached to `component`.

    Return a single spanner.

    .. note:: function will usually be called with `klass` specifier set.
    '''

    # get spanners and count spanners
    spanners_attached_to_component = get_spanners_attached_to_component(
        component, klass)
    count = len(spanners_attached_to_component)

    # raise or return
    if count == 0:
        raise MissingSpannerError
    elif count == 1:
        return spanners_attached_to_component.pop()
    else:
        raise ExtraSpannerError
