# -*- encoding: utf-8 -*-
import fractions
from abjad.tools import durationtools
from abjad.tools import scoretools
from abjad.tools.rhythmmakertools.RhythmMaker import RhythmMaker


class SkipRhythmMaker(RhythmMaker):
    r'''Skip rhythm-maker.

    ..  container:: example

        Makes skips equal to the duration of input divisions.

        ::

            >>> maker = rhythmmakertools.SkipRhythmMaker()

        ::

            >>> divisions = [(1, 4), (3, 16), (5, 8)]
            >>> music = maker(divisions)
            >>> lilypond_file = rhythmmakertools.make_lilypond_file(
            ...     music,
            ...     divisions,
            ...     )
            >>> show(lilypond_file) # doctest: +SKIP

    Usage follows the two-step configure-then-call pattern shown here.
    '''

    ### SPECIAL METHODS ###

    def __call__(self, divisions, seeds=None):
        r'''Calls skip rhythm-maker on `divisions`.

        Returns list of skips.
        '''
        result = []
        for division in divisions:
            written_duration = durationtools.Duration(1)
            multiplied_duration = division
            skip = scoretools.make_skips_with_multiplied_durations(
                written_duration, [multiplied_duration])
            result.append(skip)
        return result

    def __format__(self, format_specification=''):
        r'''Formats skip rhythm-maker.

        Set `format_specification` to `''` or `'storage'`.

        ..  container:: example

            ::

                >>> print format(maker)
                rhythmmakertools.SkipRhythmMaker(
                    beam_cells_together=False,
                    beam_each_cell=True,
                    decrease_durations_monotonically=True,
                    )

        Returns string.
        '''
        superclass = super(SkipRhythmMaker, self)
        return superclass.__format__(format_specification=format_specification)

    def __makenew__(self, *args, **kwargs):
        r'''Makes new skip rhythm-maker with `kwargs`.

        ..  container:: example

            ::

                >>> new_maker = new(maker)

            ::

                >>> print format(new_maker)
                rhythmmakertools.SkipRhythmMaker(
                    beam_cells_together=False,
                    beam_each_cell=True,
                    decrease_durations_monotonically=True,
                    )

            ::

                >>> divisions = [(1, 4), (3, 16), (5, 8)]
                >>> music = maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     music,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

        Returns new skip rhythm-maker.
        '''
        return RhythmMaker.__makenew__(self, *args, **kwargs)

    ### PUBLIC METHODS ###

    def reverse(self):
        r'''Reverses skip rhythm-maker.

        ..  container:: example

            ::

                >>> reversed_maker = maker.reverse()

            ::

                >>> print format(reversed_maker)
                rhythmmakertools.SkipRhythmMaker(
                    beam_cells_together=False,
                    beam_each_cell=True,
                    decrease_durations_monotonically=True,
                    )

            ::

                >>> divisions = [(1, 4), (3, 16), (5, 8)]
                >>> music = maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     music,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

        Returns new skip rhythm-maker.
        '''
        return RhythmMaker.reverse(self)
