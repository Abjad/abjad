# -*- encoding: utf-8 -*-
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

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    _class_name_abbreviation = 'S'

    _human_readable_class_name = 'skip rhythm-maker'

    ### SPECIAL METHODS ###

    def __call__(self, divisions, seeds=None):
        r'''Calls skip rhythm-maker on `divisions`.

        Returns list of skips.
        '''
        return RhythmMaker.__call__(
            self,
            divisions,
            seeds=seeds,
            )

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
                    tie_across_divisions=False,
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
                    tie_across_divisions=False,
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

    ### PRIVATE METHODS ###

    def _make_music(self, duration_pairs, seeds):
        result = []
        for duration_pair in duration_pairs:
            written_duration = durationtools.Duration(1)
            multiplied_duration = duration_pair
            skip = scoretools.make_skips_with_multiplied_durations(
                written_duration, [multiplied_duration])
            result.append(skip)
        return result

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
                    decrease_durations_monotonically=False,
                    tie_across_divisions=False,
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
