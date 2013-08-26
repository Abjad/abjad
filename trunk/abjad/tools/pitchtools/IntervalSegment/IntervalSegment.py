# -*- encoding: utf-8 -*-
import abc
from abjad.tools.pitchtools.Segment import Segment


class IntervalSegment(Segment):
    '''Class of abstract ordered collection of interval instances
    from which concrete classes inherit.
    '''

    ### CLASS VARIABLES ###

    __metaclass__ = abc.ABCMeta

    ### INITIALIZER ###

    @abc.abstractmethod
    def __new__(self):
        pass

    ### SPECIAL METHODS ###

    def __repr__(self):
        return '%s(%s)' % (self._class_name, self._format_string)

    def __str__(self):
        return '<%s>' % self._format_string

    ### PRIVATE PROPERTIES ###

    @property
    def _format_string(self):
        return ', '.join([str(x) for x in self])

    ### PUBLIC METHODS ###

    def rotate(self, n):
        return type(self)(self[-n:] + self[:-n])
