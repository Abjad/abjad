# -*- encoding: utf-8 -*-
from abjad.tools import scoretools
from abjad.tools.rhythmmakertools.RhythmMaker import RhythmMaker


class RestRhythmMaker(RhythmMaker):
    r'''Rest rhythm-maker.

    ..  container:: example

        Makes rests equal to the duration of input divisions.

        ::

            >>> maker = rhythmmakertools.RestRhythmMaker()

        ::

            >>> divisions = [(5, 16), (3, 8)]
            >>> leaf_lists = maker(divisions)
            >>> leaves = sequencetools.flatten_sequence(leaf_lists)
            >>> measures = scoretools.make_spacer_skip_measures(divisions)
            >>> staff = scoretools.RhythmicStaff(measures)
            >>> measures = mutate(staff).replace_measure_contents(leaves)
            >>> show(staff) # doctest: +SKIP

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

    ..  container:: example

        Forbids rests with written duration greater than or equal to ``1/4`` of
        a whole note:

        ::

            >>> maker = rhythmmakertools.RestRhythmMaker(
            ...     forbidden_written_duration=Duration(1, 4),
            ...     )

        ::

            >>> divisions = [(5, 16), (3, 8)]
            >>> leaf_lists = maker(divisions)
            >>> leaves = sequencetools.flatten_sequence(leaf_lists)
            >>> measures = scoretools.make_spacer_skip_measures(divisions)
            >>> staff = scoretools.RhythmicStaff(measures)
            >>> measures = mutate(staff).replace_measure_contents(leaves)
            >>> show(staff) # doctest: +SKIP

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

    Usage follows the two-step configure-then-call pattern shown here.
    '''

    ### INITIALIZER ###

    def __init__(
        self, 
        decrease_durations_monotonically=True,
        forbidden_written_duration=None,
        ):
        self._decrease_durations_monotonically = \
            decrease_durations_monotonically
        self._forbidden_written_duration = forbidden_written_duration

    ### SPECIAL METHODS ###

    def __call__(self, divisions, seeds=None):
        r'''Calls rest rhythm-maker on `divisions`.

        Returns list of selections.
        '''
        result = []
        for division in divisions:
            rests = scoretools.make_leaves(
                pitches=None, 
                durations=[division],
                decrease_durations_monotonically=\
                    self.decrease_durations_monotonically,
                forbidden_written_duration=self.forbidden_written_duration,
                )
            result.append(rests)
        return result

    def __format__(self, format_specification=''):
        r'''Formats rest rhythm-maker.

        Set `format_specification` to `''` or `'storage'`.

        ::

            >>> print format(maker)
            rhythmmakertools.RestRhythmMaker(
                decrease_durations_monotonically=True,
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
                decrease_durations_monotonically=True,
                forbidden_written_duration=durationtools.Duration(1, 4),
                )

        ::

            >>> divisions = [(5, 16), (3, 8)]
            >>> leaf_lists = new_maker(divisions)
            >>> leaves = sequencetools.flatten_sequence(leaf_lists)
            >>> measures = scoretools.make_spacer_skip_measures(divisions)
            >>> staff = scoretools.RhythmicStaff(measures)
            >>> measures = mutate(staff).replace_measure_contents(leaves)
            >>> show(staff) # doctest: +SKIP

        Returns new rest rhythm-maker.
        '''
        return RhythmMaker.__makenew__(self, *args, **kwargs)

    ### PUBLIC PROPERTIES ###

    @property
    def decrease_durations_monotonically(self):
        r'''Gets decrease durations monotonically flag.

        Returns boolean.
        '''
        return self._decrease_durations_monotonically

    @property
    def forbidden_written_duration(self):
        r'''Gets forbidden written duration.

        Returns duration or none.
        '''
        return self._forbidden_written_duration

    ### PUBLIC METHODS ###

    def reverse(self):
        r'''Reverses rest rhythm-maker.

        ::

            >>> reversed_maker = maker.reverse()

        ::

            >>> print format(reversed_maker)
            rhythmmakertools.RestRhythmMaker(
                decrease_durations_monotonically=True,
                forbidden_written_duration=durationtools.Duration(1, 4),
                )

        ::

            >>> divisions = [(5, 16), (3, 8)]
            >>> leaf_lists = reversed_maker(divisions)
            >>> leaves = sequencetools.flatten_sequence(leaf_lists)
            >>> measures = scoretools.make_spacer_skip_measures(divisions)
            >>> staff = scoretools.RhythmicStaff(measures)
            >>> measures = mutate(staff).replace_measure_contents(leaves)
            >>> show(staff) # doctest: +SKIP

        Returns new rest rhythm-maker.
        '''
        return RhythmMaker.reverse(self)
