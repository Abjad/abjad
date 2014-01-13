# -*- encoding: utf-8 -*-
from abjad.tools import mathtools
from abjad.tools import sequencetools
from abjad.tools.rhythmmakertools.TaleaRhythmMaker \
	import TaleaRhythmMaker


class OutputBurnishedTaleaRhythmMaker(TaleaRhythmMaker):
    r'''Output-burnished talea rhythm-maker:

    ::

        >>> maker = rhythmmakertools.OutputBurnishedTaleaRhythmMaker(
        ...     talea=(1, 2, 3),
        ...     talea_denominator=16,
        ...     prolation_addenda=(0, 2),
        ...     lefts=(-1,),
        ...     middles=(0,),
        ...     rights=(-1,),
        ...     left_lengths=(1,),
        ...     right_lengths=(1,),
        ...     secondary_divisions=(9,),
        ...     beam_each_cell=True,
        ...     )

    Configure at initialization and then call on any list of divisions:

    ::

        >>> divisions = [(3, 8), (4, 8)]
        >>> music = maker(divisions)
        >>> music = sequencetools.flatten_sequence(music)
        >>> measures = scoretools.make_spacer_skip_measures(divisions)
        >>> staff = scoretools.RhythmicStaff(measures)
        >>> measures = mutate(staff).replace_measure_contents(music)
        >>> show(staff) # doctest: +SKIP

    Usage follows the two-step configure-then-call pattern shown here.
    '''

    ### CLASS VARIABLES ###

    _burnish_first_and_last_divisions = True

    ### SPECIAL METHODS ###

    def __format__(self, format_specification=''):
        r'''Formats output-burnished talea rhythm-maker.

        Set `format_specification` to `''` or `'storage'`.

        ::

            >>> print format(maker)
            rhythmmakertools.OutputBurnishedTaleaRhythmMaker(
                talea=(1, 2, 3),
                talea_denominator=16,
                prolation_addenda=(0, 2),
                lefts=(-1,),
                middles=(0,),
                rights=(-1,),
                left_lengths=(1,),
                right_lengths=(1,),
                secondary_divisions=(9,),
                beam_each_cell=True,
                beam_cells_together=False,
                decrease_durations_monotonically=True,
                tie_split_notes=False,
                )

        Returns string.
        '''
        superclass = super(OutputBurnishedTaleaRhythmMaker, self)
        return superclass.__format__(format_specification=format_specification)

    def __makenew__(self, *args, **kwargs):
        r'''Makes new output-burnished talea rhythm-maker with `kwargs`.

        ::

            >>> new_maker = new(maker, secondary_divisions=(10,))

        ::

            >>> print format(new_maker)
            rhythmmakertools.OutputBurnishedTaleaRhythmMaker(
                talea=(1, 2, 3),
                talea_denominator=16,
                prolation_addenda=(0, 2),
                lefts=(-1,),
                middles=(0,),
                rights=(-1,),
                left_lengths=(1,),
                right_lengths=(1,),
                secondary_divisions=(10,),
                beam_each_cell=True,
                beam_cells_together=False,
                decrease_durations_monotonically=True,
                tie_split_notes=False,
                )

        ::

            >>> divisions = [(3, 8), (4, 8)]
            >>> music = new_maker(divisions)
            >>> music = sequencetools.flatten_sequence(music)
            >>> measures = scoretools.make_spacer_skip_measures(divisions)
            >>> staff = scoretools.RhythmicStaff(measures)
            >>> measures = mutate(staff).replace_measure_contents(music)
            >>> show(staff) # doctest: +SKIP

        Returns new output-burnished talea rhythm-maker.
        '''
        return TaleaRhythmMaker.__makenew__(self, *args, **kwargs)

    ### PUBLIC METHODS ###

    def reverse(self):
        r'''Reverses output-burnished talea rhythm-maker:

        ::

            >>> reversed_maker = maker.reverse()

        ::

            >>> print format(reversed_maker)
            rhythmmakertools.OutputBurnishedTaleaRhythmMaker(
                talea=(3, 2, 1),
                talea_denominator=16,
                prolation_addenda=(2, 0),
                lefts=(-1,),
                middles=(0,),
                rights=(-1,),
                left_lengths=(1,),
                right_lengths=(1,),
                secondary_divisions=(9,),
                beam_each_cell=True,
                beam_cells_together=False,
                decrease_durations_monotonically=False,
                tie_split_notes=False,
                )

        ::

            >>> divisions = [(3, 8), (4, 8)]
            >>> music = reversed_maker(divisions)
            >>> music = sequencetools.flatten_sequence(music)
            >>> measures = scoretools.make_spacer_skip_measures(divisions)
            >>> staff = scoretools.RhythmicStaff(measures)
            >>> measures = mutate(staff).replace_measure_contents(music)
            >>> show(staff) # doctest: +SKIP

        Returns new output-burnished talea rhythm-maker.
        '''
        return TaleaRhythmMaker.reverse(self)
