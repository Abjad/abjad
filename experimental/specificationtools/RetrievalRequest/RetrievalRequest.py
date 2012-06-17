from abc import ABCMeta
from abc import abstractmethod
from abjad.tools.abctools.AbjadObject import AbjadObject


class RetrievalRequest(AbjadObject):
    r'''.. versionadded:: 1.0

    Abstract base class for retrieval request classes.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = ABCMeta

    ### INITIALIZER ###

    @abstractmethod
    def __init__(self):
        pass
