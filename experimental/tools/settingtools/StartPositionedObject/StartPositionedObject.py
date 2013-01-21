import abc
from abjad.tools import durationtools
from abjad.tools.abctools.AbjadObject import AbjadObject


class StartPositionedObject(AbjadObject):
    '''Start-positioned object.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, start_offset=None):
        start_offset = durationtools.Offset(start_offset)
        self._start_offset = start_offset

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def start_offset(self):
        '''Start-positioned object start offset.
    
        Return offset.
        '''
        return self._start_offset
