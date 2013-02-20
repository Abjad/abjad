from abjad.tools.rhythmmakertools.DivisionIncisedNoteRhythmMaker import DivisionIncisedNoteRhythmMaker


class NoteRhythmMaker(DivisionIncisedNoteRhythmMaker):
    r'''.. versionadded:: 2.8

    Note rhythm-maker:

    ::

        >>> maker = rhythmmakertools.NoteRhythmMaker()

    ::

        >>> divisions = [(5, 8), (3, 8)]
        >>> leaf_lists = maker(divisions)
        >>> leaves = sequencetools.flatten_sequence(leaf_lists)
        >>> measures = measuretools.make_measures_with_full_measure_spacer_skips(divisions)
        >>> staff = Staff(measures)
        >>> measures = measuretools.replace_contents_of_measures_in_expr(staff, leaves)

    ::

        >>> show(staff) # doctest: +SKIP

    Usage follows the two-step instantiate-then-call pattern shown here.
    '''

    ### CLASS ATTRIBUTES ###

    _default_positional_input_arguments = ()

    ### INITIALIZER ###

    def __init__(self, decrease_durations_monotonically=True, tie_rests=False):
        DivisionIncisedNoteRhythmMaker.__init__(
            self, [], [0], [], [0], 1,
            decrease_durations_monotonically=decrease_durations_monotonically, tie_rests=tie_rests
            )

    ### SPECIAL METHODS ###

    def __repr__(self):
        '''Note rhythm-maker interpreter representation.
        
        Return string.
        '''
        return '%s()' % type(self).__name__

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def storage_format(self):
        '''Note rhythm-maker storage format:

        ::

            >>> z(maker)
            rhythmmakertools.NoteRhythmMaker(
                decrease_durations_monotonically=True,
                tie_rests=False
                )

        Return string.
        '''

    ### PUBLIC METHODS ###

    def new(self, **kwargs):
        '''Create new note rhythm-maker:

        ::

            >>> new_maker = maker.new(decrease_durations_monotonically=False)

        ::
            
            >>> z(new_maker)
            rhythmmakertools.NoteRhythmMaker(
                decrease_durations_monotonically=False,
                tie_rests=False
                )

        ::

            >>> divisions = [(5, 8), (3, 8)]
            >>> leaf_lists = new_maker(divisions)
            >>> leaves = sequencetools.flatten_sequence(leaf_lists)
            >>> measures = measuretools.make_measures_with_full_measure_spacer_skips(divisions)
            >>> staff = Staff(measures)
            >>> measures = measuretools.replace_contents_of_measures_in_expr(staff, leaves)

        ::

            >>> show(staff) # doctest: +SKIP

        Return new note rhythm-maker.
        '''
        return DivisionIncisedNoteRhythmMaker.new(self, **kwargs)

    def reverse(self):
        '''Reverse note rhythm-maker:

        ::

            >>> reversed_maker = maker.reverse()

        ::
            
            >>> z(reversed_maker)
            rhythmmakertools.NoteRhythmMaker(
                decrease_durations_monotonically=False,
                tie_rests=False
                )

        ::

            >>> divisions = [(5, 8), (3, 8)]
            >>> leaf_lists = reversed_maker(divisions)
            >>> leaves = sequencetools.flatten_sequence(leaf_lists)
            >>> measures = measuretools.make_measures_with_full_measure_spacer_skips(divisions)
            >>> staff = Staff(measures)
            >>> measures = measuretools.replace_contents_of_measures_in_expr(staff, leaves)

        ::

            >>> show(staff) # doctest: +SKIP

        Return new note rhythm-maker.
        '''
        return DivisionIncisedNoteRhythmMaker.reverse(self)
