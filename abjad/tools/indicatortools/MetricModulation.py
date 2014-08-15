# -*- encoding: utf-8 -*-
from abjad.tools.abctools.AbjadObject import AbjadObject


class MetricModulation(AbjadObject):
    r'''A metric modulation.

    ..  container:: example

        ::

            >>> staff = Staff("c'4 d' e' f' e' d'")
            >>> attach(TimeSignature((3, 4)), staff)
            >>> score = Score([staff])

        ::

            >>> tempo_1 = Tempo(Duration(1, 4), 60)
            >>> attach(tempo_1, staff[0], is_annotation=True)
            >>> tempo_2 = Tempo(Duration(1, 4), 90)
            >>> attach(tempo_2, staff[3], is_annotation=True)

        ::

            >>> metric_modulation = indicatortools.MetricModulation(
            ...     left_tempo=tempo_1,
            ...     right_tempo=tempo_2,
            ...     )

        ::

            >>> print(format(metric_modulation))
            indicatortools.MetricModulation(
                left_tempo=indicatortools.Tempo(
                    duration=durationtools.Duration(1, 4),
                    units_per_minute=60,
                    ),
                right_tempo=indicatortools.Tempo(
                    duration=durationtools.Duration(1, 4),
                    units_per_minute=90,
                    ),
                )

        ::

            >>> attach(metric_modulation, staff[3])
            >>> attach(spannertools.TempoSpanner(), staff[:])
            >>> show(score) # doctest: +SKIP

        ..  doctest::

            >>> print(format(score))
            \new Score <<
                \new Staff {
                    \time 3/4
                    c'4 ^ \markup {
                        \smaller
                            \general-align
                                #Y
                                #DOWN
                                \note-by-number
                                    #2
                                    #0
                                    #1
                        \upright
                            " = 60"
                        }
                    d'4
                    e'4
                    f'4 ^ \markup {
                        \smaller
                            \general-align
                                #Y
                                #DOWN
                                \note-by-number
                                    #2
                                    #0
                                    #1
                        \upright
                            " = 90"
                        }
                    e'4
                    d'4
                }
            >>

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_left_markup',
        '_left_tempo',
        '_right_markup',
        '_right_tempo',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        left_tempo=None,
        right_tempo=None,
        left_markup=None,
        right_markup=None,
        ):
        from abjad.tools import indicatortools
        from abjad.tools import markuptools
        from abjad.tools import scoretools
        # TODO: make default scope work
        #self._default_scope = scoretools.Score
        if left_tempo is not None:
            assert isinstance(left_tempo, indicatortools.Tempo)
        self._left_tempo = left_tempo
        if right_tempo is not None:
            assert isinstance(right_tempo, indicatortools.Tempo)
        self._right_tempo = right_tempo
        if left_markup is not None:
            assert isinstance(left_markup, markuptools.Markup)
        self._left_markup = left_markup
        if right_markup is not None:
            assert isinstance(right_markup, markuptools.Markup)
        self._right_markup = right_markup

    ### PUBLIC PROPERTIES ###

    @property
    def left_markup(self):
        r'''Gets left markup of metric modulation.

        Returns markup or none.
        '''
        return self._left_markup

    @property
    def left_tempo(self):
        r'''Gets left tempo of metric modulation.

        Returns tempo or none.
        '''
        return self._left_tempo

    @property
    def right_markup(self):
        r'''Gets right markup of metric modulation.

        Returns markup or none.
        '''
        return self._right_markup

    @property
    def right_tempo(self):
        r'''Gets right tempo of metric modulation.

        Returns tempo or none.
        '''
        return self._right_tempo