# -*- coding: utf-8 -*-
import collections
import fractions
import functools
import math
import numbers
from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import schemetools
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject
from abjad.tools.topleveltools import new


@functools.total_ordering
class Tempo(AbjadValueObject):
    r'''Tempo indicator.

    ..  container:: example

        **Example 1.** Integer-valued tempo:

        ::

            >>> score = Score([])
            >>> staff = Staff("c'8 d'8 e'8 f'8")
            >>> score.append(staff)
            >>> tempo = Tempo(Duration(1, 4), 90)
            >>> attach(tempo, staff[0])
            >>> show(score) # doctest: +SKIP

        ..  doctest::

            >>> print(format(score))
            \new Score <<
                \new Staff {
                    \tempo 4=90
                    c'8
                    d'8
                    e'8
                    f'8
                }
            >>

    ..  container:: example

        **Example 2.** Float-valued tempo:

        ::

            >>> score = Score([])
            >>> staff = Staff("c'8 d'8 e'8 f'8")
            >>> score.append(staff)
            >>> tempo = Tempo(Duration(1, 4), 90.1)
            >>> attach(tempo, staff[0])
            >>> show(score) # doctest: +SKIP

        ..  doctest::

            >>> print(format(score))
            \new Score <<
                \new Staff {
                    \tempo \markup {
                        \scale
                            #'(0.75 . 0.75)
                            \score
                                {
                                    \new Score \with {
                                        \override SpacingSpanner.spacing-increment = #0.5
                                        proportionalNotationDuration = ##f
                                    } <<
                                        \new RhythmicStaff \with {
                                            \remove Time_signature_engraver
                                            \remove Staff_symbol_engraver
                                            \override Stem.direction = #up
                                            \override Stem.length = #5
                                            \override TupletBracket.bracket-visibility = ##t
                                            \override TupletBracket.direction = #up
                                            \override TupletBracket.padding = #1.25
                                            \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                            \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                            tupletFullLength = ##t
                                        } {
                                            c'4
                                        }
                                    >>
                                    \layout {
                                        indent = #0
                                        ragged-right = ##t
                                    }
                                }
                        =
                        \general-align
                            #Y
                            #-0.5
                            90.1
                        }
                    c'8
                    d'8
                    e'8
                    f'8
                }
            >>

    ..  container:: example

        **Example 3.** Rational-valued tempo:

        ::

            >>> score = Score([])
            >>> staff = Staff("c'8 d'8 e'8 f'8")
            >>> score.append(staff)
            >>> tempo = Tempo(Duration(1, 4), Fraction(181, 2))
            >>> attach(tempo, staff[0])
            >>> show(score) # doctest: +SKIP

        ..  doctest::

            >>> print(format(score))
            \new Score <<
                \new Staff {
                    \tempo \markup {
                        \scale
                            #'(0.75 . 0.75)
                            \score
                                {
                                    \new Score \with {
                                        \override SpacingSpanner.spacing-increment = #0.5
                                        proportionalNotationDuration = ##f
                                    } <<
                                        \new RhythmicStaff \with {
                                            \remove Time_signature_engraver
                                            \remove Staff_symbol_engraver
                                            \override Stem.direction = #up
                                            \override Stem.length = #5
                                            \override TupletBracket.bracket-visibility = ##t
                                            \override TupletBracket.direction = #up
                                            \override TupletBracket.padding = #1.25
                                            \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                            \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                            tupletFullLength = ##t
                                        } {
                                            c'4
                                        }
                                    >>
                                    \layout {
                                        indent = #0
                                        ragged-right = ##t
                                    }
                                }
                        =
                        \raise
                            #-0.5
                            {
                                90
                                \tiny
                                    \fraction
                                        1
                                        2
                            }
                        }
                    c'8
                    d'8
                    e'8
                    f'8
                }
            >>

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_custom_markup',
        '_default_scope',
        '_reference_duration',
        '_textual_indication',
        '_units_per_minute',
        )

    _format_slot = 'opening'

    ### INITIALIZER ###

    def __init__(
        self,
        reference_duration=None,
        units_per_minute=None,
        textual_indication=None,
        custom_markup=None,
        ):
        from abjad.tools import markuptools
        from abjad.tools import scoretools
        self._default_scope = scoretools.Score
        assert isinstance(textual_indication, (str, type(None)))
        arguments = (reference_duration, units_per_minute, textual_indication)
        if all(_ is None for _ in arguments):
            reference_duration = (1, 4)
            units_per_minute = 60
        if reference_duration:
            reference_duration = durationtools.Duration(reference_duration)
        prototype = (
            int,
            float,
            fractions.Fraction,
            collections.Sequence,
            type(None),
            )
        assert isinstance(units_per_minute, prototype)
        if isinstance(units_per_minute, collections.Sequence):
            assert len(units_per_minute) == 2
            prototype = (int, float, durationtools.Duration)
            assert all(isinstance(x, prototype) for x in units_per_minute)
            units_per_minute = tuple(sorted(units_per_minute))
        if isinstance(units_per_minute, float):
            units_per_minute = mathtools.integer_equivalent_number_to_integer(
                units_per_minute)
        self._reference_duration = reference_duration
        self._textual_indication = textual_indication
        self._units_per_minute = units_per_minute
        if custom_markup is not None:
            assert isinstance(custom_markup, markuptools.Markup), repr(
                custom_markup)
        self._custom_markup = custom_markup

    ### SPECIAL METHODS ###

    def __add__(self, expr):
        r'''Adds tempo to `expr`.

        ..  container:: example

            **Example 1.** Adds one tempo to another:

            ::

                >>> Tempo(Duration(1, 4), 60) + Tempo(Duration(1, 4), 90)
                Tempo(reference_duration=Duration(1, 4), units_per_minute=150)

        ..  container:: example

            **Example 2.** Returns none when `expr` is not a tempo:

            ::

                >>> Tempo(Duration(1, 4), 60) + 90 is None
                True

        Returns new tempo or none.
        '''
        if isinstance(expr, type(self)):
            if self.is_imprecise or expr.is_imprecise:
                raise ImpreciseTempoError
            new_quarters_per_minute = \
                self.quarters_per_minute + expr.quarters_per_minute
            minimum_denominator = \
                min((self.reference_duration.denominator, expr.reference_duration.denominator))
            nonreduced_fraction = \
                mathtools.NonreducedFraction(new_quarters_per_minute / 4)
            nonreduced_fraction = \
                nonreduced_fraction.with_denominator(minimum_denominator)
            new_units_per_minute, new_reference_duration_denominator = \
                nonreduced_fraction.pair
            new_reference_duration = \
                durationtools.Duration(1, new_reference_duration_denominator)
            new_tempo = type(self)(
                new_reference_duration,
                new_units_per_minute,
                )
            return new_tempo

    def __div__(self, expr):
        r'''Divides tempo by `expr`.

        ..  container:: example

            **Example 1.** Divides tempo by number:

            ::

                >>> Tempo(Duration(1, 4), 60) / 2
                Tempo(reference_duration=Duration(1, 4), units_per_minute=30)

        ..  container:: example

            **Example 2.** Divides tempo by other tempo:

            ::

                >>> Tempo(Duration(1, 4), 60) / Tempo(Duration(1, 4), 40)
                Multiplier(3, 2)

        Returns new tempo or multiplier.
        '''
        if self.is_imprecise:
            raise ImpreciseTempoError
        if getattr(expr, 'is_imprecise', False):
            raise ImpreciseTempoError
        if isinstance(expr, type(self)):
            result = self.quarters_per_minute / expr.quarters_per_minute
            return durationtools.Multiplier(result)
        elif isinstance(expr, numbers.Number):
            units_per_minute = self.units_per_minute / expr
            result = new(self, units_per_minute=units_per_minute)
            return result
        else:
            message = 'must be number or tempo indication: {!r}.'
            message = message.format(expr)
            raise TypeError(message)

    def __format__(self, format_specification=''):
        r'''Formats tempo.

        Set `format_specification` to `''`', `'lilypond'` or `'storage'`.
        Interprets `''` equal to `'storage'`.

        ..  container:: example

            **Example 1.** Without custom markup:

            ::

                >>> tempo = Tempo((1, 4), 84, 'Allegro')
                >>> print(format(tempo))
                indicatortools.Tempo(
                    reference_duration=durationtools.Duration(1, 4),
                    units_per_minute=84,
                    textual_indication='Allegro',
                    )

        ..  container:: example

            **Example 2.** With custom markup:

            ::

                >>> markup = Markup(r'\italic { Allegro }')
                >>> tempo = Tempo((1, 4), 84, custom_markup=markup)
                >>> print(format(tempo))
                indicatortools.Tempo(
                    reference_duration=durationtools.Duration(1, 4),
                    units_per_minute=84,
                    custom_markup=markuptools.Markup(
                        contents=(
                            markuptools.MarkupCommand(
                                'italic',
                                ['Allegro']
                                ),
                            ),
                        ),
                    )

        Returns string.
        '''
        from abjad.tools import systemtools
        if format_specification in ('', 'storage'):
            return systemtools.StorageFormatAgent(self).get_storage_format()
        elif format_specification == 'lilypond':
            return self._lilypond_format
        return str(self)

    def __lt__(self, arg):
        r'''Is true when `arg` is a tempo with quarters per minute greater than
        that of this tempo. Otherwise false.

        Returns true or false.
        '''
        assert isinstance(arg, type(self)), repr(arg)
        return self.quarters_per_minute < arg.quarters_per_minute

    def __mul__(self, multiplier):
        r'''Multiplies tempo by `multiplier`.

        ..  container:: example

            **Example 1.** Doubles tempo:

            ::

                >>> tempo = Tempo(Duration(1, 4), 84)
                >>> 2 * tempo
                Tempo(reference_duration=Duration(1, 4), units_per_minute=168)

        ..  container:: example

            **Example 2.** Triples tempo:

            ::

                >>> tempo = Tempo(Duration(1, 4), 84)
                >>> 3 * tempo
                Tempo(reference_duration=Duration(1, 4), units_per_minute=252)

        Returns new tempo.
        '''
        if not isinstance(multiplier, (int, float, durationtools.Duration)):
            return
        if self.is_imprecise:
            raise ImpreciseTempoError
        new_units_per_minute = multiplier * self.units_per_minute
        new_reference_duration = durationtools.Duration(
            self.reference_duration)
        new_tempo = type(self)(
            reference_duration=new_reference_duration,
            units_per_minute=new_units_per_minute,
            )
        return new_tempo

    def __rmul__(self, multiplier):
        r'''Multiplies `multiplier` by tempo.

        ..  container::: example

            **Example 1.** Doubles tempo:

            ::

                >>> tempo = Tempo(Duration(1, 4), 84)
                >>> tempo * 2
                Tempo(reference_duration=Duration(1, 4), units_per_minute=168)

        ..  container::: example

            **Example 2.** Triples tempo:

            ::

                >>> tempo = Tempo(Duration(1, 4), 84)
                >>> tempo * 3
                Tempo(reference_duration=Duration(1, 4), units_per_minute=252)

        Returns new tempo.
        '''
        if not isinstance(multiplier, (int, float, durationtools.Duration)):
            return
        if self.is_imprecise:
            raise ImpreciseTempoError
        new_units_per_minute = multiplier * self.units_per_minute
        new_reference_duration = durationtools.Duration(
            self.reference_duration)
        new_tempo = type(self)(
            reference_duration=new_reference_duration,
            units_per_minute=new_units_per_minute,
            )
        return new_tempo

    def __str__(self):
        r'''Gets string representation of tempo.

        ..  container:: example

            **Example 1.** Integer-valued tempo:

            ::

                >>> tempo = Tempo(Duration(1, 4), 90)
                >>> str(tempo)
                '4=90'

        ..  container:: example

            **Example 2.** Float-valued tempo:

            ::

                >>> tempo = Tempo(Duration(1, 4), 90.1)
                >>> str(tempo)
                '4=90.1'

        ..  container:: example

            **Example 3.** Rational-valued tempo:

            ::

                >>> tempo = Tempo(Duration(1, 4), Fraction(181, 2))
                >>> str(tempo)
                '4=90+1/2'

        ..  container:: example

            **Example 4.** Ranged tempo:

            ::

                >>> tempo = Tempo(Duration(1, 4), (90, 96))
                >>> str(tempo)
                '4=90-96'

        Returns string.
        '''
        #return self._equation or self.textual_indication
        if self.textual_indication is not None:
            string = self.textual_indication
        elif isinstance(self.units_per_minute, (int, float)):
            string = '{}={}'
            string = string.format(self._dotted, self.units_per_minute)
        elif (isinstance(self.units_per_minute, fractions.Fraction) and
            not mathtools.is_integer_equivalent_number(self.units_per_minute)):
            integer_part = int(self.units_per_minute)
            remainder = self.units_per_minute - integer_part
            remainder = fractions.Fraction(remainder)
            string = '{}={}+{}'
            string = string.format(self._dotted, integer_part, remainder)
        elif (isinstance(self.units_per_minute, fractions.Fraction) and
            mathtools.is_integer_equivalent_number(self.units_per_minute)):
            string = '{}={}'
            integer = int(self.units_per_minute)
            string = string.format(self._dotted, integer)
        elif isinstance(self.units_per_minute, tuple):
            string = '{}={}-{}'
            string = string.format(
                self._dotted,
                self.units_per_minute[0],
                self.units_per_minute[1],
                )
        else:
            message = 'unknown: {!r}.'
            message = message.format(self.units_per_minute)
            raise TypeError(message)
        return string

    def __sub__(self, expr):
        r'''Subtracts `expr` from tempo.

        ..  container:: example

            **Example 1.** Same reference reference durations:
            ::

                >>> tempo_1 = Tempo(Duration(1, 4), 90)
                >>> tempo_2 = Tempo(Duration(1, 4), 60)
                >>> tempo_1 - tempo_2
                Tempo(reference_duration=Duration(1, 4), units_per_minute=30)

        ..  container:: example

            **Example 2.** Different reference durations:
            ::

                >>> tempo_1 = Tempo(Duration(1, 4), 90)
                >>> tempo_2 = Tempo(Duration(1, 2), 90)
                >>> tempo_1 - tempo_2
                Tempo(reference_duration=Duration(1, 4), units_per_minute=45)

        Returns new tempo.
        '''
        if not isinstance(expr, type(self)):
            message = 'must be tempo: {!r}.'
            message = message.format(expr)
            raise Exception(message)
        if self.is_imprecise or expr.is_imprecise:
            raise ImpreciseTempoError
        new_quarters_per_minute = self.quarters_per_minute - \
            expr.quarters_per_minute
        minimum_denominator = min((
            self.reference_duration.denominator,
            expr.reference_duration.denominator,
            ))
        nonreduced_fraction = mathtools.NonreducedFraction(
            new_quarters_per_minute / 4)
        nonreduced_fraction = nonreduced_fraction.with_denominator(
            minimum_denominator)
        new_units_per_minute, new_reference_duration_denominator = \
            nonreduced_fraction.pair
        new_reference_duration = durationtools.Duration(
            1, new_reference_duration_denominator)
        new_tempo = type(self)(
            reference_duration=new_reference_duration,
            units_per_minute=new_units_per_minute,
            )
        return new_tempo

    def __truediv__(self, expr):
        r'''Divides tempo by `expr`. Operator required by Python 3.

        ..  container:: example

            **Example 1.** Divides tempo by number:

            ::

                >>> Tempo(Duration(1, 4), 60).__truediv__(2)
                Tempo(reference_duration=Duration(1, 4), units_per_minute=30)

        ..  container:: example

            **Example 2.** Divides tempo by other tempo:

            ::

                >>> Tempo(Duration(1, 4), 60).__truediv__(
                ...     Tempo(Duration(1, 4), 40)
                ...     )
                Multiplier(3, 2)

        Returns new tempo.
        '''
        return self.__div__(expr)

    ### PRIVATE METHODS ###

    def _make_lhs_score_markup(self, reference_duration=None):
        from abjad.tools import scoretools
        reference_duration = reference_duration or self.reference_duration
        selection = scoretools.make_notes([0], [reference_duration])
        markup = durationtools.Duration._to_score_markup(selection)
        return markup

    def _to_markup(self):
        from abjad.tools import markuptools
        if self.custom_markup is not None:
            return self.custom_markup
        duration_log = int(math.log(self.reference_duration.denominator, 2))
        lhs = markuptools.Markup.note_by_number(
            duration_log,
            self.reference_duration.dot_count,
            1,
            )
        lhs = lhs.general_align('Y', Down).fontsize(-6)
        equals = markuptools.Markup('=')
        #right_space = markuptools.Markup.hspace(0.1)
        units = markuptools.Markup(self.units_per_minute)
        #rhs = left_space + equals + right_space + units
        rhs = equals + units
        #rhs = rhs.fontsize(3).upright()
        rhs = rhs.upright()
        markup = lhs + rhs
        return markup

    ### PUBLIC METHODS ###

    def duration_to_milliseconds(self, duration):
        r'''Gets millisecond value of `duration` under a given tempo.

        ..  container:: example

            **Example 1.** One quarter lasts 1000 msec at quarter equals 60:

            ::

                >>> tempo = Tempo((1, 4), 60)
                >>> tempo.duration_to_milliseconds(Duration(1, 4))
                Duration(1000, 1)

        ..  container:: example

            **Example 1.** Dotted sixteenth lasts 1500 msec at quarter equals
            60:

            ::

                >>> tempo = Tempo((1, 4), 60)
                >>> tempo.duration_to_milliseconds(Duration(3, 8))
                Duration(1500, 1)

        Returns duration.
        '''
        duration = durationtools.Duration(duration)
        # TODO: rewrite formula without line breaks;
        #       use two or three temporary variables instead.
        whole_note_duration = 1000 \
            * durationtools.Multiplier(
                self.reference_duration.denominator,
                self.reference_duration.numerator,
                ) \
            * durationtools.Multiplier(
                60,
                self.units_per_minute,
                )
        return durationtools.Duration(duration * whole_note_duration)

    def list_related_tempos(
        self,
        maximum_numerator=None,
        maximum_denominator=None,
        integer_tempos_only=False,
        ):
        r'''Lists related tempos.

        ..  container:: example

            **Example 1.** Rewrites tempo ``4=58`` by ratios ``n:d`` such that
            ``1 <= n <= 8`` and ``1 <= d <= 8``.

            ::

                >>> tempo = Tempo(Duration(1, 4), 58)
                >>> pairs = tempo.list_related_tempos(
                ...     maximum_numerator=8,
                ...     maximum_denominator=8,
                ...     )

            ::

                >>> for tempo, ratio in pairs:
                ...     string = '{!s}\t{!s}'.format(tempo, ratio)
                ...     print(string)
                4=29        1:2
                4=33+1/7    4:7
                4=34+4/5    3:5
                4=36+1/4    5:8
                4=38+2/3    2:3
                4=41+3/7    5:7
                4=43+1/2    3:4
                4=46+2/5    4:5
                4=48+1/3    5:6
                4=49+5/7    6:7
                4=50+3/4    7:8
                4=58        1:1
                4=66+2/7    8:7
                4=67+2/3    7:6
                4=69+3/5    6:5
                4=72+1/2    5:4
                4=77+1/3    4:3
                4=81+1/5    7:5
                4=87        3:2
                4=92+4/5    8:5
                4=96+2/3    5:3
                4=101+1/2   7:4
                4=116       2:1

        ..  container:: example

            **Example 2.** Integer-valued tempos only:

            ::

                >>> tempo = Tempo(Duration(1, 4), 58)
                >>> pairs = tempo.list_related_tempos(
                ...     maximum_numerator=16,
                ...     maximum_denominator=16,
                ...     integer_tempos_only=True,
                ...     )

            ::

                >>> for tempo, ratio in pairs:
                ...     string = '{!s}\t{!s}'.format(tempo, ratio)
                ...     print(string)
                4=29	1:2
                4=58	1:1
                4=87	3:2
                4=116	2:1

        Constrains ratios such that ``1:2 <= n:d <= 2:1``.

        Returns list of tempo / ratio pairs.
        '''
        from abjad.tools import sequencetools
        allowable_numerators = range(1, maximum_numerator + 1)
        allowable_denominators = range(1, maximum_denominator + 1)
        pairs = sequencetools.yield_outer_product_of_sequences([
            allowable_numerators,
            allowable_denominators,
            ])
        multipliers = [durationtools.Multiplier(_) for _ in pairs]
        multipliers = [
            _ for _ in multipliers
            if fractions.Fraction(1, 2) <= _ <= fractions.Fraction(2)
            ]
        multipliers.sort()
        multipliers = sequencetools.remove_repeated_elements(multipliers)
        pairs = []
        for multiplier in multipliers:
            new_units_per_minute = multiplier * self.units_per_minute
            if (integer_tempos_only and not
                mathtools.is_integer_equivalent_number(new_units_per_minute)):
                continue
            new_tempo = type(self)(
                reference_duration=self.reference_duration,
                units_per_minute=new_units_per_minute,
                )
            ratio = mathtools.Ratio(multiplier.pair)
            pair = (new_tempo, ratio)
            pairs.append(pair)
        return pairs

    @staticmethod
    def make_tempo_equation_markup(reference_duration, units_per_minute):
        r'''Makes tempo equation markup.

        ..  container:: example

            **Example 1.** Integer-valued tempo:

            ::

                >>> markup = Tempo.make_tempo_equation_markup(Duration(1, 4), 90)
                >>> show(markup) # doctest: +SKIP

            ..  doctest::

                >>> print(format(markup))
                \markup {
                    \scale
                        #'(0.75 . 0.75)
                        \score
                            {
                                \new Score \with {
                                    \override SpacingSpanner.spacing-increment = #0.5
                                    proportionalNotationDuration = ##f
                                } <<
                                    \new RhythmicStaff \with {
                                        \remove Time_signature_engraver
                                        \remove Staff_symbol_engraver
                                        \override Stem.direction = #up
                                        \override Stem.length = #5
                                        \override TupletBracket.bracket-visibility = ##t
                                        \override TupletBracket.direction = #up
                                        \override TupletBracket.padding = #1.25
                                        \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                        \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                        tupletFullLength = ##t
                                    } {
                                        c'4
                                    }
                                >>
                                \layout {
                                    indent = #0
                                    ragged-right = ##t
                                }
                            }
                    =
                    \general-align
                        #Y
                        #-0.5
                        90
                    }

        ..  container:: example

            **Example 2.** Float-valued tempo:

            ::

                >>> markup = Tempo.make_tempo_equation_markup(Duration(1, 4), 90.1)
                >>> show(markup) # doctest: +SKIP

            ..  doctest::

                >>> print(format(markup))
                \markup {
                    \scale
                        #'(0.75 . 0.75)
                        \score
                            {
                                \new Score \with {
                                    \override SpacingSpanner.spacing-increment = #0.5
                                    proportionalNotationDuration = ##f
                                } <<
                                    \new RhythmicStaff \with {
                                        \remove Time_signature_engraver
                                        \remove Staff_symbol_engraver
                                        \override Stem.direction = #up
                                        \override Stem.length = #5
                                        \override TupletBracket.bracket-visibility = ##t
                                        \override TupletBracket.direction = #up
                                        \override TupletBracket.padding = #1.25
                                        \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                        \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                        tupletFullLength = ##t
                                    } {
                                        c'4
                                    }
                                >>
                                \layout {
                                    indent = #0
                                    ragged-right = ##t
                                }
                            }
                    =
                    \general-align
                        #Y
                        #-0.5
                        90.1
                    }

        ..  container:: example

            **Example 3.** Rational-valued tempo:

            ::

                >>> markup = Tempo.make_tempo_equation_markup(
                ...     Duration(1, 4),
                ...     Fraction(181, 2),
                ...     )
                >>> show(markup) # doctest: +SKIP

            ..  doctest::

                >>> print(format(markup))
                \markup {
                    \scale
                        #'(0.75 . 0.75)
                        \score
                            {
                                \new Score \with {
                                    \override SpacingSpanner.spacing-increment = #0.5
                                    proportionalNotationDuration = ##f
                                } <<
                                    \new RhythmicStaff \with {
                                        \remove Time_signature_engraver
                                        \remove Staff_symbol_engraver
                                        \override Stem.direction = #up
                                        \override Stem.length = #5
                                        \override TupletBracket.bracket-visibility = ##t
                                        \override TupletBracket.direction = #up
                                        \override TupletBracket.padding = #1.25
                                        \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                        \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                        tupletFullLength = ##t
                                    } {
                                        c'4
                                    }
                                >>
                                \layout {
                                    indent = #0
                                    ragged-right = ##t
                                }
                            }
                    =
                    \raise
                        #-0.5
                        {
                            90
                            \tiny
                                \fraction
                                    1
                                    2
                        }
                    }

        ..  container:: example

            **Example 4.** Reference duration expressed with ties:

            ::

                >>> markup = Tempo.make_tempo_equation_markup(Duration(5, 16), 90)
                >>> show(markup) # doctest: +SKIP

            ..  doctest::

                >>> print(format(markup))
                \markup {
                    \scale
                        #'(0.75 . 0.75)
                        \score
                            {
                                \new Score \with {
                                    \override SpacingSpanner.spacing-increment = #0.5
                                    proportionalNotationDuration = ##f
                                } <<
                                    \new RhythmicStaff \with {
                                        \remove Time_signature_engraver
                                        \remove Staff_symbol_engraver
                                        \override Stem.direction = #up
                                        \override Stem.length = #5
                                        \override TupletBracket.bracket-visibility = ##t
                                        \override TupletBracket.direction = #up
                                        \override TupletBracket.padding = #1.25
                                        \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                        \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                        tupletFullLength = ##t
                                    } {
                                        c'4 ~
                                        c'16
                                    }
                                >>
                                \layout {
                                    indent = #0
                                    ragged-right = ##t
                                }
                            }
                    =
                    \general-align
                        #Y
                        #-0.5
                        90
                    }

        ..  container:: example

            **Example 5.** Reference duration expressed as a tuplet:

            ::

                >>> markup = Tempo.make_tempo_equation_markup(Duration(1, 6), 90)
                >>> show(markup) # doctest: +SKIP

            ..  doctest::

                >>> print(format(markup))
                \markup {
                    \scale
                        #'(0.75 . 0.75)
                        \score
                            {
                                \new Score \with {
                                    \override SpacingSpanner.spacing-increment = #0.5
                                    proportionalNotationDuration = ##f
                                } <<
                                    \new RhythmicStaff \with {
                                        \remove Time_signature_engraver
                                        \remove Staff_symbol_engraver
                                        \override Stem.direction = #up
                                        \override Stem.length = #5
                                        \override TupletBracket.bracket-visibility = ##t
                                        \override TupletBracket.direction = #up
                                        \override TupletBracket.padding = #1.25
                                        \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                        \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                        tupletFullLength = ##t
                                    } {
                                        \tweak edge-height #'(0.7 . 0)
                                        \times 2/3 {
                                            c'4
                                        }
                                    }
                                >>
                                \layout {
                                    indent = #0
                                    ragged-right = ##t
                                }
                            }
                    =
                    \general-align
                        #Y
                        #-0.5
                        90
                    }

        ..  container:: example

            **Example 6.** Reference duration passed in as explicit rhythm:

            ::

                >>> durations = [Duration(1, 16), Duration(3, 16), Duration(1, 16)]
                >>> selection = scoretools.make_notes([0], durations)
                >>> attach(Tie(), selection)
                >>> attach(Beam(), selection)
                >>> markup = Tempo.make_tempo_equation_markup(selection, 90)
                >>> show(markup) # doctest: +SKIP

            ..  doctest::

                >>> print(format(markup))
                \markup {
                    \scale
                        #'(0.75 . 0.75)
                        \score
                            {
                                \new Score \with {
                                    \override SpacingSpanner.spacing-increment = #0.5
                                    proportionalNotationDuration = ##f
                                } <<
                                    \new RhythmicStaff \with {
                                        \remove Time_signature_engraver
                                        \remove Staff_symbol_engraver
                                        \override Stem.direction = #up
                                        \override Stem.length = #5
                                        \override TupletBracket.bracket-visibility = ##t
                                        \override TupletBracket.direction = #up
                                        \override TupletBracket.padding = #1.25
                                        \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                        \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                        tupletFullLength = ##t
                                    } {
                                        c'16 ~ [
                                        c'8. ~
                                        c'16 ]
                                    }
                                >>
                                \layout {
                                    indent = #0
                                    ragged-right = ##t
                                }
                            }
                    =
                    \general-align
                        #Y
                        #-0.5
                        90
                    }

            Pass rhythms like this as Abjad selections.

        Returns markup.
        '''
        from abjad.tools import markuptools
        from abjad.tools import scoretools
        from abjad.tools import selectiontools
        if isinstance(reference_duration, selectiontools.Selection):
            selection = reference_duration
        else:
            selection = scoretools.make_notes([0], [reference_duration])
        lhs_score_markup = durationtools.Duration._to_score_markup(selection)
        lhs_score_markup = lhs_score_markup.scale((0.75, 0.75))
        equal_markup = markuptools.Markup('=')
        if (isinstance(units_per_minute, fractions.Fraction) and
            not mathtools.is_integer_equivalent_number(units_per_minute)):
            rhs_markup = markuptools.Markup.make_improper_fraction_markup(
                units_per_minute)
            rhs_markup = rhs_markup.raise_(-0.5)
        else:
            rhs_markup = markuptools.Markup(units_per_minute)
            rhs_markup = rhs_markup.general_align('Y', -0.5)
        markup = lhs_score_markup + equal_markup + rhs_markup
        return markup

    def rewrite_duration(self, duration, new_tempo):
        r'''Rewrites `duration` under `new_tempo`.

        ..  container:: example

            **Example 1.** Consider the two tempo indicators below.

            ::

                >>> tempo = Tempo(Duration(1, 4), 60)
                >>> new_tempo = Tempo(Duration(1, 4), 90)

            `tempo` specifies quarter equal to ``60``.

            `new_tempo` indication specifies quarter equal to ``90``.

            `new_tempo` is ``3/2`` times as fast as `tempo`:

            ::

                >>> new_tempo / tempo
                Multiplier(3, 2)

            Note that a triplet eighth note under `tempo` equals a regular
            eighth note under `new_tempo`:

            ::

                >>> tempo.rewrite_duration(Duration(1, 12), new_tempo)
                Duration(1, 8)

            And note that a regular eighth note under `tempo` equals a dotted
            sixteenth under `new_tempo`:

            ::

                >>> tempo.rewrite_duration(Duration(1, 8), new_tempo)
                Duration(3, 16)

        Given `duration` governed by this tempo returns new duration governed
        by `new_tempo`.

        Ensures that `duration` and new duration consume the same amount of
        time in seconds.

        Returns duration.
        '''
        tempo_ratio = new_tempo / self
        new_duration = tempo_ratio * duration
        return new_duration

    ### PRIVATE PROPERTIES ###

    @property
    def _dotted(self):
        return self.reference_duration.lilypond_duration_string

    @property
    def _equation(self):
        if self.reference_duration is None:
            return
        if isinstance(self.units_per_minute, tuple):
            string = '{}={}-{}'
            string = string.format(
                self._dotted,
                self.units_per_minute[0],
                self.units_per_minute[1],
                )
            return string
        elif isinstance(self.units_per_minute, (float, fractions.Fraction)):
            markup = Tempo.make_tempo_equation_markup(
                self.reference_duration,
                self.units_per_minute,
                )
            string = str(markup)
            return string
        string = '{}={}'
        string = string.format(self._dotted, self.units_per_minute)
        return string

    @property
    def _lilypond_format(self):
        text, equation = None, None
        if self.textual_indication is not None:
            text = self.textual_indication
            text = schemetools.Scheme.format_scheme_value(text)
        if (self.reference_duration is not None and
            self.units_per_minute is not None):
            equation = self._equation
        if self.custom_markup is not None:
            return r'\tempo {}'.format(self.custom_markup)
        elif text and equation:
            return r'\tempo {} {}'.format(text, equation)
        elif equation:
            return r'\tempo {}'.format(equation)
        elif text:
            return r'\tempo {}'.format(text)
        else:
            return r'\tempo \default'

    @property
    def _one_line_menu_summary(self):
        result = self._lilypond_format
        if result.startswith(r'\tempo '):
            result = result[7:]
        elif result.startswith(r'\markup '):
            result = result[8:]
        else:
            raise ValueError(result)
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def custom_markup(self):
        r'''Gets custom markup of tempo.

        ..  container:: example

            **Example 1.** With custom markup:

            ::

                >>> markup = Tempo.make_tempo_equation_markup(
                ...     Duration(1, 4),
                ...     67.5,
                ...     )
                >>> markup = markup.with_color('red')
                >>> tempo = Tempo(
                ...     reference_duration=Duration(1, 4),
                ...     units_per_minute=67.5,
                ...     custom_markup=markup,
                ...     )
                >>> staff = Staff("c'4 d'4 e'4 f'4")
                >>> score = Score([staff])
                >>> attach(tempo, staff)
                >>> show(score) # doctest: +SKIP

            ..  doctest::

                >>> f(score)
                \new Score <<
                    \new Staff {
                        \tempo \markup {
                        \with-color
                            #red
                            {
                                \scale
                                    #'(0.75 . 0.75)
                                    \score
                                        {
                                            \new Score \with {
                                                \override SpacingSpanner.spacing-increment = #0.5
                                                proportionalNotationDuration = ##f
                                            } <<
                                                \new RhythmicStaff \with {
                                                    \remove Time_signature_engraver
                                                    \remove Staff_symbol_engraver
                                                    \override Stem.direction = #up
                                                    \override Stem.length = #5
                                                    \override TupletBracket.bracket-visibility = ##t
                                                    \override TupletBracket.direction = #up
                                                    \override TupletBracket.padding = #1.25
                                                    \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                                    \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                                    tupletFullLength = ##t
                                                } {
                                                    c'4
                                                }
                                            >>
                                            \layout {
                                                indent = #0
                                                ragged-right = ##t
                                            }
                                        }
                                =
                                \general-align
                                    #Y
                                    #-0.5
                                    67.5
                            }
                        }
                        c'4
                        d'4
                        e'4
                        f'4
                    }
                >>

        Set to markup or none.

        Defaults to none.

        Returns markup or none.
        '''
        return self._custom_markup

    @property
    def default_scope(self):
        r'''Gets default scope of tempo.

        ..  container:: example

            **Example 1.** Fifty-two eighth notes per minute:

            ::

                >>> tempo = Tempo(Duration(1, 8), 52)
                >>> tempo.default_scope
                <class 'abjad.tools.scoretools.Score.Score'>

        ..  container:: example

            **Example 2.** Ninety quarter notes per minute:

            ::

                >>> tempo = Tempo(Duration(1, 4), 90)
                >>> tempo.default_scope
                <class 'abjad.tools.scoretools.Score.Score'>

        Returns score.
        '''
        return self._default_scope

    @property
    def is_imprecise(self):
        r'''Is true if tempo is entirely textual or if tempo's
        units_per_minute is a range. Otherwise false.

        ..  container:: example

            **Example 1.** Imprecise tempos:

            ::

                >>> Tempo(Duration(1, 4), 60).is_imprecise
                False
                >>> Tempo(4, 60, 'Langsam').is_imprecise
                False
                >>> Tempo(textual_indication='Langsam').is_imprecise
                True
                >>> Tempo(4, (35, 50), 'Langsam').is_imprecise
                True
                >>> Tempo(Duration(1, 4), (35, 50)).is_imprecise
                True

        ..  container:: example

            **Example 2.** Precise tempo:

            ::

                >>> Tempo(Duration(1, 4), 60).is_imprecise
                False

        Returns true or false.
        '''
        if self.reference_duration is not None:
            if self.units_per_minute is not None:
                if not isinstance(self.units_per_minute, tuple):
                    return False
        return True

    @property
    def quarters_per_minute(self):
        r'''Gets quarters per minute of tempo.

        ..  container:: example

            **Example 1.** Fifty-two eighth notes per minute:

            ::

                >>> tempo = Tempo(Duration(1, 8), 52)
                >>> tempo.quarters_per_minute
                Fraction(104, 1)

        ..  container:: example

            **Example 2.** Ninety quarter notes per minute:

            ::

                >>> tempo = Tempo(Duration(1, 4), 90)
                >>> tempo.quarters_per_minute
                Fraction(90, 1)

        Returns tuple when tempo `units_per_minute` is a range.

        Returns none when tempo is imprecise.

        Returns fraction otherwise.
        '''
        if self.is_imprecise:
            return None
        if isinstance(self.units_per_minute, tuple):
            low = durationtools.Duration(1, 4) / self.reference_duration * \
                self.units_per_minute[0]
            high = durationtools.Duration(1, 4) / self.reference_duration * \
                self.units_per_minute[1]
            return (low, high)
        result = durationtools.Duration(1, 4) / self.reference_duration * \
            self.units_per_minute
        return fractions.Fraction(result)

    @property
    def reference_duration(self):
        r'''Gets reference duration of tempo.

        ..  container:: example

            **Example 1.** Fifty-two eighth notes per minute:

            ::

                >>> tempo = Tempo(Duration(1, 8), 52)
                >>> tempo.reference_duration
                Duration(1, 8)

        ..  container:: example

            **Example 2.** Ninety quarter notes per minute:

            ::

                >>> tempo = Tempo(Duration(1, 4), 90)
                >>> tempo.reference_duration
                Duration(1, 4)

        Returns duration.
        '''
        return self._reference_duration

    @property
    def textual_indication(self):
        r'''Gets optional textual indication of tempo.

        ..  container:: example

            **Example 1.** Fifty-two eighth notes per minute:

            ::

                >>> tempo = Tempo(Duration(1, 8), 52)
                >>> tempo.textual_indication is None
                True

        ..  container:: example

            **Example 2.** Ninety quarter notes per minute:

            ::

                >>> tempo = Tempo(Duration(1, 4), 90)
                >>> tempo.textual_indication is None
                True

        Returns string or none.
        '''
        return self._textual_indication

    @property
    def units_per_minute(self):
        r'''Gets units per minute of tempo.

        ..  container:: example

            **Example 1.** Integer-valued tempo:

            ::

                >>> tempo = Tempo(Duration(1, 4), 90)
                >>> tempo.units_per_minute
                90

        ..  container:: example

            **Example 2.** Float-valued tempo:

            ::

                >>> tempo = Tempo(Duration(1, 4), 90.1)
                >>> tempo.units_per_minute
                90.1


        ..  container:: example

            **Example 3.** Rational-valued tempo:

            ::

                >>> tempo = Tempo(Duration(1, 4), Fraction(181, 2))
                >>> tempo.units_per_minute
                Fraction(181, 2)

        Set to number or none.

        Defaults to none

        Returns number or none.
        '''
        return self._units_per_minute
