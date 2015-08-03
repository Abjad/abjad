# -*- encoding: utf-8 -*-
import math
from abjad.tools import datastructuretools
from abjad.tools import durationtools
from abjad.tools import scoretools
from abjad.tools import selectiontools
from abjad.tools.rhythmmakertools.RhythmMaker import RhythmMaker
from abjad.tools.topleveltools import attach
from abjad.tools.topleveltools import detach
from abjad.tools.topleveltools import inspect_
from abjad.tools.topleveltools import override


class AccelerandoRhythmMaker(RhythmMaker):
    r'''Accelerando rhythm-maker.

    ..  container:: example

        **Example 1.** Makes accelerando for each input division:

        ::

            >>> maker = rhythmmakertools.AccelerandoRhythmMaker(
            ...     beam_specifier=rhythmmakertools.BeamSpecifier(
            ...         use_feather_beams=True,
            ...         ),
            ...     interpolation_specifiers=rhythmmakertools.InterpolationSpecifier(
            ...         start_duration=Duration(1, 8),
            ...         stop_duration=Duration(1, 20),
            ...         written_duration=Duration(1, 16),
            ...         ),
            ...     tuplet_spelling_specifier=rhythmmakertools.TupletSpellingSpecifier(
            ...         use_note_duration_bracket=True,
            ...         ),
            ...     )

        ::

            >>> divisions = [(5, 8), (3, 8), (5, 8), (3, 8)]
            >>> music = maker(divisions)
            >>> lilypond_file = rhythmmakertools.make_lilypond_file(
            ...     music,
            ...     divisions,
            ...     )
            >>> show(lilypond_file) # doctest: +SKIP

        ..  doctest::

            >>> staff = maker._get_rhythmic_staff(lilypond_file)
            >>> print(format(staff))
            \new RhythmicStaff {
                {
                    \time 5/8
                    \override TupletNumber #'text = \markup {
                        \scale
                            #'(0.75 . 0.75)
                            \score
                                {
                                    \new Score \with {
                                        \override SpacingSpanner #'spacing-increment = #0.5
                                        proportionalNotationDuration = ##f
                                    } <<
                                        \new RhythmicStaff \with {
                                            \remove Time_signature_engraver
                                            \remove Staff_symbol_engraver
                                            \override Stem #'direction = #up
                                            \override Stem #'length = #5
                                            \override TupletBracket #'bracket-visibility = ##t
                                            \override TupletBracket #'direction = #up
                                            \override TupletBracket #'padding = #1.25
                                            \override TupletBracket #'shorten-pair = #'(-1 . -1.5)
                                            \override TupletNumber #'text = #tuplet-number::calc-fraction-text
                                            tupletFullLength = ##t
                                        } {
                                            c'2 ~
                                            c'8
                                        }
                                    >>
                                    \layout {
                                        indent = #0
                                        ragged-right = ##t
                                    }
                                }
                        }
                    \times 1/1 {
                        \once \override Beam #'grow-direction = #right
                        c'16 * 61/32 [
                        c'16 * 115/64
                        c'16 * 49/32
                        c'16 * 5/4
                        c'16 * 33/32
                        c'16 * 57/64
                        c'16 * 13/16
                        c'16 * 25/32 ]
                    }
                    \revert TupletNumber #'text
                }
                {
                    \time 3/8
                    \override TupletNumber #'text = \markup {
                        \scale
                            #'(0.75 . 0.75)
                            \score
                                {
                                    \new Score \with {
                                        \override SpacingSpanner #'spacing-increment = #0.5
                                        proportionalNotationDuration = ##f
                                    } <<
                                        \new RhythmicStaff \with {
                                            \remove Time_signature_engraver
                                            \remove Staff_symbol_engraver
                                            \override Stem #'direction = #up
                                            \override Stem #'length = #5
                                            \override TupletBracket #'bracket-visibility = ##t
                                            \override TupletBracket #'direction = #up
                                            \override TupletBracket #'padding = #1.25
                                            \override TupletBracket #'shorten-pair = #'(-1 . -1.5)
                                            \override TupletNumber #'text = #tuplet-number::calc-fraction-text
                                            tupletFullLength = ##t
                                        } {
                                            c'4.
                                        }
                                    >>
                                    \layout {
                                        indent = #0
                                        ragged-right = ##t
                                    }
                                }
                        }
                    \times 1/1 {
                        \once \override Beam #'grow-direction = #right
                        c'16 * 117/64 [
                        c'16 * 99/64
                        c'16 * 69/64
                        c'16 * 13/16
                        c'16 * 47/64 ]
                    }
                    \revert TupletNumber #'text
                }
                {
                    \time 5/8
                    \override TupletNumber #'text = \markup {
                        \scale
                            #'(0.75 . 0.75)
                            \score
                                {
                                    \new Score \with {
                                        \override SpacingSpanner #'spacing-increment = #0.5
                                        proportionalNotationDuration = ##f
                                    } <<
                                        \new RhythmicStaff \with {
                                            \remove Time_signature_engraver
                                            \remove Staff_symbol_engraver
                                            \override Stem #'direction = #up
                                            \override Stem #'length = #5
                                            \override TupletBracket #'bracket-visibility = ##t
                                            \override TupletBracket #'direction = #up
                                            \override TupletBracket #'padding = #1.25
                                            \override TupletBracket #'shorten-pair = #'(-1 . -1.5)
                                            \override TupletNumber #'text = #tuplet-number::calc-fraction-text
                                            tupletFullLength = ##t
                                        } {
                                            c'2 ~
                                            c'8
                                        }
                                    >>
                                    \layout {
                                        indent = #0
                                        ragged-right = ##t
                                    }
                                }
                        }
                    \times 1/1 {
                        \once \override Beam #'grow-direction = #right
                        c'16 * 61/32 [
                        c'16 * 115/64
                        c'16 * 49/32
                        c'16 * 5/4
                        c'16 * 33/32
                        c'16 * 57/64
                        c'16 * 13/16
                        c'16 * 25/32 ]
                    }
                    \revert TupletNumber #'text
                }
                {
                    \time 3/8
                    \override TupletNumber #'text = \markup {
                        \scale
                            #'(0.75 . 0.75)
                            \score
                                {
                                    \new Score \with {
                                        \override SpacingSpanner #'spacing-increment = #0.5
                                        proportionalNotationDuration = ##f
                                    } <<
                                        \new RhythmicStaff \with {
                                            \remove Time_signature_engraver
                                            \remove Staff_symbol_engraver
                                            \override Stem #'direction = #up
                                            \override Stem #'length = #5
                                            \override TupletBracket #'bracket-visibility = ##t
                                            \override TupletBracket #'direction = #up
                                            \override TupletBracket #'padding = #1.25
                                            \override TupletBracket #'shorten-pair = #'(-1 . -1.5)
                                            \override TupletNumber #'text = #tuplet-number::calc-fraction-text
                                            tupletFullLength = ##t
                                        } {
                                            c'4.
                                        }
                                    >>
                                    \layout {
                                        indent = #0
                                        ragged-right = ##t
                                    }
                                }
                        }
                    \times 1/1 {
                        \once \override Beam #'grow-direction = #right
                        c'16 * 117/64 [
                        c'16 * 99/64
                        c'16 * 69/64
                        c'16 * 13/16
                        c'16 * 47/64 ]
                    }
                    \revert TupletNumber #'text
                }
            }

    ..  container:: example

        **Example 2.** Makes ritardando for each input division:

        ::

            >>> maker = rhythmmakertools.AccelerandoRhythmMaker(
            ...     beam_specifier=rhythmmakertools.BeamSpecifier(
            ...         use_feather_beams=True,
            ...         ),
            ...     interpolation_specifiers=rhythmmakertools.InterpolationSpecifier(
            ...         start_duration=Duration(1, 20),
            ...         stop_duration=Duration(1, 8),
            ...         written_duration=Duration(1, 16),
            ...         ),
            ...     tuplet_spelling_specifier=rhythmmakertools.TupletSpellingSpecifier(
            ...         use_note_duration_bracket=True,
            ...         ),
            ...     )

        ::

            >>> divisions = [(5, 8), (3, 8), (5, 8), (3, 8)]
            >>> music = maker(divisions)
            >>> lilypond_file = rhythmmakertools.make_lilypond_file(
            ...     music,
            ...     divisions,
            ...     )
            >>> show(lilypond_file) # doctest: +SKIP

        ..  doctest::

            >>> staff = maker._get_rhythmic_staff(lilypond_file)
            >>> print(format(staff))
            \new RhythmicStaff {
                {
                    \time 5/8
                    \override TupletNumber #'text = \markup {
                        \scale
                            #'(0.75 . 0.75)
                            \score
                                {
                                    \new Score \with {
                                        \override SpacingSpanner #'spacing-increment = #0.5
                                        proportionalNotationDuration = ##f
                                    } <<
                                        \new RhythmicStaff \with {
                                            \remove Time_signature_engraver
                                            \remove Staff_symbol_engraver
                                            \override Stem #'direction = #up
                                            \override Stem #'length = #5
                                            \override TupletBracket #'bracket-visibility = ##t
                                            \override TupletBracket #'direction = #up
                                            \override TupletBracket #'padding = #1.25
                                            \override TupletBracket #'shorten-pair = #'(-1 . -1.5)
                                            \override TupletNumber #'text = #tuplet-number::calc-fraction-text
                                            tupletFullLength = ##t
                                        } {
                                            c'2 ~
                                            c'8
                                        }
                                    >>
                                    \layout {
                                        indent = #0
                                        ragged-right = ##t
                                    }
                                }
                        }
                    \times 1/1 {
                        \once \override Beam #'grow-direction = #left
                        c'16 * 45/64 [
                        c'16 * 23/32
                        c'16 * 25/32
                        c'16 * 55/64
                        c'16 * 1
                        c'16 * 75/64
                        c'16 * 89/64
                        c'16 * 103/64
                        c'16 * 113/64 ]
                    }
                    \revert TupletNumber #'text
                }
                {
                    \time 3/8
                    \override TupletNumber #'text = \markup {
                        \scale
                            #'(0.75 . 0.75)
                            \score
                                {
                                    \new Score \with {
                                        \override SpacingSpanner #'spacing-increment = #0.5
                                        proportionalNotationDuration = ##f
                                    } <<
                                        \new RhythmicStaff \with {
                                            \remove Time_signature_engraver
                                            \remove Staff_symbol_engraver
                                            \override Stem #'direction = #up
                                            \override Stem #'length = #5
                                            \override TupletBracket #'bracket-visibility = ##t
                                            \override TupletBracket #'direction = #up
                                            \override TupletBracket #'padding = #1.25
                                            \override TupletBracket #'shorten-pair = #'(-1 . -1.5)
                                            \override TupletNumber #'text = #tuplet-number::calc-fraction-text
                                            tupletFullLength = ##t
                                        } {
                                            c'4.
                                        }
                                    >>
                                    \layout {
                                        indent = #0
                                        ragged-right = ##t
                                    }
                                }
                        }
                    \times 1/1 {
                        \once \override Beam #'grow-direction = #left
                        c'16 * 5/8 [
                        c'16 * 43/64
                        c'16 * 51/64
                        c'16 * 65/64
                        c'16 * 85/64
                        c'16 * 25/16 ]
                    }
                    \revert TupletNumber #'text
                }
                {
                    \time 5/8
                    \override TupletNumber #'text = \markup {
                        \scale
                            #'(0.75 . 0.75)
                            \score
                                {
                                    \new Score \with {
                                        \override SpacingSpanner #'spacing-increment = #0.5
                                        proportionalNotationDuration = ##f
                                    } <<
                                        \new RhythmicStaff \with {
                                            \remove Time_signature_engraver
                                            \remove Staff_symbol_engraver
                                            \override Stem #'direction = #up
                                            \override Stem #'length = #5
                                            \override TupletBracket #'bracket-visibility = ##t
                                            \override TupletBracket #'direction = #up
                                            \override TupletBracket #'padding = #1.25
                                            \override TupletBracket #'shorten-pair = #'(-1 . -1.5)
                                            \override TupletNumber #'text = #tuplet-number::calc-fraction-text
                                            tupletFullLength = ##t
                                        } {
                                            c'2 ~
                                            c'8
                                        }
                                    >>
                                    \layout {
                                        indent = #0
                                        ragged-right = ##t
                                    }
                                }
                        }
                    \times 1/1 {
                        \once \override Beam #'grow-direction = #left
                        c'16 * 45/64 [
                        c'16 * 23/32
                        c'16 * 25/32
                        c'16 * 55/64
                        c'16 * 1
                        c'16 * 75/64
                        c'16 * 89/64
                        c'16 * 103/64
                        c'16 * 113/64 ]
                    }
                    \revert TupletNumber #'text
                }
                {
                    \time 3/8
                    \override TupletNumber #'text = \markup {
                        \scale
                            #'(0.75 . 0.75)
                            \score
                                {
                                    \new Score \with {
                                        \override SpacingSpanner #'spacing-increment = #0.5
                                        proportionalNotationDuration = ##f
                                    } <<
                                        \new RhythmicStaff \with {
                                            \remove Time_signature_engraver
                                            \remove Staff_symbol_engraver
                                            \override Stem #'direction = #up
                                            \override Stem #'length = #5
                                            \override TupletBracket #'bracket-visibility = ##t
                                            \override TupletBracket #'direction = #up
                                            \override TupletBracket #'padding = #1.25
                                            \override TupletBracket #'shorten-pair = #'(-1 . -1.5)
                                            \override TupletNumber #'text = #tuplet-number::calc-fraction-text
                                            tupletFullLength = ##t
                                        } {
                                            c'4.
                                        }
                                    >>
                                    \layout {
                                        indent = #0
                                        ragged-right = ##t
                                    }
                                }
                        }
                    \times 1/1 {
                        \once \override Beam #'grow-direction = #left
                        c'16 * 5/8 [
                        c'16 * 43/64
                        c'16 * 51/64
                        c'16 * 65/64
                        c'16 * 85/64
                        c'16 * 25/16 ]
                    }
                    \revert TupletNumber #'text
                }
            }

    Set `written_duration` to `1/16` or less for multiple beams.

    Usage follows the two-step configure-once / call-repeatedly pattern shown
    here.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Rhythm-makers'

    __slots__ = (
        '_exponent',
        '_interpolation_specifiers',
        )

    _class_name_abbreviation = 'Acc'

    _human_readable_class_name = 'accelerando rhythm-maker'

    ### INITIALIZER ###

    def __init__(
        self,
        beam_specifier=None,
        duration_spelling_specifier=None,
        interpolation_specifiers=None,
        output_masks=None,
        tie_specifier=None,
        tuplet_spelling_specifier=None,
        ):
        RhythmMaker.__init__(
            self,
            beam_specifier=beam_specifier,
            duration_spelling_specifier=duration_spelling_specifier,
            output_masks=output_masks,
            tie_specifier=tie_specifier,
            tuplet_spelling_specifier=tuplet_spelling_specifier,
            )
        self._interpolation_specifiers = interpolation_specifiers

    ### SPECIAL METHODS ###

    def __call__(self, divisions, rotation=None):
        r'''Calls interpolated rhythm-maker on `divisions`.

        Ignores `rotation`.

        Returns list of selections.
        '''
        return RhythmMaker.__call__(
            self,
            divisions,
            rotation=rotation,
            )

    ### PRIVATE METHODS ###

    def _fix_rounding_error(
        self, 
        selection, 
        total_duration,
        interpolation_specifier,
        ):
        selection_duration = selection.get_duration()
        if not selection_duration == total_duration:
            needed_duration = total_duration - selection[:-1].get_duration()
            multiplier = needed_duration / \
                interpolation_specifier.written_duration
            multiplier = durationtools.Multiplier(multiplier)
            detach(durationtools.Multiplier, selection[-1])
            attach(multiplier, selection[-1])

    def _get_interpolation_specifiers(self):
        from abjad.tools import rhythmmakertools
        specifiers = self.interpolation_specifiers
        if specifiers is None:
            specifiers = datastructuretools.CyclicTuple([
                rhythmmakertools.InterpolationSpecifier(),
                ])
        elif isinstance(specifiers, rhythmmakertools.InterpolationSpecifier):
            specifiers = datastructuretools.CyclicTuple([specifiers])
        else:
            specifiers = datastructuretools.CyclicTuple(specifiers)
        return specifiers

    @staticmethod
    def _interpolate_cosine(y1, y2, mu):
        r'''Perorms cosine interpolation of `y1` and `y2` with `mu` ``[0, 1]``
        normalized:

        ::

            >>> rhythmmakertools.AccelerandoRhythmMaker._interpolate_cosine(
            ...     y1=0,
            ...     y2=1,
            ...     mu=0.5,
            ...     )
            0.49999999999999994

        Returns float.
        '''

        mu2 = (1 - math.cos(mu * math.pi)) / 2
        return (y1 * (1 - mu2) + y2 * mu2)

    @staticmethod
    def _interpolate_divide(
        total_duration,
        start_duration,
        stop_duration,
        exponent='cosine',
        ):
        r'''Divides `total_duration` into durations computed from interpolating
        between `start_duration` and `stop_duration`:

        ::

            >>> rhythmmakertools.AccelerandoRhythmMaker._interpolate_divide(
            ...     total_duration=10,
            ...     start_duration=1,
            ...     stop_duration=1,
            ...     exponent=1,
            ...     )
            [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
            >>> sum(_)
            10.0

        ::

            >>> rhythmmakertools.AccelerandoRhythmMaker._interpolate_divide(
            ...     total_duration=10,
            ...     start_duration=5,
            ...     stop_duration=1,
            ...     )
            [4.798..., 2.879..., 1.326..., 0.995...]
            >>> sum(_)
            10.0

        Set `exponent` to ``'cosine'`` for cosine interpolation.

        Set `exponent` to a numeric value for exponential interpolation with
        `exponent` as the exponent.

        Scales resulting durations so that their sum equals `total_duration`
        exactly.

        Returns a list of floats.
        '''
        if total_duration <= 0:
            message = "Total duration must be positive."
            raise ValueError(message)
        if start_duration <= 0 or stop_duration <= 0:
            message = "Both 'start_duration' and 'stop_duration'"
            message += ' must be positive.'
            raise ValueError(message)
        if total_duration < (stop_duration + start_duration):
            return 'too small'
        durations = []
        total_duration = float(total_duration)
        partial_sum = 0
        while partial_sum < total_duration:
            if exponent == 'cosine':
                duration = AccelerandoRhythmMaker._interpolate_cosine(
                    start_duration,
                    stop_duration,
                    partial_sum / total_duration,
                    )
            else:
                duration = AccelerandoRhythmMaker._interpolate_exponential(
                    start_duration,
                    stop_duration,
                    partial_sum / total_duration,
                    exponent,
                    )
            durations.append(duration)
            partial_sum += duration
        # scale result to fit total exaclty
        durations = [_ * total_duration / sum(durations) for _ in durations]
        return durations

    @staticmethod
    def _interpolate_divide_multiple(
        total_durations,
        reference_durations,
        exponent='cosine',
        ):
        '''Interpolates `reference_durations` such that the sum of the
        resulting interpolated values equals the given `total_durations`:

        ::

            >>> durations = rhythmmakertools.AccelerandoRhythmMaker._interpolate_divide_multiple(
            ...     total_durations=[100, 50],
            ...     reference_durations=[20, 10, 20],
            ...     )
            >>> for duration in durations:
            ...     duration
            19.448...
            18.520...
            16.227...
            13.715...
            11.748...
            10.487...
            9.8515...
            9.5130...
            10.421...
            13.073...
            16.991...

        The operation is the same as the interpolate_divide() method
        implemented on this class. But this function takes multiple
        total durations and multiple reference durations at one time.

        Precondition: ``len(totals_durations) == len(reference_durations)-1``.

        Set `exponent` to `cosine` for cosine interpolation. Set `exponent` to
        a number for exponential interpolation.

        Returns a list of floats.
        '''
        assert len(total_durations) == len(reference_durations) - 1
        durations = []
        for i in range(len(total_durations)):
            durations_ = AccelerandoRhythmMaker._interpolate_divide(
                total_durations[i],
                reference_durations[i],
                reference_durations[i + 1],
                exponent,
                )
            # we want a flat list
            durations.extend(durations_)
        return durations

    @staticmethod
    def _interpolate_exponential(y1, y2, mu, exponent=1):
        r'''Performs exponential interpolation from `y1` to `y2` with `mu`
        ``[0, 1]`` normalized:

        ::

            >>> rhythmmakertools.AccelerandoRhythmMaker._interpolate_exponential(
            ...     y1=0,
            ...     y2=1,
            ...     mu=0.5,
            ...     exponent=4,
            ...     )
            0.0625

        Set `exponent` equal to the exponent of interpolation.

        Returns float.
        '''

        result = (y1 * (1 - mu ** exponent) + y2 * mu ** exponent)
        return result

    def _is_accelerando(self, selection):
        first_duration = inspect_(selection[0]).get_duration()
        last_duration = inspect_(selection[-1]).get_duration()
        if last_duration < first_duration:
            return True
        return False

    def _is_ritardando(self, selection):
        first_duration = inspect_(selection[0]).get_duration()
        last_duration = inspect_(selection[-1]).get_duration()
        if first_duration < last_duration:
            return True
        return False

    def _make_accelerando(self, total_duration, index):
        r'''Makes notes with LilyPond multipliers.

        Returns as many interpolation values as necessary to fill `total`
        duration requested.

        Computes duration multipliers interpolated from `start` to `stop`.

        Sets note durations to `written_duration` multiplied by interpolation
        multipliers.

        Returns selection of notes.
        '''
        from abjad.tools import rhythmmakertools
        total_duration = durationtools.Duration(total_duration)
        interpolation_specifiers = self._get_interpolation_specifiers()
        interpolation_specifier = interpolation_specifiers[index]
        durations = AccelerandoRhythmMaker._interpolate_divide(
            total_duration=total_duration,
            start_duration=interpolation_specifier.start_duration,
            stop_duration=interpolation_specifier.stop_duration,
            )
        if durations == 'too small':
            notes = scoretools.make_notes([0], [total_duration])
            return notes
        durations = [
            durationtools.Duration(int(round(_ * 2**10)), 2**10)
            for _ in durations
            ]
        notes = []
        for i, duration in enumerate(durations):
            note = scoretools.Note(0, interpolation_specifier.written_duration)
            multiplier = duration / interpolation_specifier.written_duration
            multiplier = durationtools.Multiplier(multiplier)
            attach(multiplier, note)
            notes.append(note)
        selection = selectiontools.Selection(notes)
        self._fix_rounding_error(
            selection, 
            total_duration,
            interpolation_specifier,
            )
        pair = (selection.get_duration(), total_duration)
        assert pair[0] == pair[1], repr(pair)
        beam_specifier = self._get_beam_specifier()
        if not beam_specifier.use_feather_beams:
            pass
        elif self._is_accelerando(selection):
            override(selection[0]).beam.grow_direction = Right
        elif self._is_ritardando(selection):
            override(selection[0]).beam.grow_direction = Left
        tuplet = scoretools.Tuplet((1, 1), selection)
        tuplet_spelling_specifier = self._get_tuplet_spelling_specifier()
        if tuplet_spelling_specifier.use_note_duration_bracket:
            tuplet.force_times_command = True
            duration = inspect_(tuplet).get_duration()
            markup = duration.to_score_markup()
            markup = markup.scale((0.75, 0.75))
            override(tuplet).tuplet_number.text = markup
        selection = selectiontools.Selection([tuplet])
        return selection

    def _make_music(self, divisions, rotation):
        selections = []
        for index, division in enumerate(divisions):
            accelerando = self._make_accelerando(division, index)
            selections.append(accelerando)
        self._apply_beam_specifier(selections)
        selections = self._apply_output_masks(selections, rotation)
        return selections

    ### PUBLIC PROPERTIES ###

    @property
    def beam_specifier(self):
        r'''Gets beam specifier of accelerando rhythm-maker.

        ..  container:: example

            **Example 1.** Feather beams each division:

            ::

                >>> maker = rhythmmakertools.AccelerandoRhythmMaker(
                ...     beam_specifier=rhythmmakertools.BeamSpecifier(
                ...         beam_each_division=True,
                ...         use_feather_beams=True,
                ...         ),
                ...     interpolation_specifiers=rhythmmakertools.InterpolationSpecifier(
                ...         start_duration=Duration(1, 8),
                ...         stop_duration=Duration(1, 20),
                ...         written_duration=Duration(1, 16),
                ...         ),
                ...     tuplet_spelling_specifier=rhythmmakertools.TupletSpellingSpecifier(
                ...         use_note_duration_bracket=True,
                ...         ),
                ...     )

            ::

                >>> divisions = [(5, 8), (3, 8), (5, 8), (3, 8)]
                >>> music = maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     music,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = maker._get_rhythmic_staff(lilypond_file)
                >>> print(format(staff))
                \new RhythmicStaff {
                    {
                        \time 5/8
                        \override TupletNumber #'text = \markup {
                            \scale
                                #'(0.75 . 0.75)
                                \score
                                    {
                                        \new Score \with {
                                            \override SpacingSpanner #'spacing-increment = #0.5
                                            proportionalNotationDuration = ##f
                                        } <<
                                            \new RhythmicStaff \with {
                                                \remove Time_signature_engraver
                                                \remove Staff_symbol_engraver
                                                \override Stem #'direction = #up
                                                \override Stem #'length = #5
                                                \override TupletBracket #'bracket-visibility = ##t
                                                \override TupletBracket #'direction = #up
                                                \override TupletBracket #'padding = #1.25
                                                \override TupletBracket #'shorten-pair = #'(-1 . -1.5)
                                                \override TupletNumber #'text = #tuplet-number::calc-fraction-text
                                                tupletFullLength = ##t
                                            } {
                                                c'2 ~
                                                c'8
                                            }
                                        >>
                                        \layout {
                                            indent = #0
                                            ragged-right = ##t
                                        }
                                    }
                            }
                        \times 1/1 {
                            \once \override Beam #'grow-direction = #right
                            c'16 * 61/32 [
                            c'16 * 115/64
                            c'16 * 49/32
                            c'16 * 5/4
                            c'16 * 33/32
                            c'16 * 57/64
                            c'16 * 13/16
                            c'16 * 25/32 ]
                        }
                        \revert TupletNumber #'text
                    }
                    {
                        \time 3/8
                        \override TupletNumber #'text = \markup {
                            \scale
                                #'(0.75 . 0.75)
                                \score
                                    {
                                        \new Score \with {
                                            \override SpacingSpanner #'spacing-increment = #0.5
                                            proportionalNotationDuration = ##f
                                        } <<
                                            \new RhythmicStaff \with {
                                                \remove Time_signature_engraver
                                                \remove Staff_symbol_engraver
                                                \override Stem #'direction = #up
                                                \override Stem #'length = #5
                                                \override TupletBracket #'bracket-visibility = ##t
                                                \override TupletBracket #'direction = #up
                                                \override TupletBracket #'padding = #1.25
                                                \override TupletBracket #'shorten-pair = #'(-1 . -1.5)
                                                \override TupletNumber #'text = #tuplet-number::calc-fraction-text
                                                tupletFullLength = ##t
                                            } {
                                                c'4.
                                            }
                                        >>
                                        \layout {
                                            indent = #0
                                            ragged-right = ##t
                                        }
                                    }
                            }
                        \times 1/1 {
                            \once \override Beam #'grow-direction = #right
                            c'16 * 117/64 [
                            c'16 * 99/64
                            c'16 * 69/64
                            c'16 * 13/16
                            c'16 * 47/64 ]
                        }
                        \revert TupletNumber #'text
                    }
                    {
                        \time 5/8
                        \override TupletNumber #'text = \markup {
                            \scale
                                #'(0.75 . 0.75)
                                \score
                                    {
                                        \new Score \with {
                                            \override SpacingSpanner #'spacing-increment = #0.5
                                            proportionalNotationDuration = ##f
                                        } <<
                                            \new RhythmicStaff \with {
                                                \remove Time_signature_engraver
                                                \remove Staff_symbol_engraver
                                                \override Stem #'direction = #up
                                                \override Stem #'length = #5
                                                \override TupletBracket #'bracket-visibility = ##t
                                                \override TupletBracket #'direction = #up
                                                \override TupletBracket #'padding = #1.25
                                                \override TupletBracket #'shorten-pair = #'(-1 . -1.5)
                                                \override TupletNumber #'text = #tuplet-number::calc-fraction-text
                                                tupletFullLength = ##t
                                            } {
                                                c'2 ~
                                                c'8
                                            }
                                        >>
                                        \layout {
                                            indent = #0
                                            ragged-right = ##t
                                        }
                                    }
                            }
                        \times 1/1 {
                            \once \override Beam #'grow-direction = #right
                            c'16 * 61/32 [
                            c'16 * 115/64
                            c'16 * 49/32
                            c'16 * 5/4
                            c'16 * 33/32
                            c'16 * 57/64
                            c'16 * 13/16
                            c'16 * 25/32 ]
                        }
                        \revert TupletNumber #'text
                    }
                    {
                        \time 3/8
                        \override TupletNumber #'text = \markup {
                            \scale
                                #'(0.75 . 0.75)
                                \score
                                    {
                                        \new Score \with {
                                            \override SpacingSpanner #'spacing-increment = #0.5
                                            proportionalNotationDuration = ##f
                                        } <<
                                            \new RhythmicStaff \with {
                                                \remove Time_signature_engraver
                                                \remove Staff_symbol_engraver
                                                \override Stem #'direction = #up
                                                \override Stem #'length = #5
                                                \override TupletBracket #'bracket-visibility = ##t
                                                \override TupletBracket #'direction = #up
                                                \override TupletBracket #'padding = #1.25
                                                \override TupletBracket #'shorten-pair = #'(-1 . -1.5)
                                                \override TupletNumber #'text = #tuplet-number::calc-fraction-text
                                                tupletFullLength = ##t
                                            } {
                                                c'4.
                                            }
                                        >>
                                        \layout {
                                            indent = #0
                                            ragged-right = ##t
                                        }
                                    }
                            }
                        \times 1/1 {
                            \once \override Beam #'grow-direction = #right
                            c'16 * 117/64 [
                            c'16 * 99/64
                            c'16 * 69/64
                            c'16 * 13/16
                            c'16 * 47/64 ]
                        }
                        \revert TupletNumber #'text
                    }
                }

        ..  container:: example

            **Example 2.** Beams divisions together (without feathering):

            ::

                >>> maker = rhythmmakertools.AccelerandoRhythmMaker(
                ...     beam_specifier=rhythmmakertools.BeamSpecifier(
                ...         beam_divisions_together=True,
                ...         use_feather_beams=False,
                ...         ),
                ...     interpolation_specifiers=rhythmmakertools.InterpolationSpecifier(
                ...         start_duration=Duration(1, 8),
                ...         stop_duration=Duration(1, 20),
                ...         written_duration=Duration(1, 16),
                ...         ),
                ...     tuplet_spelling_specifier=rhythmmakertools.TupletSpellingSpecifier(
                ...         use_note_duration_bracket=True,
                ...         ),
                ...     )

            ::

                >>> divisions = [(5, 8), (3, 8), (5, 8), (3, 8)]
                >>> music = maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     music,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = maker._get_rhythmic_staff(lilypond_file)
                >>> print(format(staff))
                \new RhythmicStaff {
                    {
                        \time 5/8
                        \override TupletNumber #'text = \markup {
                            \scale
                                #'(0.75 . 0.75)
                                \score
                                    {
                                        \new Score \with {
                                            \override SpacingSpanner #'spacing-increment = #0.5
                                            proportionalNotationDuration = ##f
                                        } <<
                                            \new RhythmicStaff \with {
                                                \remove Time_signature_engraver
                                                \remove Staff_symbol_engraver
                                                \override Stem #'direction = #up
                                                \override Stem #'length = #5
                                                \override TupletBracket #'bracket-visibility = ##t
                                                \override TupletBracket #'direction = #up
                                                \override TupletBracket #'padding = #1.25
                                                \override TupletBracket #'shorten-pair = #'(-1 . -1.5)
                                                \override TupletNumber #'text = #tuplet-number::calc-fraction-text
                                                tupletFullLength = ##t
                                            } {
                                                c'2 ~
                                                c'8
                                            }
                                        >>
                                        \layout {
                                            indent = #0
                                            ragged-right = ##t
                                        }
                                    }
                            }
                        \times 1/1 {
                            \set stemLeftBeamCount = #0
                            \set stemRightBeamCount = #2
                            c'16 * 61/32 [
                            \set stemLeftBeamCount = #2
                            \set stemRightBeamCount = #2
                            c'16 * 115/64
                            \set stemLeftBeamCount = #2
                            \set stemRightBeamCount = #2
                            c'16 * 49/32
                            \set stemLeftBeamCount = #2
                            \set stemRightBeamCount = #2
                            c'16 * 5/4
                            \set stemLeftBeamCount = #2
                            \set stemRightBeamCount = #2
                            c'16 * 33/32
                            \set stemLeftBeamCount = #2
                            \set stemRightBeamCount = #2
                            c'16 * 57/64
                            \set stemLeftBeamCount = #2
                            \set stemRightBeamCount = #2
                            c'16 * 13/16
                            \set stemLeftBeamCount = #2
                            \set stemRightBeamCount = #1
                            c'16 * 25/32
                        }
                        \revert TupletNumber #'text
                    }
                    {
                        \time 3/8
                        \override TupletNumber #'text = \markup {
                            \scale
                                #'(0.75 . 0.75)
                                \score
                                    {
                                        \new Score \with {
                                            \override SpacingSpanner #'spacing-increment = #0.5
                                            proportionalNotationDuration = ##f
                                        } <<
                                            \new RhythmicStaff \with {
                                                \remove Time_signature_engraver
                                                \remove Staff_symbol_engraver
                                                \override Stem #'direction = #up
                                                \override Stem #'length = #5
                                                \override TupletBracket #'bracket-visibility = ##t
                                                \override TupletBracket #'direction = #up
                                                \override TupletBracket #'padding = #1.25
                                                \override TupletBracket #'shorten-pair = #'(-1 . -1.5)
                                                \override TupletNumber #'text = #tuplet-number::calc-fraction-text
                                                tupletFullLength = ##t
                                            } {
                                                c'4.
                                            }
                                        >>
                                        \layout {
                                            indent = #0
                                            ragged-right = ##t
                                        }
                                    }
                            }
                        \times 1/1 {
                            \set stemLeftBeamCount = #1
                            \set stemRightBeamCount = #2
                            c'16 * 117/64
                            \set stemLeftBeamCount = #2
                            \set stemRightBeamCount = #2
                            c'16 * 99/64
                            \set stemLeftBeamCount = #2
                            \set stemRightBeamCount = #2
                            c'16 * 69/64
                            \set stemLeftBeamCount = #2
                            \set stemRightBeamCount = #2
                            c'16 * 13/16
                            \set stemLeftBeamCount = #2
                            \set stemRightBeamCount = #1
                            c'16 * 47/64
                        }
                        \revert TupletNumber #'text
                    }
                    {
                        \time 5/8
                        \override TupletNumber #'text = \markup {
                            \scale
                                #'(0.75 . 0.75)
                                \score
                                    {
                                        \new Score \with {
                                            \override SpacingSpanner #'spacing-increment = #0.5
                                            proportionalNotationDuration = ##f
                                        } <<
                                            \new RhythmicStaff \with {
                                                \remove Time_signature_engraver
                                                \remove Staff_symbol_engraver
                                                \override Stem #'direction = #up
                                                \override Stem #'length = #5
                                                \override TupletBracket #'bracket-visibility = ##t
                                                \override TupletBracket #'direction = #up
                                                \override TupletBracket #'padding = #1.25
                                                \override TupletBracket #'shorten-pair = #'(-1 . -1.5)
                                                \override TupletNumber #'text = #tuplet-number::calc-fraction-text
                                                tupletFullLength = ##t
                                            } {
                                                c'2 ~
                                                c'8
                                            }
                                        >>
                                        \layout {
                                            indent = #0
                                            ragged-right = ##t
                                        }
                                    }
                            }
                        \times 1/1 {
                            \set stemLeftBeamCount = #1
                            \set stemRightBeamCount = #2
                            c'16 * 61/32
                            \set stemLeftBeamCount = #2
                            \set stemRightBeamCount = #2
                            c'16 * 115/64
                            \set stemLeftBeamCount = #2
                            \set stemRightBeamCount = #2
                            c'16 * 49/32
                            \set stemLeftBeamCount = #2
                            \set stemRightBeamCount = #2
                            c'16 * 5/4
                            \set stemLeftBeamCount = #2
                            \set stemRightBeamCount = #2
                            c'16 * 33/32
                            \set stemLeftBeamCount = #2
                            \set stemRightBeamCount = #2
                            c'16 * 57/64
                            \set stemLeftBeamCount = #2
                            \set stemRightBeamCount = #2
                            c'16 * 13/16
                            \set stemLeftBeamCount = #2
                            \set stemRightBeamCount = #1
                            c'16 * 25/32
                        }
                        \revert TupletNumber #'text
                    }
                    {
                        \time 3/8
                        \override TupletNumber #'text = \markup {
                            \scale
                                #'(0.75 . 0.75)
                                \score
                                    {
                                        \new Score \with {
                                            \override SpacingSpanner #'spacing-increment = #0.5
                                            proportionalNotationDuration = ##f
                                        } <<
                                            \new RhythmicStaff \with {
                                                \remove Time_signature_engraver
                                                \remove Staff_symbol_engraver
                                                \override Stem #'direction = #up
                                                \override Stem #'length = #5
                                                \override TupletBracket #'bracket-visibility = ##t
                                                \override TupletBracket #'direction = #up
                                                \override TupletBracket #'padding = #1.25
                                                \override TupletBracket #'shorten-pair = #'(-1 . -1.5)
                                                \override TupletNumber #'text = #tuplet-number::calc-fraction-text
                                                tupletFullLength = ##t
                                            } {
                                                c'4.
                                            }
                                        >>
                                        \layout {
                                            indent = #0
                                            ragged-right = ##t
                                        }
                                    }
                            }
                        \times 1/1 {
                            \set stemLeftBeamCount = #1
                            \set stemRightBeamCount = #2
                            c'16 * 117/64
                            \set stemLeftBeamCount = #2
                            \set stemRightBeamCount = #2
                            c'16 * 99/64
                            \set stemLeftBeamCount = #2
                            \set stemRightBeamCount = #2
                            c'16 * 69/64
                            \set stemLeftBeamCount = #2
                            \set stemRightBeamCount = #2
                            c'16 * 13/16
                            \set stemLeftBeamCount = #2
                            \set stemRightBeamCount = #0
                            c'16 * 47/64 ]
                        }
                        \revert TupletNumber #'text
                    }
                }

            It is important to leave feathering turned off here
            because LilyPond feathers conjoint beams poorly.

        ..  container:: example

            **Example 3.** Makes no beams:

            ::

                >>> maker = rhythmmakertools.AccelerandoRhythmMaker(
                ...     beam_specifier=rhythmmakertools.BeamSpecifier(
                ...         beam_divisions_together=False,
                ...         beam_each_division=False,
                ...         ),
                ...     interpolation_specifiers=rhythmmakertools.InterpolationSpecifier(
                ...         start_duration=Duration(1, 8),
                ...         stop_duration=Duration(1, 20),
                ...         written_duration=Duration(1, 16),
                ...         ),
                ...     tuplet_spelling_specifier=rhythmmakertools.TupletSpellingSpecifier(
                ...         use_note_duration_bracket=True,
                ...         ),
                ...     )

            ::

                >>> divisions = [(5, 8), (3, 8), (5, 8), (3, 8)]
                >>> music = maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     music,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = maker._get_rhythmic_staff(lilypond_file)
                >>> print(format(staff))
                \new RhythmicStaff {
                    {
                        \time 5/8
                        \override TupletNumber #'text = \markup {
                            \scale
                                #'(0.75 . 0.75)
                                \score
                                    {
                                        \new Score \with {
                                            \override SpacingSpanner #'spacing-increment = #0.5
                                            proportionalNotationDuration = ##f
                                        } <<
                                            \new RhythmicStaff \with {
                                                \remove Time_signature_engraver
                                                \remove Staff_symbol_engraver
                                                \override Stem #'direction = #up
                                                \override Stem #'length = #5
                                                \override TupletBracket #'bracket-visibility = ##t
                                                \override TupletBracket #'direction = #up
                                                \override TupletBracket #'padding = #1.25
                                                \override TupletBracket #'shorten-pair = #'(-1 . -1.5)
                                                \override TupletNumber #'text = #tuplet-number::calc-fraction-text
                                                tupletFullLength = ##t
                                            } {
                                                c'2 ~
                                                c'8
                                            }
                                        >>
                                        \layout {
                                            indent = #0
                                            ragged-right = ##t
                                        }
                                    }
                            }
                        \times 1/1 {
                            c'16 * 61/32
                            c'16 * 115/64
                            c'16 * 49/32
                            c'16 * 5/4
                            c'16 * 33/32
                            c'16 * 57/64
                            c'16 * 13/16
                            c'16 * 25/32
                        }
                        \revert TupletNumber #'text
                    }
                    {
                        \time 3/8
                        \override TupletNumber #'text = \markup {
                            \scale
                                #'(0.75 . 0.75)
                                \score
                                    {
                                        \new Score \with {
                                            \override SpacingSpanner #'spacing-increment = #0.5
                                            proportionalNotationDuration = ##f
                                        } <<
                                            \new RhythmicStaff \with {
                                                \remove Time_signature_engraver
                                                \remove Staff_symbol_engraver
                                                \override Stem #'direction = #up
                                                \override Stem #'length = #5
                                                \override TupletBracket #'bracket-visibility = ##t
                                                \override TupletBracket #'direction = #up
                                                \override TupletBracket #'padding = #1.25
                                                \override TupletBracket #'shorten-pair = #'(-1 . -1.5)
                                                \override TupletNumber #'text = #tuplet-number::calc-fraction-text
                                                tupletFullLength = ##t
                                            } {
                                                c'4.
                                            }
                                        >>
                                        \layout {
                                            indent = #0
                                            ragged-right = ##t
                                        }
                                    }
                            }
                        \times 1/1 {
                            c'16 * 117/64
                            c'16 * 99/64
                            c'16 * 69/64
                            c'16 * 13/16
                            c'16 * 47/64
                        }
                        \revert TupletNumber #'text
                    }
                    {
                        \time 5/8
                        \override TupletNumber #'text = \markup {
                            \scale
                                #'(0.75 . 0.75)
                                \score
                                    {
                                        \new Score \with {
                                            \override SpacingSpanner #'spacing-increment = #0.5
                                            proportionalNotationDuration = ##f
                                        } <<
                                            \new RhythmicStaff \with {
                                                \remove Time_signature_engraver
                                                \remove Staff_symbol_engraver
                                                \override Stem #'direction = #up
                                                \override Stem #'length = #5
                                                \override TupletBracket #'bracket-visibility = ##t
                                                \override TupletBracket #'direction = #up
                                                \override TupletBracket #'padding = #1.25
                                                \override TupletBracket #'shorten-pair = #'(-1 . -1.5)
                                                \override TupletNumber #'text = #tuplet-number::calc-fraction-text
                                                tupletFullLength = ##t
                                            } {
                                                c'2 ~
                                                c'8
                                            }
                                        >>
                                        \layout {
                                            indent = #0
                                            ragged-right = ##t
                                        }
                                    }
                            }
                        \times 1/1 {
                            c'16 * 61/32
                            c'16 * 115/64
                            c'16 * 49/32
                            c'16 * 5/4
                            c'16 * 33/32
                            c'16 * 57/64
                            c'16 * 13/16
                            c'16 * 25/32
                        }
                        \revert TupletNumber #'text
                    }
                    {
                        \time 3/8
                        \override TupletNumber #'text = \markup {
                            \scale
                                #'(0.75 . 0.75)
                                \score
                                    {
                                        \new Score \with {
                                            \override SpacingSpanner #'spacing-increment = #0.5
                                            proportionalNotationDuration = ##f
                                        } <<
                                            \new RhythmicStaff \with {
                                                \remove Time_signature_engraver
                                                \remove Staff_symbol_engraver
                                                \override Stem #'direction = #up
                                                \override Stem #'length = #5
                                                \override TupletBracket #'bracket-visibility = ##t
                                                \override TupletBracket #'direction = #up
                                                \override TupletBracket #'padding = #1.25
                                                \override TupletBracket #'shorten-pair = #'(-1 . -1.5)
                                                \override TupletNumber #'text = #tuplet-number::calc-fraction-text
                                                tupletFullLength = ##t
                                            } {
                                                c'4.
                                            }
                                        >>
                                        \layout {
                                            indent = #0
                                            ragged-right = ##t
                                        }
                                    }
                            }
                        \times 1/1 {
                            c'16 * 117/64
                            c'16 * 99/64
                            c'16 * 69/64
                            c'16 * 13/16
                            c'16 * 47/64
                        }
                        \revert TupletNumber #'text
                    }
                }

        Returns beam specifier.
        '''
        superclass = super(AccelerandoRhythmMaker, self)
        return superclass.beam_specifier

    @property
    def interpolation_specifiers(self):
        r'''Gets interpolation specifier of accelerando rhythm-maker.

        ..  container:: example

            **Example 1.** Makes accelerando for each input division:

            ::

                >>> maker = rhythmmakertools.AccelerandoRhythmMaker(
                ...     beam_specifier=rhythmmakertools.BeamSpecifier(
                ...         use_feather_beams=True,
                ...         ),
                ...     interpolation_specifiers=rhythmmakertools.InterpolationSpecifier(
                ...         start_duration=Duration(1, 8),
                ...         stop_duration=Duration(1, 20),
                ...         written_duration=Duration(1, 16),
                ...         ),
                ...     tuplet_spelling_specifier=rhythmmakertools.TupletSpellingSpecifier(
                ...         use_note_duration_bracket=True,
                ...         ),
                ...     )

            ::

                >>> divisions = [(5, 8), (3, 8), (5, 8), (3, 8)]
                >>> music = maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     music,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = maker._get_rhythmic_staff(lilypond_file)
                >>> print(format(staff))
                \new RhythmicStaff {
                    {
                        \time 5/8
                        \override TupletNumber #'text = \markup {
                            \scale
                                #'(0.75 . 0.75)
                                \score
                                    {
                                        \new Score \with {
                                            \override SpacingSpanner #'spacing-increment = #0.5
                                            proportionalNotationDuration = ##f
                                        } <<
                                            \new RhythmicStaff \with {
                                                \remove Time_signature_engraver
                                                \remove Staff_symbol_engraver
                                                \override Stem #'direction = #up
                                                \override Stem #'length = #5
                                                \override TupletBracket #'bracket-visibility = ##t
                                                \override TupletBracket #'direction = #up
                                                \override TupletBracket #'padding = #1.25
                                                \override TupletBracket #'shorten-pair = #'(-1 . -1.5)
                                                \override TupletNumber #'text = #tuplet-number::calc-fraction-text
                                                tupletFullLength = ##t
                                            } {
                                                c'2 ~
                                                c'8
                                            }
                                        >>
                                        \layout {
                                            indent = #0
                                            ragged-right = ##t
                                        }
                                    }
                            }
                        \times 1/1 {
                            \once \override Beam #'grow-direction = #right
                            c'16 * 61/32 [
                            c'16 * 115/64
                            c'16 * 49/32
                            c'16 * 5/4
                            c'16 * 33/32
                            c'16 * 57/64
                            c'16 * 13/16
                            c'16 * 25/32 ]
                        }
                        \revert TupletNumber #'text
                    }
                    {
                        \time 3/8
                        \override TupletNumber #'text = \markup {
                            \scale
                                #'(0.75 . 0.75)
                                \score
                                    {
                                        \new Score \with {
                                            \override SpacingSpanner #'spacing-increment = #0.5
                                            proportionalNotationDuration = ##f
                                        } <<
                                            \new RhythmicStaff \with {
                                                \remove Time_signature_engraver
                                                \remove Staff_symbol_engraver
                                                \override Stem #'direction = #up
                                                \override Stem #'length = #5
                                                \override TupletBracket #'bracket-visibility = ##t
                                                \override TupletBracket #'direction = #up
                                                \override TupletBracket #'padding = #1.25
                                                \override TupletBracket #'shorten-pair = #'(-1 . -1.5)
                                                \override TupletNumber #'text = #tuplet-number::calc-fraction-text
                                                tupletFullLength = ##t
                                            } {
                                                c'4.
                                            }
                                        >>
                                        \layout {
                                            indent = #0
                                            ragged-right = ##t
                                        }
                                    }
                            }
                        \times 1/1 {
                            \once \override Beam #'grow-direction = #right
                            c'16 * 117/64 [
                            c'16 * 99/64
                            c'16 * 69/64
                            c'16 * 13/16
                            c'16 * 47/64 ]
                        }
                        \revert TupletNumber #'text
                    }
                    {
                        \time 5/8
                        \override TupletNumber #'text = \markup {
                            \scale
                                #'(0.75 . 0.75)
                                \score
                                    {
                                        \new Score \with {
                                            \override SpacingSpanner #'spacing-increment = #0.5
                                            proportionalNotationDuration = ##f
                                        } <<
                                            \new RhythmicStaff \with {
                                                \remove Time_signature_engraver
                                                \remove Staff_symbol_engraver
                                                \override Stem #'direction = #up
                                                \override Stem #'length = #5
                                                \override TupletBracket #'bracket-visibility = ##t
                                                \override TupletBracket #'direction = #up
                                                \override TupletBracket #'padding = #1.25
                                                \override TupletBracket #'shorten-pair = #'(-1 . -1.5)
                                                \override TupletNumber #'text = #tuplet-number::calc-fraction-text
                                                tupletFullLength = ##t
                                            } {
                                                c'2 ~
                                                c'8
                                            }
                                        >>
                                        \layout {
                                            indent = #0
                                            ragged-right = ##t
                                        }
                                    }
                            }
                        \times 1/1 {
                            \once \override Beam #'grow-direction = #right
                            c'16 * 61/32 [
                            c'16 * 115/64
                            c'16 * 49/32
                            c'16 * 5/4
                            c'16 * 33/32
                            c'16 * 57/64
                            c'16 * 13/16
                            c'16 * 25/32 ]
                        }
                        \revert TupletNumber #'text
                    }
                    {
                        \time 3/8
                        \override TupletNumber #'text = \markup {
                            \scale
                                #'(0.75 . 0.75)
                                \score
                                    {
                                        \new Score \with {
                                            \override SpacingSpanner #'spacing-increment = #0.5
                                            proportionalNotationDuration = ##f
                                        } <<
                                            \new RhythmicStaff \with {
                                                \remove Time_signature_engraver
                                                \remove Staff_symbol_engraver
                                                \override Stem #'direction = #up
                                                \override Stem #'length = #5
                                                \override TupletBracket #'bracket-visibility = ##t
                                                \override TupletBracket #'direction = #up
                                                \override TupletBracket #'padding = #1.25
                                                \override TupletBracket #'shorten-pair = #'(-1 . -1.5)
                                                \override TupletNumber #'text = #tuplet-number::calc-fraction-text
                                                tupletFullLength = ##t
                                            } {
                                                c'4.
                                            }
                                        >>
                                        \layout {
                                            indent = #0
                                            ragged-right = ##t
                                        }
                                    }
                            }
                        \times 1/1 {
                            \once \override Beam #'grow-direction = #right
                            c'16 * 117/64 [
                            c'16 * 99/64
                            c'16 * 69/64
                            c'16 * 13/16
                            c'16 * 47/64 ]
                        }
                        \revert TupletNumber #'text
                    }
                }

        ..  container:: example

            **Example 2.** Makes accelerandi and ritardandi on alternate
            divisions:

            ::

                >>> maker = rhythmmakertools.AccelerandoRhythmMaker(
                ...     beam_specifier=rhythmmakertools.BeamSpecifier(
                ...         use_feather_beams=True,
                ...         ),
                ...     interpolation_specifiers=[
                ...         rhythmmakertools.InterpolationSpecifier(
                ...             start_duration=Duration(1, 8),
                ...             stop_duration=Duration(1, 20),
                ...             written_duration=Duration(1, 16),
                ...             ),
                ...         rhythmmakertools.InterpolationSpecifier(
                ...             start_duration=Duration(1, 20),
                ...             stop_duration=Duration(1, 8),
                ...             written_duration=Duration(1, 16),
                ...             ),
                ...         ],
                ...     tuplet_spelling_specifier=rhythmmakertools.TupletSpellingSpecifier(
                ...         use_note_duration_bracket=True,
                ...         ),
                ...     )

            ::

                >>> divisions = [(5, 8), (3, 8), (5, 8), (3, 8)]
                >>> music = maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     music,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = maker._get_rhythmic_staff(lilypond_file)
                >>> print(format(staff))
                \new RhythmicStaff {
                    {
                        \time 5/8
                        \override TupletNumber #'text = \markup {
                            \scale
                                #'(0.75 . 0.75)
                                \score
                                    {
                                        \new Score \with {
                                            \override SpacingSpanner #'spacing-increment = #0.5
                                            proportionalNotationDuration = ##f
                                        } <<
                                            \new RhythmicStaff \with {
                                                \remove Time_signature_engraver
                                                \remove Staff_symbol_engraver
                                                \override Stem #'direction = #up
                                                \override Stem #'length = #5
                                                \override TupletBracket #'bracket-visibility = ##t
                                                \override TupletBracket #'direction = #up
                                                \override TupletBracket #'padding = #1.25
                                                \override TupletBracket #'shorten-pair = #'(-1 . -1.5)
                                                \override TupletNumber #'text = #tuplet-number::calc-fraction-text
                                                tupletFullLength = ##t
                                            } {
                                                c'2 ~
                                                c'8
                                            }
                                        >>
                                        \layout {
                                            indent = #0
                                            ragged-right = ##t
                                        }
                                    }
                            }
                        \times 1/1 {
                            \once \override Beam #'grow-direction = #right
                            c'16 * 61/32 [
                            c'16 * 115/64
                            c'16 * 49/32
                            c'16 * 5/4
                            c'16 * 33/32
                            c'16 * 57/64
                            c'16 * 13/16
                            c'16 * 25/32 ]
                        }
                        \revert TupletNumber #'text
                    }
                    {
                        \time 3/8
                        \override TupletNumber #'text = \markup {
                            \scale
                                #'(0.75 . 0.75)
                                \score
                                    {
                                        \new Score \with {
                                            \override SpacingSpanner #'spacing-increment = #0.5
                                            proportionalNotationDuration = ##f
                                        } <<
                                            \new RhythmicStaff \with {
                                                \remove Time_signature_engraver
                                                \remove Staff_symbol_engraver
                                                \override Stem #'direction = #up
                                                \override Stem #'length = #5
                                                \override TupletBracket #'bracket-visibility = ##t
                                                \override TupletBracket #'direction = #up
                                                \override TupletBracket #'padding = #1.25
                                                \override TupletBracket #'shorten-pair = #'(-1 . -1.5)
                                                \override TupletNumber #'text = #tuplet-number::calc-fraction-text
                                                tupletFullLength = ##t
                                            } {
                                                c'4.
                                            }
                                        >>
                                        \layout {
                                            indent = #0
                                            ragged-right = ##t
                                        }
                                    }
                            }
                        \times 1/1 {
                            \once \override Beam #'grow-direction = #left
                            c'16 * 5/8 [
                            c'16 * 43/64
                            c'16 * 51/64
                            c'16 * 65/64
                            c'16 * 85/64
                            c'16 * 25/16 ]
                        }
                        \revert TupletNumber #'text
                    }
                    {
                        \time 5/8
                        \override TupletNumber #'text = \markup {
                            \scale
                                #'(0.75 . 0.75)
                                \score
                                    {
                                        \new Score \with {
                                            \override SpacingSpanner #'spacing-increment = #0.5
                                            proportionalNotationDuration = ##f
                                        } <<
                                            \new RhythmicStaff \with {
                                                \remove Time_signature_engraver
                                                \remove Staff_symbol_engraver
                                                \override Stem #'direction = #up
                                                \override Stem #'length = #5
                                                \override TupletBracket #'bracket-visibility = ##t
                                                \override TupletBracket #'direction = #up
                                                \override TupletBracket #'padding = #1.25
                                                \override TupletBracket #'shorten-pair = #'(-1 . -1.5)
                                                \override TupletNumber #'text = #tuplet-number::calc-fraction-text
                                                tupletFullLength = ##t
                                            } {
                                                c'2 ~
                                                c'8
                                            }
                                        >>
                                        \layout {
                                            indent = #0
                                            ragged-right = ##t
                                        }
                                    }
                            }
                        \times 1/1 {
                            \once \override Beam #'grow-direction = #right
                            c'16 * 61/32 [
                            c'16 * 115/64
                            c'16 * 49/32
                            c'16 * 5/4
                            c'16 * 33/32
                            c'16 * 57/64
                            c'16 * 13/16
                            c'16 * 25/32 ]
                        }
                        \revert TupletNumber #'text
                    }
                    {
                        \time 3/8
                        \override TupletNumber #'text = \markup {
                            \scale
                                #'(0.75 . 0.75)
                                \score
                                    {
                                        \new Score \with {
                                            \override SpacingSpanner #'spacing-increment = #0.5
                                            proportionalNotationDuration = ##f
                                        } <<
                                            \new RhythmicStaff \with {
                                                \remove Time_signature_engraver
                                                \remove Staff_symbol_engraver
                                                \override Stem #'direction = #up
                                                \override Stem #'length = #5
                                                \override TupletBracket #'bracket-visibility = ##t
                                                \override TupletBracket #'direction = #up
                                                \override TupletBracket #'padding = #1.25
                                                \override TupletBracket #'shorten-pair = #'(-1 . -1.5)
                                                \override TupletNumber #'text = #tuplet-number::calc-fraction-text
                                                tupletFullLength = ##t
                                            } {
                                                c'4.
                                            }
                                        >>
                                        \layout {
                                            indent = #0
                                            ragged-right = ##t
                                        }
                                    }
                            }
                        \times 1/1 {
                            \once \override Beam #'grow-direction = #left
                            c'16 * 5/8 [
                            c'16 * 43/64
                            c'16 * 51/64
                            c'16 * 65/64
                            c'16 * 85/64
                            c'16 * 25/16 ]
                        }
                        \revert TupletNumber #'text
                    }
                }

        ..  container:: example

            **Example 3.** Makes a single note in the case that interpolation
            would take too long for a given division:

            ::

                >>> maker = rhythmmakertools.AccelerandoRhythmMaker(
                ...     beam_specifier=rhythmmakertools.BeamSpecifier(
                ...         use_feather_beams=True,
                ...         ),
                ...     interpolation_specifiers=rhythmmakertools.InterpolationSpecifier(
                ...         start_duration=Duration(1, 8),
                ...         stop_duration=Duration(1, 20),
                ...         written_duration=Duration(1, 16),
                ...         ),
                ...     tuplet_spelling_specifier=rhythmmakertools.TupletSpellingSpecifier(
                ...         use_note_duration_bracket=True,
                ...         ),
                ...     )

            ::

                >>> divisions = [(5, 8), (3, 8), (1, 8)]
                >>> music = maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     music,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = maker._get_rhythmic_staff(lilypond_file)
                >>> print(format(staff))
                \new RhythmicStaff {
                    {
                        \time 5/8
                        \override TupletNumber #'text = \markup {
                            \scale
                                #'(0.75 . 0.75)
                                \score
                                    {
                                        \new Score \with {
                                            \override SpacingSpanner #'spacing-increment = #0.5
                                            proportionalNotationDuration = ##f
                                        } <<
                                            \new RhythmicStaff \with {
                                                \remove Time_signature_engraver
                                                \remove Staff_symbol_engraver
                                                \override Stem #'direction = #up
                                                \override Stem #'length = #5
                                                \override TupletBracket #'bracket-visibility = ##t
                                                \override TupletBracket #'direction = #up
                                                \override TupletBracket #'padding = #1.25
                                                \override TupletBracket #'shorten-pair = #'(-1 . -1.5)
                                                \override TupletNumber #'text = #tuplet-number::calc-fraction-text
                                                tupletFullLength = ##t
                                            } {
                                                c'2 ~
                                                c'8
                                            }
                                        >>
                                        \layout {
                                            indent = #0
                                            ragged-right = ##t
                                        }
                                    }
                            }
                        \times 1/1 {
                            \once \override Beam #'grow-direction = #right
                            c'16 * 61/32 [
                            c'16 * 115/64
                            c'16 * 49/32
                            c'16 * 5/4
                            c'16 * 33/32
                            c'16 * 57/64
                            c'16 * 13/16
                            c'16 * 25/32 ]
                        }
                        \revert TupletNumber #'text
                    }
                    {
                        \time 3/8
                        \override TupletNumber #'text = \markup {
                            \scale
                                #'(0.75 . 0.75)
                                \score
                                    {
                                        \new Score \with {
                                            \override SpacingSpanner #'spacing-increment = #0.5
                                            proportionalNotationDuration = ##f
                                        } <<
                                            \new RhythmicStaff \with {
                                                \remove Time_signature_engraver
                                                \remove Staff_symbol_engraver
                                                \override Stem #'direction = #up
                                                \override Stem #'length = #5
                                                \override TupletBracket #'bracket-visibility = ##t
                                                \override TupletBracket #'direction = #up
                                                \override TupletBracket #'padding = #1.25
                                                \override TupletBracket #'shorten-pair = #'(-1 . -1.5)
                                                \override TupletNumber #'text = #tuplet-number::calc-fraction-text
                                                tupletFullLength = ##t
                                            } {
                                                c'4.
                                            }
                                        >>
                                        \layout {
                                            indent = #0
                                            ragged-right = ##t
                                        }
                                    }
                            }
                        \times 1/1 {
                            \once \override Beam #'grow-direction = #right
                            c'16 * 117/64 [
                            c'16 * 99/64
                            c'16 * 69/64
                            c'16 * 13/16
                            c'16 * 47/64 ]
                        }
                        \revert TupletNumber #'text
                    }
                    {
                        \time 1/8
                        c'8
                    }
                }

        Defaults to none.

        Set to interpolation specifier or none.

        Returns interpolation specifier or none.
        '''
        return self._interpolation_specifiers

    @property
    def output_masks(self):
        r'''Gets output masks of accelerando rhythm-maker.

        ..  container:: example

            **Example 1.** No output masks:

            ::

                >>> maker = rhythmmakertools.AccelerandoRhythmMaker(
                ...     beam_specifier=rhythmmakertools.BeamSpecifier(
                ...         use_feather_beams=True,
                ...         ),
                ...     interpolation_specifiers=rhythmmakertools.InterpolationSpecifier(
                ...         start_duration=Duration(1, 8),
                ...         stop_duration=Duration(1, 20),
                ...         written_duration=Duration(1, 16),
                ...         ),
                ...     output_masks=None,
                ...     tuplet_spelling_specifier=rhythmmakertools.TupletSpellingSpecifier(
                ...         use_note_duration_bracket=True,
                ...         ),
                ...     )

            ::

                >>> divisions = [(5, 8), (3, 8), (5, 8), (3, 8)]
                >>> music = maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     music,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = maker._get_rhythmic_staff(lilypond_file)
                >>> print(format(staff))
                \new RhythmicStaff {
                    {
                        \time 5/8
                        \override TupletNumber #'text = \markup {
                            \scale
                                #'(0.75 . 0.75)
                                \score
                                    {
                                        \new Score \with {
                                            \override SpacingSpanner #'spacing-increment = #0.5
                                            proportionalNotationDuration = ##f
                                        } <<
                                            \new RhythmicStaff \with {
                                                \remove Time_signature_engraver
                                                \remove Staff_symbol_engraver
                                                \override Stem #'direction = #up
                                                \override Stem #'length = #5
                                                \override TupletBracket #'bracket-visibility = ##t
                                                \override TupletBracket #'direction = #up
                                                \override TupletBracket #'padding = #1.25
                                                \override TupletBracket #'shorten-pair = #'(-1 . -1.5)
                                                \override TupletNumber #'text = #tuplet-number::calc-fraction-text
                                                tupletFullLength = ##t
                                            } {
                                                c'2 ~
                                                c'8
                                            }
                                        >>
                                        \layout {
                                            indent = #0
                                            ragged-right = ##t
                                        }
                                    }
                            }
                        \times 1/1 {
                            \once \override Beam #'grow-direction = #right
                            c'16 * 61/32 [
                            c'16 * 115/64
                            c'16 * 49/32
                            c'16 * 5/4
                            c'16 * 33/32
                            c'16 * 57/64
                            c'16 * 13/16
                            c'16 * 25/32 ]
                        }
                        \revert TupletNumber #'text
                    }
                    {
                        \time 3/8
                        \override TupletNumber #'text = \markup {
                            \scale
                                #'(0.75 . 0.75)
                                \score
                                    {
                                        \new Score \with {
                                            \override SpacingSpanner #'spacing-increment = #0.5
                                            proportionalNotationDuration = ##f
                                        } <<
                                            \new RhythmicStaff \with {
                                                \remove Time_signature_engraver
                                                \remove Staff_symbol_engraver
                                                \override Stem #'direction = #up
                                                \override Stem #'length = #5
                                                \override TupletBracket #'bracket-visibility = ##t
                                                \override TupletBracket #'direction = #up
                                                \override TupletBracket #'padding = #1.25
                                                \override TupletBracket #'shorten-pair = #'(-1 . -1.5)
                                                \override TupletNumber #'text = #tuplet-number::calc-fraction-text
                                                tupletFullLength = ##t
                                            } {
                                                c'4.
                                            }
                                        >>
                                        \layout {
                                            indent = #0
                                            ragged-right = ##t
                                        }
                                    }
                            }
                        \times 1/1 {
                            \once \override Beam #'grow-direction = #right
                            c'16 * 117/64 [
                            c'16 * 99/64
                            c'16 * 69/64
                            c'16 * 13/16
                            c'16 * 47/64 ]
                        }
                        \revert TupletNumber #'text
                    }
                    {
                        \time 5/8
                        \override TupletNumber #'text = \markup {
                            \scale
                                #'(0.75 . 0.75)
                                \score
                                    {
                                        \new Score \with {
                                            \override SpacingSpanner #'spacing-increment = #0.5
                                            proportionalNotationDuration = ##f
                                        } <<
                                            \new RhythmicStaff \with {
                                                \remove Time_signature_engraver
                                                \remove Staff_symbol_engraver
                                                \override Stem #'direction = #up
                                                \override Stem #'length = #5
                                                \override TupletBracket #'bracket-visibility = ##t
                                                \override TupletBracket #'direction = #up
                                                \override TupletBracket #'padding = #1.25
                                                \override TupletBracket #'shorten-pair = #'(-1 . -1.5)
                                                \override TupletNumber #'text = #tuplet-number::calc-fraction-text
                                                tupletFullLength = ##t
                                            } {
                                                c'2 ~
                                                c'8
                                            }
                                        >>
                                        \layout {
                                            indent = #0
                                            ragged-right = ##t
                                        }
                                    }
                            }
                        \times 1/1 {
                            \once \override Beam #'grow-direction = #right
                            c'16 * 61/32 [
                            c'16 * 115/64
                            c'16 * 49/32
                            c'16 * 5/4
                            c'16 * 33/32
                            c'16 * 57/64
                            c'16 * 13/16
                            c'16 * 25/32 ]
                        }
                        \revert TupletNumber #'text
                    }
                    {
                        \time 3/8
                        \override TupletNumber #'text = \markup {
                            \scale
                                #'(0.75 . 0.75)
                                \score
                                    {
                                        \new Score \with {
                                            \override SpacingSpanner #'spacing-increment = #0.5
                                            proportionalNotationDuration = ##f
                                        } <<
                                            \new RhythmicStaff \with {
                                                \remove Time_signature_engraver
                                                \remove Staff_symbol_engraver
                                                \override Stem #'direction = #up
                                                \override Stem #'length = #5
                                                \override TupletBracket #'bracket-visibility = ##t
                                                \override TupletBracket #'direction = #up
                                                \override TupletBracket #'padding = #1.25
                                                \override TupletBracket #'shorten-pair = #'(-1 . -1.5)
                                                \override TupletNumber #'text = #tuplet-number::calc-fraction-text
                                                tupletFullLength = ##t
                                            } {
                                                c'4.
                                            }
                                        >>
                                        \layout {
                                            indent = #0
                                            ragged-right = ##t
                                        }
                                    }
                            }
                        \times 1/1 {
                            \once \override Beam #'grow-direction = #right
                            c'16 * 117/64 [
                            c'16 * 99/64
                            c'16 * 69/64
                            c'16 * 13/16
                            c'16 * 47/64 ]
                        }
                        \revert TupletNumber #'text
                    }
                }

        ..  container:: example

            **Example 2.** Silences every other division:

            ::

                >>> maker = rhythmmakertools.AccelerandoRhythmMaker(
                ...     beam_specifier=rhythmmakertools.BeamSpecifier(
                ...         use_feather_beams=True,
                ...         ),
                ...     interpolation_specifiers=rhythmmakertools.InterpolationSpecifier(
                ...         start_duration=Duration(1, 8),
                ...         stop_duration=Duration(1, 20),
                ...         written_duration=Duration(1, 16),
                ...         ),
                ...     output_masks=[
                ...         rhythmmakertools.SilenceMask(
                ...             indices=[1],
                ...             period=2,
                ...             ),
                ...         ],
                ...     tuplet_spelling_specifier=rhythmmakertools.TupletSpellingSpecifier(
                ...         use_note_duration_bracket=True,
                ...         ),
                ...     )

            ::

                >>> divisions = [(5, 8), (3, 8), (5, 8), (3, 8)]
                >>> music = maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     music,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = maker._get_rhythmic_staff(lilypond_file)
                >>> print(format(staff))
                \new RhythmicStaff {
                    {
                        \time 5/8
                        \override TupletNumber #'text = \markup {
                            \scale
                                #'(0.75 . 0.75)
                                \score
                                    {
                                        \new Score \with {
                                            \override SpacingSpanner #'spacing-increment = #0.5
                                            proportionalNotationDuration = ##f
                                        } <<
                                            \new RhythmicStaff \with {
                                                \remove Time_signature_engraver
                                                \remove Staff_symbol_engraver
                                                \override Stem #'direction = #up
                                                \override Stem #'length = #5
                                                \override TupletBracket #'bracket-visibility = ##t
                                                \override TupletBracket #'direction = #up
                                                \override TupletBracket #'padding = #1.25
                                                \override TupletBracket #'shorten-pair = #'(-1 . -1.5)
                                                \override TupletNumber #'text = #tuplet-number::calc-fraction-text
                                                tupletFullLength = ##t
                                            } {
                                                c'2 ~
                                                c'8
                                            }
                                        >>
                                        \layout {
                                            indent = #0
                                            ragged-right = ##t
                                        }
                                    }
                            }
                        \times 1/1 {
                            \once \override Beam #'grow-direction = #right
                            c'16 * 61/32 [
                            c'16 * 115/64
                            c'16 * 49/32
                            c'16 * 5/4
                            c'16 * 33/32
                            c'16 * 57/64
                            c'16 * 13/16
                            c'16 * 25/32 ]
                        }
                        \revert TupletNumber #'text
                    }
                    {
                        \time 3/8
                        r4.
                    }
                    {
                        \time 5/8
                        \override TupletNumber #'text = \markup {
                            \scale
                                #'(0.75 . 0.75)
                                \score
                                    {
                                        \new Score \with {
                                            \override SpacingSpanner #'spacing-increment = #0.5
                                            proportionalNotationDuration = ##f
                                        } <<
                                            \new RhythmicStaff \with {
                                                \remove Time_signature_engraver
                                                \remove Staff_symbol_engraver
                                                \override Stem #'direction = #up
                                                \override Stem #'length = #5
                                                \override TupletBracket #'bracket-visibility = ##t
                                                \override TupletBracket #'direction = #up
                                                \override TupletBracket #'padding = #1.25
                                                \override TupletBracket #'shorten-pair = #'(-1 . -1.5)
                                                \override TupletNumber #'text = #tuplet-number::calc-fraction-text
                                                tupletFullLength = ##t
                                            } {
                                                c'2 ~
                                                c'8
                                            }
                                        >>
                                        \layout {
                                            indent = #0
                                            ragged-right = ##t
                                        }
                                    }
                            }
                        \times 1/1 {
                            \once \override Beam #'grow-direction = #right
                            c'16 * 61/32 [
                            c'16 * 115/64
                            c'16 * 49/32
                            c'16 * 5/4
                            c'16 * 33/32
                            c'16 * 57/64
                            c'16 * 13/16
                            c'16 * 25/32 ]
                        }
                        \revert TupletNumber #'text
                    }
                    {
                        \time 3/8
                        r4.
                    }
                }

        '''
        superclass = super(AccelerandoRhythmMaker, self)
        return superclass.output_masks

    @property
    def tie_specifier(self):
        r'''Gets tie specifier of rhythm-maker.

        ..  container:: example

            **Example 1.** Does not tie across divisions:

            ::

                >>> maker = rhythmmakertools.AccelerandoRhythmMaker(
                ...     beam_specifier=rhythmmakertools.BeamSpecifier(
                ...         use_feather_beams=True,
                ...         ),
                ...     interpolation_specifiers=rhythmmakertools.InterpolationSpecifier(
                ...         start_duration=Duration(1, 8),
                ...         stop_duration=Duration(1, 20),
                ...         written_duration=Duration(1, 16),
                ...         ),
                ...     tie_specifier=rhythmmakertools.TieSpecifier(
                ...         tie_across_divisions=False,
                ...         ),
                ...     tuplet_spelling_specifier=rhythmmakertools.TupletSpellingSpecifier(
                ...         use_note_duration_bracket=True,
                ...         ),
                ...     )

            ::

                >>> divisions = [(5, 8), (3, 8), (5, 8), (3, 8)]
                >>> music = maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     music,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = maker._get_rhythmic_staff(lilypond_file)
                >>> print(format(staff))
                \new RhythmicStaff {
                    {
                        \time 5/8
                        \override TupletNumber #'text = \markup {
                            \scale
                                #'(0.75 . 0.75)
                                \score
                                    {
                                        \new Score \with {
                                            \override SpacingSpanner #'spacing-increment = #0.5
                                            proportionalNotationDuration = ##f
                                        } <<
                                            \new RhythmicStaff \with {
                                                \remove Time_signature_engraver
                                                \remove Staff_symbol_engraver
                                                \override Stem #'direction = #up
                                                \override Stem #'length = #5
                                                \override TupletBracket #'bracket-visibility = ##t
                                                \override TupletBracket #'direction = #up
                                                \override TupletBracket #'padding = #1.25
                                                \override TupletBracket #'shorten-pair = #'(-1 . -1.5)
                                                \override TupletNumber #'text = #tuplet-number::calc-fraction-text
                                                tupletFullLength = ##t
                                            } {
                                                c'2 ~
                                                c'8
                                            }
                                        >>
                                        \layout {
                                            indent = #0
                                            ragged-right = ##t
                                        }
                                    }
                            }
                        \times 1/1 {
                            \once \override Beam #'grow-direction = #right
                            c'16 * 61/32 [
                            c'16 * 115/64
                            c'16 * 49/32
                            c'16 * 5/4
                            c'16 * 33/32
                            c'16 * 57/64
                            c'16 * 13/16
                            c'16 * 25/32 ]
                        }
                        \revert TupletNumber #'text
                    }
                    {
                        \time 3/8
                        \override TupletNumber #'text = \markup {
                            \scale
                                #'(0.75 . 0.75)
                                \score
                                    {
                                        \new Score \with {
                                            \override SpacingSpanner #'spacing-increment = #0.5
                                            proportionalNotationDuration = ##f
                                        } <<
                                            \new RhythmicStaff \with {
                                                \remove Time_signature_engraver
                                                \remove Staff_symbol_engraver
                                                \override Stem #'direction = #up
                                                \override Stem #'length = #5
                                                \override TupletBracket #'bracket-visibility = ##t
                                                \override TupletBracket #'direction = #up
                                                \override TupletBracket #'padding = #1.25
                                                \override TupletBracket #'shorten-pair = #'(-1 . -1.5)
                                                \override TupletNumber #'text = #tuplet-number::calc-fraction-text
                                                tupletFullLength = ##t
                                            } {
                                                c'4.
                                            }
                                        >>
                                        \layout {
                                            indent = #0
                                            ragged-right = ##t
                                        }
                                    }
                            }
                        \times 1/1 {
                            \once \override Beam #'grow-direction = #right
                            c'16 * 117/64 [
                            c'16 * 99/64
                            c'16 * 69/64
                            c'16 * 13/16
                            c'16 * 47/64 ]
                        }
                        \revert TupletNumber #'text
                    }
                    {
                        \time 5/8
                        \override TupletNumber #'text = \markup {
                            \scale
                                #'(0.75 . 0.75)
                                \score
                                    {
                                        \new Score \with {
                                            \override SpacingSpanner #'spacing-increment = #0.5
                                            proportionalNotationDuration = ##f
                                        } <<
                                            \new RhythmicStaff \with {
                                                \remove Time_signature_engraver
                                                \remove Staff_symbol_engraver
                                                \override Stem #'direction = #up
                                                \override Stem #'length = #5
                                                \override TupletBracket #'bracket-visibility = ##t
                                                \override TupletBracket #'direction = #up
                                                \override TupletBracket #'padding = #1.25
                                                \override TupletBracket #'shorten-pair = #'(-1 . -1.5)
                                                \override TupletNumber #'text = #tuplet-number::calc-fraction-text
                                                tupletFullLength = ##t
                                            } {
                                                c'2 ~
                                                c'8
                                            }
                                        >>
                                        \layout {
                                            indent = #0
                                            ragged-right = ##t
                                        }
                                    }
                            }
                        \times 1/1 {
                            \once \override Beam #'grow-direction = #right
                            c'16 * 61/32 [
                            c'16 * 115/64
                            c'16 * 49/32
                            c'16 * 5/4
                            c'16 * 33/32
                            c'16 * 57/64
                            c'16 * 13/16
                            c'16 * 25/32 ]
                        }
                        \revert TupletNumber #'text
                    }
                    {
                        \time 3/8
                        \override TupletNumber #'text = \markup {
                            \scale
                                #'(0.75 . 0.75)
                                \score
                                    {
                                        \new Score \with {
                                            \override SpacingSpanner #'spacing-increment = #0.5
                                            proportionalNotationDuration = ##f
                                        } <<
                                            \new RhythmicStaff \with {
                                                \remove Time_signature_engraver
                                                \remove Staff_symbol_engraver
                                                \override Stem #'direction = #up
                                                \override Stem #'length = #5
                                                \override TupletBracket #'bracket-visibility = ##t
                                                \override TupletBracket #'direction = #up
                                                \override TupletBracket #'padding = #1.25
                                                \override TupletBracket #'shorten-pair = #'(-1 . -1.5)
                                                \override TupletNumber #'text = #tuplet-number::calc-fraction-text
                                                tupletFullLength = ##t
                                            } {
                                                c'4.
                                            }
                                        >>
                                        \layout {
                                            indent = #0
                                            ragged-right = ##t
                                        }
                                    }
                            }
                        \times 1/1 {
                            \once \override Beam #'grow-direction = #right
                            c'16 * 117/64 [
                            c'16 * 99/64
                            c'16 * 69/64
                            c'16 * 13/16
                            c'16 * 47/64 ]
                        }
                        \revert TupletNumber #'text
                    }
                }

        ..  container:: example

            **Example 2.** Ties across divisions:

            ::

                >>> maker = rhythmmakertools.AccelerandoRhythmMaker(
                ...     beam_specifier=rhythmmakertools.BeamSpecifier(
                ...         use_feather_beams=True,
                ...         ),
                ...     interpolation_specifiers=rhythmmakertools.InterpolationSpecifier(
                ...         start_duration=Duration(1, 8),
                ...         stop_duration=Duration(1, 20),
                ...         written_duration=Duration(1, 16),
                ...         ),
                ...     tie_specifier=rhythmmakertools.TieSpecifier(
                ...         tie_across_divisions=True,
                ...         ),
                ...     tuplet_spelling_specifier=rhythmmakertools.TupletSpellingSpecifier(
                ...         use_note_duration_bracket=True,
                ...         ),
                ...     )

            ::

                >>> divisions = [(5, 8), (3, 8), (5, 8), (3, 8)]
                >>> music = maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     music,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = maker._get_rhythmic_staff(lilypond_file)
                >>> print(format(staff))
                \new RhythmicStaff {
                    {
                        \time 5/8
                        \override TupletNumber #'text = \markup {
                            \scale
                                #'(0.75 . 0.75)
                                \score
                                    {
                                        \new Score \with {
                                            \override SpacingSpanner #'spacing-increment = #0.5
                                            proportionalNotationDuration = ##f
                                        } <<
                                            \new RhythmicStaff \with {
                                                \remove Time_signature_engraver
                                                \remove Staff_symbol_engraver
                                                \override Stem #'direction = #up
                                                \override Stem #'length = #5
                                                \override TupletBracket #'bracket-visibility = ##t
                                                \override TupletBracket #'direction = #up
                                                \override TupletBracket #'padding = #1.25
                                                \override TupletBracket #'shorten-pair = #'(-1 . -1.5)
                                                \override TupletNumber #'text = #tuplet-number::calc-fraction-text
                                                tupletFullLength = ##t
                                            } {
                                                c'2 ~
                                                c'8
                                            }
                                        >>
                                        \layout {
                                            indent = #0
                                            ragged-right = ##t
                                        }
                                    }
                            }
                        \times 1/1 {
                            \once \override Beam #'grow-direction = #right
                            c'16 * 61/32 [
                            c'16 * 115/64
                            c'16 * 49/32
                            c'16 * 5/4
                            c'16 * 33/32
                            c'16 * 57/64
                            c'16 * 13/16
                            c'16 * 25/32 ~ ]
                        }
                        \revert TupletNumber #'text
                    }
                    {
                        \time 3/8
                        \override TupletNumber #'text = \markup {
                            \scale
                                #'(0.75 . 0.75)
                                \score
                                    {
                                        \new Score \with {
                                            \override SpacingSpanner #'spacing-increment = #0.5
                                            proportionalNotationDuration = ##f
                                        } <<
                                            \new RhythmicStaff \with {
                                                \remove Time_signature_engraver
                                                \remove Staff_symbol_engraver
                                                \override Stem #'direction = #up
                                                \override Stem #'length = #5
                                                \override TupletBracket #'bracket-visibility = ##t
                                                \override TupletBracket #'direction = #up
                                                \override TupletBracket #'padding = #1.25
                                                \override TupletBracket #'shorten-pair = #'(-1 . -1.5)
                                                \override TupletNumber #'text = #tuplet-number::calc-fraction-text
                                                tupletFullLength = ##t
                                            } {
                                                c'4.
                                            }
                                        >>
                                        \layout {
                                            indent = #0
                                            ragged-right = ##t
                                        }
                                    }
                            }
                        \times 1/1 {
                            \once \override Beam #'grow-direction = #right
                            c'16 * 117/64 [
                            c'16 * 99/64
                            c'16 * 69/64
                            c'16 * 13/16
                            c'16 * 47/64 ~ ]
                        }
                        \revert TupletNumber #'text
                    }
                    {
                        \time 5/8
                        \override TupletNumber #'text = \markup {
                            \scale
                                #'(0.75 . 0.75)
                                \score
                                    {
                                        \new Score \with {
                                            \override SpacingSpanner #'spacing-increment = #0.5
                                            proportionalNotationDuration = ##f
                                        } <<
                                            \new RhythmicStaff \with {
                                                \remove Time_signature_engraver
                                                \remove Staff_symbol_engraver
                                                \override Stem #'direction = #up
                                                \override Stem #'length = #5
                                                \override TupletBracket #'bracket-visibility = ##t
                                                \override TupletBracket #'direction = #up
                                                \override TupletBracket #'padding = #1.25
                                                \override TupletBracket #'shorten-pair = #'(-1 . -1.5)
                                                \override TupletNumber #'text = #tuplet-number::calc-fraction-text
                                                tupletFullLength = ##t
                                            } {
                                                c'2 ~
                                                c'8
                                            }
                                        >>
                                        \layout {
                                            indent = #0
                                            ragged-right = ##t
                                        }
                                    }
                            }
                        \times 1/1 {
                            \once \override Beam #'grow-direction = #right
                            c'16 * 61/32 [
                            c'16 * 115/64
                            c'16 * 49/32
                            c'16 * 5/4
                            c'16 * 33/32
                            c'16 * 57/64
                            c'16 * 13/16
                            c'16 * 25/32 ~ ]
                        }
                        \revert TupletNumber #'text
                    }
                    {
                        \time 3/8
                        \override TupletNumber #'text = \markup {
                            \scale
                                #'(0.75 . 0.75)
                                \score
                                    {
                                        \new Score \with {
                                            \override SpacingSpanner #'spacing-increment = #0.5
                                            proportionalNotationDuration = ##f
                                        } <<
                                            \new RhythmicStaff \with {
                                                \remove Time_signature_engraver
                                                \remove Staff_symbol_engraver
                                                \override Stem #'direction = #up
                                                \override Stem #'length = #5
                                                \override TupletBracket #'bracket-visibility = ##t
                                                \override TupletBracket #'direction = #up
                                                \override TupletBracket #'padding = #1.25
                                                \override TupletBracket #'shorten-pair = #'(-1 . -1.5)
                                                \override TupletNumber #'text = #tuplet-number::calc-fraction-text
                                                tupletFullLength = ##t
                                            } {
                                                c'4.
                                            }
                                        >>
                                        \layout {
                                            indent = #0
                                            ragged-right = ##t
                                        }
                                    }
                            }
                        \times 1/1 {
                            \once \override Beam #'grow-direction = #right
                            c'16 * 117/64 [
                            c'16 * 99/64
                            c'16 * 69/64
                            c'16 * 13/16
                            c'16 * 47/64 ]
                        }
                        \revert TupletNumber #'text
                    }
                }

        ..  container:: example

            **Example 3.** Patterns ties across divisions:

            ::

                >>> pattern = rhythmmakertools.BooleanPattern(
                ...      indices=[0],
                ...      period=2,
                ...  )
                >>> maker = rhythmmakertools.AccelerandoRhythmMaker(
                ...     beam_specifier=rhythmmakertools.BeamSpecifier(
                ...         use_feather_beams=True,
                ...         ),
                ...     interpolation_specifiers=rhythmmakertools.InterpolationSpecifier(
                ...         start_duration=Duration(1, 8),
                ...         stop_duration=Duration(1, 20),
                ...         written_duration=Duration(1, 16),
                ...         ),
                ...     tie_specifier=rhythmmakertools.TieSpecifier(
                ...         tie_across_divisions=pattern,
                ...         ),
                ...     tuplet_spelling_specifier=rhythmmakertools.TupletSpellingSpecifier(
                ...         use_note_duration_bracket=True,
                ...         ),
                ...     )

            ::

                >>> divisions = [(5, 8), (3, 8), (5, 8), (3, 8)]
                >>> music = maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     music,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = maker._get_rhythmic_staff(lilypond_file)
                >>> print(format(staff))
                \new RhythmicStaff {
                    {
                        \time 5/8
                        \override TupletNumber #'text = \markup {
                            \scale
                                #'(0.75 . 0.75)
                                \score
                                    {
                                        \new Score \with {
                                            \override SpacingSpanner #'spacing-increment = #0.5
                                            proportionalNotationDuration = ##f
                                        } <<
                                            \new RhythmicStaff \with {
                                                \remove Time_signature_engraver
                                                \remove Staff_symbol_engraver
                                                \override Stem #'direction = #up
                                                \override Stem #'length = #5
                                                \override TupletBracket #'bracket-visibility = ##t
                                                \override TupletBracket #'direction = #up
                                                \override TupletBracket #'padding = #1.25
                                                \override TupletBracket #'shorten-pair = #'(-1 . -1.5)
                                                \override TupletNumber #'text = #tuplet-number::calc-fraction-text
                                                tupletFullLength = ##t
                                            } {
                                                c'2 ~
                                                c'8
                                            }
                                        >>
                                        \layout {
                                            indent = #0
                                            ragged-right = ##t
                                        }
                                    }
                            }
                        \times 1/1 {
                            \once \override Beam #'grow-direction = #right
                            c'16 * 61/32 [
                            c'16 * 115/64
                            c'16 * 49/32
                            c'16 * 5/4
                            c'16 * 33/32
                            c'16 * 57/64
                            c'16 * 13/16
                            c'16 * 25/32 ~ ]
                        }
                        \revert TupletNumber #'text
                    }
                    {
                        \time 3/8
                        \override TupletNumber #'text = \markup {
                            \scale
                                #'(0.75 . 0.75)
                                \score
                                    {
                                        \new Score \with {
                                            \override SpacingSpanner #'spacing-increment = #0.5
                                            proportionalNotationDuration = ##f
                                        } <<
                                            \new RhythmicStaff \with {
                                                \remove Time_signature_engraver
                                                \remove Staff_symbol_engraver
                                                \override Stem #'direction = #up
                                                \override Stem #'length = #5
                                                \override TupletBracket #'bracket-visibility = ##t
                                                \override TupletBracket #'direction = #up
                                                \override TupletBracket #'padding = #1.25
                                                \override TupletBracket #'shorten-pair = #'(-1 . -1.5)
                                                \override TupletNumber #'text = #tuplet-number::calc-fraction-text
                                                tupletFullLength = ##t
                                            } {
                                                c'4.
                                            }
                                        >>
                                        \layout {
                                            indent = #0
                                            ragged-right = ##t
                                        }
                                    }
                            }
                        \times 1/1 {
                            \once \override Beam #'grow-direction = #right
                            c'16 * 117/64 [
                            c'16 * 99/64
                            c'16 * 69/64
                            c'16 * 13/16
                            c'16 * 47/64 ]
                        }
                        \revert TupletNumber #'text
                    }
                    {
                        \time 5/8
                        \override TupletNumber #'text = \markup {
                            \scale
                                #'(0.75 . 0.75)
                                \score
                                    {
                                        \new Score \with {
                                            \override SpacingSpanner #'spacing-increment = #0.5
                                            proportionalNotationDuration = ##f
                                        } <<
                                            \new RhythmicStaff \with {
                                                \remove Time_signature_engraver
                                                \remove Staff_symbol_engraver
                                                \override Stem #'direction = #up
                                                \override Stem #'length = #5
                                                \override TupletBracket #'bracket-visibility = ##t
                                                \override TupletBracket #'direction = #up
                                                \override TupletBracket #'padding = #1.25
                                                \override TupletBracket #'shorten-pair = #'(-1 . -1.5)
                                                \override TupletNumber #'text = #tuplet-number::calc-fraction-text
                                                tupletFullLength = ##t
                                            } {
                                                c'2 ~
                                                c'8
                                            }
                                        >>
                                        \layout {
                                            indent = #0
                                            ragged-right = ##t
                                        }
                                    }
                            }
                        \times 1/1 {
                            \once \override Beam #'grow-direction = #right
                            c'16 * 61/32 [
                            c'16 * 115/64
                            c'16 * 49/32
                            c'16 * 5/4
                            c'16 * 33/32
                            c'16 * 57/64
                            c'16 * 13/16
                            c'16 * 25/32 ~ ]
                        }
                        \revert TupletNumber #'text
                    }
                    {
                        \time 3/8
                        \override TupletNumber #'text = \markup {
                            \scale
                                #'(0.75 . 0.75)
                                \score
                                    {
                                        \new Score \with {
                                            \override SpacingSpanner #'spacing-increment = #0.5
                                            proportionalNotationDuration = ##f
                                        } <<
                                            \new RhythmicStaff \with {
                                                \remove Time_signature_engraver
                                                \remove Staff_symbol_engraver
                                                \override Stem #'direction = #up
                                                \override Stem #'length = #5
                                                \override TupletBracket #'bracket-visibility = ##t
                                                \override TupletBracket #'direction = #up
                                                \override TupletBracket #'padding = #1.25
                                                \override TupletBracket #'shorten-pair = #'(-1 . -1.5)
                                                \override TupletNumber #'text = #tuplet-number::calc-fraction-text
                                                tupletFullLength = ##t
                                            } {
                                                c'4.
                                            }
                                        >>
                                        \layout {
                                            indent = #0
                                            ragged-right = ##t
                                        }
                                    }
                            }
                        \times 1/1 {
                            \once \override Beam #'grow-direction = #right
                            c'16 * 117/64 [
                            c'16 * 99/64
                            c'16 * 69/64
                            c'16 * 13/16
                            c'16 * 47/64 ]
                        }
                        \revert TupletNumber #'text
                    }
                }

        Returns tie specifier.
        '''
        superclass = super(AccelerandoRhythmMaker, self)
        return superclass.tie_specifier

    @property
    def tuplet_spelling_specifier(self):
        r'''Gets tuplet spelling specifier of accelerando rhythm-maker.

        ..  container:: example

            **Example 1.** Tuplets use note duration bracket:

            ::

                >>> maker = rhythmmakertools.AccelerandoRhythmMaker(
                ...     beam_specifier=rhythmmakertools.BeamSpecifier(
                ...         use_feather_beams=True,
                ...         ),
                ...     interpolation_specifiers=rhythmmakertools.InterpolationSpecifier(
                ...         start_duration=Duration(1, 8),
                ...         stop_duration=Duration(1, 20),
                ...         written_duration=Duration(1, 16),
                ...         ),
                ...     tie_specifier=rhythmmakertools.TieSpecifier(
                ...         tie_across_divisions=False,
                ...         ),
                ...     tuplet_spelling_specifier=rhythmmakertools.TupletSpellingSpecifier(
                ...         use_note_duration_bracket=True,
                ...         ),
                ...     )

            ::

                >>> divisions = [(5, 8), (3, 8), (5, 8), (3, 8)]
                >>> music = maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     music,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = maker._get_rhythmic_staff(lilypond_file)
                >>> print(format(staff))
                \new RhythmicStaff {
                    {
                        \time 5/8
                        \override TupletNumber #'text = \markup {
                            \scale
                                #'(0.75 . 0.75)
                                \score
                                    {
                                        \new Score \with {
                                            \override SpacingSpanner #'spacing-increment = #0.5
                                            proportionalNotationDuration = ##f
                                        } <<
                                            \new RhythmicStaff \with {
                                                \remove Time_signature_engraver
                                                \remove Staff_symbol_engraver
                                                \override Stem #'direction = #up
                                                \override Stem #'length = #5
                                                \override TupletBracket #'bracket-visibility = ##t
                                                \override TupletBracket #'direction = #up
                                                \override TupletBracket #'padding = #1.25
                                                \override TupletBracket #'shorten-pair = #'(-1 . -1.5)
                                                \override TupletNumber #'text = #tuplet-number::calc-fraction-text
                                                tupletFullLength = ##t
                                            } {
                                                c'2 ~
                                                c'8
                                            }
                                        >>
                                        \layout {
                                            indent = #0
                                            ragged-right = ##t
                                        }
                                    }
                            }
                        \times 1/1 {
                            \once \override Beam #'grow-direction = #right
                            c'16 * 61/32 [
                            c'16 * 115/64
                            c'16 * 49/32
                            c'16 * 5/4
                            c'16 * 33/32
                            c'16 * 57/64
                            c'16 * 13/16
                            c'16 * 25/32 ]
                        }
                        \revert TupletNumber #'text
                    }
                    {
                        \time 3/8
                        \override TupletNumber #'text = \markup {
                            \scale
                                #'(0.75 . 0.75)
                                \score
                                    {
                                        \new Score \with {
                                            \override SpacingSpanner #'spacing-increment = #0.5
                                            proportionalNotationDuration = ##f
                                        } <<
                                            \new RhythmicStaff \with {
                                                \remove Time_signature_engraver
                                                \remove Staff_symbol_engraver
                                                \override Stem #'direction = #up
                                                \override Stem #'length = #5
                                                \override TupletBracket #'bracket-visibility = ##t
                                                \override TupletBracket #'direction = #up
                                                \override TupletBracket #'padding = #1.25
                                                \override TupletBracket #'shorten-pair = #'(-1 . -1.5)
                                                \override TupletNumber #'text = #tuplet-number::calc-fraction-text
                                                tupletFullLength = ##t
                                            } {
                                                c'4.
                                            }
                                        >>
                                        \layout {
                                            indent = #0
                                            ragged-right = ##t
                                        }
                                    }
                            }
                        \times 1/1 {
                            \once \override Beam #'grow-direction = #right
                            c'16 * 117/64 [
                            c'16 * 99/64
                            c'16 * 69/64
                            c'16 * 13/16
                            c'16 * 47/64 ]
                        }
                        \revert TupletNumber #'text
                    }
                    {
                        \time 5/8
                        \override TupletNumber #'text = \markup {
                            \scale
                                #'(0.75 . 0.75)
                                \score
                                    {
                                        \new Score \with {
                                            \override SpacingSpanner #'spacing-increment = #0.5
                                            proportionalNotationDuration = ##f
                                        } <<
                                            \new RhythmicStaff \with {
                                                \remove Time_signature_engraver
                                                \remove Staff_symbol_engraver
                                                \override Stem #'direction = #up
                                                \override Stem #'length = #5
                                                \override TupletBracket #'bracket-visibility = ##t
                                                \override TupletBracket #'direction = #up
                                                \override TupletBracket #'padding = #1.25
                                                \override TupletBracket #'shorten-pair = #'(-1 . -1.5)
                                                \override TupletNumber #'text = #tuplet-number::calc-fraction-text
                                                tupletFullLength = ##t
                                            } {
                                                c'2 ~
                                                c'8
                                            }
                                        >>
                                        \layout {
                                            indent = #0
                                            ragged-right = ##t
                                        }
                                    }
                            }
                        \times 1/1 {
                            \once \override Beam #'grow-direction = #right
                            c'16 * 61/32 [
                            c'16 * 115/64
                            c'16 * 49/32
                            c'16 * 5/4
                            c'16 * 33/32
                            c'16 * 57/64
                            c'16 * 13/16
                            c'16 * 25/32 ]
                        }
                        \revert TupletNumber #'text
                    }
                    {
                        \time 3/8
                        \override TupletNumber #'text = \markup {
                            \scale
                                #'(0.75 . 0.75)
                                \score
                                    {
                                        \new Score \with {
                                            \override SpacingSpanner #'spacing-increment = #0.5
                                            proportionalNotationDuration = ##f
                                        } <<
                                            \new RhythmicStaff \with {
                                                \remove Time_signature_engraver
                                                \remove Staff_symbol_engraver
                                                \override Stem #'direction = #up
                                                \override Stem #'length = #5
                                                \override TupletBracket #'bracket-visibility = ##t
                                                \override TupletBracket #'direction = #up
                                                \override TupletBracket #'padding = #1.25
                                                \override TupletBracket #'shorten-pair = #'(-1 . -1.5)
                                                \override TupletNumber #'text = #tuplet-number::calc-fraction-text
                                                tupletFullLength = ##t
                                            } {
                                                c'4.
                                            }
                                        >>
                                        \layout {
                                            indent = #0
                                            ragged-right = ##t
                                        }
                                    }
                            }
                        \times 1/1 {
                            \once \override Beam #'grow-direction = #right
                            c'16 * 117/64 [
                            c'16 * 99/64
                            c'16 * 69/64
                            c'16 * 13/16
                            c'16 * 47/64 ]
                        }
                        \revert TupletNumber #'text
                    }
                }

        ..  container:: example

            **Example 2.** Tuplets do not use note duration bracket:

            ::

                >>> maker = rhythmmakertools.AccelerandoRhythmMaker(
                ...     beam_specifier=rhythmmakertools.BeamSpecifier(
                ...         use_feather_beams=True,
                ...         ),
                ...     interpolation_specifiers=rhythmmakertools.InterpolationSpecifier(
                ...         start_duration=Duration(1, 8),
                ...         stop_duration=Duration(1, 20),
                ...         written_duration=Duration(1, 16),
                ...         ),
                ...     tie_specifier=rhythmmakertools.TieSpecifier(
                ...         tie_across_divisions=False,
                ...         ),
                ...     tuplet_spelling_specifier=rhythmmakertools.TupletSpellingSpecifier(
                ...         use_note_duration_bracket=False,
                ...         ),
                ...     )

            ::

                >>> divisions = [(5, 8), (3, 8), (5, 8), (3, 8)]
                >>> music = maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     music,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = maker._get_rhythmic_staff(lilypond_file)
                >>> print(format(staff))
                \new RhythmicStaff {
                    {
                        \time 5/8
                        {
                            \once \override Beam #'grow-direction = #right
                            c'16 * 61/32 [
                            c'16 * 115/64
                            c'16 * 49/32
                            c'16 * 5/4
                            c'16 * 33/32
                            c'16 * 57/64
                            c'16 * 13/16
                            c'16 * 25/32 ]
                        }
                    }
                    {
                        \time 3/8
                        {
                            \once \override Beam #'grow-direction = #right
                            c'16 * 117/64 [
                            c'16 * 99/64
                            c'16 * 69/64
                            c'16 * 13/16
                            c'16 * 47/64 ]
                        }
                    }
                    {
                        \time 5/8
                        {
                            \once \override Beam #'grow-direction = #right
                            c'16 * 61/32 [
                            c'16 * 115/64
                            c'16 * 49/32
                            c'16 * 5/4
                            c'16 * 33/32
                            c'16 * 57/64
                            c'16 * 13/16
                            c'16 * 25/32 ]
                        }
                    }
                    {
                        \time 3/8
                        {
                            \once \override Beam #'grow-direction = #right
                            c'16 * 117/64 [
                            c'16 * 99/64
                            c'16 * 69/64
                            c'16 * 13/16
                            c'16 * 47/64 ]
                        }
                    }
                }

        Returns tuplet spelling specifier or none.
        '''
        superclass = super(AccelerandoRhythmMaker, self)
        return superclass.tuplet_spelling_specifier