import math
from abjad.tools import componenttools
from abjad.tools import durationtools
from abjad.tools import leaftools
from abjad.tools import mathtools
from abjad.tools import tuplettools
from abjad.tools.rhythmmakertools.RhythmMaker import RhythmMaker


class EqualDivisionRhythmMaker(RhythmMaker):
    r'''.. versionadded:: 2.10

    Equal division rhythm-maker::

        >>> maker = rhythmmakertools.EqualDivisionRhythmMaker(4)

    ::

        >>> divisions = [(1, 4), (1, 8), (1, 6), (1, 12)]
        >>> tuplet_lists = maker(divisions)
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

    Return rhythm-maker.
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

    def __call__(self, divisions, seeds=None):
        result = []
        for division in divisions:
            tuplet = self._make_tuplet(division)
            result.append([tuplet])
        return result

    ### PRIVATE METHODS ###

    def _make_tuplet(self, division):
        numerator, denominator = division
        token_duration = durationtools.Duration(division)
        ratio = self.leaf_count * [1]
        tuplet = tuplettools.make_tuplet_from_duration_and_ratio(
            token_duration, ratio, avoid_dots=True, is_diminution=self.is_diminution)
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
