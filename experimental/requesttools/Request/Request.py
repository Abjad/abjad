from abc import ABCMeta
from abc import abstractmethod
from abjad.tools.abctools.AbjadObject import AbjadObject
from experimental import helpertools


class Request(AbjadObject):
    r'''.. versionadded:: 1.0

    Abstract base class from which concrete request classes inherit.

    The purpose a request is to function as the source of a setting.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = ABCMeta

    attributes = helpertools.AttributeNameEnumeration()

    ### INITIALIZER ###

    @abstractmethod
    def __init__(self, callback=None, count=None, offset=None, reverse=None):
        assert isinstance(count, (int, type(None))), repr(count)
        assert isinstance(offset, (int, type(None))), repr(offset)
        self.callback = callback
        self.count = count
        self.offset = offset
        self.reverse = reverse
