from abjad.tools.pitchtools._IntervalClassSegment import _IntervalClassSegment


class InversionEquivalentChromaticIntervalClassSegment(_IntervalClassSegment):
    '''.. versionadded:: 2.0

    Abjad model of inversion-equivalent chromatic interval-class segment::

        abjad> pitchtools.InversionEquivalentChromaticIntervalClassSegment([2, 1, 0, 5.5, 6])
        InversionEquivalentChromaticIntervalClassSegment(2, 1, 0, 5.5, 6)

    Inversion-equivalent chromatic interval-class segments are immutable.
    '''

    def __new__(self, interval_class_tokens):
        from abjad.tools import pitchtools
        interval_classes = [pitchtools.InversionEquivalentChromaticIntervalClass(x) for x in interval_class_tokens]
        return tuple.__new__(self, interval_classes)

    ### OVERLOADS ###

    def __repr__(self):
        return '%s(%s)' % (type(self).__name__, self._format_string)

    ### PRIVATE ATTRIBUTES ###

    @property
    def _format_string(self):
        return ', '.join([str(x) for x in self])
