# -*- encoding: utf-8 -*-
from abjad.tools.rhythmmakertools.DivisionIncisedNoteRhythmMaker \
	import DivisionIncisedNoteRhythmMaker


class NoteRhythmMaker(DivisionIncisedNoteRhythmMaker):
    r'''Note rhythm-maker:

    ..  container:: example

        **Example 1:**

        ::

            >>> maker = rhythmmakertools.NoteRhythmMaker()

        ::

            >>> divisions = [(5, 8), (3, 8)]
            >>> leaf_lists = maker(divisions)
            >>> leaves = sequencetools.flatten_sequence(leaf_lists)
            >>> measures = \
            ...     measuretools.make_measures_with_full_measure_spacer_skips(
            ...     divisions)
            >>> staff = Staff(measures)
            >>> measures = measuretools.replace_contents_of_measures_in_expr(
            ...     staff, leaves)

        ..  doctest::

            >>> f(staff)
            \new Staff {
                {
                    \time 5/8
                    c'2 ~
                    c'8
                }
                {
                    \time 3/8
                    c'4.
                }
            }

        ::

            >>> show(staff) # doctest: +SKIP

    ..  container:: example
    
        **Example 2.** Forbid half notes:

        ::

            >>> maker = rhythmmakertools.NoteRhythmMaker(
            ...     forbidden_written_duration=Duration(1, 2))

        ::

            >>> divisions = [(5, 8), (3, 8)]
            >>> leaf_lists = maker(divisions)
            >>> leaves = sequencetools.flatten_sequence(leaf_lists)
            >>> measures = \
            ...     measuretools.make_measures_with_full_measure_spacer_skips(
            ...     divisions)
            >>> staff = Staff(measures)
            >>> measures = measuretools.replace_contents_of_measures_in_expr(
            ...     staff, leaves)

        ..  doctest::

            >>> f(staff)
            \new Staff {
                {
                    \time 5/8
                    c'4 ~
                    c'4 ~
                    c'8
                }
                {
                    \time 3/8
                    c'4.
                }
            }

        ::

            >>> show(staff) # doctest: +SKIP

    Usage follows the two-step instantiate-then-call pattern shown here.
    '''

    ### CLASS VARIABLES ###

    _default_positional_input_arguments = (
        )

    ### INITIALIZER ###

    def __init__(
        self,
        decrease_durations_monotonically=True,
        forbidden_written_duration=None,
        tie_rests=False,
        ):
        DivisionIncisedNoteRhythmMaker.__init__(
            self,
            [],
            [0],
            [],
            [0],
            1,
            decrease_durations_monotonically=decrease_durations_monotonically,
            forbidden_written_duration=forbidden_written_duration,
            tie_rests=tie_rests,
            )

    ### SPECIAL METHODS ###

    def __repr__(self):
        r'''Note rhythm-maker interpreter representation.

        Returns string.
        '''
        return '%s()' % self._class_name

    ### PUBLIC PROPERTIES ###

    @property
    def storage_format(self):
        r'''Note rhythm-maker storage format:

        ::

            >>> print maker.storage_format
            rhythmmakertools.NoteRhythmMaker(
                decrease_durations_monotonically=True,
                forbidden_written_duration=durationtools.Duration(1, 2),
                tie_rests=False
                )

        Returns string.
        '''
        return super(NoteRhythmMaker, self).storage_format

    ### PUBLIC METHODS ###

    def new(self, **kwargs):
        r'''Create new note rhythm-maker:

        ::

            >>> new_maker = maker.new(decrease_durations_monotonically=False)

        ::

            >>> print new_maker.storage_format
            rhythmmakertools.NoteRhythmMaker(
                decrease_durations_monotonically=False,
                forbidden_written_duration=durationtools.Duration(1, 2),
                tie_rests=False
                )

        ::

            >>> divisions = [(5, 8), (3, 8)]
            >>> leaf_lists = new_maker(divisions)
            >>> leaves = sequencetools.flatten_sequence(leaf_lists)
            >>> measures = \
            ...     measuretools.make_measures_with_full_measure_spacer_skips(
            ...     divisions)
            >>> staff = Staff(measures)
            >>> measures = measuretools.replace_contents_of_measures_in_expr(
            ...     staff, leaves)

        ::

            >>> show(staff) # doctest: +SKIP

        Returns new note rhythm-maker.
        '''
        return DivisionIncisedNoteRhythmMaker.new(self, **kwargs)

    def reverse(self):
        r'''Reverse note rhythm-maker:

        ::

            >>> reversed_maker = maker.reverse()

        ::

            >>> print reversed_maker.storage_format
            rhythmmakertools.NoteRhythmMaker(
                decrease_durations_monotonically=False,
                forbidden_written_duration=durationtools.Duration(1, 2),
                tie_rests=False
                )

        ::

            >>> divisions = [(5, 8), (3, 8)]
            >>> leaf_lists = reversed_maker(divisions)
            >>> leaves = sequencetools.flatten_sequence(leaf_lists)
            >>> measures = \
            ...     measuretools.make_measures_with_full_measure_spacer_skips(
            ...     divisions)
            >>> staff = Staff(measures)
            >>> measures = measuretools.replace_contents_of_measures_in_expr(
            ...     staff, leaves)

        ::

            >>> show(staff) # doctest: +SKIP

        Returns new note rhythm-maker.
        '''
        return DivisionIncisedNoteRhythmMaker.reverse(self)
