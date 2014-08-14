# -*- encoding: utf-8 -*-
from abjad.tools import indicatortools
from abjad.tools import lilypondnametools
from abjad.tools import markuptools
from abjad.tools.spannertools.Spanner import Spanner
from abjad.tools.topleveltools import inspect_
from abjad.tools.topleveltools import new


class TempoSpanner(Spanner):
    r'''Tempo spanner.

    ..  container:: example

            >>> staff = Staff("c'4 d' e' f' g' f' e' d' c'2")
            >>> attach(TimeSignature((2, 4)), staff)
            >>> score = Score([staff])
            >>> override(score).text_script.staff_padding = 1.5
            >>> override(score).text_spanner.staff_padding = 2

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
            \new Score \with {
                \override TextScript #'staff-padding = #1.5
                \override TextSpanner #'staff-padding = #2
            } <<
                \new Staff {
                    \time 2/4
                    \once \override TextSpanner.arrow-width = 0.25
                    \once \override TextSpanner.bound-details.left-broken.padding = -2
                    \once \override TextSpanner.bound-details.left-broken.text = \markup {
                        \parenthesize
                        \large
                            {
                                \italic
                                    {
                                        accel.
                                    }
                            }
                        \hspace
                            #0.75
                        }
                    \once \override TextSpanner.bound-details.left.stencil-align-dir-y = -0.5
                    \once \override TextSpanner.bound-details.left.text = \markup {
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
                        \hspace
                            #1.25
                        }
                    \once \override TextSpanner.bound-details.right-broken.arrow = ##f
                    \once \override TextSpanner.bound-details.right-broken.padding = 0
                    \once \override TextSpanner.bound-details.right-broken.text = ##f
                    \once \override TextSpanner.bound-details.right.arrow = ##t
                    \once \override TextSpanner.bound-details.right.padding = 2
                    \once \override TextSpanner.bound-details.right.text = ##f
                    \once \override TextSpanner.dash-fraction = 0.25
                    \once \override TextSpanner.dash-period = 1.5
                    c'4 \startTextSpan
                    d'4
                    e'4
                    f'4
                    \once \override TextSpanner.arrow-width = 0.25
                    \once \override TextSpanner.bound-details.left-broken.padding = -2
                    \once \override TextSpanner.bound-details.left-broken.text = \markup {
                        \parenthesize
                        \large
                            {
                                \italic
                                    {
                                        rit.
                                    }
                            }
                        \hspace
                            #0.75
                        }
                    \once \override TextSpanner.bound-details.left.stencil-align-dir-y = -0.5
                    \once \override TextSpanner.bound-details.left.text = \markup {
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
                        \hspace
                            #1.25
                        }
                    \once \override TextSpanner.bound-details.right-broken.arrow = ##f
                    \once \override TextSpanner.bound-details.right-broken.padding = 0
                    \once \override TextSpanner.bound-details.right-broken.text = ##f
                    \once \override TextSpanner.bound-details.right.arrow = ##t
                    \once \override TextSpanner.bound-details.right.padding = 2
                    \once \override TextSpanner.bound-details.right.text = ##f
                    \once \override TextSpanner.dash-fraction = 0.25
                    \once \override TextSpanner.dash-period = 1.5
                    g'4 \stopTextSpan \startTextSpan
                    f'4
                    e'4
                    d'4
                    c'2 \stopTextSpan ^ \markup {
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

    def _get_current_annotations(self, leaf):
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

    def _get_next_annotations(self, leaf):
        index = self._index(leaf)
        next_index = index + 1
        if next_index == len(self):
            return None, None
        for next_leaf in self[next_index:]:
            annotations = self._get_current_annotations(next_leaf)
            tempo, tempo_trend = annotations
            if tempo is not None or tempo_trend is not None:
                return annotations
        return None, None

    def _get_previous_annotations(self, leaf):
        index = self._index(leaf)
        for index in reversed(range(index)):
            previous_leaf = self[index]
            annotations = self._get_current_annotations(previous_leaf)
            tempo, tempo_trend = annotations
            if tempo is not None or tempo_trend is not None:
                return annotations
        return None, None

    def _get_lilypond_format_bundle(self, leaf):
        lilypond_format_bundle = self._get_basic_lilypond_format_bundle(leaf)
        current_annotations = self._get_current_annotations(leaf)
        current_tempo, current_tempo_trend = current_annotations
        if current_tempo is None and current_tempo_trend is None:
            return lilypond_format_bundle
        previous_annotations = self._get_previous_annotations(leaf)
        previous_tempo, previous_tempo_trend = previous_annotations
        next_annotations = self._get_next_annotations(leaf)
        next_tempo, next_tempo_trend = next_annotations
        # stop any previous tempo trend
        if previous_tempo_trend:
            spanner_stop = r'\stopTextSpan'
            lilypond_format_bundle.right.spanner_stops.append(spanner_stop)
        # use markup if no tempo trend starts now
        if current_tempo_trend is None:
            markup = current_tempo._to_markup()
            markup = new(markup, direction=Up)
            string = format(markup, 'lilypond')
            lilypond_format_bundle.right.markup.append(string)
        # use spanner if tempo trend starts now
        elif current_tempo_trend and current_tempo:
            self._start_tempo_trend_spanner_with_explicit_start(
                leaf,
                lilypond_format_bundle,
                current_tempo,
                current_tempo_trend,
                )
        # use spanner is tempo trend starts now
        elif current_tempo_trend and not current_tempo:
            self._start_tempo_trend_spanner_with_implicit_start(
                leaf,
                lilypond_format_bundle,
                current_tempo_trend,
                )
        else:
            raise Exception
        return lilypond_format_bundle

    def _make_other_text_spanner_overrides(self, lilypond_format_bundle):
        r'''Alphabetically by property.
        '''
        override_ = lilypondnametools.LilyPondGrobOverride(
            grob_name='TextSpanner',
            is_once=True,
            property_path=(
                'arrow-width',
                ),
            value=0.25,
            )
        override_string = '\n'.join(override_._override_format_pieces)
        lilypond_format_bundle.grob_overrides.append(override_string)
        #
        override_ = lilypondnametools.LilyPondGrobOverride(
            grob_name='TextSpanner',
            is_once=True,
            property_path=(
                'dash-fraction',
                ),
            value=0.25,
            )
        override_string = '\n'.join(override_._override_format_pieces)
        lilypond_format_bundle.grob_overrides.append(override_string)
        #
        override_ = lilypondnametools.LilyPondGrobOverride(
            grob_name='TextSpanner',
            is_once=True,
            property_path=(
                'dash-period',
                ),
            value=1.5,
            )
        override_string = '\n'.join(override_._override_format_pieces)
        lilypond_format_bundle.grob_overrides.append(override_string)
        #
        override_ = lilypondnametools.LilyPondGrobOverride(
            grob_name='TextSpanner',
            is_once=True,
            property_path=(
                'bound-details',
                'left',
                'stencil-align-dir-y',
                ),
            value=-0.5,
            )
        override_string = '\n'.join(override_._override_format_pieces)
        lilypond_format_bundle.grob_overrides.append(override_string)
        #
        override_ = lilypondnametools.LilyPondGrobOverride(
            grob_name='TextSpanner',
            is_once=True,
            property_path=(
                'bound-details',
                'left-broken',
                'padding',
                ),
            value=-2,
            )
        override_string = '\n'.join(override_._override_format_pieces)
        lilypond_format_bundle.grob_overrides.append(override_string)
        #
        #
        override_ = lilypondnametools.LilyPondGrobOverride(
            grob_name='TextSpanner',
            is_once=True,
            property_path=(
                'bound-details',
                'right',
                'arrow',
                ),
            value=True,
            )
        override_string = '\n'.join(override_._override_format_pieces)
        lilypond_format_bundle.grob_overrides.append(override_string)
        #
        override_ = lilypondnametools.LilyPondGrobOverride(
            grob_name='TextSpanner',
            is_once=True,
            property_path=(
                'bound-details',
                'right',
                'padding',
                ),
            value=2,
            )
        override_string = '\n'.join(override_._override_format_pieces)
        lilypond_format_bundle.grob_overrides.append(override_string)
        #
        override_ = lilypondnametools.LilyPondGrobOverride(
            grob_name='TextSpanner',
            is_once=True,
            property_path=(
                'bound-details',
                'right',
                'text',
                ),
            value=False,
            )
        override_string = '\n'.join(override_._override_format_pieces)
        lilypond_format_bundle.grob_overrides.append(override_string)
        #
        override_ = lilypondnametools.LilyPondGrobOverride(
            grob_name='TextSpanner',
            is_once=True,
            property_path=(
                'bound-details',
                'right-broken',
                'arrow',
                ),
            value=False,
            )
        override_string = '\n'.join(override_._override_format_pieces)
        lilypond_format_bundle.grob_overrides.append(override_string)
        #
        override_ = lilypondnametools.LilyPondGrobOverride(
            grob_name='TextSpanner',
            is_once=True,
            property_path=(
                'bound-details',
                'right-broken',
                'padding',
                ),
            value=0,
            )
        override_string = '\n'.join(override_._override_format_pieces)
        lilypond_format_bundle.grob_overrides.append(override_string)
        #
        override_ = lilypondnametools.LilyPondGrobOverride(
            grob_name='TextSpanner',
            is_once=True,
            property_path=(
                'bound-details',
                'right-broken',
                'text',
                ),
            value=False,
            )
        override_string = '\n'.join(override_._override_format_pieces)
        lilypond_format_bundle.grob_overrides.append(override_string)

    def _start_tempo_trend_spanner_with_explicit_start(
        self,
        leaf,
        lilypond_format_bundle,
        current_tempo,
        current_tempo_trend,
        ):
        spanner_start = r'\startTextSpan'
        lilypond_format_bundle.right.spanner_starts.append(spanner_start)
        #
        markup = current_tempo._to_markup()
        commands = list(markup.contents)
        commands.append(markuptools.MarkupCommand('hspace', 1.25))
        markup = markuptools.Markup(contents=commands)
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
        #
        markup = current_tempo_trend._to_markup()
        commands = list(markup.contents)
        commands.insert(0, markuptools.MarkupCommand('parenthesize'))
        commands.append(markuptools.MarkupCommand('hspace', 0.75))
        markup = markuptools.Markup(contents=commands)
        override_ = lilypondnametools.LilyPondGrobOverride(
            grob_name='TextSpanner',
            is_once=True,
            property_path=(
                'bound-details',
                'left-broken',
                'text',
                ),
            value=markup,
            )
        override_string = '\n'.join(override_._override_format_pieces)
        lilypond_format_bundle.grob_overrides.append(override_string)
        self._make_other_text_spanner_overrides(lilypond_format_bundle)

    def _start_tempo_trend_spanner_with_implicit_start(
        self,
        leaf,
        lilypond_format_bundle,
        current_tempo_trend,
        previous_tempo,
        ):
        spanner_start = r'\startTextSpan'
        lilypond_format_bundle.right.spanner_starts.append(spanner_start)
        #
        if previous_tempo:
            markup = previous_tempo._to_markup()
            command = markup.contents[:]
            command = markuptools.MarkupCommand('parenthesize', command)
            markup = markuptools.Markup(command)
        else:
            markup = current_tempo_trend._to_markup()
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