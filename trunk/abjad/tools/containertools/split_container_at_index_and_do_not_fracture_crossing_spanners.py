from abjad.tools.containertools.Container import Container
from abjad.tools.componenttools._split_component_at_index import _split_component_at_index


def split_container_at_index_and_do_not_fracture_crossing_spanners(container, index):
    r'''Split `container` at `index` and do not fracture crossing spanners::

        abjad> voice = Voice(Measure((3, 8), "c'8 c'8 c'8") * 2)
        abjad> pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(voice)
        abjad> beam = spannertools.BeamSpanner(voice[:])

    ::

        abjad> f(voice)
        \new Voice {
            {
                \time 3/8
                c'8 [
                d'8
                e'8
            }
            {
                \time 3/8
                f'8
                g'8
                a'8 ]
            }
        }

    ::

        abjad> containertools.split_container_at_index_and_do_not_fracture_crossing_spanners(voice[1], 1)
        (Measure(1/8, [f'8]), Measure(2/8, [g'8, a'8]))

    ::

        abjad> f(voice)
        \new Voice {
            {
                \time 3/8
                c'8 [
                d'8
                e'8
            }
            {
                \time 1/8
                f'8
            }
            {
                \time 2/8
                g'8
                a'8 ]
            }
        }

    Leave spanners and leaves untouched.

    Resize resizable containers.

    Preserve container multiplier.

    Preserve meter denominator.

    Return split parts.

    .. versionchanged:: 2.0
        renamed ``split.unfractured_at_index()`` to
        ``containertools.split_container_at_index_and_do_not_fracture_crossing_spanners()``.
    '''

    return _split_component_at_index(container, index, spanners = 'unfractured')
