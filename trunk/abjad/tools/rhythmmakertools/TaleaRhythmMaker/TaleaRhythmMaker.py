from abjad.tools.rhythmmakertools.DivisionBurnishedTaleaRhythmMaker import \
    DivisionBurnishedTaleaRhythmMaker


class TaleaRhythmMaker(DivisionBurnishedTaleaRhythmMaker):
    r'''.. versionadded:: 2.8

    Talea rhythm-maker.

    Example 1. Basic usage:

    ::

        >>> maker = rhythmmakertools.TaleaRhythmMaker(
        ...     talea=[-1, 4, -2, 3],
        ...     talea_denominator=16,
        ...     prolation_addenda=[3, 4])

    ::

        >>> divisions = [(2, 8), (5, 8)]
        >>> music = maker(divisions)
        >>> music = sequencetools.flatten_sequence(music)
        >>> measures = measuretools.make_measures_with_full_measure_spacer_skips(divisions)
        >>> staff = Staff(measures)
        >>> measures = measuretools.replace_contents_of_measures_in_expr(staff, music)

    ::

        >>> show(staff) # doctest: +SKIP

    Example 2. Tie split notes.

        >>> maker = rhythmmakertools.TaleaRhythmMaker(
        ...     talea=[5],
        ...     talea_denominator=16,
        ...     tie_split_notes=True)

    ::

        >>> divisions = [(2, 8), (2, 8), (2, 8), (2, 8)]
        >>> music = maker(divisions)
        >>> music = sequencetools.flatten_sequence(music)
        >>> measures = measuretools.make_measures_with_full_measure_spacer_skips(divisions)
        >>> staff = Staff(measures)
        >>> measures = measuretools.replace_contents_of_measures_in_expr(staff, music)

    ::

        >>> show(staff) # doctest: +SKIP

    Usage follows the two-step instantiate-then-call pattern shown here.
    '''

    ### INITIALIZER ###

    def __init__(self, talea=None, talea_denominator=None, prolation_addenda=None, secondary_divisions=None,
        talea_helper=None, prolation_addenda_helper=None, secondary_divisions_helper=None,
        beam_each_cell=False, beam_cells_together=False, tie_split_notes=False):
        lefts, middles, rights = [0], [0], [0]
        left_lengths, right_lengths = [0], [0]
        DivisionBurnishedTaleaRhythmMaker.__init__(self, talea, talea_denominator, prolation_addenda,
            lefts, middles, rights, left_lengths, right_lengths, secondary_divisions,
            talea_helper=talea_helper, prolation_addenda_helper=prolation_addenda_helper,
            secondary_divisions_helper=secondary_divisions_helper,
            beam_each_cell=beam_each_cell, beam_cells_together=beam_cells_together,
            tie_split_notes=tie_split_notes)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def storage_format(self):
        '''Talea rhythm-maker storage format:

        ::

            >>> z(maker)
            rhythmmakertools.TaleaRhythmMaker(
                talea=[5],
                talea_denominator=16,
                prolation_addenda=[],
                secondary_divisions=[],
                beam_each_cell=False,
                beam_cells_together=False,
                tie_split_notes=True
                )

        Return string.
        '''
        return DivisionBurnishedTaleaRhythmMaker.storage_format(self)

    ### PUBLIC METHODS ###

    def new(self, **kwargs):
        '''Create new talea rhythm-maker with `kwargs`:

        ::

            >>> new_maker = maker.new(prolation_addenda=[1])

        ::

            >>> z(new_maker)
            rhythmmakertools.TaleaRhythmMaker(
                talea=[5],
                talea_denominator=16,
                prolation_addenda=[1],
                secondary_divisions=[],
                beam_each_cell=False,
                beam_cells_together=False,
                tie_split_notes=True
                )

        ::

            >>> divisions = [(2, 8), (5, 8)]
            >>> music = new_maker(divisions)
            >>> music = sequencetools.flatten_sequence(music)
            >>> measures = measuretools.make_measures_with_full_measure_spacer_skips(divisions)
            >>> staff = Staff(measures)
            >>> measures = measuretools.replace_contents_of_measures_in_expr(staff, music)

        ::

            >>> show(staff) # doctest: +SKIP

        Return new talea rhythm-maker.
        '''
        return DivisionBurnishedTaleaRhythmMaker.new(self, **kwargs)

    def reverse(self):
        '''Reverse talea rhythm-maker:

        ::

            >>> reversed_maker = maker.reverse()

        ::

            >>> z(reversed_maker)
            rhythmmakertools.TaleaRhythmMaker(
                talea=[5],
                talea_denominator=16,
                prolation_addenda=[],
                secondary_divisions=[],
                beam_each_cell=False,
                beam_cells_together=False,
                tie_split_notes=True
                )

        ::

            >>> divisions = [(2, 8), (5, 8)]
            >>> music = reversed_maker(divisions)
            >>> music = sequencetools.flatten_sequence(music)
            >>> measures = measuretools.make_measures_with_full_measure_spacer_skips(divisions)
            >>> staff = Staff(measures)
            >>> measures = measuretools.replace_contents_of_measures_in_expr(staff, music)

        ::

            >>> show(staff) # doctest: +SKIP

        Return new talea rhythm-maker.
        '''
        return DivisionBurnishedTaleaRhythmMaker.reverse(self)
