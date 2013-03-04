from abjad.tools.rhythmmakertools.DivisionIncisedRestRhythmMaker import DivisionIncisedRestRhythmMaker


class RestRhythmMaker(DivisionIncisedRestRhythmMaker):
    r'''.. versionadded:: 2.8

    Rest rhythm-maker.

    Example 1:

    ::

        >>> maker = rhythmmakertools.RestRhythmMaker()

    Initialize and then call on arbitrary divisions:

    ::

        >>> divisions = [(5, 16), (3, 8)]
        >>> leaf_lists = maker(divisions)
        >>> leaves = sequencetools.flatten_sequence(leaf_lists)
        >>> measures = measuretools.make_measures_with_full_measure_spacer_skips(divisions)
        >>> staff = stafftools.RhythmicStaff(measures)
        >>> measures = measuretools.replace_contents_of_measures_in_expr(staff, leaves)

    ::

        >>> f(staff)
        \new RhythmicStaff {
            {
                \time 5/16
                r4
                r16
            }
            {
                \time 3/8
                r4.
            }
        }

    ::

        >>> show(staff) # doctest: +SKIP

    Example 2. Forbid written durations greater than or equal to a half note:

    ::

        >>> maker = rhythmmakertools.RestRhythmMaker(forbidden_written_duration=Duration(1, 4))

    ::

        >>> divisions = [(5, 16), (3, 8)]
        >>> leaf_lists = maker(divisions)
        >>> leaves = sequencetools.flatten_sequence(leaf_lists)
        >>> measures = measuretools.make_measures_with_full_measure_spacer_skips(divisions)
        >>> staff = stafftools.RhythmicStaff(measures)
        >>> measures = measuretools.replace_contents_of_measures_in_expr(staff, leaves)

    ::

        >>> f(staff)
        \new RhythmicStaff {
            {
                \time 5/16
                r8
                r8
                r16
            }
            {
                \time 3/8
                r8
                r8
                r8
            }
        }

    ::

        >>> show(staff) # doctest: +SKIP

    Usage follows the two-step instantiate-then-call pattern shown here.
    '''

    ### CLASS ATTRIBUTES ###

    _default_positional_input_arguments = ()

    ### INITIALIZER ###

    def __init__(self, forbidden_written_duration=None):
        DivisionIncisedRestRhythmMaker.__init__(
            self, [], [0], [], [0], 1,
            decrease_durations_monotonically=True, 
            forbidden_written_duration=forbidden_written_duration,
            tie_rests=False
            )

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def storage_format(self):
        '''Rest rhythm-maker storage format:

        ::

            >>> z(maker)
            rhythmmakertools.RestRhythmMaker(
                forbidden_written_duration=durationtools.Duration(1, 4)
                )

        Return string.
        '''
        return DivisionIncisedRestRhythmMaker.storage_format.fget(self)

    ### PUBLIC METHODS ###

    def new(self, **kwargs):
        '''Create new rest rhythm-maker with `kwargs`:

        ::

            >>> new_maker = maker.new()

        ::

            >>> z(new_maker)
            rhythmmakertools.RestRhythmMaker(
                forbidden_written_duration=durationtools.Duration(1, 4)
                )

        ::

            >>> divisions = [(5, 16), (3, 8)]
            >>> leaf_lists = new_maker(divisions)
            >>> leaves = sequencetools.flatten_sequence(leaf_lists)
            >>> measures = measuretools.make_measures_with_full_measure_spacer_skips(divisions)
            >>> staff = stafftools.RhythmicStaff(measures)
            >>> measures = measuretools.replace_contents_of_measures_in_expr(staff, leaves)

        ::

            >>> show(staff) # doctest: +SKIP

        Return new rest rhythm-maker.
        '''
        return DivisionIncisedRestRhythmMaker.new(self, **kwargs)

    def reverse(self):
        '''Reverse rest rhythm-maker:

        ::

            >>> reversed_maker = maker.reverse()

        ::

            >>> z(reversed_maker)
            rhythmmakertools.RestRhythmMaker(
                forbidden_written_duration=durationtools.Duration(1, 4)
                )

        ::

            >>> divisions = [(5, 16), (3, 8)]
            >>> leaf_lists = reversed_maker(divisions)
            >>> leaves = sequencetools.flatten_sequence(leaf_lists)
            >>> measures = measuretools.make_measures_with_full_measure_spacer_skips(divisions)
            >>> staff = stafftools.RhythmicStaff(measures)
            >>> measures = measuretools.replace_contents_of_measures_in_expr(staff, leaves)

        ::

            >>> show(staff) # doctest: +SKIP

        Return new rest rhythm-maker.
        '''
        return DivisionIncisedRestRhythmMaker.reverse(self)
