import math
from abjad.tools import componenttools
from abjad.tools import durationtools
from abjad.tools import leaftools
from abjad.tools import mathtools
from abjad.tools import tuplettools
from abjad.tools.rhythmmakertools.RhythmMaker import RhythmMaker


class EqualDivisionRhythmMaker(RhythmMaker):
    r'''.. versionadded:: 2.10

    Equal division rhythm-maker:

    ::

        >>> maker = rhythmmakertools.EqualDivisionRhythmMaker(leaf_count=4)

    Configure at initialization and then call on any series of divisions:

    ::

        >>> divisions = [(1, 2), (3, 8), (5, 16)]
        >>> tuplet_lists = maker(divisions)
        >>> music = sequencetools.flatten_sequence(tuplet_lists)
        >>> measures = measuretools.make_measures_with_full_measure_spacer_skips(divisions)
        >>> staff = stafftools.RhythmicStaff(measures)
        >>> measures = measuretools.replace_contents_of_measures_in_expr(staff, music)

    ::

        >>> show(staff) # doctest: +SKIP

    Usage follows the two-step instantiate-then-call pattern shown here.
    '''

    ### CLASS ATTRIBUTES ###

    _default_positional_input_arguments = ()

    ### INITIALIZER ###

    def __init__(self, leaf_count=None, is_diminution=True, beam_each_cell=True, beam_cells_together=False):
        assert mathtools.is_integer_equivalent_expr(leaf_count)
        RhythmMaker.__init__(self,
            beam_each_cell=beam_each_cell,
            beam_cells_together=beam_cells_together
            )
        leaf_count = int(leaf_count)
        self._leaf_count = leaf_count
        self._is_diminution = is_diminution

    ### SPECIAL METHODS ###

    def __call__(self, divisions, seeds=None):
        '''Call equal-division rhythm-maker on `divisions`.

        Return list of tuplet lists.
        '''
        result = []
        for division in divisions:
            tuplet = self._make_tuplet(division)
            result.append([tuplet])
        return result

    ### PRIVATE METHODS ###

    def _make_tuplet(self, division):
        numerator, talea_denominator = division
        division_duration = durationtools.Duration(division)
        ratio = self.leaf_count * [1]
        tuplet = tuplettools.make_tuplet_from_duration_and_ratio(
            division_duration, ratio, avoid_dots=True, is_diminution=self.is_diminution)
        return tuplet

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def is_diminution(self):
        '''True when output tuplets should be diminuted.

        False when output tuplets should be augmented:

        ::

            >>> maker.is_diminution
            True

        Return boolean.
        '''
        return self._is_diminution

    @property
    def leaf_count(self):
        '''Number of leaves per division:

        ::

            >>> maker.leaf_count
            4

        Return positive integer.
        '''
        return self._leaf_count

    @property
    def storage_format(self):
        '''Equal-division rhythm-maker storage format:

        ::

            >>> z(maker)
            rhythmmakertools.EqualDivisionRhythmMaker(
                leaf_count=4,
                is_diminution=True,
                beam_each_cell=True,
                beam_cells_together=False
                )

        Return string.
        '''
        return RhythmMaker.storage_format.fget(self)

    ### PUBLIC METHODS ###

    def new(self, **kwargs):
        '''Create new equal-division rhythm-maker with `kwargs`:

        ::

            >>> new_maker = maker.new(is_diminution=False)

        ::

            >>> z(new_maker)
            rhythmmakertools.EqualDivisionRhythmMaker(
                leaf_count=4,
                is_diminution=False,
                beam_each_cell=True,
                beam_cells_together=False
                )

        ::

            >>> divisions = [(1, 2), (3, 8), (5, 16)]
            >>> tuplet_lists = new_maker(divisions)
            >>> music = sequencetools.flatten_sequence(tuplet_lists)
            >>> measures = measuretools.make_measures_with_full_measure_spacer_skips(divisions)
            >>> staff = stafftools.RhythmicStaff(measures)
            >>> measures = measuretools.replace_contents_of_measures_in_expr(staff, music)

        ::

            >>> show(staff) # doctest: +SKIP

        Return new equal-division rhythm-maker.
        '''
        return RhythmMaker.new(self, **kwargs)

    def reverse(self):
        '''Reverse equal-division rhythm-maker:

        ::

            >>> reversed_maker = maker.reverse()

        ::

            >>> z(reversed_maker)
            rhythmmakertools.EqualDivisionRhythmMaker(
                leaf_count=4,
                is_diminution=True,
                beam_each_cell=True,
                beam_cells_together=False
                )

        ::

            >>> divisions = [(1, 2), (3, 8), (5, 16)]
            >>> tuplet_lists = reversed_maker(divisions)
            >>> music = sequencetools.flatten_sequence(tuplet_lists)
            >>> measures = measuretools.make_measures_with_full_measure_spacer_skips(divisions)
            >>> staff = stafftools.RhythmicStaff(measures)
            >>> measures = measuretools.replace_contents_of_measures_in_expr(staff, music)

        ::

            >>> show(staff) # doctest: +SKIP

        Defined equal to copy of maker.

        Return new equal-division rhythm-maker.
        '''
        return RhythmMaker.new(self)
