

def split_container_once_by_counts_and_do_not_fracture_crossing_spanners(container, counts):
    r'''Split `container` once by `counts` and do no fracture crossing spanners::

        abjad> container = Container("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
        abjad> voice = Voice([container])
        abjad> beam = spannertools.BeamSpanner(voice)
        abjad> slur = spannertools.SlurSpanner(container)

    ::

        abjad> f(voice)
        \new Voice {
            {
                c'8 [ (
                d'8
                e'8
                f'8
                g'8
                a'8
                b'8
                c''8 ] )
            }
        }

    ::

        abjad> containertools.split_container_once_by_counts_and_do_not_fracture_crossing_spanners(container, [1, 3])
        [[{c'8}], [{d'8, e'8, f'8}], [{g'8, a'8, b'8, c''8}]]

    ::

        abjad> f(voice)
        \new Voice {
            {
                c'8 [ (
            }
            {
                d'8
                e'8
                f'8
            }
            {
                g'8
                a'8
                b'8
                c''8 ] )
            }
        }

    Return list of list-wrapped container pieces.

    .. versionchanged:: 2.0
        renamed ``partition.unfractured_by_counts()`` to
        ``containertools.split_container_once_by_counts_and_do_not_fracture_crossing_spanners()``.
    '''
    from abjad.tools.containertools._split_container_by_counts import _split_container_by_counts

    return _split_container_by_counts(container, counts, spanners = 'unfractured')
