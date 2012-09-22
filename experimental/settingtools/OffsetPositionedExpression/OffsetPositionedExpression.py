import abc
from abjad.tools import durationtools
from abjad.tools.abctools.AbjadObject import AbjadObject


class OffsetPositionedExpression(AbjadObject):
    r'''.. versionadded:: 1.0

    Offset-positioned expression.

    Base class from which concrete expressions inherit.

    Composers do not create offset-positioned expression objects
    because offset-positioned expressions arise as a byproduct
    of interpretation.
    ''' 

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, start_offset=None, stop_offset=None):
        if start_offset is None:
            start_offset = durationtools.Offset(0)
        else:
            start_offset = durationtools.Offset(start_offset)
        self._start_offset = start_offset

    ### READ-ONLY PUBLIC PROPERTIES ###

    @abc.abstractproperty
    def duration(self):
        pass

    @property
    def start_offset(self):
        '''Rhythm expression start offset.

        Assigned at initialization during rhythm interpretation.

        Return offset.
        '''
        return self._start_offset

    @property
    def stop_offset(self):
        '''Rhythm expression stop offset.
        
        Defined equal to start offset plus 
        prolated duration of rhythm expression

        Return offset.
        '''
        return self.start_offset + self.duration
