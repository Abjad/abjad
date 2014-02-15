# -*- encoding: utf-8 -*-
from abjad.tools import sequencetools
from abjad.tools.pitchtools.Set import Set


class IntervalSet(Set):
    r'''An interval set.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(self, tokens=None, item_class=None):
        from abjad.tools import pitchtools
        prototype = (
            pitchtools.PitchClassSegment,
            pitchtools.PitchClassSet,
            pitchtools.PitchSegment,
            pitchtools.PitchSet,
            )
        if isinstance(tokens, prototype):
            tokens = list(tokens)
            pairs = sequencetools.yield_all_unordered_pairs_of_sequence(
                tokens)
            tokens = [second - first for first, second in pairs]
        Set.__init__(
            self,
            tokens=tokens,
            item_class=item_class,
            )

    ### PRIVATE PROPERTIES ###

    @property
    def _named_item_class(self):
        from abjad.tools import pitchtools
        return pitchtools.NamedInterval

    @property
    def _numbered_item_class(self):
        from abjad.tools import pitchtools
        return pitchtools.NumberedInterval

    @property
    def _parent_item_class(self):
        from abjad.tools import pitchtools
        return pitchtools.Interval

    ### PUBLIC METHODS ###

    @classmethod
    def from_selection(cls, selection, item_class=None):
        r'''Initialize interval set from component selection:

        ::

            >>> staff_1 = Staff("c'4 <d' fs' a'>4 b2")
            >>> staff_2 = Staff("c4. r8 g2")
            >>> selection = select((staff_1, staff_2))
            >>> intervals = pitchtools.IntervalSet.from_selection(
            ...     selection)
            >>> for interval in intervals:
            ...     interval
            ...
            NamedInterval('+m3')
            NamedInterval('+M3')
            NamedInterval('+P4')
            NamedInterval('+M7')
            NamedInterval('-M6')
            NamedInterval('+m2')
            NamedInterval('+aug11')
            NamedInterval('-P5')
            NamedInterval('+M13')
            NamedInterval('+P8')
            NamedInterval('-M3')
            NamedInterval('-aug4')
            NamedInterval('+M9')
            NamedInterval('+m7')
            NamedInterval('-M2')
            NamedInterval('-m3')
            NamedInterval('+P5')

        Returns interval set.
        '''
        from abjad.tools import pitchtools
        pitch_segment = pitchtools.PitchSegment.from_selection(selection)
        pairs = sequencetools.yield_all_unordered_pairs_of_sequence(
            pitch_segment)
        intervals = (second - first for first, second in pairs)
        return cls(
            tokens=intervals,
            item_class=item_class,
            )
