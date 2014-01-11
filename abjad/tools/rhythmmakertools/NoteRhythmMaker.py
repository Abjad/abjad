# -*- encoding: utf-8 -*-
from abjad.tools.rhythmmakertools.DivisionIncisedNoteRhythmMaker \
    import DivisionIncisedNoteRhythmMaker


class NoteRhythmMaker(DivisionIncisedNoteRhythmMaker):
    r'''Note rhythm-maker.

    ..  container:: example

        Makes notes equal to the duration of input divisions. Adds ties where
        necessary:

        ::

            >>> maker = rhythmmakertools.NoteRhythmMaker()

        ::

            >>> divisions = [(5, 8), (3, 8)]
            >>> leaf_lists = maker(divisions)
            >>> leaves = sequencetools.flatten_sequence(leaf_lists)
            >>> measures = scoretools.make_spacer_skip_measures(divisions)
            >>> staff = Staff(measures)
            >>> measures = mutate(staff).replace_measure_contents(leaves)
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> print format(staff)
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

    ..  container:: example
    
        Forbids notes with written duration greater than or equal to ``1/2``
        of a whole note:

        ::

            >>> maker = rhythmmakertools.NoteRhythmMaker(
            ...     forbidden_written_duration=Duration(1, 2),
            ...     )

        ::

            >>> divisions = [(5, 8), (3, 8)]
            >>> leaf_lists = maker(divisions)
            >>> leaves = sequencetools.flatten_sequence(leaf_lists)
            >>> measures = scoretools.make_spacer_skip_measures(divisions)
            >>> staff = Staff(measures)
            >>> measures = mutate(staff).replace_measure_contents(leaves)
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> print format(staff)
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

    Usage follows the two-step configure-then-call pattern shown here.
    '''

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

    def __format__(self, format_specification=''):
        r'''Formats note rhythm-maker.

        Set `format_specification` to `''` or `'storage'`.

        ::

            >>> print format(maker)
            rhythmmakertools.NoteRhythmMaker(
                decrease_durations_monotonically=True,
                forbidden_written_duration=durationtools.Duration(1, 2),
                tie_rests=False,
                )

        Returns string.
        '''
        superclass = super(NoteRhythmMaker, self)
        return superclass.__format__(format_specification=format_specification)

    def __makenew__(self, *args, **kwargs):
        r'''Makes new note rhythm-maker.

        ::

            >>> new_maker = new(maker, decrease_durations_monotonically=False)

        ::

            >>> print format(new_maker)
            rhythmmakertools.NoteRhythmMaker(
                decrease_durations_monotonically=False,
                forbidden_written_duration=durationtools.Duration(1, 2),
                tie_rests=False,
                )

        ::

            >>> divisions = [(5, 8), (3, 8)]
            >>> leaf_lists = new_maker(divisions)
            >>> leaves = sequencetools.flatten_sequence(leaf_lists)
            >>> measures = scoretools.make_spacer_skip_measures(divisions)
            >>> staff = Staff(measures)
            >>> measures = mutate(staff).replace_measure_contents(leaves)
            >>> show(staff) # doctest: +SKIP

        Returns new note rhythm-maker.
        '''
        return DivisionIncisedNoteRhythmMaker.__makenew__(
            self, *args, **kwargs)

    ### PUBLIC METHODS ###

    def reverse(self):
        r'''Reverses note rhythm-maker.

        ::

            >>> reversed_maker = maker.reverse()

        ::

            >>> print format(reversed_maker)
            rhythmmakertools.NoteRhythmMaker(
                decrease_durations_monotonically=False,
                forbidden_written_duration=durationtools.Duration(1, 2),
                tie_rests=False,
                )

        ::

            >>> divisions = [(5, 8), (3, 8)]
            >>> leaf_lists = reversed_maker(divisions)
            >>> leaves = sequencetools.flatten_sequence(leaf_lists)
            >>> measures = scoretools.make_spacer_skip_measures(divisions)
            >>> staff = Staff(measures)
            >>> measures = mutate(staff).replace_measure_contents(leaves)
            >>> show(staff) # doctest: +SKIP

        Returns new note rhythm-maker.
        '''
        return DivisionIncisedNoteRhythmMaker.reverse(self)
