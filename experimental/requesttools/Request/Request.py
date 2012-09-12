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
    def __init__(self, index=None, count=None, reverse=None, rotation=None, callback=None):
        assert isinstance(index, (int, type(None))), repr(index)
        assert isinstance(count, (int, type(None))), repr(count)
        assert isinstance(reverse, (bool, type(None))), repr(reverse)
        assert isinstance(rotation, (int, type(None))), repr(rotation)
        self._index = index
        self._count = count
        self._callback = callback
        self._reverse = reverse
        self._rotation = rotation

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def callback(self):
        return self._callback

    @property
    def count(self):
        return self._count

    @property
    def index(self):
        return self._index

    @property
    def reverse(self):
        return self._reverse

    @property
    def rotation(self):
        return self._rotation
