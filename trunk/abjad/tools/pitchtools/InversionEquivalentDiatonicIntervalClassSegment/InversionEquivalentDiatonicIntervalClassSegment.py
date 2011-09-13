from abjad.tools.pitchtools.InversionEquivalentDiatonicIntervalClass import InversionEquivalentDiatonicIntervalClass
from abjad.tools.pitchtools._IntervalSegment import _IntervalSegment


class InversionEquivalentDiatonicIntervalClassSegment(_IntervalSegment):
    '''.. versionadded:: 2.0

    Abjad model of inversion-equivalent diatonic interval-class segment::

        abjad> pitchtools.InversionEquivalentDiatonicIntervalClassSegment([('major', 2), ('major', 9), ('minor', -2), ('minor', -9)])
        InversionEquivalentDiatonicIntervalClassSegment(M2, M2, m2, m2)

    Inversion-equivalent diatonic interval-class segments are immutable.
    '''

    def __new__(self, diatonic_interval_class_tokens):
        dics = []
        for token in diatonic_interval_class_tokens:
            dic = InversionEquivalentDiatonicIntervalClass(token)
            dics.append(dic)
        return tuple.__new__(self, dics)

    ### OVERLOADS ###

    def __copy__(self):
        return type(self)(self.intervals)

    ### PUBLIC ATTRIBUTES ###

    @property
    def is_tertian(self):
        '''True when all diatonic interval-classes in segment are tertian.
        Otherwise false::

            abjad> dics = pitchtools.InversionEquivalentDiatonicIntervalClassSegment([('major', 3), ('minor', 6), ('major', 6)])
            abjad> dics.is_tertian
            True

        Return boolean.
        '''
        for dic in self:
            if not dic.number == 3:
                return False
        return True
