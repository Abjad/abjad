import abc
from abjad.tools import componenttools
from abjad.tools import mathtools
from abjad.tools.abctools.AbjadObject import AbjadObject
from experimental.timespantools.Timepoint import Timepoint


class Timespan(AbjadObject):
    r'''.. versionadded:: 1.0

    Base timespan from which concrete timespans inherit.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self):
        pass

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def duration(self):
        '''Rational-valued duration of timespan.
        
        Derived from input values.

        Return rational.
        
        .. note:: not yet implemented.

        .. note:: will probably have to be implemented as method instead of property.
        '''
        raise NotImplementedError

    @property
    def is_segment_slice(self):
        if hasattr(self, 'selector'):
            if isinstance(self.selector, selectortools.SegmentSelector):
                return True
        return False

    ### PUBLIC PROPERTIES ###

    @abc.abstractmethod
    def get_duration(self, score_specification):
        pass

    @abc.abstractmethod
    def get_segment_start_offset(self, score_specification):
        pass

    @abc.abstractmethod
    def get_segment_stop_offset(self, score_specification):
        pass

    @abc.abstractmethod
    def set_segment_identifier(self, segment_identifier):
        pass
