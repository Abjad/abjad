# -*- encoding: utf-8 -*-
from abjad.tools.rhythmmakertools.DivisionIncisedRhythmMaker \
	import DivisionIncisedRhythmMaker


class DivisionIncisedRestRhythmMaker(DivisionIncisedRhythmMaker):
    r'''Division-incised rest rhythm-maker:

    ::

        >>> maker = rhythmmakertools.DivisionIncisedRestRhythmMaker(
        ...     prefix_talea=[1],
        ...     prefix_lengths=[1, 2, 3, 4],
        ...     suffix_talea=[1],
        ...     suffix_lengths=[1],
        ...     talea_denominator=32)

    Configure at instantiation and then call on any sequence of divisions:

    ::

        >>> divisions = [(5, 16), (5, 16), (5, 16), (5, 16)]
        >>> leaf_lists = maker(divisions)
        >>> leaves = sequencetools.flatten_sequence(leaf_lists)
        >>> measures = scoretools.make_spacer_skip_measures(divisions)
        >>> staff = Staff(measures)
        >>> measures = mutate(staff).replace_measure_contents(leaves)

    ::

        >>> show(staff) # doctest: +SKIP

    Usage follows the two-step instantiate-then-call pattern shown here.
    '''

    ### SPECIAL METHODS ###

    def __format__(self, format_specification=''):
        r'''Formats division-incised rest rhythm-maker.

        Set `format_specification` to `''` or `'storage'`.

        ::

            >>> print format(maker)
            rhythmmakertools.DivisionIncisedRestRhythmMaker(
                prefix_talea=[1],
                prefix_lengths=[1, 2, 3, 4],
                suffix_talea=[1],
                suffix_lengths=[1],
                talea_denominator=32,
                prolation_addenda=[],
                secondary_divisions=[],
                decrease_durations_monotonically=True,
                tie_rests=False,
                beam_each_cell=False,
                beam_cells_together=False,
                )

        Returns string.
        '''
        superclass = super(DivisionIncisedRestRhythmMaker, self)
        return superclass.__format__(format_specification=format_specification)

    def __makenew__(self, *args, **kwargs):
        r'''Makes new division-incised rest rhythm-maker with `kwargs`.

        ::

            >>> print format(maker)
            rhythmmakertools.DivisionIncisedRestRhythmMaker(
                prefix_talea=[1],
                prefix_lengths=[1, 2, 3, 4],
                suffix_talea=[1],
                suffix_lengths=[1],
                talea_denominator=32,
                prolation_addenda=[],
                secondary_divisions=[],
                decrease_durations_monotonically=True,
                tie_rests=False,
                beam_each_cell=False,
                beam_cells_together=False,
                )

        ::

            >>> new_maker = new(maker, suffix_lengths=[0])

        ::

            >>> print format(new_maker)
            rhythmmakertools.DivisionIncisedRestRhythmMaker(
                prefix_talea=[1],
                prefix_lengths=[1, 2, 3, 4],
                suffix_talea=[1],
                suffix_lengths=[0],
                talea_denominator=32,
                prolation_addenda=[],
                secondary_divisions=[],
                decrease_durations_monotonically=True,
                tie_rests=False,
                beam_each_cell=False,
                beam_cells_together=False,
                )

        ::

            >>> divisions = [(5, 16), (5, 16), (5, 16), (5, 16)]
            >>> leaf_lists = new_maker(divisions)
            >>> leaves = sequencetools.flatten_sequence(leaf_lists)
            >>> measures = scoretools.make_spacer_skip_measures(divisions)
            >>> staff = Staff(measures)
            >>> measures = mutate(staff).replace_measure_contents(leaves)

        ::

            >>> show(staff) # doctest: +SKIP

        Returns new division-incised rest rhythm-maker.
        '''
        return DivisionIncisedRhythmMaker.__makenew__(self, *args, **kwargs)

    ### PRIVATE METHODS ###

    def _make_middle_of_numeric_map_part(self, middle):
        if 0 < middle:
            return (-abs(middle), )
        else:
            return ()

    ### PUBLIC METHODS ###

    def reverse(self):
        r'''Reverses division-incised rest rhythm-maker.

        ::

            >>> print format(maker)
            rhythmmakertools.DivisionIncisedRestRhythmMaker(
                prefix_talea=[1],
                prefix_lengths=[1, 2, 3, 4],
                suffix_talea=[1],
                suffix_lengths=[1],
                talea_denominator=32,
                prolation_addenda=[],
                secondary_divisions=[],
                decrease_durations_monotonically=True,
                tie_rests=False,
                beam_each_cell=False,
                beam_cells_together=False,
                )

        ::

            >>> reversed_maker = maker.reverse()

        ::

            >>> print format(reversed_maker)
            rhythmmakertools.DivisionIncisedRestRhythmMaker(
                prefix_talea=[1],
                prefix_lengths=[4, 3, 2, 1],
                suffix_talea=[1],
                suffix_lengths=[1],
                talea_denominator=32,
                prolation_addenda=[],
                secondary_divisions=[],
                decrease_durations_monotonically=False,
                tie_rests=False,
                beam_each_cell=False,
                beam_cells_together=False,
                )

        ::

            >>> divisions = [(5, 16), (5, 16), (5, 16), (5, 16)]
            >>> leaf_lists = reversed_maker(divisions)
            >>> leaves = sequencetools.flatten_sequence(leaf_lists)
            >>> measures = scoretools.make_spacer_skip_measures(divisions)
            >>> staff = Staff(measures)
            >>> measures = mutate(staff).replace_measure_contents(leaves)

        ::

            >>> show(staff) # doctest: +SKIP

        Returns new division-incised rest rhythm-maker.
        '''
        return DivisionIncisedRhythmMaker.reverse(self)
