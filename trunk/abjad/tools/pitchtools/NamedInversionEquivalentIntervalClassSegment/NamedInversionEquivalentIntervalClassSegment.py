# -*- encoding: utf-8 -*-
from abjad.tools.pitchtools.IntervalClassSegment import IntervalClassSegment


class NamedInversionEquivalentIntervalClassSegment(IntervalClassSegment):
    '''Abjad model of inversion-equivalent diatonic interval-class segment:

    ::

        >>> pitchtools.NamedInversionEquivalentIntervalClassSegment(
        ... [('major', 2), ('major', 9), ('minor', -2), ('minor', -9)])
        NamedInversionEquivalentIntervalClassSegment(M2, M2, m2, m2)

    Inversion-equivalent diatonic interval-class segments are immutable.
    '''

    ### CONSTRUCTOR ###

    def __init__(self, tokens=None, item_class=None, name=None):
        from abjad.tools import pitchtools
        IntervalClassSegment.__init__(
            self,
            tokens=tokens,
            item_class=pitchtools.NamedInversionEquivalentIntervalClass,
            name=None,
            )

    ### SPECIAL METHODS ###

    def __copy__(self):
        return type(self)(self.intervals)

    ### PUBLIC PROPERTIES ###

    @property
    def is_tertian(self):
        r'''True when all diatonic interval-classes in segment are tertian.
        Otherwise false:

        ::

            >>> dics = \
            ...     pitchtools.NamedInversionEquivalentIntervalClassSegment(
            ...     [('major', 3), ('minor', 6), ('major', 6)])
            >>> dics.is_tertian
            True

        Return boolean.
        '''
        for dic in self:
            if not dic.number == 3:
                return False
        return True

