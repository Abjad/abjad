import abc
from abjad.tools.abctools.AbjadObject import AbjadObject


class ScoreTemplate(AbjadObject):
    r'''.. versionadded:: 2.8

    Abstract score template.
    '''

    ### CLASS ATTRIBUTES ##

    __metaclass__ = abc.ABCMeta

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self):
        pass

    ### SPECIAL METHODS ###

    @abc.abstractmethod
    def __call__(self):
        pass
