def apply_beam_spanners_to_measures_in_expr(expr):
    r'''.. versionadded:: 1.1

    Apply beam spanners to measures in `expr`::

        >>> staff = Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")

    ::

        >>> f(staff)
        \new Staff {
            {
                \time 2/8
                c'8
                d'8
            }
            {
                e'8
                f'8
            }
        }

    ::

        >>> show(staff) # doctest: +SKIP

    ::

        >>> beamtools.apply_beam_spanners_to_measures_in_expr(staff)
        [BeamSpanner(|2/8(2)|), BeamSpanner(|2/8(2)|)]

    ::

        >>> f(staff)
        \new Staff {
            {
                \time 2/8
                c'8 [
                d'8 ]
            }
            {
                e'8 [
                f'8 ]
            }
        }

    ::

        >>> show(staff) # doctest: +SKIP

    Return list of beams created.
    '''
    from abjad.tools import beamtools
    from abjad.tools import iterationtools

    # init beams created
    beams_created = []

    # apply beam spanners to measures in expr
    for measure in iterationtools.iterate_measures_in_expr(expr):
        beam = beamtools.BeamSpanner(measure)
        beams_created.append(beam)

    # return beams created
    return beams_created
