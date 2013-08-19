# -*- encoding: utf-8 -*-
from abjad.tools.pitchtools.NamedInversionEquivalentIntervalClass \
	import NamedInversionEquivalentIntervalClass
from abjad.tools.pitchtools.IntervalSegment import IntervalSegment


class NamedInversionEquivalentIntervalClassSegment(IntervalSegment):
    '''Abjad model of inversion-equivalent diatonic interval-class segment:

    ::

        >>> pitchtools.NamedInversionEquivalentIntervalClassSegment(
        ... [('major', 2), ('major', 9), ('minor', -2), ('minor', -9)])
        NamedInversionEquivalentIntervalClassSegment(M2, M2, m2, m2)

    Inversion-equivalent diatonic interval-class segments are immutable.
    '''

    ### CONSTRUCTOR ###

    def __new__(self, diatonic_interval_class_tokens):
        dics = []
        for token in diatonic_interval_class_tokens:
            dic = NamedInversionEquivalentIntervalClass(token)
            dics.append(dic)
        return tuple.__new__(self, dics)

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
