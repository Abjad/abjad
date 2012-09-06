import abc
from abjad.tools.pitchtools.ObjectSegment import ObjectSegment


class IntervalClassObjectSegment(ObjectSegment):
    '''.. versionadded:: 2.0

    Interval-class segment base class.
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

    ### PRIVATE PROPERTIES ###

    @property
    def _format_string(self):
        return ', '.join([str(x) for x in self])

    ### PUBLIC PROPERTIES ###

    @property
    def interval_class_numbers(self):
        return tuple([interval_class.number for interval_class in self])

    @property
    def interval_classes(self):
        return tuple(self[:])
