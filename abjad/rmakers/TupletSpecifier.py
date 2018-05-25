import copy
import typing
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject
from abjad.tools.datastructuretools.Duration import Duration
from abjad.tools.datastructuretools.Multiplier import Multiplier
from abjad.tools.mathtools.NonreducedFraction import NonreducedFraction
from abjad.tools.scoretools.Selection import Selection


class TupletSpecifier(AbjadValueObject):
    """
    Tuplet specifier.

    ..  container:: example

        >>> specifier = abjad.rmakers.TupletSpecifier()
        >>> abjad.f(specifier)
        abjad.rmakers.TupletSpecifier(
            diminution=True,
            )

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Specifiers'

    __slots__ = (
        '_avoid_dots',
        '_denominator',
        '_diminution',
        '_extract_trivial',
        '_force_fraction',
        '_rewrite_rest_filled',
        '_trivialize',
        '_use_note_duration_bracket',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        avoid_dots: bool = None,
        denominator: typing.Union[str, Duration, int] = None,
        diminution: bool = True,
        extract_trivial: bool = None,
        force_fraction: bool = None,
        rewrite_rest_filled: bool = None,
        trivialize: bool = None,
        use_note_duration_bracket: bool = None,
        ) -> None:
        import abjad
        if avoid_dots is not None:
            avoid_dots = bool(avoid_dots)
        self._avoid_dots = avoid_dots
        if isinstance(denominator, tuple):
            denominator = Duration(denominator)
        self._denominator = denominator
        # TODO: Consider renaming diminution=True to augmentation=None.
        #       That would allow for all keywords to default to None,
        #       and therefore a single-line storage format.
        if diminution is not None:
            diminution = bool(diminution)
        self._diminution = diminution
        if extract_trivial is not None:
            extract_trivial = bool(extract_trivial)
        self._extract_trivial = extract_trivial
        if force_fraction is not None:
            force_fraction = bool(force_fraction)
        self._force_fraction = force_fraction
        if rewrite_rest_filled is not None:
            rewrite_rest_fille = bool(rewrite_rest_filled)
        self._rewrite_rest_filled = rewrite_rest_filled
        if trivialize is not None:
            trivialize = bool(trivialize)
        self._trivialize = trivialize
        if use_note_duration_bracket is not None:
            use_note_duration_bracket = bool(use_note_duration_bracket)
        self._use_note_duration_bracket = use_note_duration_bracket

    ### SPECIAL METHODS ###

    def __call__(
        self,
        selections: typing.List[Selection],
        divisions: typing.List[NonreducedFraction],
        ) -> typing.List[Selection]:
        """
        Calls tuplet specifier.
        """
        import abjad
        self._apply_denominator(selections, divisions)
        self._force_fraction_(selections)
        self._trivialize_(selections)
        selections = self._rewrite_rest_filled_(selections)
        # extract trivial must follow the other operations:
        selections = self._extract_trivial_(selections)
        return selections

    ### PRIVATE METHODS ###

    def _apply_denominator(self, selections, divisions):
        import abjad
        if not self.denominator:
            return
        tuplets = list(abjad.iterate(selections).components(abjad.Tuplet))
        if divisions is None:
            divisions = len(tuplets) * [None]
        assert len(selections) == len(divisions)
        assert len(tuplets) == len(divisions)
        denominator = self.denominator
        if isinstance(denominator, tuple):
            denominator = abjad.Duration(denominator)
        for tuplet, division in zip(tuplets, divisions):
            if denominator == 'divisions':
                tuplet.denominator = division.numerator
            elif isinstance(denominator, abjad.Duration):
                unit_duration = denominator
                assert unit_duration.numerator == 1
                duration = abjad.inspect(tuplet).get_duration()
                denominator_ = unit_duration.denominator
                nonreduced_fraction = duration.with_denominator(denominator_)
                tuplet.denominator = nonreduced_fraction.numerator
            elif abjad.mathtools.is_positive_integer(denominator):
                tuplet.denominator = denominator
            else:
                message = f'invalid preferred denominator: {denominator!r}.'
                raise Exception(message)

    def _extract_trivial_(self, selections):
        import abjad
        if not self.extract_trivial:
            return selections
        selections_ = []
        for selection in selections:
            selection_ = []
            for component in selection:
                if not (isinstance(component, abjad.Tuplet) and
                    component.trivial()):
                    selection_.append(component)
                    continue
                tuplet = component
                contents = abjad.mutate(tuplet).eject_contents()
                assert isinstance(contents, abjad.Selection)
                selection_.extend(contents)
            selection_ = abjad.select(selection_)
            selections_.append(selection_)
        return selections_

    def _force_fraction_(self, selections):
        import abjad
        if not self.force_fraction:
            return
        for tuplet in abjad.iterate(selections).components(abjad.Tuplet):
            tuplet.force_fraction = True

    def _rewrite_rest_filled_(self, selections):
        import abjad
        if not self.rewrite_rest_filled:
            return selections
        selections_ = []
        maker = abjad.LeafMaker()
        for selection in selections:
            selection_ = []
            for component in selection:
                if not (isinstance(component, abjad.Tuplet) and
                    component._rest_filled()):
                    selection_.append(component)
                    continue
                duration = abjad.inspect(component).get_duration()
                rests = maker([None], [duration])
                abjad.mutate(component[:]).replace(rests)
                component.multiplier = abjad.Multiplier(1)
                selection_.append(component)
            selection_ = abjad.select(selection_)
            selections_.append(selection_)
        return selections_

    def _trivialize_(self, selections):
        import abjad
        if not self.trivialize:
            return
        for tuplet in abjad.iterate(selections).components(abjad.Tuplet):
            tuplet.trivialize()

    ### PUBLIC PROPERTIES ###

    @property
    def avoid_dots(self) -> typing.Optional[bool]:
        """
        Is true when tuplet should avoid dotted rhythmic values.
        """
        return self._avoid_dots

    @property
    def denominator(self) -> typing.Optional[typing.Union[str, Duration, int]]:
        r"""
        Gets preferred denominator.

        ..  container:: example

            Tuplet numerators and denominators are reduced to numbers that are
            relatively prime when ``denominator`` is set to none. This
            means that ratios like ``6:4`` and ``10:8`` do not arise:

            >>> rhythm_maker = abjad.rmakers.TupletRhythmMaker(
            ...     tuplet_ratios=[(1, 4)],
            ...     tuplet_specifier=abjad.rmakers.TupletSpecifier(
            ...         avoid_dots=True,
            ...         denominator=None,
            ...         ),
            ...     )

            >>> divisions = [(2, 16), (4, 16), (6, 16), (8, 16)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff
                {
                    {   % measure
                        \time 2/16
                        \times 4/5 {
                            c'32
                            [
                            c'8
                            ]
                        }
                    }   % measure
                    {   % measure
                        \time 4/16
                        \times 4/5 {
                            c'16
                            c'4
                        }
                    }   % measure
                    {   % measure
                        \time 6/16
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 3/5 {
                            c'8
                            c'2
                        }
                    }   % measure
                    {   % measure
                        \time 8/16
                        \times 4/5 {
                            c'8
                            c'2
                        }
                    }   % measure
                }

        ..  container:: example

            The preferred denominator of each tuplet is set to the numerator of
            the division that generates the tuplet when ``denominator``
            is set to the string ``'divisions'``. This means that the tuplet
            numerator and denominator are not necessarily relatively prime.
            This also means that ratios like ``6:4`` and ``10:8`` may arise:

            >>> rhythm_maker = abjad.rmakers.TupletRhythmMaker(
            ...     tuplet_ratios=[(1, 4)],
            ...     tuplet_specifier=abjad.rmakers.TupletSpecifier(
            ...         avoid_dots=True,
            ...         denominator='divisions',
            ...         ),
            ...     )

            >>> divisions = [(2, 16), (4, 16), (6, 16), (8, 16)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff
                {
                    {   % measure
                        \time 2/16
                        \times 4/5 {
                            c'32
                            [
                            c'8
                            ]
                        }
                    }   % measure
                    {   % measure
                        \time 4/16
                        \times 4/5 {
                            c'16
                            c'4
                        }
                    }   % measure
                    {   % measure
                        \time 6/16
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 6/10 {
                            c'8
                            c'2
                        }
                    }   % measure
                    {   % measure
                        \time 8/16
                        \times 8/10 {
                            c'8
                            c'2
                        }
                    }   % measure
                }

        ..  container:: example

            The preferred denominator of each tuplet is set in terms of a unit
            duration when ``denominator`` is set to a duration. The
            setting does not affect the first tuplet:

            >>> rhythm_maker = abjad.rmakers.TupletRhythmMaker(
            ...     tuplet_ratios=[(1, 4)],
            ...     tuplet_specifier=abjad.rmakers.TupletSpecifier(
            ...         avoid_dots=True,
            ...         denominator=(1, 16),
            ...         ),
            ...     )

            >>> divisions = [(2, 16), (4, 16), (6, 16), (8, 16)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff
                {
                    {   % measure
                        \time 2/16
                        \times 4/5 {
                            c'32
                            [
                            c'8
                            ]
                        }
                    }   % measure
                    {   % measure
                        \time 4/16
                        \times 4/5 {
                            c'16
                            c'4
                        }
                    }   % measure
                    {   % measure
                        \time 6/16
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 6/10 {
                            c'8
                            c'2
                        }
                    }   % measure
                    {   % measure
                        \time 8/16
                        \times 8/10 {
                            c'8
                            c'2
                        }
                    }   % measure
                }

        ..  container:: example

            Sets the preferred denominator of each tuplet in terms 32nd notes.
            The setting affects all tuplets:

            >>> rhythm_maker = abjad.rmakers.TupletRhythmMaker(
            ...     tuplet_ratios=[(1, 4)],
            ...     tuplet_specifier=abjad.rmakers.TupletSpecifier(
            ...         avoid_dots=True,
            ...         denominator=(1, 32),
            ...         ),
            ...     )

            >>> divisions = [(2, 16), (4, 16), (6, 16), (8, 16)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff
                {
                    {   % measure
                        \time 2/16
                        \times 4/5 {
                            c'32
                            [
                            c'8
                            ]
                        }
                    }   % measure
                    {   % measure
                        \time 4/16
                        \times 8/10 {
                            c'16
                            c'4
                        }
                    }   % measure
                    {   % measure
                        \time 6/16
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 12/20 {
                            c'8
                            c'2
                        }
                    }   % measure
                    {   % measure
                        \time 8/16
                        \times 16/20 {
                            c'8
                            c'2
                        }
                    }   % measure
                }

        ..  container:: example

            Sets the preferred denominator each tuplet in terms 64th notes. The
            setting affects all tuplets:

            >>> rhythm_maker = abjad.rmakers.TupletRhythmMaker(
            ...     tuplet_ratios=[(1, 4)],
            ...     tuplet_specifier=abjad.rmakers.TupletSpecifier(
            ...         avoid_dots=True,
            ...         denominator=(1, 64),
            ...         ),
            ...     )

            >>> divisions = [(2, 16), (4, 16), (6, 16), (8, 16)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff
                {
                    {   % measure
                        \time 2/16
                        \times 8/10 {
                            c'32
                            [
                            c'8
                            ]
                        }
                    }   % measure
                    {   % measure
                        \time 4/16
                        \times 16/20 {
                            c'16
                            c'4
                        }
                    }   % measure
                    {   % measure
                        \time 6/16
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 24/40 {
                            c'8
                            c'2
                        }
                    }   % measure
                    {   % measure
                        \time 8/16
                        \times 32/40 {
                            c'8
                            c'2
                        }
                    }   % measure
                }

        ..  container:: example

            The preferred denominator of each tuplet is set directly when
            ``denominator`` is set to a positive integer. This example
            sets the preferred denominator of each tuplet to ``8``. Setting
            does not affect the third tuplet:

            >>> rhythm_maker = abjad.rmakers.TupletRhythmMaker(
            ...     tuplet_ratios=[(1, 4)],
            ...     tuplet_specifier=abjad.rmakers.TupletSpecifier(
            ...         avoid_dots=True,
            ...         denominator=8,
            ...         ),
            ...     )

            >>> divisions = [(2, 16), (4, 16), (6, 16), (8, 16)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff
                {
                    {   % measure
                        \time 2/16
                        \times 8/10 {
                            c'32
                            [
                            c'8
                            ]
                        }
                    }   % measure
                    {   % measure
                        \time 4/16
                        \times 8/10 {
                            c'16
                            c'4
                        }
                    }   % measure
                    {   % measure
                        \time 6/16
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 3/5 {
                            c'8
                            c'2
                        }
                    }   % measure
                    {   % measure
                        \time 8/16
                        \times 8/10 {
                            c'8
                            c'2
                        }
                    }   % measure
                }

        ..  container:: example

            Sets the preferred denominator of each tuplet to ``12``. Setting
            affects all tuplets:

            >>> rhythm_maker = abjad.rmakers.TupletRhythmMaker(
            ...     tuplet_ratios=[(1, 4)],
            ...     tuplet_specifier=abjad.rmakers.TupletSpecifier(
            ...         avoid_dots=True,
            ...         denominator=12,
            ...         ),
            ...     )

            >>> divisions = [(2, 16), (4, 16), (6, 16), (8, 16)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff
                {
                    {   % measure
                        \time 2/16
                        \times 12/15 {
                            c'32
                            [
                            c'8
                            ]
                        }
                    }   % measure
                    {   % measure
                        \time 4/16
                        \times 12/15 {
                            c'16
                            c'4
                        }
                    }   % measure
                    {   % measure
                        \time 6/16
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 12/20 {
                            c'8
                            c'2
                        }
                    }   % measure
                    {   % measure
                        \time 8/16
                        \times 12/15 {
                            c'8
                            c'2
                        }
                    }   % measure
                }

        ..  container:: example

            Sets the preferred denominator of each tuplet to ``13``. Setting
            does not affect any tuplet:

            >>> rhythm_maker = abjad.rmakers.TupletRhythmMaker(
            ...     tuplet_ratios=[(1, 4)],
            ...     tuplet_specifier=abjad.rmakers.TupletSpecifier(
            ...         avoid_dots=True,
            ...         denominator=13,
            ...         ),
            ...     )

            >>> divisions = [(2, 16), (4, 16), (6, 16), (8, 16)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff
                {
                    {   % measure
                        \time 2/16
                        \times 4/5 {
                            c'32
                            [
                            c'8
                            ]
                        }
                    }   % measure
                    {   % measure
                        \time 4/16
                        \times 4/5 {
                            c'16
                            c'4
                        }
                    }   % measure
                    {   % measure
                        \time 6/16
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 3/5 {
                            c'8
                            c'2
                        }
                    }   % measure
                    {   % measure
                        \time 8/16
                        \times 4/5 {
                            c'8
                            c'2
                        }
                    }   % measure
                }

        Set to ``'divisions'``, duration, positive integer or none.
        """
        return self._denominator

    @property
    def diminution(self) -> typing.Optional[bool]:
        """
        Is true when tuplet should be spelled as diminution.
        """
        return self._diminution

    @property
    def extract_trivial(self) -> typing.Optional[bool]:
        """
        Is true when rhythm-maker should extract trivial tuplets.
        """
        return self._extract_trivial

    @property
    def force_fraction(self) -> typing.Optional[bool]:
        r"""
        Is true when tuplet forces tuplet number fraction formatting.

        ..  container:: example

            The ``defaulti.ly`` stylesheet included in all Abjad API examples
            includes the following:
            
            ``\override TupletNumber.text = #tuplet-number::calc-fraction-text``

            This means that even simple tuplets format as explicit fractions:

            >>> rhythm_maker = abjad.rmakers.EvenDivisionRhythmMaker(
            ...     extra_counts_per_division=[1],
            ...     )

            >>> divisions = [(2, 8), (2, 8), (2, 8)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff
                {
                    {   % measure
                        \time 2/8
                        \times 2/3 {
                            c'8
                            [
                            c'8
                            c'8
                            ]
                        }
                    }   % measure
                    {   % measure
                        \times 2/3 {
                            c'8
                            [
                            c'8
                            c'8
                            ]
                        }
                    }   % measure
                    {   % measure
                        \times 2/3 {
                            c'8
                            [
                            c'8
                            c'8
                            ]
                        }
                    }   % measure
                }

            We can temporarily restore LilyPond's default tuplet numbering like
            this:

            >>> rhythm_maker = abjad.rmakers.EvenDivisionRhythmMaker(
            ...     extra_counts_per_division=[1],
            ...     )

            >>> divisions = [(2, 8), (2, 8), (2, 8)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> staff = lilypond_file[abjad.Staff]
            >>> string = 'tuplet-number::calc-denominator-text'
            >>> abjad.override(staff).tuplet_number.text = string
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff
                \with
                {
                    \override TupletNumber.text = #tuplet-number::calc-denominator-text
                }
                {
                    {   % measure
                        \time 2/8
                        \times 2/3 {
                            c'8
                            [
                            c'8
                            c'8
                            ]
                        }
                    }   % measure
                    {   % measure
                        \times 2/3 {
                            c'8
                            [
                            c'8
                            c'8
                            ]
                        }
                    }   % measure
                    {   % measure
                        \times 2/3 {
                            c'8
                            [
                            c'8
                            c'8
                            ]
                        }
                    }   % measure
                }

            Which then makes it possible to show that the force fraction
            property cancels LilyPond's default tuplet numbering once again:

            >>> rhythm_maker = abjad.rmakers.EvenDivisionRhythmMaker(
            ...     extra_counts_per_division=[1],
            ...     tuplet_specifier=abjad.rmakers.TupletSpecifier(
            ...         force_fraction=True,
            ...         ),
            ...     )

            >>> divisions = [(2, 8), (2, 8), (2, 8)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> staff = lilypond_file[abjad.Staff]
            >>> string = 'tuplet-number::calc-denominator-text'
            >>> abjad.override(staff).tuplet_number.text = string
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff
                \with
                {
                    \override TupletNumber.text = #tuplet-number::calc-denominator-text
                }
                {
                    {   % measure
                        \time 2/8
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 2/3 {
                            c'8
                            [
                            c'8
                            c'8
                            ]
                        }
                    }   % measure
                    {   % measure
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 2/3 {
                            c'8
                            [
                            c'8
                            c'8
                            ]
                        }
                    }   % measure
                    {   % measure
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 2/3 {
                            c'8
                            [
                            c'8
                            c'8
                            ]
                        }
                    }   % measure
                }

        """
        return self._force_fraction

    @property
    def rewrite_rest_filled(self) -> typing.Optional[bool]:
        """
        Is true when rhythm-maker rewrites rest-filled tuplets.
        """
        return self._rewrite_rest_filled

    @property
    def trivialize(self) -> typing.Optional[bool]:
        """
        Is true when trivializable tuplets should be trivialized.
        """
        return self._trivialize

    @property
    def use_note_duration_bracket(self) -> typing.Optional[bool]:
        """
        Is true when tuplet should override tuplet number text with note
        duration bracket giving tuplet duration.
        """
        return self._use_note_duration_bracket
