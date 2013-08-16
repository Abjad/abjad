# -*- encoding: utf-8 -*-
from abjad.tools import sequencetools


def split_container_by_indices(
    container, 
    counts, 
    fracture_spanners=False, 
    cyclic=False,
    ):
    r'''Split `container` by `counts`.

    ..  container:: example

        **Example 1.** Split container cyclically by counts:

        ::

            >>> container = Container("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
            >>> staff = Staff([container])
            >>> slur = spannertools.SlurSpanner(container)
            >>> show(container) # doctest: +SKIP

        ..  doctest::

            >>> f(staff)
            \new Staff {
                {
                    c'8 (
                    d'8
                    e'8
                    f'8
                    g'8
                    a'8
                    b'8
                    c''8 )
                }
            }

        ::

            >>> containertools.split_container_by_indices(
            ...     container, 
            ...     [1, 3], 
            ...     cyclic=True, 
            ...     fracture_spanners=False,
            ...     )
            [[{c'8}], [{d'8, e'8, f'8}], [{g'8}], [{a'8, b'8, c''8}]]
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> f(staff)
            \new Staff {
                {
                    c'8 (
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
                    c''8 )
                }
            }

    ..  container:: example

        **Example 2.** Split container cyclically by counts and fracture 
        crossing spanners:

        ::

            >>> container = Container("{ c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8 }")
            >>> beam = spannertools.BeamSpanner(container)
            >>> slur = spannertools.SlurSpanner(container[0])
            >>> show(container) # doctest: +SKIP

        ..  doctest::

            >>> f(container)
            {
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

            >>> containertools.split_container_by_indices(
            ...     container[0], 
            ...     [1, 3], 
            ...     cyclic=True, 
            ...     fracture_spanners=True,
            ...     )
            [[{c'8}], [{d'8, e'8, f'8}], [{g'8}], [{a'8, b'8, c''8}]]
            >>> show(container) # doctest: +SKIP

        ..  doctest::

            >>> f(container)
            {
                {
                    c'8 [ ( )
                }
                {
                    d'8 (
                    e'8
                    f'8 )
                }
                {
                    g'8 ( )
                }
                {
                    a'8 (
                    b'8
                    c''8 ] )
                }
            }

    ..  container:: example

        **Example 3.** Split container once by counts and do not fracture 
        crossing spanners:

        ::

            >>> container = Container("{ c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8 }")
            >>> beam = spannertools.BeamSpanner(container)
            >>> slur = spannertools.SlurSpanner(container[0])
            >>> show(container) # doctest: +SKIP

        ..  doctest::

            >>> f(container)
            {
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

            >>> containertools.split_container_by_indices(
            ...     container[0], 
            ...     [1, 3], 
            ...     cyclic=False, 
            ...     fracture_spanners=False,
            ...     )
            [[{c'8}], [{d'8, e'8, f'8}], [{g'8, a'8, b'8, c''8}]]
            >>> show(container) # doctest: +SKIP

        ..  doctest::

            >>> f(container)
            {
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

    ..  container:: example

        **Example 4.** Split container once by counts and fracture crossing 
        spanners:

        ::

            >>> container = Container("{ c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8 }")
            >>> beam = spannertools.BeamSpanner(container)
            >>> slur = spannertools.SlurSpanner(container[0])
            >>> show(container) # doctest: +SKIP

        ..  doctest::

            >>> f(container)
            {
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

            >>> containertools.split_container_by_indices(
            ...     container[0], 
            ...     [1, 3], 
            ...     cyclic=False, 
            ...     fracture_spanners=True,
            ...     )
            [[{c'8}], [{d'8, e'8, f'8}], [{g'8, a'8, b'8, c''8}]]
            >>> show(container) # doctest: +SKIP

        ..  doctest::

            >>> f(container)
            {
                {
                    c'8 [ ( )
                }
                {
                    d'8 (
                    e'8
                    f'8 )
                }
                {
                    g'8 (
                    a'8
                    b'8
                    c''8 ] )
                }
            }

    Returns list of split parts.
    '''
    from abjad.tools import containertools

    assert isinstance(container, containertools.Container)
    assert sequencetools.all_are_positive_integers(counts)

    if counts == []:
        return [[container]]

    counts = sequencetools.truncate_sequence_to_sum(counts, len(container))
    if cyclic:
        counts = sequencetools.repeat_sequence_to_weight_exactly(
            counts, 
            len(container),
            )
    if sum(counts) == len(container):
        counts = counts[:-1]

    result = []
    remaining = container
    for count in counts:
        left, remaining = containertools.split_container_at_index(
            remaining, 
            count, 
            fracture_spanners=fracture_spanners,
            )
        result.append([left])
    result.append([remaining])

    return result
