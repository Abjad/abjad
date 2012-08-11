from abjad.tools.pitchtools.InversionEquivalentDiatonicIntervalClass import InversionEquivalentDiatonicIntervalClass
from abjad.tools.pitchtools.IntervalObjectSegment import IntervalObjectSegment


class InversionEquivalentDiatonicIntervalClassSegment(IntervalObjectSegment):
    '''.. versionadded:: 2.0

    Abjad model of inversion-equivalent diatonic interval-class segment::

        >>> pitchtools.InversionEquivalentDiatonicIntervalClassSegment(
        ... [('major', 2), ('major', 9), ('minor', -2), ('minor', -9)])
        InversionEquivalentDiatonicIntervalClassSegment(M2, M2, m2, m2)

    Inversion-equivalent diatonic interval-class segments are immutable.
    '''

    def __new__(self, diatonic_interval_class_tokens):
        dics = []
        for token in diatonic_interval_class_tokens:
            dic = InversionEquivalentDiatonicIntervalClass(token)
            dics.append(dic)
        return tuple.__new__(self, dics)

    ### SPECIAL METHODS ###

    def __copy__(self):
        return type(self)(self.intervals)

    ### PUBLIC PROPERTIES ###

    @property
    def is_tertian(self):
        '''True when all diatonic interval-classes in segment are tertian.
        Otherwise false::

            >>> dics = pitchtools.InversionEquivalentDiatonicIntervalClassSegment(
            ... [('major', 3), ('minor', 6), ('major', 6)])
            >>> dics.is_tertian
            True

        Return boolean.
        '''
        for dic in self:
            if not dic.number == 3:
                return False
        return True
