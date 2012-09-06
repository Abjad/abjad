import abc
from abjad.tools.abctools.AbjadObject import AbjadObject


class HarmonicObject(AbjadObject):
    '''..versionadded:: 2.0

    Harmonic object base class.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta

    __slots__ = ()

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self):
        pass
