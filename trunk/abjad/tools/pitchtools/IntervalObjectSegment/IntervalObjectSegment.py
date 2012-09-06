import abc
from abjad.tools.pitchtools.ObjectSegment import ObjectSegment


class IntervalObjectSegment(ObjectSegment):
    '''.. versionadded:: 2.0

    Class of abstract ordered collection of interval instances
    from which concrete classes inherit.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta

    ### INITIALIZER ###

    @abc.abstractmethod
    def __new__(self):
        pass

    ### SPECIAL METHODS ###

    def __repr__(self):
        return '%s(%s)' % (type(self).__name__, self._format_string)

    def __str__(self):
        return '<%s>' % self._format_string

    ### PRIVATE PROPERTIES ###

    @property
    def _format_string(self):
        return ', '.join([str(x) for x in self])

    ### PUBLIC PROPERTIES ###

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
