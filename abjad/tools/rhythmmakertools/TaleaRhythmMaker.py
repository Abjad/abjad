# -*- encoding: utf-8 -*-
from abjad.tools.rhythmmakertools.BurnishedRhythmMaker import \
    BurnishedRhythmMaker


class TaleaRhythmMaker(BurnishedRhythmMaker):
    r'''Talea rhythm-maker.

    ..  container:: example

        **Example 1.** Basic usage:

        ::

            >>> maker = rhythmmakertools.TaleaRhythmMaker(
            ...     talea=[-1, 4, -2, 3],
            ...     talea_denominator=16,
            ...     prolation_addenda=[3, 4],
            ...     )

        ::

            >>> divisions = [(2, 8), (5, 8)]
            >>> music = maker(divisions)
            >>> music = sequencetools.flatten_sequence(music)
            >>> measures = scoretools.make_spacer_skip_measures(divisions)
            >>> staff = Staff(measures)
            >>> measures = mutate(staff).replace_measure_contents(music)
            >>> show(staff) # doctest: +SKIP

    ..  container:: example

        **Example 2.** Tie split notes.

            >>> maker = rhythmmakertools.TaleaRhythmMaker(
            ...     talea=[5],
            ...     talea_denominator=16,
            ...     tie_split_notes=True,
            ...     )

        ::

            >>> divisions = [(2, 8), (2, 8), (2, 8), (2, 8)]
            >>> music = maker(divisions)
            >>> music = sequencetools.flatten_sequence(music)
            >>> measures = scoretools.make_spacer_skip_measures(divisions)
            >>> staff = Staff(measures)
            >>> measures = mutate(staff).replace_measure_contents(music)
            >>> show(staff) # doctest: +SKIP

    Usage follows the two-step configure-then-call pattern shown here.
    '''

    ### INITIALIZER ###

    def __init__(
        self,
        talea=(-1, 4, -2, 3),
        talea_denominator=16,
        prolation_addenda=None,
        secondary_divisions=None,
        talea_helper=None,
        prolation_addenda_helper=None,
        secondary_divisions_helper=None,
        beam_each_cell=False,
        beam_cells_together=False,
        tie_split_notes=False,
        ):
        lefts, middles, rights = [0], [0], [0]
        left_lengths, right_lengths = [0], [0]
        BurnishedRhythmMaker.__init__(
            self,
            talea,
            talea_denominator,
            prolation_addenda,
            lefts,
            middles,
            rights,
            left_lengths,
            right_lengths,
            secondary_divisions,
            talea_helper=talea_helper,
            prolation_addenda_helper=prolation_addenda_helper,
            secondary_divisions_helper=secondary_divisions_helper,
            beam_each_cell=beam_each_cell,
            beam_cells_together=beam_cells_together,
            tie_split_notes=tie_split_notes,
            )

    ### SPECIAL METHODS ###

#    def __call__(self, divisions, seeds=None):
#        r'''Calls burnished rhythm-maker on `divisions`.
#
#        Returns either list of tuplets or else list of note-lists.
#        '''
#        duration_pairs, seeds = RhythmMaker.__call__(self, divisions, seeds)
#        octuplet = self._prepare_input(seeds)
#        talea, prolation_addenda = octuplet[:2]
#        secondary_divisions = octuplet[-1]
#        talee = (talea, prolation_addenda, secondary_divisions)
#        result = self._scale_talee(
#            duration_pairs, 
#            self.talea_denominator, 
#            talee,
#            )
#        duration_pairs, lcd, talea, prolation_addenda, secondary_divisions = \
#            result
#        secondary_duration_pairs = self._make_secondary_duration_pairs(
#            duration_pairs, secondary_divisions)
#        septuplet = (talea, prolation_addenda) + octuplet[2:-1]
#        numeric_map = self._make_numeric_map(
#            secondary_duration_pairs, septuplet)
#        leaf_lists = self._make_leaf_lists(numeric_map, lcd)
#        if not prolation_addenda:
#            result = leaf_lists
#        else:
#            tuplets = self._make_tuplets(secondary_duration_pairs, leaf_lists)
#            result = tuplets
#        if self.beam_each_cell:
#            for cell in result:
#                beam = spannertools.MultipartBeam()
#                attach(beam, cell)
#        if self.tie_split_notes:
#            self._add_ties(result)
#        assert isinstance(result, list), repr(result)
#        assert all(isinstance(x, selectiontools.Selection) for x in result) or \
#            all(isinstance(x, scoretools.Tuplet) for x in result)
#        return result

    def __format__(self, format_specification=''):
        r'''Formats talea rhythm-maker.

        Set `format_specification` to `''` or `'storage'`.

        ::

            >>> print format(maker)
            rhythmmakertools.TaleaRhythmMaker(
                talea=[5],
                talea_denominator=16,
                prolation_addenda=[],
                secondary_divisions=[],
                beam_each_cell=False,
                beam_cells_together=False,
                tie_split_notes=True,
                )

        Returns string.
        '''
        superclass = super(TaleaRhythmMaker, self)
        return superclass.__format__(format_specification=format_specification)

    ### PUBLIC METHODS ###

    def __makenew__(self, *args, **kwargs):
        r'''Makes new talea rhythm-maker with `kwargs`.

        ::

            >>> new_maker = new(maker, prolation_addenda=[1])

        ::

            >>> print format(new_maker)
            rhythmmakertools.TaleaRhythmMaker(
                talea=[5],
                talea_denominator=16,
                prolation_addenda=[1],
                secondary_divisions=[],
                beam_each_cell=False,
                beam_cells_together=False,
                tie_split_notes=True,
                )

        ::

            >>> divisions = [(2, 8), (5, 8)]
            >>> music = new_maker(divisions)
            >>> music = sequencetools.flatten_sequence(music)
            >>> measures = scoretools.make_spacer_skip_measures(divisions)
            >>> staff = Staff(measures)
            >>> measures = mutate(staff).replace_measure_contents(music)
            >>> show(staff) # doctest: +SKIP

        Returns new talea rhythm-maker.
        '''
        return BurnishedRhythmMaker.__makenew__(self, *args, **kwargs)

    def reverse(self):
        r'''Reverses talea rhythm-maker.

        ::

            >>> reversed_maker = maker.reverse()

        ::

            >>> print format(reversed_maker)
            rhythmmakertools.TaleaRhythmMaker(
                talea=[5],
                talea_denominator=16,
                prolation_addenda=[],
                secondary_divisions=[],
                beam_each_cell=False,
                beam_cells_together=False,
                tie_split_notes=True,
                )

        ::

            >>> divisions = [(2, 8), (5, 8)]
            >>> music = reversed_maker(divisions)
            >>> music = sequencetools.flatten_sequence(music)
            >>> measures = scoretools.make_spacer_skip_measures(divisions)
            >>> staff = Staff(measures)
            >>> measures = mutate(staff).replace_measure_contents(music)
            >>> show(staff) # doctest: +SKIP

        Returns new talea rhythm-maker.
        '''
        return BurnishedRhythmMaker.reverse(self)
