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

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _one_line_format(self):
        if self.selector is None:
            return '[{} {}]'.format(self.start._one_line_format, self.stop._one_line_format)
        else:
            # note that this is not yet implemented
            return '[{}]'.format(self.selector._one_line_format)

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
