import math
from .Container import Container


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
                    g'4. (
                    a'16 )
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
                    g'4. (
                    \times 4/5 {
                        e''32 [
                        ef''32
                        d''32
                        cs''32
                        cqs''32 ]
                    }
                    a'16 )
                }
                d'8
                e'8
            }

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Containers'

    __slots__ = (
        '_force_fraction',
        '_force_times_command',
        '_is_invisible',
        '_multiplier',
        '_preferred_denominator',
        '_signifier',
        )

    _is_counttime_component = True

    ### INITIALIZER ###

    def __init__(self, multiplier=None, components=None):
        import abjad
        Container.__init__(self, components)
        multiplier = multiplier or abjad.Multiplier(2, 3)
        self.multiplier = multiplier
        self._force_fraction = False
        self._force_times_command = False
        self._is_invisible = False
        self._preferred_denominator = None
        self._signifier = '*'

    ### SPECIAL METHODS ###

    def __getnewargs__(self):
        '''Gets new arguments of tuplet.

        Returns tuple.
        '''
        return (self.multiplier,)

    ### PRIVATE PROPERTIES ###

    @property
    def _is_rest_filled(self):
        import abjad
        return all(isinstance(_, abjad.Rest) for _ in self)

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

    def _fix(self):
        import abjad
        # find tuplet multiplier
        integer_exponent = int(math.log(self.multiplier, 2))
        leaf_multiplier = abjad.Multiplier(2) ** integer_exponent
        # scale leaves in tuplet by power of two
        for component in self:
            if isinstance(component, abjad.Leaf):
                old_written_duration = component.written_duration
                new_written_duration = leaf_multiplier * old_written_duration
                component._set_duration(new_written_duration)
        # adjust tuplet multiplier
        if self.__class__ is Tuplet:
            numerator, denominator = leaf_multiplier.pair
            multiplier = abjad.Multiplier(denominator, numerator)
            self.multiplier *= multiplier

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
        if self.is_invisible:
            return ''
        if 'text' in vars(abjad.override(self).tuplet_number):
            return''
        if (self.is_augmentation or
            not self._get_power_of_two_denominator() or
            self.force_fraction
            ):
            return r"\tweak text #tuplet-number::calc-fraction-text"
        return ''

    def _format_open_brackets_slot(self, bundle):
        result = []
        if self.multiplier:
            if self.is_invisible:
                contributor = (self, 'is_invisible')
                scale_durations_command_string = \
                    self._get_scale_durations_command_string()
                contributions = [scale_durations_command_string]
                result.append([contributor, contributions])
            else:
                contributor = ('self_brackets', 'open')
                if self.force_times_command or self.multiplier != 1:
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
                else:
                    contributions = ['{']
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
        parentage = abjad.inspect(self).get_parentage()
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
        if self.preferred_denominator is not None:
            inverse_multiplier = abjad.Multiplier(
                self.multiplier.denominator, self.multiplier.numerator)
            nonreduced_fraction = abjad.NonreducedFraction(inverse_multiplier)
            nonreduced_fraction = nonreduced_fraction.with_denominator(
                self.preferred_denominator)
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

    def _scale(self, multiplier):
        import abjad
        multiplier = abjad.Multiplier(multiplier)
        for component in self[:]:
            if isinstance(component, abjad.Leaf):
                new_duration = multiplier * component.written_duration
                component._set_duration(new_duration)
        self._fix()

    def _simplify_redundant_tuplet(self):
        import abjad
        if not self.is_redundant:
            return
        leaves = []
        logical_ties = abjad.select(self).logical_ties()
        durations = [abjad.inspect(_).get_duration() for _ in logical_ties]
        for i, logical_tie in enumerate(logical_ties):
            duration = durations[i]
            if i == len(logical_ties) - 1:
                leaf = logical_tie[-1]
            else:
                leaf = logical_tie[0]
            leaf.written_duration = duration
            leaves.append(leaf)
        self[:] = leaves
        self.multiplier = abjad.Multiplier(1)

    ### PUBLIC PROPERTIES ###

    @property
    def force_fraction(self):
        r'''Gets and sets flag to force fraction formatting of tuplet.

        ..  container:: example

            Gets forced fraction formatting of tuplet:

            >>> tuplet = abjad.Tuplet((2, 3), "c'8 d'8 e'8")
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(tuplet)
                \times 2/3 {
                    c'8
                    d'8
                    e'8
                }


            >>> tuplet.force_fraction
            False

        ..  container:: example

            Sets forced fraction formatting of tuplet:

            >>> tuplet.force_fraction = True
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(tuplet)
                \tweak text #tuplet-number::calc-fraction-text
                \times 2/3 {
                    c'8
                    d'8
                    e'8
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
                \new Staff {
                    \override TupletNumber.text = \markup {
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
                        }
                    \times 2/3 {
                        c'8
                        d'8
                        e'8
                    }
                    \revert TupletNumber.text
                }

        Returns boolean or none.
        '''
        return self._force_fraction

    @force_fraction.setter
    def force_fraction(self, argument):
        if isinstance(argument, (bool)):
            self._force_fraction = argument
        else:
            message = 'must be true or false: {!r}.'
            message = message.format(argument)
            raise TypeError(message)

    @property
    def force_times_command(self):
        r'''Is true when trivial tuplets print LilyPond ``\times`` command.
        Otherwise false.

        ..  container:: example

            Trivial tuplets normally print as a LilyPond container enclosed in
            ``{`` and ``}`` but without the LilyPond ``\times`` command:

            >>> trivial_tuplet = abjad.Tuplet((1, 1), "c'4 d' e'")
            >>> trivial_tuplet.force_times_command
            False

            >>> abjad.f(trivial_tuplet)
            {
                c'4
                d'4
                e'4
            }

            >>> abjad.show(trivial_tuplet) # doctest: +SKIP

        ..  container:: example

            But it is possible to force a trivial tuplet to format the LilyPond
            ``\times`` command:

            >>> trivial_tuplet = abjad.Tuplet((1, 1), "c'4 d' e'")
            >>> trivial_tuplet.force_times_command = True

            >>> abjad.f(trivial_tuplet)
            \times 1/1 {
                c'4
                d'4
                e'4
            }


                >>> abjad.show(trivial_tuplet) # doctest: +SKIP

        ..  container:: example

            This makes it possible to override tuplet number text:

            >>> trivial_tuplet = abjad.Tuplet((1, 1), "c'4 d' e'")
            >>> trivial_tuplet.force_times_command = True
            >>> duration = abjad.inspect(trivial_tuplet).get_duration()
            >>> markup = duration.to_score_markup()
            >>> markup = markup.scale((0.75, 0.75))
            >>> abjad.override(trivial_tuplet).tuplet_number.text = markup
            >>> staff = abjad.Staff([trivial_tuplet])

            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff {
                    \override TupletNumber.text = \markup {
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
                                            c'2.
                                        }
                                    >>
                                    \layout {
                                        indent = #0
                                        ragged-right = ##t
                                    }
                                }
                        }
                    \times 1/1 {
                        c'4
                        d'4
                        e'4
                    }
                    \revert TupletNumber.text
                }

        Defaults to false.

        Set to true or false.

        Returns true or false.
        '''
        return self._force_times_command

    @force_times_command.setter
    def force_times_command(self, argument):
        if isinstance(argument, (bool, type(None))):
            self._force_times_command = argument
        else:
            message = 'must be true or false: {!r}.'
            message = message.format(argument)
            raise TypeError(message)

    @property
    def implied_prolation(self):
        r'''Gets implied prolation of tuplet.

        ..  container:: example

            >>> tuplet = abjad.Tuplet((2, 3), "c'8 d'8 e'8")
            >>> abjad.show(tuplet) # doctest: +SKIP

            >>> tuplet.implied_prolation
            Multiplier(2, 3)

        Defined equal to tuplet multiplier.

        Returns multiplier.
        '''
        return self.multiplier

    @property
    def is_augmentation(self):
        r'''Is true when tuplet multiplier is greater than ``1``.
        Otherwise false.

        ..  container:: example

            Augmented tuplet:

            >>> tuplet = abjad.Tuplet((4, 3), "c'8 d'8 e'8")
            >>> abjad.show(tuplet) # doctest: +SKIP

            >>> tuplet.is_augmentation
            True

        ..  container:: example

            Diminished tuplet:

            >>> tuplet = abjad.Tuplet((2, 3), "c'4 d'4 e'4")
            >>> abjad.show(tuplet) # doctest: +SKIP

            >>> tuplet.is_augmentation
            False

        ..  container:: example

            Trivial tuplet:

            >>> tuplet = abjad.Tuplet((1, 1), "c'8. d'8. e'8.")
            >>> abjad.show(tuplet) # doctest: +SKIP

            >>> tuplet.is_augmentation
            False

        Returns true or false.
        '''
        if self.multiplier:
            return 1 < self.multiplier
        else:
            return False

    @property
    def is_diminution(self):
        r'''Is true when tuplet multiplier is less than ``1``.
        Otherwise false.

        ..  container:: example

            Augmented tuplet:

            >>> tuplet = abjad.Tuplet((4, 3), "c'8 d'8 e'8")
            >>> abjad.show(tuplet) # doctest: +SKIP

            >>> tuplet.is_diminution
            False

        ..  container:: example

            Diminished tuplet:

            >>> tuplet = abjad.Tuplet((2, 3), "c'4 d'4 e'4")
            >>> abjad.show(tuplet) # doctest: +SKIP

            >>> tuplet.is_diminution
            True

        ..  container:: example

            Trivial tuplet:

            >>> tuplet = abjad.Tuplet((1, 1), "c'8. d'8. e'8.")
            >>> abjad.show(tuplet) # doctest: +SKIP

            >>> tuplet.is_diminution
            False

        Returns true or false.
        '''
        if self.multiplier:
            return self.multiplier < 1
        else:
            return False

    @property
    def is_invisible(self):
        r'''Gets and sets invisibility status of tuplet.

        ..  container:: example

            Gets tuplet invisibility flag:

            >>> tuplet = abjad.Tuplet((2, 3), "c'8 d'8 e'8")
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(tuplet)
                \times 2/3 {
                    c'8
                    d'8
                    e'8
                }

            >>> tuplet.is_invisible
            False

        ..  container:: example

            Sets tuplet invisibility flag:

            >>> tuplet_1 = abjad.Tuplet((2, 3), "c'4 d'4 e'4")
            >>> tuplet_2 = abjad.Tuplet((2, 3), "d'4 e'4 f'4")
            >>> staff = abjad.Staff([tuplet_1, tuplet_2])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff {
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

            >>> staff[0].is_invisible = True
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff {
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

        Preserves tuplet duration when true.

        Returns boolean or none.
        '''
        return self._is_invisible

    @is_invisible.setter
    def is_invisible(self, argument):
        assert isinstance(argument, bool), repr(argument)
        self._is_invisible = argument

    @property
    def is_redundant(self):
        r'''Is true when tuplet is redundant. Otherwise false.

        Two conditions must be true for Abjad to identify a tuplet as
        redundant. First, the tuplet must contain only leaves (not other
        tuplets). Second, the durations of all leaves contained in the tuplet
        must be able to be rewritten without a tuplet bracket.

        ..  container:: example

            Redudant tuplet:

            >>> tuplet = abjad.Tuplet((3, 4), "c'4 c'4")
            >>> measure = abjad.Measure((3, 8), [tuplet])
            >>> abjad.show(measure) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(measure)
                { % measure
                    \time 3/8
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 3/4 {
                        c'4
                        c'4
                    }
                } % measure

            >>> tuplet.is_redundant
            True

            Can be rewritten without a tuplet bracket:

                >>> measure = abjad.Measure((3, 8), "c'8. c'8.")
                >>> abjad.show(measure) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(measure)
                { % measure
                    \time 3/8
                    c'8.
                    c'8.
                } % measure

        ..  container:: example

            Nonredundant tuplet:

            >>> tuplet = abjad.Tuplet((3, 5), "c'4 c'4 c'4 c'4 c'4")
            >>> measure = abjad.Measure((3, 4), [tuplet])
            >>> abjad.show(measure) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(measure)
                { % measure
                    \time 3/4
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 3/5 {
                        c'4
                        c'4
                        c'4
                        c'4
                        c'4
                    }
                } % measure

            >>> tuplet.is_redundant
            False

            Can not be rewritten without a tuplet bracket.

        Returns true or false.
        '''
        import abjad
        descendants = abjad.inspect(self).get_descendants()
        leaves = list(abjad.iterate(self).leaves())
        for logical_tie in abjad.iterate(leaves).logical_ties():
            leaves = [_ for _ in logical_tie if _ in descendants]
            if not abjad.inspect(leaves).get_duration().is_assignable:
                return False
        return True

    @property
    def is_trivial(self):
        r'''Is true when tuplet multiplier is equal to ``1``.
        Otherwise false:

        ..  container:: example

            >>> tuplet = abjad.Tuplet((1, 1), "c'8 d'8 e'8")

            >>> abjad.show(tuplet) # doctest: +SKIP

            >>> tuplet.is_trivial
            True

        Returns true or false.
        '''
        return self.multiplier == 1

    @property
    def multiplied_duration(self):
        r'''Multiplied duration of tuplet.

        ..  container:: example

            >>> tuplet = abjad.Tuplet((2, 3), "c'8 d'8 e'8")

            >>> abjad.show(tuplet) # doctest: +SKIP

            >>> tuplet.multiplied_duration
            Duration(1, 4)

        Returns duration.
        '''
        return self.multiplier * self._get_contents_duration()

    @property
    def multiplier(self):
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

        Returns multiplier.
        '''
        return self._multiplier

    @multiplier.setter
    def multiplier(self, argument):
        import abjad
        if isinstance(argument, (int, abjad.Fraction)):
            rational = abjad.Multiplier(argument)
        elif isinstance(argument, tuple):
            rational = abjad.Multiplier(argument)
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

    @property
    def preferred_denominator(self):
        r'''Gets and sets preferred denominator of tuplet.

        ..  container:: example

            Gets preferred denominator of tuplet:

            >>> tuplet = abjad.Tuplet((2, 3), "c'8 d'8 e'8")
            >>> tuplet.preferred_denominator is None
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

            >>> tuplet.preferred_denominator = 4
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(tuplet)
                \times 4/6 {
                    c'8
                    d'8
                    e'8
                }

        Returns positive integer or none.
        '''
        return self._preferred_denominator

    @preferred_denominator.setter
    def preferred_denominator(self, argument):
        if isinstance(argument, int):
            if not 0 < argument:
                raise ValueError(argument)
        elif not isinstance(argument, type(None)):
            raise TypeError(argument)
        self._preferred_denominator = argument

    ### PUBLIC METHODS ###

    def append(self, component, preserve_duration=False):
        r'''Appends `component` to tuplet.

        ..  container:: example

            Appends note to tuplet:

            >>> tuplet = abjad.Tuplet((2, 3), "c'4 ( d'4 f'4 )")
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(tuplet)
                \times 2/3 {
                    c'4 (
                    d'4
                    f'4 )
                }

            >>> tuplet.append(abjad.Note("e'4"))
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(tuplet)
                \tweak edge-height #'(0.7 . 0)
                \times 2/3 {
                    c'4 (
                    d'4
                    f'4 )
                    e'4
                }

        ..  container:: example

            Appends note to tuplet and preserves tuplet duration:

            >>> tuplet = abjad.Tuplet((2, 3), "c'4 ( d'4 f'4 )")
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(tuplet)
                \times 2/3 {
                    c'4 (
                    d'4
                    f'4 )
                }

            >>> tuplet.append(abjad.Note("e'4"), preserve_duration=True)
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(tuplet)
                \times 1/2 {
                    c'4 (
                    d'4
                    f'4 )
                    e'4
                }

        Returns none.
        '''
        import abjad
        if preserve_duration:
            old_duration = abjad.inspect(self).get_duration()
        superclass = super(Tuplet, self)
        superclass.append(component)
        if preserve_duration:
            new_duration = self._get_contents_duration()
            multiplier = old_duration / new_duration
            self.multiplier = multiplier
            assert abjad.inspect(self).get_duration() == old_duration

    def extend(self, argument, preserve_duration=False):
        r'''Extends tuplet with `argument`.

        ..  container:: example

            Extends tuplet with three notes:

            >>> tuplet = abjad.Tuplet((2, 3), "c'4 ( d'4 f'4 )")
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(tuplet)
                \times 2/3 {
                    c'4 (
                    d'4
                    f'4 )
                }

            >>> notes = [abjad.Note("e'32"), abjad.Note("d'32"), abjad.Note("e'16")]
            >>> tuplet.extend(notes)
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(tuplet)
                \tweak edge-height #'(0.7 . 0)
                \times 2/3 {
                    c'4 (
                    d'4
                    f'4 )
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
                    c'4 (
                    d'4
                    f'4 )
                }

            >>> notes = [abjad.Note("e'32"), abjad.Note("d'32"), abjad.Note("e'16")]
            >>> tuplet.extend(notes, preserve_duration=True)
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(tuplet)
                \times 4/7 {
                    c'4 (
                    d'4
                    f'4 )
                    e'32
                    d'32
                    e'16
                }

        Returns none.
        '''
        import abjad
        if preserve_duration:
            old_duration = abjad.inspect(self).get_duration()
        superclass = super(Tuplet, self)
        superclass.extend(argument)
        if preserve_duration:
            new_duration = self._get_contents_duration()
            multiplier = old_duration / new_duration
            self.multiplier = multiplier
            assert abjad.inspect(self).get_duration() == old_duration

    @staticmethod
    def from_duration(duration, components):
        r'''Makes tuplet from `duration` and `components`.

        ..  container:: example

            Makes tuplet equal to two eighths of a whole note:

            >>> tuplet = abjad.Tuplet.from_duration((2, 8), "c'8 d' e'")
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(tuplet)
                \times 2/3 {
                    c'8
                    d'8
                    e'8
                }

        Returns newly constructed tuplet equal in duration to `duration`.
        '''
        import abjad
        if not len(components):
            message = 'components must be nonempty: {!r}.'
            message = message.format(components)
            raise Exception(message)
        target_duration = abjad.Duration(duration)
        tuplet = Tuplet(1, components)
        contents_duration = abjad.inspect(tuplet).get_duration()
        multiplier = target_duration / contents_duration
        tuplet.multiplier = multiplier
        return tuplet

    @staticmethod
    def from_duration_and_ratio(
        duration,
        ratio,
        avoid_dots=True,
        decrease_monotonic=True,
        is_diminution=True,
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
            ...     is_diminution=False,
            ...     )
            >>> staff = abjad.Staff(
            ...     [abjad.Measure((3, 16), [tuplet])],
            ...     context_name='RhythmicStaff',
            ...     )
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff[0])
                { % measure
                    \time 3/16
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 6/5 {
                        c'32
                        c'32
                        c'32
                        r32
                        r32
                    }
                } % measure

            Allows tupletted leaves to return with dots when some `ratio`
            do not equal ``1``:

            >>> tuplet = abjad.Tuplet.from_duration_and_ratio(
            ...     abjad.Duration(3, 16),
            ...     abjad.Ratio((1, -2, -2, 3, 3)),
            ...     avoid_dots=True,
            ...     is_diminution=False,
            ...     )
            >>> staff = abjad.Staff(
            ...     [abjad.Measure((3, 16), [tuplet])],
            ...     context_name='RhythmicStaff',
            ...     )
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff[0])
                { % measure
                    \time 3/16
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 12/11 {
                        c'64
                        r32
                        r32
                        c'32.
                        c'32.
                    }
                } % measure

            Interprets nonassignable `ratio` according to `decrease_monotonic`:

            >>> tuplet = abjad.Tuplet.from_duration_and_ratio(
            ...     abjad.Duration(3, 16),
            ...     abjad.Ratio((5, -1, 5)),
            ...     avoid_dots=True,
            ...     decrease_monotonic=False,
            ...     is_diminution=False,
            ...     )
            >>> staff = abjad.Staff(
            ...     [abjad.Measure((3, 16), [tuplet])],
            ...     context_name='RhythmicStaff',
            ...     )
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff[0])
                { % measure
                    \time 3/16
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 12/11 {
                        c'64 ~
                        c'16
                        r64
                        c'64 ~
                        c'16
                    }
                } % measure

        ..  container:: example

            Makes augmented tuplet from `duration` and `ratio` and encourages
            dots:

            >>> tuplet = abjad.Tuplet.from_duration_and_ratio(
            ...     abjad.Duration(3, 16),
            ...     abjad.Ratio((1, 1, 1, -1, -1)),
            ...     avoid_dots=False,
            ...     is_diminution=False,
            ...     )
            >>> staff = abjad.Staff(
            ...     [abjad.Measure((3, 16), [tuplet])],
            ...     context_name='RhythmicStaff',
            ...     )
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff[0])
                { % measure
                    \time 3/16
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 8/5 {
                        c'64.
                        c'64.
                        c'64.
                        r64.
                        r64.
                    }
                } % measure

            Interprets nonassignable `ratio` according to `decrease_monotonic`:

            >>> tuplet = abjad.Tuplet.from_duration_and_ratio(
            ...     abjad.Duration(3, 16),
            ...     abjad.Ratio((5, -1, 5)),
            ...     avoid_dots=False,
            ...     decrease_monotonic=False,
            ...     is_diminution=False,
            ...     )
            >>> staff = abjad.Staff(
            ...     [abjad.Measure((3, 16), [tuplet])],
            ...     context_name='RhythmicStaff',
            ...     )
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff[0])
                { % measure
                    \time 3/16
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 16/11 {
                        c'32...
                        r128.
                        c'32...
                    }
                } % measure

        ..  container:: example

            Makes diminished tuplet from `duration` and nonzero integer
            `ratio`.

            Makes tupletted leaves strictly without dots when all
            `ratio` equal ``1``:

            >>> tuplet = abjad.Tuplet.from_duration_and_ratio(
            ...     abjad.Duration(3, 16),
            ...     abjad.Ratio((1, 1, 1, -1, -1)),
            ...     avoid_dots=True,
            ...     is_diminution=True,
            ...     )
            >>> staff = abjad.Staff(
            ...     [abjad.Measure((3, 16), [tuplet])],
            ...     context_name='RhythmicStaff',
            ...     )
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff[0])
                { % measure
                    \time 3/16
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 3/5 {
                        c'16
                        c'16
                        c'16
                        r16
                        r16
                    }
                } % measure

            Allows tupletted leaves to return with dots when some `ratio`
            do not equal ``1``:

            >>> tuplet = abjad.Tuplet.from_duration_and_ratio(
            ...     abjad.Duration(3, 16),
            ...     abjad.Ratio((1, -2, -2, 3, 3)),
            ...     avoid_dots=True,
            ...     is_diminution=True,
            ...     )
            >>> staff = abjad.Staff(
            ...     [abjad.Measure((3, 16), [tuplet])],
            ...     context_name='RhythmicStaff',
            ...     )
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff[0])
                { % measure
                    \time 3/16
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 6/11 {
                        c'32
                        r16
                        r16
                        c'16.
                        c'16.
                    }
                } % measure

            Interprets nonassignable `ratio` according to `decrease_monotonic`:

            >>> tuplet = abjad.Tuplet.from_duration_and_ratio(
            ...     abjad.Duration(3, 16),
            ...     abjad.Ratio((5, -1, 5)),
            ...     avoid_dots=True,
            ...     decrease_monotonic=False,
            ...     is_diminution=True,
            ...     )
            >>> staff = abjad.Staff(
            ...     [abjad.Measure((3, 16), [tuplet])],
            ...     context_name='RhythmicStaff',
            ...     )
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff[0])
                { % measure
                    \time 3/16
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 6/11 {
                        c'32 ~
                        c'8
                        r32
                        c'32 ~
                        c'8
                    }
                } % measure

        ..  container:: example

            Makes diminished tuplet from `duration` and `ratio` and encourages
            dots:

            >>> tuplet = abjad.Tuplet.from_duration_and_ratio(
            ...     abjad.Duration(3, 16),
            ...     abjad.Ratio((1, 1, 1, -1, -1)),
            ...     avoid_dots=False,
            ...     is_diminution=True,
            ...     )
            >>> staff = abjad.Staff(
            ...     [abjad.Measure((3, 16), [tuplet])],
            ...     context_name = 'RhythmicStaff',
            ...     )
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff[0])
                { % measure
                    \time 3/16
                    \times 4/5 {
                        c'32.
                        c'32.
                        c'32.
                        r32.
                        r32.
                    }
                } % measure

            Interprets nonassignable `ratio` according to `direction`:

            >>> tuplet = abjad.Tuplet.from_duration_and_ratio(
            ...     abjad.Duration(3, 16),
            ...     abjad.Ratio((5, -1, 5)),
            ...     avoid_dots=False,
            ...     decrease_monotonic=False,
            ...     is_diminution=True,
            ...     )
            >>> staff = abjad.Staff(
            ...     [abjad.Measure((3, 16), [tuplet])],
            ...     context_name='RhythmicStaff',
            ...     )
            >>> abjad.show(measure) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff[0])
                { % measure
                    \time 3/16
                    \times 8/11 {
                        c'16...
                        r64.
                        c'16...
                    }
                } % measure

        Reduces `ratio` relative to each other.

        Interprets negative `ratio` as rests.

        Returns tuplet.
        '''
        import abjad
        # coerce duration and ratio
        duration = abjad.Duration(duration)
        ratio = abjad.Ratio(ratio)
        # find basic duration of note in tuplet
        basic_prolated_duration = duration / abjad.mathtools.weight(
            ratio.numbers)
        # find basic written duration of note in tuplet
        if avoid_dots:
            basic_written_duration = \
                basic_prolated_duration.equal_or_greater_power_of_two
        else:
            basic_written_duration = \
                basic_prolated_duration.equal_or_greater_assignable
        # find written duration of each note in tuplet
        written_durations = [x * basic_written_duration for x in ratio.numbers]
        leaf_maker = abjad.LeafMaker(decrease_monotonic=decrease_monotonic)
        # make tuplet leaves
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
        # make tuplet
        tuplet = abjad.Tuplet.from_duration(duration, notes)
        # fix tuplet contents if necessary
        tuplet._fix()
        # change prolation if necessary
        if not tuplet.multiplier == 1:
            if is_diminution:
                if not tuplet.is_diminution:
                    tuplet.toggle_prolation()
            else:
                if tuplet.is_diminution:
                    tuplet.toggle_prolation()
        # return tuplet
        return tuplet

    @staticmethod
    def from_leaf_and_ratio(leaf, ratio, is_diminution=True):
        r'''Makes tuplet from `leaf` and `ratio`.

        >>> note = abjad.Note("c'8.")

        ..  container:: example

            Changes leaf to augmented tuplets with `ratio`:

            >>> tuplet = abjad.Tuplet.from_leaf_and_ratio(
            ...     note,
            ...     abjad.Ratio((1,)),
            ...     is_diminution=False,
            ...     )
            >>> staff = abjad.Staff(
            ...     [abjad.Measure((3, 16), [tuplet])],
            ...     context_name='RhythmicStaff',
            ...     )
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(tuplet)
                {
                    c'8.
                }

        ..  container:: example

            Changes leaf to augmented tuplets with `ratio`:

            >>> tuplet = abjad.Tuplet.from_leaf_and_ratio(
            ...     note,
            ...     [1, 2],
            ...     is_diminution=False,
            ...     )
            >>> staff = abjad.Staff(
            ...     [abjad.Measure((3, 16), [tuplet])],
            ...     context_name='RhythmicStaff',
            ...     )
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(tuplet)
                {
                    c'16
                    c'8
                }

        ..  container:: example

            Changes leaf to augmented tuplets with `ratio`:

            >>> tuplet = abjad.Tuplet.from_leaf_and_ratio(
            ...     note,
            ...     abjad.Ratio((1, 2, 2)),
            ...     is_diminution=False,
            ...     )
            >>> staff = abjad.Staff(
            ...     [abjad.Measure((3, 16), [tuplet])],
            ...     context_name='RhythmicStaff',
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
            ...     is_diminution=False,
            ...     )
            >>> staff = abjad.Staff(
            ...     [abjad.Measure((3, 16), [tuplet])],
            ...     context_name='RhythmicStaff',
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
            ...     is_diminution=False,
            ...     )
            >>> staff = abjad.Staff(
            ...     [abjad.Measure((3, 16), [tuplet])],
            ...     context_name='RhythmicStaff',
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
            ...     is_diminution=False,
            ...     )
            >>> staff = abjad.Staff(
            ...     [abjad.Measure((3, 16), [tuplet])],
            ...     context_name='RhythmicStaff',
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
            ...     is_diminution=True,
            ...     )
            >>> staff = abjad.Staff(
            ...     [abjad.Measure((3, 16), [tuplet])],
            ...     context_name='RhythmicStaff',
            ...     )
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(tuplet)
                {
                    c'8.
                }

        ..  container:: example

            Changes leaf to diminished tuplets with `ratio`:

            >>> tuplet = abjad.Tuplet.from_leaf_and_ratio(
            ...     note,
            ...     [1, 2],
            ...     is_diminution=True,
            ...     )
            >>> staff = abjad.Staff(
            ...     [abjad.Measure((3, 16), [tuplet])],
            ...     context_name='RhythmicStaff',
            ...     )
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(tuplet)
                {
                    c'16
                    c'8
                }

        ..  container:: example

            Changes leaf to diminished tuplets with `ratio`:

            >>> tuplet = abjad.Tuplet.from_leaf_and_ratio(
            ...     note,
            ...     [1, 2, 2],
            ...     is_diminution=True,
            ...     )
            >>> staff = abjad.Staff(
            ...     [abjad.Measure((3, 16), [tuplet])],
            ...     context_name='RhythmicStaff',
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
            ...     is_diminution=True,
            ...     )
            >>> staff = abjad.Staff(
            ...     [abjad.Measure((3, 16), [tuplet])],
            ...     context_name='RhythmicStaff',
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
            ...     is_diminution=True,
            ...     )
            >>> staff = abjad.Staff(
            ...     [abjad.Measure((3, 16), [tuplet])],
            ...     context_name='RhythmicStaff',
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
            ...     is_diminution=True,
            ...     )
            >>> staff = abjad.Staff(
            ...     [abjad.Measure((3, 16), [tuplet])],
            ...     context_name='RhythmicStaff',
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
        tuplet = leaf._to_tuplet_with_ratio(
            ratio,
            is_diminution=is_diminution,
            )
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
            ...     context_name='RhythmicStaff',
            ...     )
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff[0])
                { % measure
                    \time 7/16
                    {
                        c'4..
                    }
                } % measure

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
            ...     context_name='RhythmicStaff',
            ...     )
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff[0])
                { % measure
                    \time 7/16
                    {
                        c'4..
                    }
                } % measure

        ..  container:: example

            Makes tuplet when prolation is necessary:

            >>> tuplet = abjad.Tuplet.from_ratio_and_pair(
            ...     abjad.NonreducedRatio((1, 2)),
            ...     abjad.NonreducedFraction(7, 16),
            ...     )
            >>> staff = abjad.Staff(
            ...     [abjad.Measure((7, 16), [tuplet])],
            ...     context_name='RhythmicStaff',
            ...     )
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff[0])
                { % measure
                    \time 7/16
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 7/6 {
                        c'8
                        c'4
                    }
                } % measure

            >>> tuplet = abjad.Tuplet.from_ratio_and_pair(
            ...     abjad.NonreducedRatio((1, 2, 4)),
            ...     abjad.NonreducedFraction(7, 16),
            ...     )
            >>> staff = abjad.Staff(
            ...     [abjad.Measure((7, 16), [tuplet])],
            ...     context_name='RhythmicStaff',
            ...     )
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff[0])
                { % measure
                    \time 7/16
                    {
                        c'16
                        c'8
                        c'4
                    }
                } % measure

            >>> tuplet = abjad.Tuplet.from_ratio_and_pair(
            ...     abjad.NonreducedRatio((1, 2, 4, 1)),
            ...     abjad.NonreducedFraction(7, 16),
            ...     )
            >>> staff = abjad.Staff(
            ...     [abjad.Measure((7, 16), [tuplet])],
            ...     context_name='RhythmicStaff',
            ...     )
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff[0])
                { % measure
                    \time 7/16
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 7/8 {
                        c'16
                        c'8
                        c'4
                        c'16
                    }
                } % measure

            >>> tuplet = abjad.Tuplet.from_ratio_and_pair(
            ...     abjad.NonreducedRatio((1, 2, 4, 1, 2)),
            ...     abjad.NonreducedFraction(7, 16),
            ...     )
            >>> staff = abjad.Staff(
            ...     [abjad.Measure((7, 16), [tuplet])],
            ...     context_name='RhythmicStaff',
            ...     )
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff[0])
                { % measure
                    \time 7/16
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 7/10 {
                        c'16
                        c'8
                        c'4
                        c'16
                        c'8
                    }
                } % measure

            >>> tuplet = abjad.Tuplet.from_ratio_and_pair(
            ...     abjad.NonreducedRatio((1, 2, 4, 1, 2, 4)),
            ...     abjad.NonreducedFraction(7, 16),
            ...     )
            >>> staff = abjad.Staff(
            ...     [abjad.Measure((7, 16), [tuplet])],
            ...     context_name='RhythmicStaff',
            ...     )
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff[0])
                { % measure
                    \time 7/16
                    \times 1/2 {
                        c'16
                        c'8
                        c'4
                        c'16
                        c'8
                        c'4
                    }
                } % measure

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
                        duration = abjad.inspect(note).get_duration()
                        tuplet = abjad.Tuplet.from_duration(duration, [note])
                        return tuplet
                    else:
                        return abjad.Container([note])
                except AssignabilityError:
                    maker = abjad.NoteMaker()
                    notes = maker(0, duration)
                    if allow_trivial:
                        duration = abjad.inspect(notes).get_duration()
                        return abjad.Tuplet.from_duration(duration, notes)
                    else:
                        return abjad.Container(notes)
            elif ratio.numbers[0] < 0:
                try:
                    rest = abjad.Rest(duration)
                    if allow_trivial:
                        duration = abjad.inspect(rest).get_duration()
                        return abjad.Tuplet.from_duration(duration, [rest])
                    else:
                        return abjad.Container([rest])
                except AssignabilityError:
                    maker = abjad.LeafMaker()
                    rests = maker([None], duration)
                    if allow_trivial:
                        duration = abjad.inspect(rests).get_duration()
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

    def set_minimum_denominator(self, denominator):
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

        Returns none.
        '''
        import abjad
        assert abjad.mathtools.is_nonnegative_integer_power_of_two(denominator)
        Duration = abjad.Duration
        self.force_fraction = True
        durations = [
            self._get_contents_duration(),
            self._get_preprolated_duration(),
            abjad.Duration(1, denominator),
            ]
        nonreduced_fractions = Duration.durations_to_nonreduced_fractions(
            durations)
        self.preferred_denominator = nonreduced_fractions[1].numerator

    def toggle_prolation(self):
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

        Returns none.
        '''
        import abjad
        if self.is_diminution:
            while self.is_diminution:
                self.multiplier *= 2
                for leaf in abjad.iterate(self).leaves():
                    leaf.written_duration /= 2
        elif not self.is_diminution:
            while not self.is_diminution:
                self.multiplier /= 2
                for leaf in abjad.iterate(self).leaves():
                    leaf.written_duration *= 2
