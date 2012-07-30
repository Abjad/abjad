from abc import ABCMeta
from abc import abstractmethod
from abjad.tools import componenttools
from abjad.tools import mathtools
from abjad.tools.abctools.AbjadObject import AbjadObject
from experimental.timespantools.Timepoint import Timepoint


class Timespan(AbjadObject):
    r'''.. versionadded:: 1.0

    Base timespan from which concrete timespans inherit.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = ABCMeta

    ### INITIALIZER ###

    @abstractmethod
    def __init__(self):
        pass

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def duration(self):
        '''Rational-valued duration of timespan.
        
        Derived from input values.

        Return rational.
        
        .. note:: not yet implemented.
        '''
        raise NotImplementedError

    @property
    def is_segment_slice(self):
        if hasattr(self, 'selector'):
            if isinstance(self.selector, selectortools.SegmentSliceSelector):
                return True
        return False
