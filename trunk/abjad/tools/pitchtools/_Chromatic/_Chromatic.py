from abc import ABCMeta
from abc import abstractmethod
from abjad.tools.abctools.AbjadObject import AbjadObject


class _Chromatic(AbjadObject):
    '''..versionadded:: 2.0

    Chromatic object base class.
    '''

    __metaclass__ = ABCMeta
    __slots__ = ()
