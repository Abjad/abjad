from abc import ABCMeta
from abc import abstractmethod
from abjad.tools.abctools.AbjadObject import AbjadObject


class ScoreTemplate(AbjadObject):
    r'''.. versionadded:: 2.8

    Abstract score template.
    '''

    ### CLASS ATTRIBUTES ##

    __metaclass__ = ABCMeta

    ### INITIALIZER ###

    @abstractmethod
    def __init__(self):
        pass

    ### SPECIAL METHODS ###

    @abstractmethod
    def __call__(self):
        pass
