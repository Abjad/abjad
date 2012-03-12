from abc import ABCMeta
from abjad.tools.abctools.AbjadObject import AbjadObject


class _Numbered(AbjadObject):
    '''..versionadded: 1.1.2

    Numbered object base class.
    '''

    __metaclass__ = ABCMeta
    __slots__ = ()
