# -*- encoding: utf-8 -*-
import math
from abjad.tools import datastructuretools
from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import scoretools
from abjad.tools import selectiontools
from abjad.tools import sequencetools
from abjad.tools import spannertools
from abjad.tools.rhythmmakertools.RhythmMaker import RhythmMaker
from abjad.tools.topleveltools import attach
from abjad.tools.topleveltools import detach
from abjad.tools.topleveltools import new


class AccelerandoRhythmMaker(RhythmMaker):
    r'''Accelerando rhythm-maker.

    ..  container:: example

        **Example 1.** Makes an accelerando for each input division:

        ::

            >>> maker = rhythmmakertools.AccelerandoRhythmMaker(
            ...     start_duration=Duration(1, 8),
            ...     stop_duration=Duration(1, 20),
            ...     written_duration=Duration(1, 8),
            ...     )

        ::

            >>> divisions = [(5, 8), (3, 8)]
            >>> music = maker(divisions)
            >>> lilypond_file = rhythmmakertools.make_lilypond_file(
            ...     music,
            ...     divisions,
            ...     )
            >>> show(lilypond_file) # doctest: +SKIP

        ..  doctest::

            >>> staff = maker._get_rhythmic_staff(lilypond_file)
            >>> f(staff)
            \new RhythmicStaff {
                {
                    \time 5/8
                    c'8 * 61/64 [
                    c'8 * 115/128
                    c'8 * 49/64
                    c'8 * 5/8
                    c'8 * 33/64
                    c'8 * 57/128
                    c'8 * 13/32
                    c'8 * 25/64 ]
                }
                {
                    \time 3/8
                    c'8 * 117/128 [
                    c'8 * 99/128
                    c'8 * 69/128
                    c'8 * 13/32
                    c'8 * 47/128 ]
                }
            }

    ..  container:: example

        **Example 2.** Makes a ritardando for each input division:

        ::

            >>> maker = rhythmmakertools.AccelerandoRhythmMaker(
            ...     start_duration=Duration(1, 20),
            ...     stop_duration=Duration(1, 8),
            ...     written_duration=Duration(1, 8),
            ...     )

        ::

            >>> divisions = [(5, 8), (3, 8)]
            >>> music = maker(divisions)
            >>> lilypond_file = rhythmmakertools.make_lilypond_file(
            ...     music,
            ...     divisions,
            ...     )
            >>> show(lilypond_file) # doctest: +SKIP

        ..  doctest::

            >>> staff = maker._get_rhythmic_staff(lilypond_file)
            >>> f(staff)
            \new RhythmicStaff {
                {
                    \time 5/8
                    c'8 * 45/128 [
                    c'8 * 23/64
                    c'8 * 25/64
                    c'8 * 55/128
                    c'8 * 1/2
                    c'8 * 75/128
                    c'8 * 89/128
                    c'8 * 103/128
                    c'8 * 113/128 ]
                }
                {
                    \time 3/8
                    c'8 * 5/16 [
                    c'8 * 43/128
                    c'8 * 51/128
                    c'8 * 65/128
                    c'8 * 85/128
                    c'8 * 25/32 ]
                }
            }

    Usage follows the two-step configure-once / call-repeatedly pattern shown
    here.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_exponent',
        '_start_duration',
        '_stop_duration',
        '_written_duration',
        )

    _class_name_abbreviation = 'Acc'

    _human_readable_class_name = 'accelerando rhythm-maker'

    ### INITIALIZER ###

    def __init__(
        self,
        beam_specifier=None,
        duration_spelling_specifier=None,
        output_masks=None,
        start_duration=None,
        stop_duration=None,
        tie_specifier=None,
        tuplet_spelling_specifier=None,
        written_duration=None,
        ):
        from abjad.tools import rhythmmakertools
        RhythmMaker.__init__(
            self,
            beam_specifier=beam_specifier,
            duration_spelling_specifier=duration_spelling_specifier,
            output_masks=output_masks,
            tie_specifier=tie_specifier,
            tuplet_spelling_specifier=tuplet_spelling_specifier,
            )
        start_duration = durationtools.Duration(start_duration)
        self._start_duration = start_duration
        stop_duration = durationtools.Duration(stop_duration)
        self._stop_duration = stop_duration
        written_duration = durationtools.Duration(written_duration)
        self._written_duration = written_duration

    ### SPECIAL METHODS ###

    def __call__(self, divisions, seeds=None):
        r'''Calls interpolated rhythm-maker on `divisions`.

        Ignores `seeds`.

        Returns list of selections.
        '''
        return RhythmMaker.__call__(
            self,
            divisions,
            seeds=seeds,
            )

    ### PRIVATE METHODS ###

    def _fix_rounding_error(self, selection, total_duration):
        selection_duration = selection.get_duration()
        if not selection_duration == total_duration:
            needed_duration = total_duration - selection[:-1].get_duration()
            multiplier = needed_duration / self.written_duration
            multiplier = durationtools.Multiplier(multiplier)
            detach(durationtools.Multiplier, selection[-1])
            attach(multiplier, selection[-1])

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
        if total_duration <=0 :
            message = "Total duration must be positive."
            raise ValueError(message)
        if start_duration <= 0 or stop_duration <= 0:
            message = "Both 'start_duration' and 'stop_duration'"
            message += ' must be positive.'
            raise ValueError(message)
        if total_duration < (stop_duration + start_duration):
            message = "'start_duration' + 'stop_duration'"
            message += " must be < 'total_duration'."
            raise ValueError(message)
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
                reference_durations[i+1], 
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

    def _make_accelerando(self, total_duration):
        r'''Makes notes with LilyPond multipliers.

        Returns as many interpolation values as necessary to fill `total` 
        duration requested.

        Computes duration multipliers interpolated from `start` to `stop`.

        Sets note durations to `written_duration` multiplied by interpolation
        multipliers.

        Returns selection of notes.
        '''
        total_duration = durationtools.Duration(total_duration)
        durations = AccelerandoRhythmMaker._interpolate_divide(
            total_duration=total_duration,
            start_duration=self.start_duration,
            stop_duration=self.stop_duration,
            )
        durations = [
            durationtools.Duration(int(round(_ * 2**10)), 2**10) 
            for _ in durations
            ]
        notes = []
        for i, duration in enumerate(durations):
            note = scoretools.Note(0, self.written_duration)
            multiplier = duration / self.written_duration
            multiplier = durationtools.Multiplier(multiplier)
            attach(multiplier, note)
            notes.append(note)
        selection = selectiontools.Selection(notes)
        self._fix_rounding_error(selection, total_duration)
        pair = (selection.get_duration(), total_duration)
        assert pair[0] == pair[1], repr(pair)
        return selection

    def _make_music(self, divisions, seeds):
        selections = []
        for i, division in enumerate(divisions):
            accelerando = self._make_accelerando(division)
            selections.append(accelerando)
        self._apply_beam_specifier(selections)
        selections = self._apply_output_masks(selections, seeds)
        return selections

    ### PUBLIC PROPERTIES ###

    @property
    def start_duration(self):
        r'''Gets start duration of accelerando rhythm-maker.
        '''
        return self._start_duration

    @property
    def stop_duration(self):
        r'''Gets stop duration of accelerando rhythm-maker.
        '''
        return self._stop_duration

    @property
    def written_duration(self):
        r'''Gets written duration of accelerando rhythm-maker.
        '''
        return self._written_duration