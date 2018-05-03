import math
import typing
from .Container import Container
from .Leaf import Leaf
from abjad.tools.exceptiontools import AssignabilityError
from abjad.tools.datastructuretools.Duration import Duration
from abjad.tools.datastructuretools.Multiplier import Multiplier
from abjad.tools.topleveltools.inspect import inspect
from abjad.tools.topleveltools.iterate import iterate
from abjad.tools import mathtools


class Tuplet(Container):
    r'''Tuplet.

    ..  container:: example

        A tuplet:

        >>> tuplet = abjad.Tuplet((2, 3), "c'8 d'8 e'8")
        >>> abjad.show(tuplet) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(tuplet)
            \times 2/3 {
                c'8
                d'8
                e'8
            }

    ..  container:: example

        A nested tuplet:

        >>> second_tuplet = abjad.Tuplet((4, 7), "g'4. ( a'16 )")
        >>> tuplet.insert(1, second_tuplet)
        >>> abjad.show(tuplet) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(tuplet)
            \tweak edge-height #'(0.7 . 0)
            \times 2/3 {
                c'8
                \times 4/7 {
                    g'4.
                    (
                    a'16
                    )
                }
                d'8
                e'8
            }


    ..  container:: example

        A doubly nested tuplet:

            >>> third_tuplet = abjad.Tuplet((4, 5), [])
            >>> third_tuplet.extend("e''32 [ ef''32 d''32 cs''32 cqs''32 ]")
            >>> second_tuplet.insert(1, third_tuplet)
            >>> abjad.show(tuplet) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(tuplet)
            \tweak edge-height #'(0.7 . 0)
            \times 2/3 {
                c'8
                \tweak edge-height #'(0.7 . 0)
                \times 4/7 {
                    g'4.
                    (
                    \times 4/5 {
                        e''32
                        [
                        ef''32
                        d''32
                        cs''32
                        cqs''32
                        ]
                    }
                    a'16
                    )
                }
                d'8
                e'8
            }

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Containers'

    __slots__ = (
        '_denominator',
        '_force_fraction',
        '_hide',
        '_multiplier',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        multiplier=None,
        components=None,
        denominator: int = None,
        force_fraction: bool = None,
        hide: bool = None,
        ) -> None:
        import abjad
        Container.__init__(self, components)
        multiplier = multiplier or Multiplier(2, 3)
        self.multiplier = multiplier
        self.denominator = denominator
        self.force_fraction = force_fraction
        self.hide = hide

    ### SPECIAL METHODS ###

    def __getnewargs__(self) -> tuple:
        '''Gets new arguments of tuplet.
        '''
        return (self.multiplier,)

    ### PRIVATE METHODS ###

    def _as_graphviz_node(self):
        import abjad
        node = abjad.Component._as_graphviz_node(self)
        node[0].extend([
            abjad.graphtools.GraphvizTableRow([
                abjad.graphtools.GraphvizTableCell(
                    label=type(self).__name__,
                    attributes={'border': 0},
                    ),
                ]),
            abjad.graphtools.GraphvizTableHorizontalRule(),
            abjad.graphtools.GraphvizTableRow([
                abjad.graphtools.GraphvizTableCell(
                    label='* {!s}'.format(self.multiplier),
                    attributes={'border': 0},
                    ),
                ]),
            ])
        return node

    def _format_after_slot(self, bundle):
        result = []
        result.append(('grob reverts', bundle.grob_reverts))
        result.append(('commands', bundle.after.commands))
        result.append(('comments', bundle.after.comments))
        return tuple(result)

    def _format_before_slot(self, bundle):
        result = []
        result.append(('comments', bundle.before.comments))
        result.append(('commands', bundle.before.commands))
        result.append(('grob overrides', bundle.grob_overrides))
        result.append(('context settings', bundle.context_settings))
        return tuple(result)

    def _format_close_brackets_slot(self, bundle):
        result = []
        if self.multiplier:
            result.append([('self_brackets', 'close'), '}'])
        return tuple(result)

    def _format_closing_slot(self, bundle):
        result = []
        result.append(('commands', bundle.closing.commands))
        result.append(('comments', bundle.closing.comments))
        return self._format_slot_contributions_with_indent(result)

    def _format_lilypond_fraction_command_string(self):
        import abjad
        if self.hide:
            return ''
        if 'text' in vars(abjad.override(self).tuplet_number):
            return ''
        if (self.augmentation() or
            not self._get_power_of_two_denominator() or
            self.multiplier.denominator == 1 or
            self.force_fraction
            ):
            return r"\tweak text #tuplet-number::calc-fraction-text"
        return ''

    def _format_open_brackets_slot(self, bundle):
        result = []
        if self.multiplier:
            if self.hide:
                contributor = (self, 'hide')
                scale_durations_command_string = \
                    self._get_scale_durations_command_string()
                contributions = [scale_durations_command_string]
                result.append([contributor, contributions])
            else:
                contributor = ('self_brackets', 'open')
                contributions = []
                fraction_command_string = \
                    self._format_lilypond_fraction_command_string()
                if fraction_command_string:
                    contributions.append(fraction_command_string)
                edge_height_tweak_string = \
                    self._get_edge_height_tweak_string()
                if edge_height_tweak_string:
                    contributions.append(edge_height_tweak_string)
                times_command_string = self._get_times_command_string()
                contributions.append(times_command_string)
                result.append([contributor, contributions])
        return tuple(result)

    def _format_opening_slot(self, bundle):
        result = []
        result.append(('comments', bundle.opening.comments))
        result.append(('commands', bundle.opening.commands))
        return self._format_slot_contributions_with_indent(result)

    def _get_compact_representation(self):
        if not self:
            return '{{ {!s} }}'.format(self.multiplier)
        return '{{ {!s} {} }}'.format(
            self.multiplier,
            self._get_contents_summary(),
            )

    def _get_edge_height_tweak_string(self):
        import abjad
        parentage = inspect(self).get_parentage()
        measure = parentage.get_first(abjad.Measure)
        if measure and measure.implicit_scaling:
            return
        duration = self._get_preprolated_duration()
        denominator = duration.denominator
        if not abjad.mathtools.is_nonnegative_integer_power_of_two(
            denominator):
            return r"\tweak edge-height #'(0.7 . 0)"

    def _get_format_specification(self):
        import abjad
        return abjad.FormatSpecification(
            client=self,
            repr_args_values=[self.multiplier, self._get_contents_summary()],
            storage_format_args_values=[self.multiplier, self[:]],
            storage_format_kwargs_names=[],
            )

    def _get_lilypond_format(self):
        self._update_now(indicators=True)
        return self._format_component()

    def _get_multiplier_fraction_string(self):
        import abjad
        if self.denominator is not None:
            inverse_multiplier = Multiplier(
                self.multiplier.denominator, self.multiplier.numerator)
            nonreduced_fraction = abjad.NonreducedFraction(inverse_multiplier)
            nonreduced_fraction = nonreduced_fraction.with_denominator(
                self.denominator)
            denominator, numerator = nonreduced_fraction.pair
        else:
            numerator, denominator = self.multiplier.numerator, self.multiplier.denominator
        return '%s/%s' % (numerator, denominator)

    def _get_power_of_two_denominator(self):
        import abjad
        if self.multiplier:
            return abjad.mathtools.is_nonnegative_integer_power_of_two(
                self.multiplier.numerator)
        else:
            return True

    def _get_preprolated_duration(self):
        return self.multiplied_duration

    def _get_ratio_string(self):
        multiplier = self.multiplier
        if multiplier is not None:
            numerator = multiplier.numerator
            denominator = multiplier.denominator
            ratio_string = '{}:{}'.format(denominator, numerator)
            return ratio_string
        else:
            return None

    def _get_scale_durations_command_string(self):
        multiplier = self.multiplier
        string = r"\scaleDurations #'({} . {}) {{"
        string = string.format(multiplier.numerator, multiplier.denominator)
        return string

    def _get_summary(self):
        if 0 < len(self):
            return ', '.join([str(x) for x in self.components])
        else:
            return ''

    def _get_times_command_string(self):
        string = r'\times {} {{'.format(
            self._get_multiplier_fraction_string()
            )
        return string

    def _rest_filled(self):
        import abjad
        return all(isinstance(_, abjad.Rest) for _ in self)

    def _scale(self, multiplier):
        import abjad
        multiplier = Multiplier(multiplier)
        for component in self[:]:
            if isinstance(component, Leaf):
                new_duration = multiplier * component.written_duration
                component._set_duration(new_duration)
        self.normalize_multiplier()

    ### PUBLIC PROPERTIES ###

    @property
    def denominator(self) -> typing.Optional[int]:
        r'''Gets and sets preferred denominator of tuplet.

        ..  container:: example

            Gets preferred denominator of tuplet:

            >>> tuplet = abjad.Tuplet((2, 3), "c'8 d'8 e'8")
            >>> tuplet.denominator is None
            True
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(tuplet)
                \times 2/3 {
                    c'8
                    d'8
                    e'8
                }

        ..  container:: example

            Sets preferred denominator of tuplet:

            >>> tuplet = abjad.Tuplet((2, 3), "c'8 d'8 e'8")
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(tuplet)
                \times 2/3 {
                    c'8
                    d'8
                    e'8
                }

            >>> tuplet.denominator = 4
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(tuplet)
                \times 4/6 {
                    c'8
                    d'8
                    e'8
                }

        '''
        return self._denominator

    @denominator.setter
    def denominator(self, argument):
        if isinstance(argument, int):
            if not 0 < argument:
                raise ValueError(argument)
        elif not isinstance(argument, type(None)):
            raise TypeError(argument)
        self._denominator = argument

    @property
    def force_fraction(self) -> typing.Optional[bool]:
        r'''Gets and sets force fraction flag.

        ..  container:: example

            The ``default.ly`` stylesheet included in all Abjad API examples
            includes the following:
            
            ``\override TupletNumber.text = #tuplet-number::calc-fraction-text``

            This means that even simple tuplets format as explicit fractions:

            >>> staff = abjad.Staff()
            >>> staff.append(abjad.Tuplet((2, 3), "c'4 d' e'"))
            >>> staff.append(abjad.Tuplet((2, 3), "c'4 d' e'"))
            >>> staff.append(abjad.Tuplet((2, 3), "c'4 d' e'"))
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \times 2/3 {
                        c'4
                        d'4
                        e'4
                    }
                    \times 2/3 {
                        c'4
                        d'4
                        e'4
                    }
                    \times 2/3 {
                        c'4
                        d'4
                        e'4
                    }
                }

            To illustrate the effect of Abjad's force fraction property, we can
            temporarily restore LilyPond's default tuplet number formatting
            like this:

            >>> staff = abjad.Staff()
            >>> staff.append(abjad.Tuplet((2, 3), "c'4 d' e'"))
            >>> staff.append(abjad.Tuplet((2, 3), "c'4 d' e'"))
            >>> staff.append(abjad.Tuplet((2, 3), "c'4 d' e'"))
            >>> string = 'tuplet-number::calc-denominator-text'
            >>> abjad.override(staff).tuplet_number.text = string
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    \override TupletNumber.text = #tuplet-number::calc-denominator-text
                }
                {
                    \times 2/3 {
                        c'4
                        d'4
                        e'4
                    }
                    \times 2/3 {
                        c'4
                        d'4
                        e'4
                    }
                    \times 2/3 {
                        c'4
                        d'4
                        e'4
                    }
                }

            Which makes it possible to see the effect of setting force fraction
            to true on a single tuplet:

            >>> tuplet = staff[1]
            >>> tuplet.force_fraction = True
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    \override TupletNumber.text = #tuplet-number::calc-denominator-text
                }
                {
                    \times 2/3 {
                        c'4
                        d'4
                        e'4
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 2/3 {
                        c'4
                        d'4
                        e'4
                    }
                    \times 2/3 {
                        c'4
                        d'4
                        e'4
                    }
                }

        ..  container:: example

            Ignored when tuplet number text is overridden explicitly:

            >>> tuplet = abjad.Tuplet((2, 3), "c'8 d'8 e'8")
            >>> duration = abjad.inspect(tuplet).get_duration()
            >>> markup = duration.to_score_markup()
            >>> abjad.override(tuplet).tuplet_number.text = markup
            >>> staff = abjad.Staff([tuplet])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \override TupletNumber.text = \markup {
                        \score
                            {
                                \new Score
                                \with
                                {
                                    \override SpacingSpanner.spacing-increment = #0.5
                                    proportionalNotationDuration = ##f
                                }
                                <<
                                    \new RhythmicStaff
                                    \with
                                    {
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
                                    }
                                    {
                                        c'4
                                    }
                                >>
                                \layout {
                                    indent = #0
                                    ragged-right = ##t
                                }
                            }
                        }
                    \times 2/3 {
                        c'8
                        d'8
                        e'8
                    }
                    \revert TupletNumber.text
                }

        '''
        return self._force_fraction

    @force_fraction.setter
    def force_fraction(self, argument):
        if isinstance(argument, (bool, type(None))):
            self._force_fraction = argument
        else:
            message = f'force fraction must be boolean (not {argument!r}).'
            raise TypeError(message)

    @property
    def hide(self) -> typing.Optional[bool]:
        r'''Is true when tuplet bracket hides.

        ..  container:: example

            >>> tuplet = abjad.Tuplet((2, 3), "c'8 d'8 e'8")
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(tuplet)
                \times 2/3 {
                    c'8
                    d'8
                    e'8
                }

            >>> tuplet.hide is None
            True

        ..  container:: example

            >>> tuplet_1 = abjad.Tuplet((2, 3), "c'4 d'4 e'4")
            >>> tuplet_2 = abjad.Tuplet((2, 3), "d'4 e'4 f'4")
            >>> staff = abjad.Staff([tuplet_1, tuplet_2])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \times 2/3 {
                        c'4
                        d'4
                        e'4
                    }
                    \times 2/3 {
                        d'4
                        e'4
                        f'4
                    }
                }

            >>> staff[0].hide = True
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \scaleDurations #'(2 . 3) {
                        c'4
                        d'4
                        e'4
                    }
                    \times 2/3 {
                        d'4
                        e'4
                        f'4
                    }
                }

        Hides tuplet bracket and tuplet number when true.
        '''
        return self._hide

    @hide.setter
    def hide(self, argument):
        assert isinstance(argument, (bool, type(None))), repr(argument)
        self._hide = argument

    @property
    def implied_prolation(self) -> Multiplier:
        r'''Gets implied prolation of tuplet.

        ..  container:: example

            Defined equal to tuplet multiplier:

            >>> tuplet = abjad.Tuplet((2, 3), "c'8 d'8 e'8")
            >>> abjad.show(tuplet) # doctest: +SKIP

            >>> tuplet.implied_prolation
            Multiplier(2, 3)

        '''
        return self.multiplier

    @property
    def multiplied_duration(self) -> Duration:
        r'''Multiplied duration of tuplet.

        ..  container:: example

            >>> tuplet = abjad.Tuplet((2, 3), "c'8 d'8 e'8")

            >>> abjad.show(tuplet) # doctest: +SKIP

            >>> tuplet.multiplied_duration
            Duration(1, 4)

        '''
        return self.multiplier * self._get_contents_duration()

    @property
    def multiplier(self) -> Multiplier:
        r'''Gets and sets multiplier of tuplet.

        ..  container:: example

            Gets tuplet multiplier:

                >>> tuplet = abjad.Tuplet((2, 3), "c'8 d'8 e'8")
                >>> abjad.show(tuplet) # doctest: +SKIP

            >>> tuplet.multiplier
            Multiplier(2, 3)

        ..  container:: example

            Sets tuplet multiplier:

                >>> tuplet.multiplier = abjad.Multiplier(4, 3)
                >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(tuplet)
                \tweak text #tuplet-number::calc-fraction-text
                \times 4/3 {
                    c'8
                    d'8
                    e'8
                }

        '''
        return self._multiplier

    @multiplier.setter
    def multiplier(self, argument):
        import abjad
        if isinstance(argument, (int, abjad.Fraction)):
            rational = Multiplier(argument)
        elif isinstance(argument, tuple):
            rational = Multiplier(argument)
        else:
            message = 'can not set tuplet multiplier: {!r}.'
            message = message.format(argument)
            raise ValueError(message)
        if 0 < rational:
            self._multiplier = rational
        else:
            message = 'tuplet multiplier must be positive: {!r}.'
            message = message.format(argument)
            raise ValueError(message)

    ### PUBLIC METHODS ###

    def append(self, component, preserve_duration=False) -> None:
        r'''Appends `component` to tuplet.

        ..  container:: example

            Appends note to tuplet:

            >>> tuplet = abjad.Tuplet((2, 3), "c'4 ( d'4 f'4 )")
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(tuplet)
                \times 2/3 {
                    c'4
                    (
                    d'4
                    f'4
                    )
                }

            >>> tuplet.append(abjad.Note("e'4"))
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(tuplet)
                \tweak edge-height #'(0.7 . 0)
                \times 2/3 {
                    c'4
                    (
                    d'4
                    f'4
                    )
                    e'4
                }

        ..  container:: example

            Appends note to tuplet and preserves tuplet duration:

            >>> tuplet = abjad.Tuplet((2, 3), "c'4 ( d'4 f'4 )")
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(tuplet)
                \times 2/3 {
                    c'4
                    (
                    d'4
                    f'4
                    )
                }

            >>> tuplet.append(abjad.Note("e'4"), preserve_duration=True)
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(tuplet)
                \times 1/2 {
                    c'4
                    (
                    d'4
                    f'4
                    )
                    e'4
                }

        '''
        import abjad
        if preserve_duration:
            old_duration = inspect(self).get_duration()
        Container.append(self, component)
        if preserve_duration:
            new_duration = self._get_contents_duration()
            multiplier = old_duration / new_duration
            self.multiplier = multiplier
            assert inspect(self).get_duration() == old_duration

    def augmentation(self) -> bool:
        r'''Is true when tuplet multiplier is greater than ``1``.
        Otherwise false.

        ..  container:: example

            Augmented tuplet:

            >>> tuplet = abjad.Tuplet((4, 3), "c'8 d'8 e'8")
            >>> abjad.show(tuplet) # doctest: +SKIP

            >>> tuplet.augmentation()
            True

        ..  container:: example

            Diminished tuplet:

            >>> tuplet = abjad.Tuplet((2, 3), "c'4 d'4 e'4")
            >>> abjad.show(tuplet) # doctest: +SKIP

            >>> tuplet.augmentation()
            False

        ..  container:: example

            Trivial tuplet:

            >>> tuplet = abjad.Tuplet((1, 1), "c'8. d'8. e'8.")
            >>> abjad.show(tuplet) # doctest: +SKIP

            >>> tuplet.augmentation()
            False

        '''
        if self.multiplier:
            return 1 < self.multiplier
        else:
            return False

    def diminution(self) -> bool:
        r'''Is true when tuplet multiplier is less than ``1``.

        ..  container:: example

            Augmented tuplet:

            >>> tuplet = abjad.Tuplet((4, 3), "c'8 d'8 e'8")
            >>> abjad.show(tuplet) # doctest: +SKIP

            >>> tuplet.diminution()
            False

        ..  container:: example

            Diminished tuplet:

            >>> tuplet = abjad.Tuplet((2, 3), "c'4 d'4 e'4")
            >>> abjad.show(tuplet) # doctest: +SKIP

            >>> tuplet.diminution()
            True

        ..  container:: example

            Trivial tuplet:

            >>> tuplet = abjad.Tuplet((1, 1), "c'8. d'8. e'8.")
            >>> abjad.show(tuplet) # doctest: +SKIP

            >>> tuplet.diminution()
            False

        '''
        if self.multiplier:
            return self.multiplier < 1
        else:
            return False

    def extend(self, argument, preserve_duration=False) -> None:
        r'''Extends tuplet with `argument`.

        ..  container:: example

            Extends tuplet with three notes:

            >>> tuplet = abjad.Tuplet((2, 3), "c'4 ( d'4 f'4 )")
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(tuplet)
                \times 2/3 {
                    c'4
                    (
                    d'4
                    f'4
                    )
                }

            >>> notes = [abjad.Note("e'32"), abjad.Note("d'32"), abjad.Note("e'16")]
            >>> tuplet.extend(notes)
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(tuplet)
                \tweak edge-height #'(0.7 . 0)
                \times 2/3 {
                    c'4
                    (
                    d'4
                    f'4
                    )
                    e'32
                    d'32
                    e'16
                }

        ..  container:: example

            Extends tuplet with three notes and preserves tuplet duration:

            >>> tuplet = abjad.Tuplet((2, 3), "c'4 ( d'4 f'4 )")
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(tuplet)
                \times 2/3 {
                    c'4
                    (
                    d'4
                    f'4
                    )
                }

            >>> notes = [abjad.Note("e'32"), abjad.Note("d'32"), abjad.Note("e'16")]
            >>> tuplet.extend(notes, preserve_duration=True)
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(tuplet)
                \times 4/7 {
                    c'4
                    (
                    d'4
                    f'4
                    )
                    e'32
                    d'32
                    e'16
                }

        '''
        import abjad
        if preserve_duration:
            old_duration = inspect(self).get_duration()
        Container.extend(self, argument)
        if preserve_duration:
            new_duration = self._get_contents_duration()
            multiplier = old_duration / new_duration
            self.multiplier = multiplier
            assert inspect(self).get_duration() == old_duration

    @staticmethod
    def from_duration(duration, components):
        r'''Makes tuplet from `duration` and `components`.

        ..  container:: example

            Makes diminution:

            >>> tuplet = abjad.Tuplet.from_duration((2, 8), "c'8 d' e'")
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(tuplet)
                \times 2/3 {
                    c'8
                    d'8
                    e'8
                }

        '''
        import abjad
        if not len(components):
            message = 'components must be nonempty: {!r}.'
            message = message.format(components)
            raise Exception(message)
        target_duration = Duration(duration)
        tuplet = Tuplet(1, components)
        contents_duration = inspect(tuplet).get_duration()
        multiplier = target_duration / contents_duration
        tuplet.multiplier = multiplier
        return tuplet

    @staticmethod
    def from_duration_and_ratio(
        duration,
        ratio,
        avoid_dots=True,
        decrease_monotonic=True,
        diminution=True,
        ):
        r'''Makes tuplet from `duration` and `ratio`.

        ..  container:: example

            Makes augmented tuplet from `duration` and `ratio` and avoid dots.

            Makes tupletted leaves strictly without dots when all
            `ratio` equal ``1``:

            >>> tuplet = abjad.Tuplet.from_duration_and_ratio(
            ...     abjad.Duration(3, 16),
            ...     abjad.Ratio((1, 1, 1, -1, -1)),
            ...     avoid_dots=True,
            ...     diminution=False,
            ...     )
            >>> staff = abjad.Staff(
            ...     [abjad.Measure((3, 16), [tuplet])],
            ...     lilypond_type='RhythmicStaff',
            ...     )
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff[0])
                {   % measure
                    \time 3/16
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 6/5 {
                        c'32
                        c'32
                        c'32
                        r32
                        r32
                    }
                }   % measure

            Allows tupletted leaves to return with dots when some `ratio`
            do not equal ``1``:

            >>> tuplet = abjad.Tuplet.from_duration_and_ratio(
            ...     abjad.Duration(3, 16),
            ...     abjad.Ratio((1, -2, -2, 3, 3)),
            ...     avoid_dots=True,
            ...     diminution=False,
            ...     )
            >>> staff = abjad.Staff(
            ...     [abjad.Measure((3, 16), [tuplet])],
            ...     lilypond_type='RhythmicStaff',
            ...     )
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff[0])
                {   % measure
                    \time 3/16
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 12/11 {
                        c'64
                        r32
                        r32
                        c'32.
                        c'32.
                    }
                }   % measure

            Interprets nonassignable `ratio` according to `decrease_monotonic`:

            >>> tuplet = abjad.Tuplet.from_duration_and_ratio(
            ...     abjad.Duration(3, 16),
            ...     abjad.Ratio((5, -1, 5)),
            ...     avoid_dots=True,
            ...     decrease_monotonic=False,
            ...     diminution=False,
            ...     )
            >>> staff = abjad.Staff(
            ...     [abjad.Measure((3, 16), [tuplet])],
            ...     lilypond_type='RhythmicStaff',
            ...     )
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff[0])
                {   % measure
                    \time 3/16
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 12/11 {
                        c'64
                        ~
                        c'16
                        r64
                        c'64
                        ~
                        c'16
                    }
                }   % measure

        ..  container:: example

            Makes augmented tuplet from `duration` and `ratio` and encourages
            dots:

            >>> tuplet = abjad.Tuplet.from_duration_and_ratio(
            ...     abjad.Duration(3, 16),
            ...     abjad.Ratio((1, 1, 1, -1, -1)),
            ...     avoid_dots=False,
            ...     diminution=False,
            ...     )
            >>> staff = abjad.Staff(
            ...     [abjad.Measure((3, 16), [tuplet])],
            ...     lilypond_type='RhythmicStaff',
            ...     )
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff[0])
                {   % measure
                    \time 3/16
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 8/5 {
                        c'64.
                        c'64.
                        c'64.
                        r64.
                        r64.
                    }
                }   % measure

            Interprets nonassignable `ratio` according to `decrease_monotonic`:

            >>> tuplet = abjad.Tuplet.from_duration_and_ratio(
            ...     abjad.Duration(3, 16),
            ...     abjad.Ratio((5, -1, 5)),
            ...     avoid_dots=False,
            ...     decrease_monotonic=False,
            ...     diminution=False,
            ...     )
            >>> staff = abjad.Staff(
            ...     [abjad.Measure((3, 16), [tuplet])],
            ...     lilypond_type='RhythmicStaff',
            ...     )
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff[0])
                {   % measure
                    \time 3/16
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 16/11 {
                        c'32...
                        r128.
                        c'32...
                    }
                }   % measure

        ..  container:: example

            Makes diminished tuplet from `duration` and nonzero integer
            `ratio`.

            Makes tupletted leaves strictly without dots when all
            `ratio` equal ``1``:

            >>> tuplet = abjad.Tuplet.from_duration_and_ratio(
            ...     abjad.Duration(3, 16),
            ...     abjad.Ratio((1, 1, 1, -1, -1)),
            ...     avoid_dots=True,
            ...     diminution=True,
            ...     )
            >>> staff = abjad.Staff(
            ...     [abjad.Measure((3, 16), [tuplet])],
            ...     lilypond_type='RhythmicStaff',
            ...     )
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff[0])
                {   % measure
                    \time 3/16
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 3/5 {
                        c'16
                        c'16
                        c'16
                        r16
                        r16
                    }
                }   % measure

            Allows tupletted leaves to return with dots when some `ratio`
            do not equal ``1``:

            >>> tuplet = abjad.Tuplet.from_duration_and_ratio(
            ...     abjad.Duration(3, 16),
            ...     abjad.Ratio((1, -2, -2, 3, 3)),
            ...     avoid_dots=True,
            ...     diminution=True,
            ...     )
            >>> staff = abjad.Staff(
            ...     [abjad.Measure((3, 16), [tuplet])],
            ...     lilypond_type='RhythmicStaff',
            ...     )
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff[0])
                {   % measure
                    \time 3/16
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 6/11 {
                        c'32
                        r16
                        r16
                        c'16.
                        c'16.
                    }
                }   % measure

            Interprets nonassignable `ratio` according to `decrease_monotonic`:

            >>> tuplet = abjad.Tuplet.from_duration_and_ratio(
            ...     abjad.Duration(3, 16),
            ...     abjad.Ratio((5, -1, 5)),
            ...     avoid_dots=True,
            ...     decrease_monotonic=False,
            ...     diminution=True,
            ...     )
            >>> staff = abjad.Staff(
            ...     [abjad.Measure((3, 16), [tuplet])],
            ...     lilypond_type='RhythmicStaff',
            ...     )
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff[0])
                {   % measure
                    \time 3/16
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 6/11 {
                        c'32
                        ~
                        c'8
                        r32
                        c'32
                        ~
                        c'8
                    }
                }   % measure

        ..  container:: example

            Makes diminished tuplet from `duration` and `ratio` and encourages
            dots:

            >>> tuplet = abjad.Tuplet.from_duration_and_ratio(
            ...     abjad.Duration(3, 16),
            ...     abjad.Ratio((1, 1, 1, -1, -1)),
            ...     avoid_dots=False,
            ...     diminution=True,
            ...     )
            >>> staff = abjad.Staff(
            ...     [abjad.Measure((3, 16), [tuplet])],
            ...     lilypond_type = 'RhythmicStaff',
            ...     )
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff[0])
                {   % measure
                    \time 3/16
                    \times 4/5 {
                        c'32.
                        c'32.
                        c'32.
                        r32.
                        r32.
                    }
                }   % measure

            Interprets nonassignable `ratio` according to `direction`:

            >>> tuplet = abjad.Tuplet.from_duration_and_ratio(
            ...     abjad.Duration(3, 16),
            ...     abjad.Ratio((5, -1, 5)),
            ...     avoid_dots=False,
            ...     decrease_monotonic=False,
            ...     diminution=True,
            ...     )
            >>> staff = abjad.Staff(
            ...     [abjad.Measure((3, 16), [tuplet])],
            ...     lilypond_type='RhythmicStaff',
            ...     )
            >>> abjad.show(measure) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff[0])
                {   % measure
                    \time 3/16
                    \times 8/11 {
                        c'16...
                        r64.
                        c'16...
                    }
                }   % measure

        Reduces `ratio` relative to each other.

        Interprets negative `ratio` as rests.

        Returns tuplet.
        '''
        import abjad
        duration = abjad.Duration(duration)
        ratio = abjad.Ratio(ratio)
        basic_prolated_duration = duration / abjad.mathtools.weight(
            ratio.numbers)
        if avoid_dots:
            basic_written_duration = \
                basic_prolated_duration.equal_or_greater_power_of_two
        else:
            basic_written_duration = \
                basic_prolated_duration.equal_or_greater_assignable
        written_durations = [x * basic_written_duration for x in ratio.numbers]
        leaf_maker = abjad.LeafMaker(decrease_monotonic=decrease_monotonic)
        try:
            notes = [
                abjad.Note(0, x) if 0 < x else abjad.Rest(abs(x))
                for x in written_durations
                ]
        except AssignabilityError:
            denominator = duration.denominator
            note_durations = [
                abjad.Duration(x, denominator)
                for x in ratio.numbers
                ]
            pitches = [
                None if note_duration < 0 else 0
                for note_duration in note_durations
                ]
            leaf_durations = [
                abs(note_duration)
                for note_duration in note_durations
                ]
            notes = leaf_maker(pitches, leaf_durations)
        tuplet = abjad.Tuplet.from_duration(duration, notes)
        tuplet.normalize_multiplier()
        if tuplet.multiplier != 1:
            if diminution:
                if not tuplet.diminution():
                    tuplet.toggle_prolation()
            else:
                if tuplet.diminution():
                    tuplet.toggle_prolation()
        return tuplet

    @staticmethod
    def from_leaf_and_ratio(leaf, ratio, diminution=True):
        r'''Makes tuplet from `leaf` and `ratio`.

        >>> note = abjad.Note("c'8.")

        ..  container:: example

            Changes leaf to augmented tuplets with `ratio`:

            >>> tuplet = abjad.Tuplet.from_leaf_and_ratio(
            ...     note,
            ...     abjad.Ratio((1,)),
            ...     diminution=False,
            ...     )
            >>> staff = abjad.Staff(
            ...     [abjad.Measure((3, 16), [tuplet])],
            ...     lilypond_type='RhythmicStaff',
            ...     )
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(tuplet)
                \tweak text #tuplet-number::calc-fraction-text
                \times 1/1 {
                    c'8.
                }

        ..  container:: example

            Changes leaf to augmented tuplets with `ratio`:

            >>> tuplet = abjad.Tuplet.from_leaf_and_ratio(
            ...     note,
            ...     [1, 2],
            ...     diminution=False,
            ...     )
            >>> staff = abjad.Staff(
            ...     [abjad.Measure((3, 16), [tuplet])],
            ...     lilypond_type='RhythmicStaff',
            ...     )
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(tuplet)
                \tweak text #tuplet-number::calc-fraction-text
                \times 1/1 {
                    c'16
                    c'8
                }

        ..  container:: example

            Changes leaf to augmented tuplets with `ratio`:

            >>> tuplet = abjad.Tuplet.from_leaf_and_ratio(
            ...     note,
            ...     abjad.Ratio((1, 2, 2)),
            ...     diminution=False,
            ...     )
            >>> staff = abjad.Staff(
            ...     [abjad.Measure((3, 16), [tuplet])],
            ...     lilypond_type='RhythmicStaff',
            ...     )
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(tuplet)
                \tweak text #tuplet-number::calc-fraction-text
                \times 8/5 {
                    c'64.
                    c'32.
                    c'32.
                }

        ..  container:: example

            Changes leaf to augmented tuplets with `ratio`:

            >>> tuplet = abjad.Tuplet.from_leaf_and_ratio(
            ...     note,
            ...     [1, 2, 2, 3],
            ...     diminution=False,
            ...     )
            >>> staff = abjad.Staff(
            ...     [abjad.Measure((3, 16), [tuplet])],
            ...     lilypond_type='RhythmicStaff',
            ...     )
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(tuplet)
                \tweak text #tuplet-number::calc-fraction-text
                \times 3/2 {
                    c'64
                    c'32
                    c'32
                    c'32.
                }

        ..  container:: example

            Changes leaf to augmented tuplets with `ratio`:

            >>> tuplet = abjad.Tuplet.from_leaf_and_ratio(
            ...     note,
            ...     [1, 2, 2, 3, 3],
            ...     diminution=False,
            ...     )
            >>> staff = abjad.Staff(
            ...     [abjad.Measure((3, 16), [tuplet])],
            ...     lilypond_type='RhythmicStaff',
            ...     )
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(tuplet)
                \tweak text #tuplet-number::calc-fraction-text
                \times 12/11 {
                    c'64
                    c'32
                    c'32
                    c'32.
                    c'32.
                }

        ..  container:: example

            Changes leaf to augmented tuplets with `ratio`:

            >>> tuplet = abjad.Tuplet.from_leaf_and_ratio(
            ...     note,
            ...     abjad.Ratio((1, 2, 2, 3, 3, 4)),
            ...     diminution=False,
            ...     )
            >>> staff = abjad.Staff(
            ...     [abjad.Measure((3, 16), [tuplet])],
            ...     lilypond_type='RhythmicStaff',
            ...     )
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(tuplet)
                \tweak text #tuplet-number::calc-fraction-text
                \times 8/5 {
                    c'128
                    c'64
                    c'64
                    c'64.
                    c'64.
                    c'32
                }

        ..  container:: example

            Changes leaf to diminished tuplets with `ratio`:

            >>> tuplet = abjad.Tuplet.from_leaf_and_ratio(
            ...     note,
            ...     [1],
            ...     diminution=True,
            ...     )
            >>> staff = abjad.Staff(
            ...     [abjad.Measure((3, 16), [tuplet])],
            ...     lilypond_type='RhythmicStaff',
            ...     )
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(tuplet)
                \tweak text #tuplet-number::calc-fraction-text
                \times 1/1 {
                    c'8.
                }

        ..  container:: example

            Changes leaf to diminished tuplets with `ratio`:

            >>> tuplet = abjad.Tuplet.from_leaf_and_ratio(
            ...     note,
            ...     [1, 2],
            ...     diminution=True,
            ...     )
            >>> staff = abjad.Staff(
            ...     [abjad.Measure((3, 16), [tuplet])],
            ...     lilypond_type='RhythmicStaff',
            ...     )
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(tuplet)
                \tweak text #tuplet-number::calc-fraction-text
                \times 1/1 {
                    c'16
                    c'8
                }

        ..  container:: example

            Changes leaf to diminished tuplets with `ratio`:

            >>> tuplet = abjad.Tuplet.from_leaf_and_ratio(
            ...     note,
            ...     [1, 2, 2],
            ...     diminution=True,
            ...     )
            >>> staff = abjad.Staff(
            ...     [abjad.Measure((3, 16), [tuplet])],
            ...     lilypond_type='RhythmicStaff',
            ...     )
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(tuplet)
                \times 4/5 {
                    c'32.
                    c'16.
                    c'16.
                }

        ..  container:: example

            Changes leaf to diminished tuplets with `ratio`:

            >>> tuplet = abjad.Tuplet.from_leaf_and_ratio(
            ...     note,
            ...     [1, 2, 2, 3],
            ...     diminution=True,
            ...     )
            >>> staff = abjad.Staff(
            ...     [abjad.Measure((3, 16), [tuplet])],
            ...     lilypond_type='RhythmicStaff',
            ...     )
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(tuplet)
                \tweak text #tuplet-number::calc-fraction-text
                \times 3/4 {
                    c'32
                    c'16
                    c'16
                    c'16.
                }

        ..  container:: example

            Changes leaf to diminished tuplets with `ratio`:

            >>> tuplet = abjad.Tuplet.from_leaf_and_ratio(
            ...     note,
            ...     [1, 2, 2, 3, 3],
            ...     diminution=True,
            ...     )
            >>> staff = abjad.Staff(
            ...     [abjad.Measure((3, 16), [tuplet])],
            ...     lilypond_type='RhythmicStaff',
            ...     )
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(tuplet)
                \tweak text #tuplet-number::calc-fraction-text
                \times 6/11 {
                    c'32
                    c'16
                    c'16
                    c'16.
                    c'16.
                }

        ..  container:: example

            Changes leaf to diminished tuplets with `ratio`:

            >>> tuplet = abjad.Tuplet.from_leaf_and_ratio(
            ...     note,
            ...     [1, 2, 2, 3, 3, 4],
            ...     diminution=True,
            ...     )
            >>> staff = abjad.Staff(
            ...     [abjad.Measure((3, 16), [tuplet])],
            ...     lilypond_type='RhythmicStaff',
            ...     )
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(tuplet)
                \times 4/5 {
                    c'64
                    c'32
                    c'32
                    c'32.
                    c'32.
                    c'16
                }

        Returns tuplet.
        '''
        tuplet = leaf._to_tuplet_with_ratio(ratio, diminution=diminution)
        return tuplet

    @staticmethod
    def from_ratio_and_pair(
        ratio,
        fraction,
        allow_trivial=False,
        ):
        r'''Makes tuplet from nonreduced `ratio` and nonreduced `fraction`.

        ..  container:: example

            Makes container when no prolation is necessary:

            >>> tuplet = abjad.Tuplet.from_ratio_and_pair(
            ...     abjad.NonreducedRatio((1,)),
            ...     abjad.NonreducedFraction(7, 16),
            ...     )
            >>> staff = abjad.Staff(
            ...     [abjad.Measure((7, 16), [tuplet])],
            ...     lilypond_type='RhythmicStaff',
            ...     )
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff[0])
                {   % measure
                    \time 7/16
                    {
                        c'4..
                    }
                }   % measure

        ..  container:: example

            Makes trivial tuplet when no prolation is necessary and
            `allow_trivial` is true:

            >>> tuplet = abjad.Tuplet.from_ratio_and_pair(
            ...     abjad.NonreducedRatio((1,)),
            ...     abjad.NonreducedFraction(7, 16),
            ...     allow_trivial=True,
            ...     )
            >>> staff = abjad.Staff(
            ...     [abjad.Measure((7, 16), [tuplet])],
            ...     lilypond_type='RhythmicStaff',
            ...     )
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff[0])
                {   % measure
                    \time 7/16
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 1/1 {
                        c'4..
                    }
                }   % measure

        ..  container:: example

            Makes tuplet when prolation is necessary:

            >>> tuplet = abjad.Tuplet.from_ratio_and_pair(
            ...     abjad.NonreducedRatio((1, 2)),
            ...     abjad.NonreducedFraction(7, 16),
            ...     )
            >>> staff = abjad.Staff(
            ...     [abjad.Measure((7, 16), [tuplet])],
            ...     lilypond_type='RhythmicStaff',
            ...     )
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff[0])
                {   % measure
                    \time 7/16
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 7/6 {
                        c'8
                        c'4
                    }
                }   % measure

            >>> tuplet = abjad.Tuplet.from_ratio_and_pair(
            ...     abjad.NonreducedRatio((1, 2, 4)),
            ...     abjad.NonreducedFraction(7, 16),
            ...     )
            >>> staff = abjad.Staff(
            ...     [abjad.Measure((7, 16), [tuplet])],
            ...     lilypond_type='RhythmicStaff',
            ...     )
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff[0])
                {   % measure
                    \time 7/16
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 1/1 {
                        c'16
                        c'8
                        c'4
                    }
                }   % measure

            >>> tuplet = abjad.Tuplet.from_ratio_and_pair(
            ...     abjad.NonreducedRatio((1, 2, 4, 1)),
            ...     abjad.NonreducedFraction(7, 16),
            ...     )
            >>> staff = abjad.Staff(
            ...     [abjad.Measure((7, 16), [tuplet])],
            ...     lilypond_type='RhythmicStaff',
            ...     )
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff[0])
                {   % measure
                    \time 7/16
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 7/8 {
                        c'16
                        c'8
                        c'4
                        c'16
                    }
                }   % measure

            >>> tuplet = abjad.Tuplet.from_ratio_and_pair(
            ...     abjad.NonreducedRatio((1, 2, 4, 1, 2)),
            ...     abjad.NonreducedFraction(7, 16),
            ...     )
            >>> staff = abjad.Staff(
            ...     [abjad.Measure((7, 16), [tuplet])],
            ...     lilypond_type='RhythmicStaff',
            ...     )
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff[0])
                {   % measure
                    \time 7/16
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 7/10 {
                        c'16
                        c'8
                        c'4
                        c'16
                        c'8
                    }
                }   % measure

            >>> tuplet = abjad.Tuplet.from_ratio_and_pair(
            ...     abjad.NonreducedRatio((1, 2, 4, 1, 2, 4)),
            ...     abjad.NonreducedFraction(7, 16),
            ...     )
            >>> staff = abjad.Staff(
            ...     [abjad.Measure((7, 16), [tuplet])],
            ...     lilypond_type='RhythmicStaff',
            ...     )
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff[0])
                {   % measure
                    \time 7/16
                    \times 1/2 {
                        c'16
                        c'8
                        c'4
                        c'16
                        c'8
                        c'4
                    }
                }   % measure

        Interprets `d` as tuplet denominator.

        Returns tuplet or container.
        '''
        import abjad
        ratio = abjad.NonreducedRatio(ratio)
        if isinstance(fraction, tuple):
            fraction = abjad.NonreducedFraction(*fraction)
        numerator = fraction.numerator
        denominator = fraction.denominator
        duration = abjad.Duration(fraction)
        if len(ratio.numbers) == 1:
            if 0 < ratio.numbers[0]:
                try:
                    note = abjad.Note(0, duration)
                    if allow_trivial:
                        duration = inspect(note).get_duration()
                        tuplet = abjad.Tuplet.from_duration(duration, [note])
                        return tuplet
                    else:
                        return abjad.Container([note])
                except AssignabilityError:
                    maker = abjad.NoteMaker()
                    notes = maker(0, duration)
                    if allow_trivial:
                        duration = inspect(notes).get_duration()
                        return abjad.Tuplet.from_duration(duration, notes)
                    else:
                        return abjad.Container(notes)
            elif ratio.numbers[0] < 0:
                try:
                    rest = abjad.Rest(duration)
                    if allow_trivial:
                        duration = inspect(rest).get_duration()
                        return abjad.Tuplet.from_duration(duration, [rest])
                    else:
                        return abjad.Container([rest])
                except AssignabilityError:
                    maker = abjad.LeafMaker()
                    rests = maker([None], duration)
                    if allow_trivial:
                        duration = inspect(rests).get_duration()
                        return abjad.Tuplet.from_duration(duration, rests)
                    else:
                        return abjad.Container(rests)
            else:
                message = 'no divide zero values.'
                raise ValueError(message)
        if 1 < len(ratio.numbers):
            exponent = int(
                math.log(
                    abjad.mathtools.weight(ratio.numbers), 2) - 
                    math.log(numerator, 2)
                    )
            denominator = int(denominator * 2 ** exponent)
            components = []
            for x in ratio.numbers:
                if not x:
                    message = 'no divide zero values.'
                    raise ValueError(message)
                if 0 < x:
                    try:
                        note = abjad.Note(0, (x, denominator))
                        components.append(note)
                    except AssignabilityError:
                        maker = abjad.NoteMaker()
                        notes = maker(0, (x, denominator))
                        components.extend(notes)
                else:
                    rests = abjad.Rest((-x, denominator))
                    components.append(rests)
            return abjad.Tuplet.from_duration(duration, components)

    def normalize_multiplier(self) -> None:
        r'''Normalizes tuplet multiplier.

        ..  container:: example

            >>> tuplet = abjad.Tuplet((1, 3), "c'4 d' e'")
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(tuplet)
                \times 1/3 {
                    c'4
                    d'4
                    e'4
                }

            >>> tuplet.multiplier.normalized()
            False

            >>> tuplet.normalize_multiplier()
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(tuplet)
                \times 2/3 {
                    c'8
                    d'8
                    e'8
                }

            >>> tuplet.multiplier.normalized()
            True

        ..  container:: example

            >>> tuplet = abjad.Tuplet((8, 3), "c'32 d'32 e'32")
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(tuplet)
                \tweak text #tuplet-number::calc-fraction-text
                \times 8/3 {
                    c'32
                    d'32
                    e'32
                }

            >>> tuplet.multiplier.normalized()
            False

            >>> tuplet.normalize_multiplier()
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(tuplet)
                \tweak text #tuplet-number::calc-fraction-text
                \times 4/3 {
                    c'16
                    d'16
                    e'16
                }

            >>> tuplet.multiplier.normalized()
            True

        ..  container:: example

            >>> tuplet = abjad.Tuplet((5, 12), "c'4 d'4 e'4")
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(tuplet)
                \tweak text #tuplet-number::calc-fraction-text
                \times 5/12 {
                    c'4
                    d'4
                    e'4
                }

            >>> tuplet.multiplier.normalized()
            False

            >>> tuplet.normalize_multiplier()
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(tuplet)
                \tweak text #tuplet-number::calc-fraction-text
                \times 5/6 {
                    c'8
                    d'8
                    e'8
                }

            >>> tuplet.multiplier.normalized()
            True

        '''
        import abjad
        # find tuplet multiplier
        integer_exponent = int(math.log(self.multiplier, 2))
        leaf_multiplier = Multiplier(2) ** integer_exponent
        # scale leaves in tuplet by power of two
        for component in self:
            if isinstance(component, Leaf):
                old_written_duration = component.written_duration
                new_written_duration = leaf_multiplier * old_written_duration
                component._set_duration(new_written_duration)
        numerator, denominator = leaf_multiplier.pair
        multiplier = Multiplier(denominator, numerator)
        self.multiplier *= multiplier

    def set_minimum_denominator(self, denominator) -> None:
        r'''Sets preferred denominator of tuplet to at least `denominator`.

        ..  container:: example

            Sets preferred denominator of tuplet to ``8`` at least:

            >>> tuplet = abjad.Tuplet((3, 5), "c'4 d'8 e'8 f'4 g'2")
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(tuplet)
                \tweak text #tuplet-number::calc-fraction-text
                \times 3/5 {
                    c'4
                    d'8
                    e'8
                    f'4
                    g'2
                }

            >>> tuplet.set_minimum_denominator(8)
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(tuplet)
                \tweak text #tuplet-number::calc-fraction-text
                \times 6/10 {
                    c'4
                    d'8
                    e'8
                    f'4
                    g'2
                }

        '''
        assert mathtools.is_nonnegative_integer_power_of_two(denominator)
        self.force_fraction = True
        durations = [
            self._get_contents_duration(),
            self._get_preprolated_duration(),
            Duration(1, denominator),
            ]
        nonreduced_fractions = Duration.durations_to_nonreduced_fractions(
            durations)
        self.denominator = nonreduced_fractions[1].numerator

    def toggle_prolation(self) -> None:
        r'''Changes augmented tuplets to diminished;
        changes diminished tuplets to augmented.

        ..  container:: example

            Changes augmented tuplet to diminished:

            >>> tuplet = abjad.Tuplet((4, 3), "c'8 d'8 e'8")
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(tuplet)
                \tweak text #tuplet-number::calc-fraction-text
                \times 4/3 {
                    c'8
                    d'8
                    e'8
                }

            >>> tuplet.toggle_prolation()
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(tuplet)
                \times 2/3 {
                    c'4
                    d'4
                    e'4
                }

            Multiplies the written duration of the leaves in tuplet
            by the least power of ``2`` necessary to diminshed tuplet.

        ..  container:: example

            Changes diminished tuplet to augmented:

            >>> tuplet = abjad.Tuplet((2, 3), "c'4 d'4 e'4")
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(tuplet)
                \times 2/3 {
                    c'4
                    d'4
                    e'4
                }

            >>> tuplet.toggle_prolation()
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(tuplet)
                \tweak text #tuplet-number::calc-fraction-text
                \times 4/3 {
                    c'8
                    d'8
                    e'8
                }

            Divides the written duration of the leaves in tuplet
            by the least power of ``2`` necessary to diminshed tuplet.

        Does not yet work with nested tuplets.
        '''
        import abjad
        if self.diminution():
            while self.diminution():
                self.multiplier *= 2
                for leaf in iterate(self).leaves():
                    leaf.written_duration /= 2
        elif not self.diminution():
            while not self.diminution():
                self.multiplier /= 2
                for leaf in iterate(self).leaves():
                    leaf.written_duration *= 2

    def trivial(self) -> bool:
        r'''Is true when tuplet multiplier is equal to ``1`` and no multipliers
        attach to any leaves in tuplet.

        ..  container:: example

            >>> tuplet = abjad.Tuplet((1, 1), "c'8 d'8 e'8")
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(tuplet)
                \tweak text #tuplet-number::calc-fraction-text
                \times 1/1 {
                    c'8
                    d'8
                    e'8
                }

            >>> tuplet.trivial()
            True

        ..  container:: example

            Tuplet is not trivial when multipliers attach to tuplet leaves:

            >>> tuplet = abjad.Tuplet((1, 1), "c'8 d'8 e'8")
            >>> abjad.attach(abjad.Multiplier(3, 2), tuplet[0])
            >>> abjad.attach(abjad.Multiplier(1, 2), tuplet[-1])
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(tuplet)
                \tweak text #tuplet-number::calc-fraction-text
                \times 1/1 {
                    c'8 * 3/2
                    d'8
                    e'8 * 1/2
                }

            >>> tuplet.trivial()
            False

        '''
        for leaf in iterate(self).leaves():
            if inspect(leaf).has_indicator(Multiplier):
                return False
        return self.multiplier == 1

    def trivializable(self) -> bool:
        r'''Is true when tuplet is trivializable (can be rewritten with a ratio
        of 1:1). Otherwise false.

        ..  container:: example

            Redudant tuplet:

            >>> tuplet = abjad.Tuplet((3, 4), "c'4 c'4")
            >>> measure = abjad.Measure((3, 8), [tuplet])
            >>> abjad.show(measure) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(measure)
                {   % measure
                    \time 3/8
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 3/4 {
                        c'4
                        c'4
                    }
                }   % measure

            >>> tuplet.trivializable()
            True

            Can be rewritten without a tuplet bracket:

                >>> measure = abjad.Measure((3, 8), "c'8. c'8.")
                >>> abjad.show(measure) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(measure)
                {   % measure
                    \time 3/8
                    c'8.
                    c'8.
                }   % measure

        ..  container:: example

            Nontrivializable tuplet:

            >>> tuplet = abjad.Tuplet((3, 5), "c'4 c'4 c'4 c'4 c'4")
            >>> measure = abjad.Measure((3, 4), [tuplet])
            >>> abjad.show(measure) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(measure)
                {   % measure
                    \time 3/4
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 3/5 {
                        c'4
                        c'4
                        c'4
                        c'4
                        c'4
                    }
                }   % measure

            >>> tuplet.trivializable()
            False

            Can not be rewritten without a tuplet bracket.

        ..  container:: example

            REGRESSION. Nontrivializable tuplet:

            >>> tuplet = abjad.Tuplet((3, 4), "c'2. c4")
            >>> measure = abjad.Measure((3, 4), [tuplet])
            >>> abjad.show(measure) # doctest: +SKIP

            ..  docs::

                        >>> abjad.f(measure)
                        {   % measure
                            \time 3/4
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 3/4 {
                                c'2.
                                c4
                            }
                        }   % measure

            >>> tuplet.trivializable()
            False

        '''
        for component in self:
            if isinstance(component, Tuplet):
                continue
            assert isinstance(component, Leaf), repr(component)
            duration = component.written_duration * self.multiplier
            if not duration.is_assignable:
                return False
        return True

    def trivialize(self) -> None:
        r'''Trivializes tuplet.

        ..  container:: example

            >>> tuplet = abjad.Tuplet((3, 4), "c'2")
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(tuplet)
                \tweak text #tuplet-number::calc-fraction-text
                \times 3/4 {
                    c'2
                }

            >>> tuplet.trivializable()
            True

            >>> tuplet.trivialize()
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(tuplet)
                \tweak text #tuplet-number::calc-fraction-text
                \times 1/1 {
                    c'4.
                }

        '''
        import abjad
        if not self.trivializable():
            return
        for component in self:
            if isinstance(component, Tuplet):
                component.multiplier *= self.multiplier
            elif isinstance(component, Leaf):
                component.written_duration *= self.multiplier
            else:
                raise TypeError(component)
        self.multiplier = Multiplier(1)
