from abjad.tools.pitchtools._Segment import _Segment


class _IntervalSegment(_Segment):
    '''.. versionadded:: 2.0

    Class of abstract ordered collection of interval instances
    from which concrete classes inherit.
    '''

    ### OVERLOADS ###

    def __repr__(self):
        return '%s(%s)' % (type(self).__name__, self._format_string)

    def __str__(self):
        return '<%s>' % self._format_string

    ### PRIVATE ATTRIBUTES ###

    @property
    def _format_string(self):
        return ', '.join([str(x) for x in self])

    ### PUBLIC ATTRIBUTES ###

    @property
    def interval_classes(self):
        return tuple([interval.interval_class for interval in self])

    @property
    def intervals(self):
        return self[:]

    ### PUBLIC METHODS ###

    def rotate(self, n):
        #self[:] = self[-n:] + self[:-n]
        return type(self)(self[-n:] + self[:-n])
