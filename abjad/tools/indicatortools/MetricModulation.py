# -*- encoding: utf-8 -*-
import copy
from abjad.tools import durationtools
from abjad.tools import markuptools
from abjad.tools import mathtools
from abjad.tools.abctools.AbjadObject import AbjadObject
from abjad.tools.topleveltools.new import new


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
            ...     left_rhythm=Note("c'4"),
            ...     right_rhythm=Note("c'4."),
            ...     )

        ::

            >>> print(format(metric_modulation))
            indicatortools.MetricModulation(
                left_rhythm=selectiontools.Selection(
                    (
                        scoretools.Note("c'4"),
                        )
                    ),
                right_rhythm=selectiontools.Selection(
                    (
                        scoretools.Note("c'4."),
                        )
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
                    f'4
                        ^ \markup {
                            \combine
                                c'4
                                " = "
                                c'4.
                            }
                        ^ \markup {
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
        '_left_rhythm',
        '_right_markup',
        '_right_rhythm',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        left_rhythm=None,
        right_rhythm=None,
        left_markup=None,
        right_markup=None,
        ):
        from abjad.tools import indicatortools
        from abjad.tools import markuptools
        from abjad.tools import scoretools
        # TODO: make default scope work
        #self._default_scope = scoretools.Score
        left_rhythm = self._initialize_rhythm(left_rhythm)
        self._left_rhythm = left_rhythm
        right_rhythm = self._initialize_rhythm(right_rhythm)
        self._right_rhythm = right_rhythm
        self._right_rhythm = right_rhythm
        if left_markup is not None:
            assert isinstance(left_markup, markuptools.Markup)
        self._left_markup = left_markup
        if right_markup is not None:
            assert isinstance(right_markup, markuptools.Markup)
        self._right_markup = right_markup

    ### SPECIAL METHODS ###

    def __copy__(self, *args):
        r'''Copies metric modulation.

        ..  container:: example

            ::

                >>> import copy
                >>> metric_modulation_1 = indicatortools.MetricModulation(
                ...     left_rhythm=Note("c'4"),
                ...     right_rhythm=Note("c'4."),
                ...     )
                >>> metric_modulation_2 = copy.copy(metric_modulation_1)

            ::

                >>> str(metric_modulation_1) == str(metric_modulation_2)
                True

            ::

                >>> metric_modulation_1 == metric_modulation_2
                True

            ::

                >>> metric_modulation_1 is metric_modulation_2
                False

        Returns new metric modulation.
        '''
        return type(self)(
            left_rhythm=self.left_rhythm,
            right_rhythm=self.right_rhythm,
            left_markup=self.left_markup,
            right_markup=self.right_markup,
            )

    def __eq__(self, expr):
        r'''Is true `expr` is another metric modulation with the same ratio as
        this metric modulation. Otherwise false.

        ..  container:: example

            ::

                >>> metric_modulation_1 = indicatortools.MetricModulation(
                ...     left_rhythm=Note("c'4"),
                ...     right_rhythm=Note("c'4."),
                ...     )
                >>> metric_modulation_2 = indicatortools.MetricModulation(
                ...     left_rhythm=Tuplet((2, 3), [Note("c'4")]),
                ...     right_rhythm=Note("c'4"),
                ...     )
                >>> notes = scoretools.make_notes([0], [Duration(5, 16)])
                >>> metric_modulation_3 = indicatortools.MetricModulation(
                ...     left_rhythm=Note("c'4"),
                ...     right_rhythm=notes,
                ...     )

            ::

                >>> metric_modulation_1.ratio
                Ratio(2, 3)
                >>> metric_modulation_2.ratio
                Ratio(2, 3)
                >>> metric_modulation_3.ratio
                Ratio(4, 5)

            ::

                >>> metric_modulation_1 == metric_modulation_1
                True
                >>> metric_modulation_1 == metric_modulation_2
                True
                >>> metric_modulation_1 == metric_modulation_3
                False

            ::

                >>> metric_modulation_2 == metric_modulation_1
                True
                >>> metric_modulation_2 == metric_modulation_2
                True
                >>> metric_modulation_2 == metric_modulation_3
                False

            ::

                >>> metric_modulation_3 == metric_modulation_1
                False
                >>> metric_modulation_3 == metric_modulation_2
                False
                >>> metric_modulation_3 == metric_modulation_3
                True

        Returns boolean.
        '''
        if isinstance(expr, type(self)):
            if self.ratio == expr.ratio:
                return True
        return False

    def __hash__(self):
        r'''Hashes metric modulation.

        Required to be explicitly redefined on Python 3 if __eq__ changes.

        Returns integer.
        '''
        return super(MetricModulation, self).__hash__()

    def __str__(self):
        r'''Gets string representation of metric modulation.

        ..  container:: example

            ::

                >>> metric_modulation = indicatortools.MetricModulation(
                ...     left_rhythm=Tuplet((2, 3), [Note("c'4")]),
                ...     right_rhythm=Note("c'4"),
                ...     )

            ::

                >>> print(str(metric_modulation))
                \markup {
                    \combine
                        "Tuplet(Multiplier(2, 3), c'4 )"
                        " = "
                        c'4
                    }

        Returns string.
        '''
        return str(self._get_markup())

    ### PRIVATE PROPERTIES ###

    @property
    def _attribute_manifest(self):
        from abjad.tools import systemtools
        from scoremanager import idetools
        return systemtools.AttributeManifest(
            systemtools.AttributeDetail(
                name='left_rhythm',
                command='lh',
                editor=idetools.getters.get_rhythm,
                ),
            systemtools.AttributeDetail(
                name='right_rhythm',
                command='rh',
                editor=idetools.getters.get_rhythm,
                ),
            systemtools.AttributeDetail(
                name='left_markup',
                command='lk',
                editor=idetools.getters.get_markup,
                ),
            systemtools.AttributeDetail(
                name='right_markup',
                command='rk',
                editor=idetools.getters.get_markup,
                ),
            )

    @property
    def _contents_repr_string(self):
        return str(self)

    @property
    def _lilypond_format(self):
        return str(self)

    @property
    def _lilypond_format_bundle(self):
        from abjad.tools import systemtools
        lilypond_format_bundle = systemtools.LilyPondFormatBundle()
        markup = self._get_markup()
        markup = new(markup, direction=Up)
        markup_format_pieces = markup._get_format_pieces()
        lilypond_format_bundle.right.markup.extend(markup_format_pieces)
        return lilypond_format_bundle

    ### PRIVATE METHODS ###

    def _get_left_markup(self):
        if self.left_markup is not None:
            return self.left_markup
        markup = self._to_markup(self.left_rhythm)
        return markup

    def _get_markup(self):
        left_markup = self._get_left_markup()
        right_markup = self._get_right_markup()
        commands = []
        commands.extend(left_markup.contents)
        commands.append(' = ')
        commands.extend(right_markup.contents)
        command = markuptools.MarkupCommand('combine', *commands)
        markup = markuptools.Markup(contents=command)
        return markup

    def _get_right_markup(self):
        if self.right_markup is not None:
            return self.right_markup
        markup = self._to_markup(self.right_rhythm)
        return markup

    def _initialize_rhythm(self, rhythm):
        from abjad.tools import scoretools
        from abjad.tools import selectiontools
        if isinstance(rhythm, scoretools.Component):
            #rhythm = copy.copy(rhythm)
            selection = selectiontools.Selection([rhythm])
        elif isinstance(rhythm, selectiontools.Selection):
            #selection = copy.copy(rhythm)
            selection = rhythm
        else:
            message = 'rhythm must be duration, component or selection: {!r}.'
            message = message.format(rhythm)
            raise TypeError(message)
        assert isinstance(selection, selectiontools.Selection)
        return selection

    def _to_markup(self, selection):
        component = selection[0]
        string = str(component)
        markup = markuptools.Markup(string)
        return markup

    ### PUBLIC PROPERTIES ###

    @property
    def left_markup(self):
        r'''Gets left markup of metric modulation.

        Returns markup or none.
        '''
        return self._left_markup

    @property
    def left_rhythm(self):
        r'''Gets left rhythm of metric modulation.

        Returns selection.
        '''
        return self._left_rhythm

    @property
    def ratio(self):
        r'''Gets ratio of metric modulation.

        ..  container:: example

            ::

                >>> metric_modulation = indicatortools.MetricModulation(
                ...     left_rhythm=Tuplet((2, 3), [Note("c'4")]),
                ...     right_rhythm=Note("c'4"),
                ...     )
                >>> metric_modulation.ratio
                Ratio(2, 3)

        Returns ratio.
        '''
        left_duration = self.left_rhythm.get_duration()
        right_duration = self.right_rhythm.get_duration()
        duration = left_duration / right_duration
        ratio = mathtools.Ratio(duration.pair)
        return ratio

    @property
    def right_markup(self):
        r'''Gets right markup of metric modulation.

        Returns markup or none.
        '''
        return self._right_markup

    @property
    def right_rhythm(self):
        r'''Gets right tempo of metric modulation.

        Returns selection.
        '''
        return self._right_rhythm