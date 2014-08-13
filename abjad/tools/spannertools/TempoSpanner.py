# -*- encoding: utf-8 -*-
from abjad.tools import indicatortools
from abjad.tools import lilypondnametools
from abjad.tools.spannertools.Spanner import Spanner
from abjad.tools.topleveltools import inspect_


class TempoSpanner(Spanner):
    r'''Tempo spanner.

    ..  container:: example

            >>> staff = Staff("c'4 d' e' f' g' f' e' d' c'2")
            >>> attach(TimeSignature((2, 4)), staff)
            >>> score = Score([staff])

        ::

            >>> tempo = Tempo(Duration(1, 4), 60)
            >>> tempo._annotation_only = True
            >>> attach(tempo, staff[0])
            >>> tempo = Tempo(Duration(1, 4), 90)
            >>> tempo._annotation_only = True
            >>> attach(tempo, staff[4])
            >>> tempo = Tempo(Duration(1, 4), 60)
            >>> tempo._annotation_only = True
            >>> attach(tempo, staff[-1])

        ::

            >>> accelerando = indicatortools.Accelerando()
            >>> accelerando._annotation_only = True
            >>> attach(accelerando, staff[0])
            >>> ritardando = indicatortools.Ritardando()
            >>> ritardando._annotation_only = True
            >>> attach(ritardando, staff[4])

        ::

            >>> attach(spannertools.TempoSpanner(), staff[:])
            >>> show(score) # doctest: +SKIP

        ..  doctest::

            >>> print(format(score))
            \new Score <<
                \new Staff {
                    \time 2/4
                    \once \override TextSpanner.bound-details.left.text = \markup {
                        \smaller
                            \general-align
                                #Y
                                #DOWN
                                \note-by-number
                                    #2
                                    #0
                                    #1
                        " = 60"
                        }
                    c'4 \startTextSpan
                    d'4
                    e'4
                    f'4
                    \once \override TextSpanner.bound-details.left.text = \markup {
                        \smaller
                            \general-align
                                #Y
                                #DOWN
                                \note-by-number
                                    #2
                                    #0
                                    #1
                        " = 90"
                        }
                    g'4 \startTextSpan
                    f'4
                    e'4
                    d'4
                    c'2 \stopTextSpan
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

    ### PRIVATE METHODS ###

    def _get_previous_tempo(self, leaf):
        index = self._index(leaf)
        for index in reversed(range(index)):
            earlier_leaf = self[index]
            indicators = self._get_tempo_related_indicators(earlier_leaf)
            tempo, tempo_trend = indicators
            if tempo is not None:
                return tempo

    def _get_previous_tempo_trend(self, leaf):
        index = self._index(leaf)
        for index in reversed(range(index)):
            earlier_leaf = self[index]
            indicators = self._get_tempo_related_indicators(earlier_leaf)
            tempo, tempo_trend = indicators
            if tempo_trend is not None:
                return tempo_trend
            elif tempo is not None:
                return

    def _get_tempo_related_indicators(self, leaf):
        inspector = inspect_(leaf)
        tempo = None
        prototype = indicatortools.Tempo,
        if inspector.has_indicator(prototype):
            tempo = inspector.get_indicator(prototype)
        tempo_trend = None
        prototype = (
            indicatortools.Accelerando,
            indicatortools.Ritardando,
            )
        if inspector.has_indicator(prototype):
            tempo_trend = inspector.get_indicator(prototype)
        return (
            tempo,
            tempo_trend,
            )

    def _get_lilypond_format_bundle(self, leaf):
        lilypond_format_bundle = self._get_basic_lilypond_format_bundle(leaf)
        indicators = self._get_tempo_related_indicators(leaf)
        tempo = indicators[0]
        tempo_trend = indicators[1]
        if tempo is None and tempo_trend is None:
            pass
        elif tempo is None and tempo_trend is not None:
            self._start_tempo_trend_spanner_with_implicit_start(
                leaf,
                lilypond_format_bundle=lilypond_format_bundle,
                tempo_trend=tempo_trend,
                )
        elif tempo is not None and tempo_trend is None:
            self._make_lone_tempo_markup(
                leaf,
                lilypond_format_bundle=lilypond_format_bundle,
                tempo=tempo,
                )
        elif tempo is not None and tempo_trend is not None:
            self._start_tempo_trend_spanner_with_explicit_start(
                lilypond_format_bundle,
                tempo,
                tempo_trend,
                )
        else:
            raise Exception
        return lilypond_format_bundle

    def _make_lone_tempo_markup(
        self, 
        leaf,
        lilypond_format_bundle=None,
        tempo=None,
        ):
        assert tempo is not None
        previous_tempo_trend = self._get_previous_tempo_trend(leaf)
        if previous_tempo_trend is not None:
            string = r'\stopTextSpan'
            lilypond_format_bundle.right.spanner_stops.append(string)
        markup = tempo._to_markup()
        string = format(markup, 'lilypond')
        lilypond_format_bundle.opening.markup.append(string)

    def _start_tempo_trend_spanner_with_explicit_start(
        self,
        lilypond_format_bundle,
        tempo,
        tempo_trend,
        ):
        assert tempo is not None and tempo_trend is not None
        command = r'\startTextSpan'
        lilypond_format_bundle.right.spanner_starts.append(command)
        # TODO: implement parenthesization
        #tempo = tempo._parenthesize()
        markup = tempo._to_markup()
        override_ = lilypondnametools.LilyPondGrobOverride(
            grob_name='TextSpanner',
            is_once=True,
            property_path=(
                'bound-details',
                'left',
                'text',
                ),
            value=markup,
            )
        override_string = '\n'.join(override_._override_format_pieces)
        lilypond_format_bundle.grob_overrides.append(override_string)

    def _start_tempo_trend_spanner_with_implicit_start(
        self,
        leaf,
        lilypond_format_bundle=None,
        tempo_trend=None,
        ):
        assert tempo_trend is not None
        command = r'\startTextSpan'
        lilypond_format_bundle.right.spanner_starts.append(command)
        previous_tempo = self._get_previous_tempo(leaf)
        # TODO: implement parenthesization
        #previous_tempo = previous_tempo._parenthesize()
        markup = previous_tempo._to_markup()
        override_ = lilypondnametools.LilyPondGrobOverride(
            grob_name='TextSpanner',
            is_once=True,
            property_path=(
                'bound-details',
                'left',
                'text',
                ),
            value=markup,
            )
        override_string = '\n'.join(override_._override_format_pieces)
        lilypond_format_bundle.grob_overrides.append(override_string)