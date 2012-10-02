import math
from abjad.tools import componenttools
from abjad.tools import durationtools
from abjad.tools import leaftools
from abjad.tools import mathtools
from abjad.tools import tuplettools
from abjad.tools.timetokentools.TimeTokenMaker import TimeTokenMaker


class EqualDivisionTimeTokenMaker(TimeTokenMaker):
    r'''.. versionadded:: 2.10

    Equal division time-token maker::

        >>> maker = timetokentools.EqualDivisionTimeTokenMaker(4)

    ::

        >>> duration_tokens = [(1, 4), (1, 8), (1, 6), (1, 12)]
        >>> tuplet_lists = maker(duration_tokens)
        >>> tuplets = sequencetools.flatten_sequence(tuplet_lists)

    ::

        >>> staff = Staff(tuplets)

    ::

        >>> f(staff)
        \new Staff {
            {
                c'16
                c'16
                c'16
                c'16
            }
            {
                c'32
                c'32
                c'32
                c'32
            }
            \times 2/3 {
                c'16
                c'16
                c'16
                c'16
            }
            \times 2/3 {
                c'32
                c'32
                c'32
                c'32
            }
        }

    Usage follows the two-step instantiate-then-call pattern shown here.

    Return time-token maker.
    '''

    ### CLASS ATTRIBUTES ###

    _default_mandatory_input_arguments = ()

    ### INITIALIZER ###

    def __init__(self, leaf_count, is_diminution=True):
        assert mathtools.is_integer_equivalent_expr(leaf_count)
        leaf_count = int(leaf_count)
        self._leaf_count = leaf_count
        self._is_diminution = is_diminution

    ### SPECIAL METHODS ###

    def __call__(self, duration_tokens, seeds=None):
        result = []
        for duration_token in duration_tokens:
            tuplet = self._make_tuplet(duration_token)
            result.append([tuplet])
        return result

    ### PRIVATE METHODS ###

    def _make_tuplet(self, duration_token):
        numerator, denominator = duration_token
        token_duration = durationtools.Duration(duration_token)
        proportions = self.leaf_count * [1]
        tuplet = tuplettools.make_tuplet_from_duration_and_proportions(
            token_duration, proportions, avoid_dots=True, is_diminution=self.is_diminution)
        return tuplet

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def is_diminution(self):
        '''Return boolean.
        '''
        return self._is_diminution

    @property
    def leaf_count(self):
        '''Leaf count.

        .. note:: add example.

        Return positive integer.
        '''
        return self._leaf_count
