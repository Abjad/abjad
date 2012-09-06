import abc
from abjad.tools.abctools.AbjadObject import AbjadObject


class NumberedObject(AbjadObject):
    '''..versionadded: 1.1.2

    Numbered object base class.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta

    __slots__ = ()

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self):
        pass
