from abjad.tools import beamtools
from abjad.tools import containertools
from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import notetools
from abjad.tools.rhythmmakertools.RhythmMaker import RhythmMaker


class EvenRunRhythmMaker(RhythmMaker):
    r'''.. versionadded:: 2.11

    Even run rhythm-maker.

    Example 1. Make even run of notes each equal in duration to ``1/d``
    with ``d`` equal to the denominator of each division on which
    the rhythm-maker is called:

    ::

        >>> maker = rhythmmakertools.EvenRunRhythmMaker()

    ::

        >>> divisions = [(4, 8), (3, 4), (2, 4)]
        >>> lists = maker(divisions)
        >>> music = sequencetools.flatten_sequence(lists)
        >>> measures = measuretools.make_measures_with_full_measure_spacer_skips(divisions)
        >>> staff = stafftools.RhythmicStaff(measures)
        >>> measures = measuretools.replace_contents_of_measures_in_expr(staff, music)

    ::

        >>> show(staff) # doctest: +SKIP

    Example 2. Make even run of notes each equal in duration to ``1/(2**d)``
    with ``d`` equal to the denominator of each division on which
    the rhythm-maker is called::

        >>> maker = rhythmmakertools.EvenRunRhythmMaker(1)

    ::

        >>> divisions = [(4, 8), (3, 4), (2, 4)]
        >>> lists = maker(divisions)
        >>> music = sequencetools.flatten_sequence(lists)
        >>> measures = measuretools.make_measures_with_full_measure_spacer_skips(divisions)
        >>> staff = stafftools.RhythmicStaff(measures)
        >>> measures = measuretools.replace_contents_of_measures_in_expr(staff, music)

    ::

        >>> show(staff) # doctest: +SKIP

    Output a list of lists of depth-``2`` note-bearing containers.

    Even-run rhythm-maker doesn't yet work with non-power-of-two divisions.

    Usage follows the two-step instantiate-then-call pattern shown here.
    '''

    ### CLASS ATTRIBUTES ###

    _default_positional_input_arguments = ()

    ### INITIALIZER ###

    def __init__(self, denominator_multiplier_exponent=0, beam_each_cell=True, beam_cells_together=False):
        assert mathtools.is_nonnegative_integer(denominator_multiplier_exponent)
        RhythmMaker.__init__(self,
            beam_each_cell=beam_each_cell,
            beam_cells_together=beam_cells_together
            )
        self._denominator_multiplier_exponent = denominator_multiplier_exponent

    ### SPECIAL METHODS ###

    def __call__(self, divisions, seeds=None):
        '''Call even-run rhythm-maker on `divisions`.

        Return list of container lists.
        '''
        result = []
        for division in divisions:
            container = self._make_container(division)
            result.append([container])
        return result

    ### PRIVATE METHODS ###

    def _make_container(self, division):
        numerator, denominator = division
        # eventually allow for non-power-of-two divisions
        assert mathtools.is_positive_integer_power_of_two(denominator)
        denominator_multiplier = 2 ** self.denominator_multiplier_exponent
        denominator *= denominator_multiplier
        unit_duration = durationtools.Duration(1, denominator)
        numerator *= denominator_multiplier
        notes = notetools.make_notes(numerator * [0], [unit_duration])
        container = containertools.Container(notes)
        if self.beam_each_cell:
            beam_spanner = beamtools.BeamSpanner()
            beam_spanner(container)
        return container

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def denominator_multiplier_exponent(self):
        '''Denominator multiplier exponent provided at initialization.

        ::

            >>> maker.denominator_multiplier_exponent
            1
        
        Return nonnegative integer.
        '''
        return self._denominator_multiplier_exponent

    @property
    def storage_format(self):
        '''Even-run rhythm-maker storage format:

        ::

            >>> z(maker)
            rhythmmakertools.EvenRunRhythmMaker(
                denominator_multiplier_exponent=1,
                beam_each_cell=True,
                beam_cells_together=False
                )

        Return string.
        '''
        return RhythmMaker.storage_format.fget(self)

    ### PUBLIC METHODS ###

    def new(self, **kwargs):
        '''Create new even-run rhythm-maker with `kwargs`:

        ::

            >>> new_maker = maker.new(denominator_multiplier_exponent=0)

        ::

            >>> z(new_maker)
            rhythmmakertools.EvenRunRhythmMaker(
                denominator_multiplier_exponent=0,
                beam_each_cell=True,
                beam_cells_together=False
                )

        ::

            >>> divisions = [(4, 8), (3, 4), (2, 4)]
            >>> lists = new_maker(divisions)
            >>> music = sequencetools.flatten_sequence(lists)
            >>> measures = measuretools.make_measures_with_full_measure_spacer_skips(divisions)
            >>> staff = stafftools.RhythmicStaff(measures)
            >>> measures = measuretools.replace_contents_of_measures_in_expr(staff, music)

        ::

            >>> show(staff) # doctest: +SKIP

        Return new even-run rhythm-maker.
        '''
        return RhythmMaker.new(self, **kwargs)

    def reverse(self):
        '''Reverse even-run rhythm-maker:

        ::

            >>> reversed_maker = maker.reverse()

        ::

            >>> z(reversed_maker)
            rhythmmakertools.EvenRunRhythmMaker(
                denominator_multiplier_exponent=1,
                beam_each_cell=True,
                beam_cells_together=False
                )

        ::
            
            >>> divisions = [(4, 8), (3, 4), (2, 4)]
            >>> lists = reversed_maker(divisions)
            >>> music = sequencetools.flatten_sequence(lists)
            >>> measures = measuretools.make_measures_with_full_measure_spacer_skips(divisions)
            >>> staff = stafftools.RhythmicStaff(measures)
            >>> measures = measuretools.replace_contents_of_measures_in_expr(staff, music)

        ::

            >>> show(staff) # doctest: +SKIP

        Defined equal to copy of even-run rhythm-maker.

        Return new even-run rhythm-maker.
        '''
        return RhythmMaker.reverse(self)
