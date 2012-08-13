def split_container_cyclically_by_counts_and_do_not_fracture_crossing_spanners(container, counts):
    r'''Split `container` cyclically by `counts` and do not fracture crossing spanners::

    .. note:: Deprecated. Use ``containertools.split_container_by_counts()`` instead.

        >>> container = Container("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
        >>> voice = Voice([container])
        >>> beam = beamtools.BeamSpanner(voice)
        >>> slur = spannertools.SlurSpanner(container)

    ::

        >>> f(voice)
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

        >>> containertools.split_container_cyclically_by_counts_and_do_not_fracture_crossing_spanners(container, [1, 3])
        [[{c'8}], [{d'8, e'8, f'8}], [{g'8}], [{a'8, b'8, c''8}]]

    ::

        >>> f(voice)
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
            }
            {
                a'8
                b'8
                c''8 ] )
            }
        }

    Return list of list-wrapped container pieces.

    .. versionchanged:: 2.0
        renamed ``partition.cyclic_unfractured_by_counts()`` to
        ``containertools.split_container_cyclically_by_counts_and_do_not_fracture_crossing_spanners()``.
    '''
    from abjad.tools import containertools

    return containertools.split_container_by_counts(container, counts, fracture_spanners=False, cyclic=True)
