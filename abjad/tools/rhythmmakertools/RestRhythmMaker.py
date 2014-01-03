# -*- encoding: utf-8 -*-
from abjad.tools.rhythmmakertools.DivisionIncisedRestRhythmMaker \
	import DivisionIncisedRestRhythmMaker


class RestRhythmMaker(DivisionIncisedRestRhythmMaker):
    r'''Rest rhythm-maker.

    ..  container:: example

        **Example 1:**

        ::

            >>> maker = rhythmmakertools.RestRhythmMaker()

        Initialize and then call on arbitrary divisions:

        ::

            >>> divisions = [(5, 16), (3, 8)]
            >>> leaf_lists = maker(divisions)
            >>> leaves = sequencetools.flatten_sequence(leaf_lists)
            >>> measures = \
            ...     scoretools.make_spacer_skip_measures(
            ...     divisions)
            >>> staff = scoretools.RhythmicStaff(measures)
            >>> measures = scoretools.replace_contents_of_measures_in_expr(
            ...     staff, leaves)

        ..  doctest::

            >>> print format(staff)
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

    ..  container:: example

        **Example 2.** Forbid written durations greater than or equal to a half 
        note:

        ::

            >>> maker = rhythmmakertools.RestRhythmMaker(
            ...     forbidden_written_duration=Duration(1, 4))

        ::

            >>> divisions = [(5, 16), (3, 8)]
            >>> leaf_lists = maker(divisions)
            >>> leaves = sequencetools.flatten_sequence(leaf_lists)
            >>> measures = \
            ...     scoretools.make_spacer_skip_measures(
            ...     divisions)
            >>> staff = scoretools.RhythmicStaff(measures)
            >>> measures = scoretools.replace_contents_of_measures_in_expr(
            ...     staff, leaves)

        ..  doctest::

            >>> print format(staff)
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

    ### CLASS VARIABLES ###

    _default_positional_input_arguments = (
        )

    ### INITIALIZER ###

    def __init__(self, forbidden_written_duration=None):
        DivisionIncisedRestRhythmMaker.__init__(
            self, [],
            [0],
            [],
            [0],
            1,
            decrease_durations_monotonically=True,
            forbidden_written_duration=forbidden_written_duration,
            tie_rests=False,
            )

    ### SPECIAL METHODS ###

    def __format__(self, format_specification=''):
        r'''Formats rest rhythm-maker.

        Set `format_specification` to `''` or `'storage'`.

        ::

            >>> print format(maker)
            rhythmmakertools.RestRhythmMaker(
                forbidden_written_duration=durationtools.Duration(1, 4),
                )

        Returns string.
        '''
        superclass = super(RestRhythmMaker, self)
        return superclass.__format__(format_specification=format_specification)

    def __makenew__(self, *args, **kwargs):
        r'''Makes new rest rhythm-maker with `kwargs`.

        ::

            >>> new_maker = new(maker)

        ::

            >>> print format(new_maker)
            rhythmmakertools.RestRhythmMaker(
                forbidden_written_duration=durationtools.Duration(1, 4),
                )

        ::

            >>> divisions = [(5, 16), (3, 8)]
            >>> leaf_lists = new_maker(divisions)
            >>> leaves = sequencetools.flatten_sequence(leaf_lists)
            >>> measures = \
            ...     scoretools.make_spacer_skip_measures(
            ...     divisions)
            >>> staff = scoretools.RhythmicStaff(measures)
            >>> measures = scoretools.replace_contents_of_measures_in_expr(
            ...     staff, leaves)

        ::

            >>> show(staff) # doctest: +SKIP

        Returns new rest rhythm-maker.
        '''
        return DivisionIncisedRestRhythmMaker.__makenew__(
            self, *args, **kwargs)

    ### PUBLIC METHODS ###

    def reverse(self):
        r'''Reverses rest rhythm-maker.

        ::

            >>> reversed_maker = maker.reverse()

        ::

            >>> print format(reversed_maker)
            rhythmmakertools.RestRhythmMaker(
                forbidden_written_duration=durationtools.Duration(1, 4),
                )

        ::

            >>> divisions = [(5, 16), (3, 8)]
            >>> leaf_lists = reversed_maker(divisions)
            >>> leaves = sequencetools.flatten_sequence(leaf_lists)
            >>> measures = \
            ...     scoretools.make_spacer_skip_measures(
            ...     divisions)
            >>> staff = scoretools.RhythmicStaff(measures)
            >>> measures = scoretools.replace_contents_of_measures_in_expr(
            ...     staff, leaves)

        ::

            >>> show(staff) # doctest: +SKIP

        Returns new rest rhythm-maker.
        '''
        return DivisionIncisedRestRhythmMaker.reverse(self)
