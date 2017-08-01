# -*- coding: utf-8 -*-
from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools.abctools import AbjadValueObject
from abjad.tools.topleveltools import inspect
from abjad.tools.topleveltools import iterate


class TupletSpellingSpecifier(AbjadValueObject):
    r'''Tuplet spelling specifier.

    ::

        >>> import abjad
        >>> from abjad.tools import rhythmmakertools

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Specifiers'

    __slots__ = (
        '_avoid_dots',
        '_rewrite_rest_filled_tuplets',
        '_flatten_trivial_tuplets',
        '_is_diminution',
        '_preferred_denominator',
        '_simplify_redundant_tuplets',
        '_use_note_duration_bracket',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        avoid_dots=False,
        flatten_trivial_tuplets=False,
        is_diminution=True,
        preferred_denominator=None,
        rewrite_rest_filled_tuplets=False,
        simplify_redundant_tuplets=False,
        use_note_duration_bracket=False,
        ):
        # TODO: Consider renaming is_diminution=True to is_augmentation=None.
        #       That would allow for all keywords to default to None,
        #       and therefore a single-line storage format.
        self._avoid_dots = bool(avoid_dots)
        self._flatten_trivial_tuplets = bool(flatten_trivial_tuplets)
        self._is_diminution = bool(is_diminution)
        if isinstance(preferred_denominator, tuple):
            preferred_denominator = durationtools.Duration(
                preferred_denominator
                )
        self._preferred_denominator = preferred_denominator
        self._rewrite_rest_filled_tuplets = bool(rewrite_rest_filled_tuplets)
        self._simplify_redundant_tuplets = bool(simplify_redundant_tuplets)
        self._use_note_duration_bracket = bool(use_note_duration_bracket)

    ### PRIVATE METHODS ###

    def _apply_preferred_denominator(self, selections, divisions):
        from abjad.tools import scoretools
        if not self.preferred_denominator:
            return
        tuplets = iterate(selections).by_class(scoretools.Tuplet)
        tuplets = list(tuplets)
        if divisions is None:
            divisions = len(tuplets) * [None]
        assert len(selections) == len(divisions)
        assert len(tuplets) == len(divisions)
        preferred_denominator = self.preferred_denominator
        if isinstance(preferred_denominator, tuple):
            preferred_denominator = durationtools.Duration(
                preferred_denominator,
                )
        for tuplet, division in zip(tuplets, divisions):
            if preferred_denominator == 'divisions':
                tuplet.preferred_denominator = division.numerator
            elif isinstance(preferred_denominator, durationtools.Duration):
                unit_duration = preferred_denominator
                assert unit_duration.numerator == 1
                duration = inspect(tuplet).get_duration()
                denominator = unit_duration.denominator
                nonreduced_fraction = duration.with_denominator(denominator)
                tuplet.preferred_denominator = nonreduced_fraction.numerator
            elif mathtools.is_positive_integer(preferred_denominator):
                tuplet.preferred_denominator = preferred_denominator
            else:
                message = 'invalid value for preferred denominator: {!r}.'
                message = message.format(preferred_denominator)
                raise Exception(message)

    def _do_simplify_redundant_tuplets(self, selections):
        from abjad.tools import scoretools
        if not self.simplify_redundant_tuplets:
            return
        for tuplet in iterate(selections).by_class(scoretools.Tuplet):
            tuplet._simplify_redundant_tuplet()

    ### PUBLIC PROPERTIES ###

    @property
    def avoid_dots(self):
        r'''Is true when tuplet spelling should avoid dotted rhythmic values.
        Otherwise false.

        Defaults to false.

        Set to true or false.

        Returns true or false.
        '''
        return self._avoid_dots

    @property
    def flatten_trivial_tuplets(self):
        r'''Is true when tuplet spelling should flatten trivial tuplets.
        Otherwise false.

        Defaults to false.

        Set to true or false.

        Returns true or false.
        '''
        return self._flatten_trivial_tuplets

    @property
    def is_diminution(self):
        r'''Is true when tuplet should be spelled as diminution. Otherwise
        false.

        Defaults to true.

        Set to true or false.

        Returns true or false.
        '''
        return self._is_diminution

    @property
    def preferred_denominator(self):
        r'''Gets preferred denominator.

        ..  container:: example

            Tuplet numerators and denominators are reduced to numbers that are
            relatively prime when `preferred_denominator` is set to none. This
            means that ratios like ``6:4`` and ``10:8`` do not arise:

            ::

                >>> rhythm_maker = rhythmmakertools.TupletRhythmMaker(
                ...     tuplet_ratios=[(1, 4)],
                ...     tuplet_spelling_specifier=rhythmmakertools.TupletSpellingSpecifier(
                ...         avoid_dots=True,
                ...         preferred_denominator=None,
                ...         ),
                ...     )

            ::

                >>> divisions = [(2, 16), (4, 16), (6, 16), (8, 16)]
                >>> selections = rhythm_maker(divisions)
                >>> lilypond_file = abjad.LilyPondFile.rhythm(
                ...     selections,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new RhythmicStaff {
                    {
                        \time 2/16
                        \times 4/5 {
                            c'32 [
                            c'8 ]
                        }
                    }
                    {
                        \time 4/16
                        \times 4/5 {
                            c'16
                            c'4
                        }
                    }
                    {
                        \time 6/16
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 3/5 {
                            c'8
                            c'2
                        }
                    }
                    {
                        \time 8/16
                        \times 4/5 {
                            c'8
                            c'2
                        }
                    }
                }

        ..  container:: example

            The preferred denominator of each tuplet is set to the numerator of
            the division that generates the tuplet when `preferred_denominator`
            is set to the string ``'divisions'``. This means that the tuplet
            numerator and denominator are not necessarily relatively prime.
            This also means that ratios like ``6:4`` and ``10:8`` may arise:

            ::

                >>> rhythm_maker = rhythmmakertools.TupletRhythmMaker(
                ...     tuplet_ratios=[(1, 4)],
                ...     tuplet_spelling_specifier=rhythmmakertools.TupletSpellingSpecifier(
                ...         avoid_dots=True,
                ...         preferred_denominator='divisions',
                ...         ),
                ...     )

            ::

                >>> divisions = [(2, 16), (4, 16), (6, 16), (8, 16)]
                >>> selections = rhythm_maker(divisions)
                >>> lilypond_file = abjad.LilyPondFile.rhythm(
                ...     selections,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new RhythmicStaff {
                    {
                        \time 2/16
                        \times 4/5 {
                            c'32 [
                            c'8 ]
                        }
                    }
                    {
                        \time 4/16
                        \times 4/5 {
                            c'16
                            c'4
                        }
                    }
                    {
                        \time 6/16
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 6/10 {
                            c'8
                            c'2
                        }
                    }
                    {
                        \time 8/16
                        \times 8/10 {
                            c'8
                            c'2
                        }
                    }
                }

        ..  container:: example

            The preferred denominator of each tuplet is set in terms of a unit
            duration when `preferred_denominator` is set to a duration. The
            setting does not affect the first tuplet:

            ::

                >>> rhythm_maker = rhythmmakertools.TupletRhythmMaker(
                ...     tuplet_ratios=[(1, 4)],
                ...     tuplet_spelling_specifier=rhythmmakertools.TupletSpellingSpecifier(
                ...         avoid_dots=True,
                ...         preferred_denominator=(1, 16),
                ...         ),
                ...     )

            ::

                >>> divisions = [(2, 16), (4, 16), (6, 16), (8, 16)]
                >>> selections = rhythm_maker(divisions)
                >>> lilypond_file = abjad.LilyPondFile.rhythm(
                ...     selections,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new RhythmicStaff {
                    {
                        \time 2/16
                        \times 4/5 {
                            c'32 [
                            c'8 ]
                        }
                    }
                    {
                        \time 4/16
                        \times 4/5 {
                            c'16
                            c'4
                        }
                    }
                    {
                        \time 6/16
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 6/10 {
                            c'8
                            c'2
                        }
                    }
                    {
                        \time 8/16
                        \times 8/10 {
                            c'8
                            c'2
                        }
                    }
                }

        ..  container:: example

            Sets the preferred denominator of each tuplet in terms 32nd notes.
            The setting affects all tuplets:

            ::

                >>> rhythm_maker = rhythmmakertools.TupletRhythmMaker(
                ...     tuplet_ratios=[(1, 4)],
                ...     tuplet_spelling_specifier=rhythmmakertools.TupletSpellingSpecifier(
                ...         avoid_dots=True,
                ...         preferred_denominator=(1, 32),
                ...         ),
                ...     )

            ::

                >>> divisions = [(2, 16), (4, 16), (6, 16), (8, 16)]
                >>> selections = rhythm_maker(divisions)
                >>> lilypond_file = abjad.LilyPondFile.rhythm(
                ...     selections,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new RhythmicStaff {
                    {
                        \time 2/16
                        \times 4/5 {
                            c'32 [
                            c'8 ]
                        }
                    }
                    {
                        \time 4/16
                        \times 8/10 {
                            c'16
                            c'4
                        }
                    }
                    {
                        \time 6/16
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 12/20 {
                            c'8
                            c'2
                        }
                    }
                    {
                        \time 8/16
                        \times 16/20 {
                            c'8
                            c'2
                        }
                    }
                }

        ..  container:: example

            Sets the preferred denominator each tuplet in terms 64th notes. The
            setting affects all tuplets:

            ::

                >>> rhythm_maker = rhythmmakertools.TupletRhythmMaker(
                ...     tuplet_ratios=[(1, 4)],
                ...     tuplet_spelling_specifier=rhythmmakertools.TupletSpellingSpecifier(
                ...         avoid_dots=True,
                ...         preferred_denominator=(1, 64),
                ...         ),
                ...     )

            ::

                >>> divisions = [(2, 16), (4, 16), (6, 16), (8, 16)]
                >>> selections = rhythm_maker(divisions)
                >>> lilypond_file = abjad.LilyPondFile.rhythm(
                ...     selections,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new RhythmicStaff {
                    {
                        \time 2/16
                        \times 8/10 {
                            c'32 [
                            c'8 ]
                        }
                    }
                    {
                        \time 4/16
                        \times 16/20 {
                            c'16
                            c'4
                        }
                    }
                    {
                        \time 6/16
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 24/40 {
                            c'8
                            c'2
                        }
                    }
                    {
                        \time 8/16
                        \times 32/40 {
                            c'8
                            c'2
                        }
                    }
                }

        ..  container:: example

            The preferred denominator of each tuplet is set directly when
            `preferred_denominator` is set to a positive integer. This example
            sets the preferred denominator of each tuplet to ``8``. Setting
            does not affect the third tuplet:

            ::

                >>> rhythm_maker = rhythmmakertools.TupletRhythmMaker(
                ...     tuplet_ratios=[(1, 4)],
                ...     tuplet_spelling_specifier=rhythmmakertools.TupletSpellingSpecifier(
                ...         avoid_dots=True,
                ...         preferred_denominator=8,
                ...         ),
                ...     )

            ::

                >>> divisions = [(2, 16), (4, 16), (6, 16), (8, 16)]
                >>> selections = rhythm_maker(divisions)
                >>> lilypond_file = abjad.LilyPondFile.rhythm(
                ...     selections,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new RhythmicStaff {
                    {
                        \time 2/16
                        \times 8/10 {
                            c'32 [
                            c'8 ]
                        }
                    }
                    {
                        \time 4/16
                        \times 8/10 {
                            c'16
                            c'4
                        }
                    }
                    {
                        \time 6/16
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 3/5 {
                            c'8
                            c'2
                        }
                    }
                    {
                        \time 8/16
                        \times 8/10 {
                            c'8
                            c'2
                        }
                    }
                }

        ..  container:: example

            Sets the preferred denominator of each tuplet to ``12``. Setting
            affects all tuplets:

            ::

                >>> rhythm_maker = rhythmmakertools.TupletRhythmMaker(
                ...     tuplet_ratios=[(1, 4)],
                ...     tuplet_spelling_specifier=rhythmmakertools.TupletSpellingSpecifier(
                ...         avoid_dots=True,
                ...         preferred_denominator=12,
                ...         ),
                ...     )

            ::

                >>> divisions = [(2, 16), (4, 16), (6, 16), (8, 16)]
                >>> selections = rhythm_maker(divisions)
                >>> lilypond_file = abjad.LilyPondFile.rhythm(
                ...     selections,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new RhythmicStaff {
                    {
                        \time 2/16
                        \times 12/15 {
                            c'32 [
                            c'8 ]
                        }
                    }
                    {
                        \time 4/16
                        \times 12/15 {
                            c'16
                            c'4
                        }
                    }
                    {
                        \time 6/16
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 12/20 {
                            c'8
                            c'2
                        }
                    }
                    {
                        \time 8/16
                        \times 12/15 {
                            c'8
                            c'2
                        }
                    }
                }

        ..  container:: example

            Sets the preferred denominator of each tuplet to ``13``. Setting
            does not affect any tuplet:

            ::

                >>> rhythm_maker = rhythmmakertools.TupletRhythmMaker(
                ...     tuplet_ratios=[(1, 4)],
                ...     tuplet_spelling_specifier=rhythmmakertools.TupletSpellingSpecifier(
                ...         avoid_dots=True,
                ...         preferred_denominator=13,
                ...         ),
                ...     )

            ::

                >>> divisions = [(2, 16), (4, 16), (6, 16), (8, 16)]
                >>> selections = rhythm_maker(divisions)
                >>> lilypond_file = abjad.LilyPondFile.rhythm(
                ...     selections,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new RhythmicStaff {
                    {
                        \time 2/16
                        \times 4/5 {
                            c'32 [
                            c'8 ]
                        }
                    }
                    {
                        \time 4/16
                        \times 4/5 {
                            c'16
                            c'4
                        }
                    }
                    {
                        \time 6/16
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 3/5 {
                            c'8
                            c'2
                        }
                    }
                    {
                        \time 8/16
                        \times 4/5 {
                            c'8
                            c'2
                        }
                    }
                }

        Defaults to none.

        Set to ``'divisions'``, duration, positive integer or none.

        Returns ``'divisions'``, duration, positive integer or none.
        '''
        return self._preferred_denominator

    @property
    def rewrite_rest_filled_tuplets(self):
        r'''Is true when tuplet spelling should flatten rest-filled tuplets.
        Otherwise false.

        Defaults to false.

        Set to true or false.

        Returns true or false.
        '''
        return self._rewrite_rest_filled_tuplets

    @property
    def simplify_redundant_tuplets(self):
        r'''Is true when tuplets should be simplified. Otherwise false.

        Defaults to false.

        Set to true or false

        Returns true or false.
        '''
        return self._simplify_redundant_tuplets

    @property
    def use_note_duration_bracket(self):
        r'''Is true when tuplet should override tuplet number text with note
        duration bracket giving tuplet duration. Otherwise false.

        Defaults to false.

        Set to true or false.

        Returns true or false.
        '''
        return self._use_note_duration_bracket
