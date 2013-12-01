# -*- encoding: utf-8 -*-
from abjad.tools import sequencetools
from abjad.tools.pitchtools.Vector import Vector


class IntervalClassVector(Vector):
    r'''An interval-class vector.

    ::

        >>> pitch_segment = pitchtools.PitchSegment(
        ...     tokens=[0, 11, 7, 4, 2, 9, 3, 8, 10, 1, 5, 6],
        ...     )
        >>> numbered_interval_class_vector = pitchtools.IntervalClassVector(
        ...     tokens=pitch_segment,
        ...     item_class=pitchtools.NumberedInversionEquivalentIntervalClass,
        ...     )
        >>> for interval, count in numbered_interval_class_vector.iteritems():
        ...     print interval, count
        ...
        2 12
        3 12
        5 12
        4 12
        6 6
        1 12

    '''

    ### INITIALIZER ###

    def __init__(self, tokens=None, item_class=None, custom_identifier=None):
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
            custom_identifier=custom_identifier,
            )

    ### PRIVATE PROPERTIES ###

    @property
    def _named_item_class(self):
        from abjad.tools import pitchtools
        return pitchtools.NamedIntervalClass
    
    @property
    def _numbered_item_class(self):
        from abjad.tools import pitchtools
        return pitchtools.NumberedIntervalClass

    @property
    def _parent_item_class(self):
        from abjad.tools import pitchtools
        return pitchtools.IntervalClass

    ### PUBLIC METHODS ###

    @classmethod
    def from_selection(
        cls, 
        selection, 
        item_class=None, 
        custom_identifier=None,
        ):
        r'''Makes interval-class vector from `selection`.

        Returns interval-class vector.
        '''
        from abjad.tools import pitchtools
        pitch_segment = pitchtools.PitchSegment.from_selection(selection)
        return cls(
            pitch_segment,
            item_class=item_class,
            custom_identifier=custom_identifier,
            )
