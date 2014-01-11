# -*- encoding: utf-8 -*-
import fractions
from abjad.tools import durationtools
from abjad.tools import scoretools
from abjad.tools.rhythmmakertools.RhythmMaker import RhythmMaker


class SkipRhythmMaker(RhythmMaker):
    r'''Skip rhythm-maker.

    ::

        >>> maker = rhythmmakertools.SkipRhythmMaker()

    Initialize and then call on arbitrary divisions:

    ::

        >>> divisions = [(1, 4), (3, 16), (5, 8)]
        >>> leaf_lists = maker(divisions)
        >>> music = sequencetools.flatten_sequence(leaf_lists)
        >>> measures = scoretools.make_spacer_skip_measures(divisions)
        >>> staff = scoretools.RhythmicStaff(measures)
        >>> measures = mutate(staff).replace_measure_contents(music)
        >>> show(staff) # doctest: +SKIP

    Usage follows the two-step instantiate-then-call pattern shown here.
    '''

    ### CLASS VARIABLES ###

    _default_positional_input_arguments = (
        )

    ### INITIALIZER ###

    def __init__(self):
        pass

    ### SPECIAL METHODS ###

    def __call__(self, divisions, seeds=None):
        r'''Calls skip rhythm-maker on `divisions`.

        Returns list of skips.
        '''
        result = []
        for division in divisions:
            written_duration = durationtools.Duration(1)
            multiplied_duration = division
            skip = scoretools.make_skips_with_multiplied_durations(
                written_duration, [multiplied_duration])
            result.append(skip)
        return result

    def __format__(self, format_specification=''):
        r'''Formats skip rhythm-maker.

        Set `format_specification` to `''` or `'storage'`.

        ::

            >>> print format(maker)
            rhythmmakertools.SkipRhythmMaker()

        Returns string.
        '''
        superclass = super(SkipRhythmMaker, self)
        return superclass.__format__(format_specification=format_specification)

    def __makenew__(self, *args, **kwargs):
        r'''Makes new skip rhythm-maker with `kwargs`.

        ::

            >>> new_maker = new(maker)

        ::

            >>> print format(new_maker)
            rhythmmakertools.SkipRhythmMaker()

        ::

            >>> divisions = [(1, 4), (3, 16), (5, 8)]
            >>> leaf_lists = new_maker(divisions)
            >>> music = sequencetools.flatten_sequence(leaf_lists)
            >>> measures = scoretools.make_spacer_skip_measures(divisions)
            >>> staff = scoretools.RhythmicStaff(measures)
            >>> measures = mutate(staff).replace_measure_contents(music)
            >>> show(staff) # doctest: +SKIP

        Returns new skip rhythm-maker.
        '''
        return RhythmMaker.__makenew__(self, *args, **kwargs)

    ### PUBLIC METHODS ###

    def reverse(self):
        r'''Reverses skip rhythm-maker.

        ::

            >>> reversed_maker = maker.reverse()

        ::

            >>> print format(reversed_maker)
            rhythmmakertools.SkipRhythmMaker()

        ::

            >>> divisions = [(1, 4), (3, 16), (5, 8)]
            >>> leaf_lists = reversed_maker(divisions)
            >>> music = sequencetools.flatten_sequence(leaf_lists)
            >>> measures = scoretools.make_spacer_skip_measures(divisions)
            >>> staff = scoretools.RhythmicStaff(measures)
            >>> measures = mutate(staff).replace_measure_contents(music)
            >>> show(staff) # doctest: +SKIP

        Returns new skip rhythm-maker.
        '''
        return RhythmMaker.reverse(self)
