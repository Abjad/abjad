# -*- coding: utf-8 -*-
from abjad.tools.abctools import AbjadObject


class Quantizer(AbjadObject):
    r'''``Quantizer`` quantizes sequences of attack-points, encapsulated by
    ``QEventSequences``, into score trees.

    ::

        >>> quantizer = quantizationtools.Quantizer()

    ::

        >>> durations = [1000] * 8
        >>> pitches = range(8)
        >>> q_event_sequence = \
        ...     quantizationtools.QEventSequence.from_millisecond_pitch_pairs(
        ...     tuple(zip(durations, pitches)))

    Quantization defaults to outputting into a 4/4, quarter=60 musical
    structure:

    ::

        >>> result = quantizer(q_event_sequence)
        >>> score = Score([Staff([result])])
        >>> print(format(score))
        \new Score <<
            \new Staff {
                \new Voice {
                    {
                        \tempo 4=60
                        \time 4/4
                        c'4
                        cs'4
                        d'4
                        ef'4
                    }
                    {
                        e'4
                        f'4
                        fs'4
                        g'4
                    }
                }
            }
        >>

    ::

        >>> show(score) # doctest: +SKIP

    However, the behavior of the ``Quantizer`` can be modified at call-time.
    Passing a ``QSchema`` instance will alter the macro-structure of the
    output.

    Here, we quantize using settings specified by a ``MeasurewiseQSchema``,
    which will cause the ``Quantizer`` to group the output into measures
    with different tempi and time signatures:

    ::

        >>> measurewise_q_schema = quantizationtools.MeasurewiseQSchema(
        ...     {'tempo': ((1, 4), 78), 'time_signature': (2, 4)},
        ...     {'tempo': ((1, 8), 57), 'time_signature': (5, 4)},
        ...     )

    ::

        >>> result = quantizer(q_event_sequence, q_schema=measurewise_q_schema)
        >>> score = Score([Staff([result])])
        >>> print(format(score))
        \new Score <<
            \new Staff {
                \new Voice {
                    {
                        \tempo 4=78
                        \time 2/4
                        c'4 ~
                        \times 4/5 {
                            c'16.
                            cs'8.. ~
                        }
                    }
                    {
                        \tempo 8=57
                        \time 5/4
                        \times 4/7 {
                            cs'16.
                            d'8 ~
                        }
                        \times 4/5 {
                            d'16
                            ef'16. ~
                        }
                        \times 2/3 {
                            ef'16
                            e'8 ~
                        }
                        \times 4/7 {
                            e'16
                            f'8 ~
                            f'32 ~
                        }
                        f'32
                        fs'16. ~
                        \times 4/5 {
                            fs'32
                            g'8 ~
                        }
                        \times 4/7 {
                            g'32
                            r32
                            r16
                            r16
                            r16
                            r16
                            r16
                            r16
                        }
                        r4
                    }
                }
            }
        >>

    ::

        >>> show(score) # doctest: +SKIP

    Here we quantize using settings specified by a ``BeatwiseQSchema``,
    which keeps the output of the quantizer "flattened", without measures or
    explicit time signatures.  The default beat-wise settings of quarter=60
    persists until the third "beatspan":

    ::

        >>> beatwise_q_schema = quantizationtools.BeatwiseQSchema(
        ... {
        ...     2: {'tempo': ((1, 4), 120)},
        ...     5: {'tempo': ((1, 4), 90)},
        ...     7: {'tempo': ((1, 4), 30)},
        ... })

    ::

        >>> result = quantizer(
        ...     q_event_sequence,
        ...     q_schema=beatwise_q_schema,
        ...     )
        >>> score = Score([Staff([result])])
        >>> print(format(score))
        \new Score <<
            \new Staff {
                \new Voice {
                    \tempo 4=60
                    c'4
                    cs'4
                    \tempo 4=120
                    d'2
                    ef'4 ~
                    \tempo 4=90
                    ef'8.
                    e'4 ~
                    e'16 ~
                    \times 2/3 {
                        \tempo 4=30
                        e'32
                        f'8.
                        fs'8 ~
                        fs'32 ~
                    }
                    \times 2/3 {
                        fs'32
                        g'8.
                        r32
                        r8
                    }
                }
            }
        >>

    ::

        >>> show(score) # doctest: +SKIP

    Note that ``TieChains`` are generally fused together in the above example,
    but break at tempo changes.

    Other keyword arguments are:

        * ``grace_handler``: a ``GraceHandler`` instance controls whether and
          how grace notes are used in the output.  Options currently include
          ``CollapsingGraceHandler``, ``ConcatenatingGraceHandler`` and
          ``DiscardingGraceHandler``.

        * ``heuristic``: a ``Heuristic`` instance controls how output rhythms
          are selected from a pool of candidates.  Options currently include
          the ``DistanceHeuristic`` class.

        * ``job_handler``: a ``JobHandler`` instance controls whether or not
          parallel processing is used during the quantization process.
          Options include the ``SerialJobHandler`` and ``ParallelJobHandler``
          classes.

        * ``attack_point_optimizer``: an ``AttackPointOptimizer`` instance
          controls whether and how logical ties are re-notated.
          Options currently include ``MeasurewiseAttackPointOptimizer``,
          ``NaiveAttackPointOptimizer`` and ``NullAttackPointOptimizer``.

    Refer to the reference pages for ``BeatwiseQSchema`` and
    ``MeasurewiseQSchema`` for more information on controlling the
    ``Quantizer``'s output, and to the reference on ``SearchTree`` for
    information on controlling the rhythmic complexity of that same output.
    '''

    ### INITIALIZER ###

    def __init__(self):
        pass

    ### SPECIAL METHODS ###

    def __call__(self,
        q_event_sequence,
        q_schema=None,
        grace_handler=None,
        heuristic=None,
        job_handler=None,
        attack_point_optimizer=None,
        attach_tempos=True,
        ):
        r'''Calls quantizer.

        Returns Abjad components.
        '''
        from abjad.tools import quantizationtools

        q_event_sequence = quantizationtools.QEventSequence(q_event_sequence)

        if q_schema is None:
            q_schema = quantizationtools.MeasurewiseQSchema()
        assert isinstance(q_schema, quantizationtools.QSchema)

        q_target = q_schema(q_event_sequence.duration_in_ms)

        notation = q_target(q_event_sequence,
            grace_handler=grace_handler,
            heuristic=heuristic,
            job_handler=job_handler,
            attack_point_optimizer=attack_point_optimizer,
            attach_tempos=attach_tempos,
            )

        return notation
