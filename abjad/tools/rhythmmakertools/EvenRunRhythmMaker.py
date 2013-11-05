# -*- encoding: utf-8 -*-
from abjad.tools import scoretools
from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import scoretools
from abjad.tools import spannertools
from abjad.tools.rhythmmakertools.RhythmMaker import RhythmMaker
from abjad.tools.functiontools import attach


class EvenRunRhythmMaker(RhythmMaker):
    r'''Even run rhythm-maker.

    ..  container:: example
    
        **Example 1.** Make even run of notes each equal in duration to ``1/d``
        with ``d`` equal to the denominator of each division on which
        the rhythm-maker is called:

        ::

            >>> maker = rhythmmakertools.EvenRunRhythmMaker()

        ::

            >>> divisions = [(4, 8), (3, 4), (2, 4)]
            >>> lists = maker(divisions)
            >>> music = sequencetools.flatten_sequence(lists)
            >>> measures = \
            ...     scoretools.make_measures_with_full_measure_spacer_skips(
            ...     divisions)
            >>> staff = scoretools.RhythmicStaff(measures)
            >>> measures = scoretools.replace_contents_of_measures_in_expr(
            ...     staff, music)

        ::

            >>> show(staff) # doctest: +SKIP

    ..  container:: example

        **Example 2.** Make even run of notes each equal in duration to ``1/(2**d)``
        with ``d`` equal to the denominator of each division on which
        the rhythm-maker is called:

        ::

            >>> maker = rhythmmakertools.EvenRunRhythmMaker(1)

        ::

            >>> divisions = [(4, 8), (3, 4), (2, 4)]
            >>> lists = maker(divisions)
            >>> music = sequencetools.flatten_sequence(lists)
            >>> measures = \
            ...     scoretools.make_measures_with_full_measure_spacer_skips(
            ...     divisions)
            >>> staff = scoretools.RhythmicStaff(measures)
            >>> measures = scoretools.replace_contents_of_measures_in_expr(
            ...     staff, music)

        ::

            >>> show(staff) # doctest: +SKIP

    Output a list of lists of depth-``2`` note-bearing containers.

    Even-run rhythm-maker doesn't yet work with non-power-of-two divisions.

    Usage follows the two-step instantiate-then-call pattern shown here.
    '''

    ### CLASS VARIABLES ###

    _default_positional_input_arguments = ()

    ### INITIALIZER ###

    def __init__(
        self,
        denominator_multiplier_exponent=0,
        beam_each_cell=True,
        beam_cells_together=False,
        ):
        assert mathtools.is_nonnegative_integer(
            denominator_multiplier_exponent)
        RhythmMaker.__init__(self,
            beam_each_cell=beam_each_cell,
            beam_cells_together=beam_cells_together
            )
        self._denominator_multiplier_exponent = \
            denominator_multiplier_exponent

    ### SPECIAL METHODS ###

    def __call__(self, divisions, seeds=None):
        r'''Calls even-run rhythm-maker on `divisions`.

        Returns list of container lists.
        '''
        result = []
        for division in divisions:
            container = self._make_container(division)
            result.append([container])
        return result

    def __format__(self, format_specification=''):
        r'''Formats even run rhythm-maker.

        Set `format_specification` to `''` or `'storage'`.

        ::

            >>> print format(maker)
            rhythmmakertools.EvenRunRhythmMaker(
                denominator_multiplier_exponent=1,
                beam_each_cell=True,
                beam_cells_together=False
                )

        Returns string.
        '''
        superclass = super(EvenRunRhythmMaker, self)
        return superclass.__format__(format_specification=format_specification)

    ### PRIVATE METHODS ###

    def _make_container(self, division):
        numerator, denominator = division
        # eventually allow for non-power-of-two divisions
        assert mathtools.is_positive_integer_power_of_two(denominator)
        denominator_multiplier = 2 ** self.denominator_multiplier_exponent
        denominator *= denominator_multiplier
        unit_duration = durationtools.Duration(1, denominator)
        numerator *= denominator_multiplier
        notes = scoretools.make_notes(numerator * [0], [unit_duration])
        container = scoretools.Container(notes)
        if self.beam_each_cell:
            beam = spannertools.BeamSpanner()
            attach(beam, container)
        return container

    ### PUBLIC PROPERTIES ###

    @property
    def denominator_multiplier_exponent(self):
        r'''Denominator multiplier exponent provided at initialization.

        ::

            >>> maker.denominator_multiplier_exponent
            1

        Returns nonnegative integer.
        '''
        return self._denominator_multiplier_exponent

    ### PUBLIC METHODS ###

    def new(self, **kwargs):
        r'''Creates new even-run rhythm-maker with `kwargs`.

        ::

            >>> new_maker = maker.new(denominator_multiplier_exponent=0)

        ::

            >>> print format(new_maker)
            rhythmmakertools.EvenRunRhythmMaker(
                denominator_multiplier_exponent=0,
                beam_each_cell=True,
                beam_cells_together=False
                )

        ::

            >>> divisions = [(4, 8), (3, 4), (2, 4)]
            >>> lists = new_maker(divisions)
            >>> music = sequencetools.flatten_sequence(lists)
            >>> measures = \
            ...     scoretools.make_measures_with_full_measure_spacer_skips(
            ...     divisions)
            >>> staff = scoretools.RhythmicStaff(measures)
            >>> measures = scoretools.replace_contents_of_measures_in_expr(
            ...     staff, music)

        ::

            >>> show(staff) # doctest: +SKIP

        Returns new even-run rhythm-maker.
        '''
        return RhythmMaker.new(self, **kwargs)

    def reverse(self):
        r'''Reverses even-run rhythm-maker:

        ::

            >>> reversed_maker = maker.reverse()

        ::

            >>> print format(reversed_maker)
            rhythmmakertools.EvenRunRhythmMaker(
                denominator_multiplier_exponent=1,
                beam_each_cell=True,
                beam_cells_together=False
                )

        ::

            >>> divisions = [(4, 8), (3, 4), (2, 4)]
            >>> lists = reversed_maker(divisions)
            >>> music = sequencetools.flatten_sequence(lists)
            >>> measures = \
            ...     scoretools.make_measures_with_full_measure_spacer_skips(
            ...     divisions)
            >>> staff = scoretools.RhythmicStaff(measures)
            >>> measures = scoretools.replace_contents_of_measures_in_expr(
            ...     staff, music)

        ::

            >>> show(staff) # doctest: +SKIP

        Defined equal to copy of even-run rhythm-maker.

        Returns new even-run rhythm-maker.
        '''
        return RhythmMaker.reverse(self)
