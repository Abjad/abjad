import abc
from abjad.tools.abctools.AbjadObject import AbjadObject
from experimental import helpertools


class Request(AbjadObject):
    r'''.. versionadded:: 1.0

    Abstract base class from which concrete request classes inherit.

    The purpose a request is to function as the source of a setting.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta

    attributes = helpertools.AttributeNameEnumeration()

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, callback=None, count=None, index=None, reverse=None):
        assert isinstance(count, (int, type(None))), repr(count)
        assert isinstance(index, (int, type(None))), repr(index)
        self.callback = callback
        self.count = count
        self.index = index
        self.reverse = reverse
