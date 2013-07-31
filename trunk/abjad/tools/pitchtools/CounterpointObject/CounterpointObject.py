import abc
from abjad.tools.abctools.AbjadObject import AbjadObject


class CounterpointObject(AbjadObject):
    r'''Counterpoint object base class.
    '''

    ### CLASS VARIABLES ###

    __metaclass__ = abc.ABCMeta

    __slots__ = ()

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self):
        pass
