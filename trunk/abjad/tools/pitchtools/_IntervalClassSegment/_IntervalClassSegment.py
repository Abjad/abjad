from abjad.tools.pitchtools._Segment import _Segment


class _IntervalClassSegment(_Segment):
    '''.. versionadded:: 2.0

    Interval-class segment base class.
    '''

    ### OVERLOADS ###

    def __repr__(self):
        return '%s(%s)' % (type(self).__name__, self._format_string)

    ### PRIVATE ATTRIBUTES ###

    @property
    def _format_string(self):
        return ', '.join([str(x) for x in self])

    ### PUBLIC ATTRIBUTES ###

    @property
    def interval_class_numbers(self):
        return tuple([interval_class.number for interval_class in self])

    @property
    def interval_classes(self):
        return tuple(self[:])
