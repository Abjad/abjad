# -*- encoding: utf-8 -*-
from abjad.tools.spannertools.Spanner import Spanner


class TempoSpanner(Spanner):
    r'''Tempo spanner.

    ..  container:: example

            >>> staff = Staff("c'4 d' e' f' g' f' e' d' c'2")
            >>> attach(TimeSignature((2, 4)), staff)
            >>> score = Score([staff])

        ::

            >>> attach(Tempo(Duration(1, 4), 60), staff[0])
            >>> attach(Tempo(Duration(1, 4), 90), staff[4])
            >>> attach(Tempo(Duration(1, 4), 60), staff[-1])

        ::

            >>> attach(spannertools.TempoSpanner(), staff[:])
            >>> show(score) # doctest: +SKIP

        ..  doctest::

            >>> print(format(score))
            \new Score <<
                \new Staff {
                    \time 2/4
                    \tempo 4=60
                    c'4
                    d'4
                    e'4
                    f'4
                    \tempo 4=90
                    g'4
                    f'4
                    e'4
                    d'4
                    \tempo 4=60
                    c'2
                }
            >>

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(
        self,
        overrides=None,
        ):
        Spanner.__init__(
            self,
            overrides=overrides,
            )