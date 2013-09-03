from abjad.tools import sequencetools
from abjad.tools.pitchtools.Vector import Vector


class IntervalVector(Vector):

    ### INITIALIZER ###

    def __init__(self, tokens=None, item_class=None, name=None):
        from abjad.tools import pitchtools
        if isinstance(tokens, (
            pitchtools.PitchSegment, 
            pitchtools.PitchSet,
            pitchtools.PitchClassSegment,
            pitchtools.PitchClassSet,
            )):
            intervals = []
            for first, second in \
                sequencetools.yield_all_unordered_pairs_of_sequence(
                    tuple(tokens)):
                intervals.append(second - first)
            tokens = intervals
        Vector.__init__(
            self,
            tokens=tokens,
            item_class=item_class,
            name=name,
            )

    ### PRIVATE PROPERTIES ###

    @property
    def _named_item_class(self):
        from abjad.tools import pitchtools
        return pitchtools.NamedMelodicInterval
    
    @property
    def _numbered_item_class(self):
        from abjad.tools import pitchtools
        return pitchtools.NumberedMelodicInterval

    @property
    def _parent_item_class(self):
        from abjad.tools import pitchtools
        return pitchtools.Interval

    ### PUBLIC METHODS ###

    @classmethod
    def from_selection(cls, selection, item_class=None, name=None):
        from abjad.tools import pitchtools
        pitch_segment = pitchtools.PitchSegment.from_selection(selection)
        return cls(
            pitch_segment,
            item_class=item_class,
            name=name,
            )
