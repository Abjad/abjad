from abjad.tools import durationtools
from abjad.tools import skiptools
from abjad.tools.timetokentools.TimeTokenMaker import TimeTokenMaker
import fractions


class SkipFilledTimeTokenMaker(TimeTokenMaker):
    r'''.. versionadded:: 2.10

    Skip-filled time-token maker::

        >>> maker = timetokentools.SkipFilledTimeTokenMaker()

    ::

        >>> duration_tokens = [(1, 5), (1, 4), (1, 6), (7, 9)]
        >>> leaf_lists = maker(duration_tokens)
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

    Usage follows the two-step instantiate-then-call pattern shown here.

    Return time-token maker.
    '''

    ### CLASS ATTRIBUTES ###

    _default_mandatory_input_arguments = ()

    ### INITIALIZER ###

    def __init__(self):
        pass

    ### SPECIAL METHODS ###

    def __call__(self, duration_tokens, seeds=None):
        result = []
        for duration_token in duration_tokens:
            written_duration = durationtools.Duration(1)
            multiplied_duration = duration_token
            skip = skiptools.make_skips_with_multiplied_durations(written_duration, [multiplied_duration])
            result.append(skip)
        return result
