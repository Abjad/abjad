from abjad.tools import durationtools
from abjad.tools import skiptools
from abjad.tools.rhythmmakertools.RhythmMaker import RhythmMaker
import fractions


class SkipFilledRhythmMaker(RhythmMaker):
    r'''.. versionadded:: 2.10

    Skip-filled rhythm maker::

        >>> maker = rhythmmakertools.SkipFilledRhythmMaker()

    ::

        >>> divisions = [(1, 5), (1, 4), (1, 6), (7, 9)]
        >>> leaf_lists = maker(divisions)
        >>> leaves = sequencetools.flatten_sequence(leaf_lists)

    ::

        >>> staff = Staff(leaves)

    ::

        >>> f(staff)
        \new Staff {
            s1 * 1/5
            s1 * 1/4
            s1 * 1/6
            s1 * 7/9
        }

    Usage follows the two-step instantiate-then-call talea shown here.

    Return rhythm maker.
    '''

    ### CLASS ATTRIBUTES ###

    _default_mandatory_input_arguments = ()

    ### INITIALIZER ###

    def __init__(self):
        pass

    ### SPECIAL METHODS ###

    def __call__(self, divisions, seeds=None):
        result = []
        for division in divisions:
            written_duration = durationtools.Duration(1)
            multiplied_duration = division
            skip = skiptools.make_skips_with_multiplied_durations(written_duration, [multiplied_duration])
            result.append(skip)
        return result
