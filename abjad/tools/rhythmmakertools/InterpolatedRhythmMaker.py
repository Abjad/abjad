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
from abjad.tools.topleveltools import new


class InterpolatedRhythmMaker(RhythmMaker):
    r'''Interpolated rhythm-maker.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_exponent',
        '_start_duration',
        '_stop_duration',
        '_total_duration',
        '_written_duration',
        )

    _class_name_abbreviation = 'Int'

    _human_readable_class_name = 'interpolated rhythm-maker'

    ### INITIALIZER ###

    def __init__(
        self,
        beam_specifier=None,
        duration_spelling_specifier=None,
        output_masks=None,
        tie_specifier=None,
        tuplet_spelling_specifier=None,
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

    @staticmethod
    def _interpolate_cosine(y1, y2, mu):
        r'''Perorms cosine interpolation of `y1` and `y2` with `mu` ``[0, 1]``
        normalized:

        ::

            >>> rhythmmakertools.InterpolatedRhythmMaker._interpolate_cosine(
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

            >>> rhythmmakertools.InterpolatedRhythmMaker._interpolate_divide(
            ...     total_duration=10,
            ...     start_duration=1,
            ...     stop_duration=1,
            ...     exponent=1,
            ...     )
            [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
            >>> sum(_)
            10.0

        ::

            >>> rhythmmakertools.InterpolatedRhythmMaker._interpolate_divide(
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
                duration = InterpolatedRhythmMaker._interpolate_cosine(
                    start_duration, 
                    stop_duration, 
                    partial_sum / total_duration,
                    )
            else:
                duration = InterpolatedRhythmMaker._interpolate_exponential(
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

            >>> durations = rhythmmakertools.InterpolatedRhythmMaker._interpolate_divide_multiple(
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
            durations_ = InterpolatedRhythmMaker._interpolate_divide(
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

            >>> rhythmmakertools.InterpolatedRhythmMaker._interpolate_exponential(
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

    #def _make_music(self, divisions, seeds):
    @staticmethod
    def _make_music(
        start_duration=None,
        stop_duration=None,
        total_duration=None,
        written_duration=None,
        ):
        r'''Makes accelerating notes with LilyPond multipliers:

        ::

            >>> notes = rhythmmakertools.InterpolatedRhythmMaker._make_music(
            ...     start_duration=Duration(1, 4),
            ...     stop_duration=Duration(1, 16),
            ...     total_duration=Duration(4, 4),
            ...     written_duration=Duration(1, 8),
            ...     )

        ::

            >>> staff = Staff(notes)
            >>> attach(Beam(), staff[:])
            >>> attach(Slur(), staff[:])

        ::

            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> f(staff)
            \new Staff {
                c'8 * 245/128 [ (
                c'8 * 109/64
                c'8 * 161/128
                c'8 * 115/128
                c'8 * 87/128
                c'8 * 9/16
                c'8 * 1/2
                c'8 * 61/128 ] )
            }

        Returns as many interpolation values as necessary to fill `total` 
        duration requested.

        Computes duration multipliers interpolated from `start` to `stop`.

        Sets note durations to `written_duration` multiplied by interpolation
        multipliers.

        Returns selection of notes.
        '''
        total_duration = durationtools.Duration(total_duration)
        start_duration = durationtools.Duration(start_duration)
        stop_duration = durationtools.Duration(stop_duration)
        written_duration = durationtools.Duration(written_duration)
        multipliers = InterpolatedRhythmMaker._interpolate_divide(
            total_duration=total_duration,
            start_duration=start_duration,
            stop_duration=stop_duration,
            )
        multipliers = [
            durationtools.Multiplier(int(round(_ * 2**10)), 2**10) 
            for _ in multipliers
            ]
        notes = []
        for i, multiplier in enumerate(multipliers):
            note = scoretools.Note(0, written_duration)
            multiplier = multiplier / written_duration
            multiplier = durationtools.Multiplier(multiplier)
            attach(multiplier, note)
            notes.append(note)
        selection = selectiontools.Selection(notes)
        return selection