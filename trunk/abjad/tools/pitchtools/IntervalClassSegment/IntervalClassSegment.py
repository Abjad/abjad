# -*- encoding: utf-8 -*-
import abc
from abjad.tools.pitchtools.Segment import Segment


class IntervalClassSegment(Segment):
    '''.. versionadded:: 2.0

    Interval-class segment base class.
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
