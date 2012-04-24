from abc import ABCMeta
from abc import abstractmethod
from abjad.tools.abctools.AbjadObject import AbjadObject


class ScoreSelection(AbjadObject):
    '''.. versionadded:: 2.9

    Abstract base class from which selection classes inherit.
    '''

    ### CLASS ATTRIBUTES ###

    __metclass__ = ABCMeta
    __slots__ = ()

    ### INITIALIZER ###

    @abstractmethod
    def __init__(self):
        pass
