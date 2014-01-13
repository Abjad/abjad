# -*- encoding: utf-8 -*-
from abjad.tools import mathtools
from abjad.tools import sequencetools
from abjad.tools.rhythmmakertools.TaleaRhythmMaker \
	import TaleaRhythmMaker


class DivisionBurnishedTaleaRhythmMaker(TaleaRhythmMaker):
    r'''Division-burnished talea rhythm-maker.

    ..  container:: example

        ::

            >>> maker = rhythmmakertools.DivisionBurnishedTaleaRhythmMaker(
            ...     talea=(1, 1, 2, 4),
            ...     talea_denominator=16,
            ...     prolation_addenda=(0, 3),
            ...     lefts=(-1,),
            ...     middles=(0,),
            ...     rights=(-1,),
            ...     left_lengths=(1,),
            ...     right_lengths=(1,),
            ...     secondary_divisions=(14,),
            ...     )

        ::

            >>> divisions = [(5, 8), (5, 8)]
            >>> music = maker(divisions)
            >>> music = sequencetools.flatten_sequence(music)
            >>> measures = scoretools.make_spacer_skip_measures(divisions)
            >>> staff = scoretools.RhythmicStaff(measures)
            >>> measures = mutate(staff).replace_measure_contents(music)
            >>> show(staff) # doctest: +SKIP

    Usage follows the two-step configure-then-call pattern shown here.
    '''

    ### CLASS VARIABLES ###

    _burnish_divisions = True

    ### SPECIAL METHODS ###

    def __format__(self, format_specification=''):
        r'''Formats division-burnished talea rhythm-maker.

        Set `format_specification` to `''` or `'storage'`.

        ::

            >>> print format(maker)
            rhythmmakertools.DivisionBurnishedTaleaRhythmMaker(
                talea=(1, 1, 2, 4),
                talea_denominator=16,
                prolation_addenda=(0, 3),
                lefts=(-1,),
                middles=(0,),
                rights=(-1,),
                left_lengths=(1,),
                right_lengths=(1,),
                secondary_divisions=(14,),
                beam_each_cell=False,
                beam_cells_together=False,
                decrease_durations_monotonically=True,
                tie_split_notes=False,
                burnish_divisions=False,
                burnish_output=False,
                )

        Returns string.
        '''
        superclass = super(DivisionBurnishedTaleaRhythmMaker, self)
        return superclass.__format__(format_specification=format_specification)

    def __makenew__(self, *args, **kwargs):
        r'''Makes new rhythm-maker with `kwargs`.

        ::

            >>> print format(maker)
            rhythmmakertools.DivisionBurnishedTaleaRhythmMaker(
                talea=(1, 1, 2, 4),
                talea_denominator=16,
                prolation_addenda=(0, 3),
                lefts=(-1,),
                middles=(0,),
                rights=(-1,),
                left_lengths=(1,),
                right_lengths=(1,),
                secondary_divisions=(14,),
                beam_each_cell=False,
                beam_cells_together=False,
                decrease_durations_monotonically=True,
                tie_split_notes=False,
                burnish_divisions=False,
                burnish_output=False,
                )

        ::

            >>> new_maker = new(maker, talea=(1, 1, 2))

        ::

            >>> print format(new_maker)
            rhythmmakertools.DivisionBurnishedTaleaRhythmMaker(
                talea=(1, 1, 2),
                talea_denominator=16,
                prolation_addenda=(0, 3),
                lefts=(-1,),
                middles=(0,),
                rights=(-1,),
                left_lengths=(1,),
                right_lengths=(1,),
                secondary_divisions=(14,),
                beam_each_cell=False,
                beam_cells_together=False,
                decrease_durations_monotonically=True,
                tie_split_notes=False,
                burnish_divisions=False,
                burnish_output=False,
                )

        ::

            >>> divisions = [(5, 8), (5, 8)]
            >>> music = new_maker(divisions)
            >>> music = sequencetools.flatten_sequence(music)
            >>> measures = scoretools.make_spacer_skip_measures(divisions)
            >>> staff = scoretools.RhythmicStaff(measures)
            >>> measures = mutate(staff).replace_measure_contents(music)
            >>> show(staff) # doctest: +SKIP

        Returns new division-burnished talea rhythm-maker.
        '''
        return TaleaRhythmMaker.__makenew__(self, *args, **kwargs)

    ### PUBLIC METHODS ###

    def reverse(self):
        r'''Reverses division-burnished talea rhythm-maker.

        Nonreversed output:

        ::

            >>> print format(maker)
            rhythmmakertools.DivisionBurnishedTaleaRhythmMaker(
                talea=(1, 1, 2, 4),
                talea_denominator=16,
                prolation_addenda=(0, 3),
                lefts=(-1,),
                middles=(0,),
                rights=(-1,),
                left_lengths=(1,),
                right_lengths=(1,),
                secondary_divisions=(14,),
                beam_each_cell=False,
                beam_cells_together=False,
                decrease_durations_monotonically=True,
                tie_split_notes=False,
                burnish_divisions=False,
                burnish_output=False,
                )

        ::

            >>> divisions = [(5, 8), (5, 8)]
            >>> music = maker(divisions)
            >>> music = sequencetools.flatten_sequence(music)
            >>> measures = scoretools.make_spacer_skip_measures(divisions)
            >>> staff = scoretools.RhythmicStaff(measures)
            >>> measures = mutate(staff).replace_measure_contents(music)
            >>> show(staff) # doctest: +SKIP

        Reversed output:

        ::

            >>> reversed_maker = maker.reverse()

        ::

            >>> print format(reversed_maker)
            rhythmmakertools.DivisionBurnishedTaleaRhythmMaker(
                talea=(4, 2, 1, 1),
                talea_denominator=16,
                prolation_addenda=(3, 0),
                lefts=(-1,),
                middles=(0,),
                rights=(-1,),
                left_lengths=(1,),
                right_lengths=(1,),
                secondary_divisions=(14,),
                beam_each_cell=False,
                beam_cells_together=False,
                decrease_durations_monotonically=False,
                tie_split_notes=False,
                burnish_divisions=False,
                burnish_output=False,
                )

        ::

            >>> divisions = [(5, 8), (5, 8)]
            >>> music = reversed_maker(divisions)
            >>> music = sequencetools.flatten_sequence(music)
            >>> measures = scoretools.make_spacer_skip_measures(divisions)
            >>> staff = scoretools.RhythmicStaff(measures)
            >>> measures = mutate(staff).replace_measure_contents(music)
            >>> show(staff) # doctest: +SKIP

        Returns new division-burnished talea rhythm-maker.
        '''
        return TaleaRhythmMaker.reverse(self)
