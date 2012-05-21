from abc import ABCMeta
from abc import abstractmethod
from abjad.tools.abctools.AbjadObject import AbjadObject


class MelodicObject(AbjadObject):
    '''..versionadded:: 2.0

    Melodic object base class.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = ABCMeta

    __slots__ = ()

    ### INITIALIZER ###
    
    @abstractmethod
    def __init__(self):
        pass
