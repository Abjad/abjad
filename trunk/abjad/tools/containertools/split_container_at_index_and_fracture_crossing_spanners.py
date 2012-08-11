from abjad.tools.containertools.Container import Container
from abjad.tools.componenttools._split_component_at_index import _split_component_at_index


def split_container_at_index_and_fracture_crossing_spanners(container, index):
    r'''Split `container` at `index` and fracture crossing spanners::

        >>> voice = Voice(tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 c'8 c'8") * 2)
        >>> tuplet = voice[1]
        >>> pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(voice)
        >>> beam = beamtools.BeamSpanner(voice[:])

    ::

        >>> f(voice)
        \new Voice {
            \times 2/3 {
                c'8 [
                d'8
                e'8
            }
            \times 2/3 {
                f'8
                g'8
                a'8 ]
            }
        }

    ::

        >>> left, right = containertools.split_container_at_index_and_fracture_crossing_spanners(tuplet, 1)

    ::

        >>> f(voice)
        \new Voice {
            \times 2/3 {
                c'8 [
                d'8
                e'8
            }
            \times 2/3 {
                f'8 ]
            }
            \times 2/3 {
                g'8 [
                a'8 ]
            }
        }

    Leave leaves untouched.

    Create two new copies of `container`.

    Empty `container` of original contents.

    Return split parts.

    .. versionchanged:: 2.0
        renamed ``split.fractured_at_index()`` to
        ``containertools.split_container_at_index_and_fracture_crossing_spanners()``.
    '''

    return _split_component_at_index(container, index, fracture_spanners=True)
