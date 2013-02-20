from abjad.tools import durationtools
from abjad.tools import skiptools
from abjad.tools.rhythmmakertools.RhythmMaker import RhythmMaker
import fractions


class SkipRhythmMaker(RhythmMaker):
    r'''.. versionadded:: 2.10

    Skip rhythm-maker:

    ::

        >>> maker = rhythmmakertools.SkipRhythmMaker()

    Initialize and then call on arbitrary divisions:

    ::

        >>> divisions = [(1, 4), (3, 16), (5, 8)]
        >>> leaf_lists = maker(divisions)
        >>> music = sequencetools.flatten_sequence(leaf_lists)
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

    def __init__(self):
        pass

    ### SPECIAL METHODS ###

    def __call__(self, divisions, seeds=None):
        '''Call skip rhythm-maker on `divisions`.

        Return list of skips.
        '''
        result = []
        for division in divisions:
            written_duration = durationtools.Duration(1)
            multiplied_duration = division
            skip = skiptools.make_skips_with_multiplied_durations(written_duration, [multiplied_duration])
            result.append(skip)
        return result

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def storage_format(self):
        '''Skip rhythm-maker storage format:

        ::

            >>> z(maker)
            rhythmmakertools.SkipRhythmMaker()

        Return string.
        '''
        return RhythmMaker.storage_format(self)

    ### PUBLIC METHODS ###

    def new(self, **kwargs):
        '''Create new skip rhythm-maker with `kwargs`:

        ::

            >>> new_maker = maker.new()

        ::

            >>> z(new_maker)
            rhythmmakertools.SkipRhythmMaker()

        ::
    
            >>> divisions = [(1, 4), (3, 16), (5, 8)]
            >>> leaf_lists = new_maker(divisions)
            >>> music = sequencetools.flatten_sequence(leaf_lists)
            >>> measures = measuretools.make_measures_with_full_measure_spacer_skips(divisions)
            >>> staff = stafftools.RhythmicStaff(measures)
            >>> measures = measuretools.replace_contents_of_measures_in_expr(staff, music)

        ::

            >>> show(staff) # doctest: +SKIP

        Return new skip rhythm-maker.
        '''
        return RhythmMaker.new(self, **kwargs)

    def reverse(self):
        '''Reverse skip rhythm-maker:

        ::

            >>> reversed_maker = maker.reverse()

        ::

            >>> z(reversed_maker)
            rhythmmakertools.SkipRhythmMaker()

        ::
    
            >>> divisions = [(1, 4), (3, 16), (5, 8)]
            >>> leaf_lists = reversed_maker(divisions)
            >>> music = sequencetools.flatten_sequence(leaf_lists)
            >>> measures = measuretools.make_measures_with_full_measure_spacer_skips(divisions)
            >>> staff = stafftools.RhythmicStaff(measures)
            >>> measures = measuretools.replace_contents_of_measures_in_expr(staff, music)

        ::

            >>> show(staff) # doctest: +SKIP

        Return new skip rhythm-maker.
        '''
        return RhythmMaker.reverse(self)
