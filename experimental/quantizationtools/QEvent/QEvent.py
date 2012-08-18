from abc import ABCMeta, abstractmethod
from abjad.tools import abctools
from abjad.tools import durationtools


class QEvent(abctools.AbjadObject):
    '''Abstract base class from which concrete QEvent subclasses inherit.

    Represents an attack point to be quantized.

    All QEvents have a rational offset, in milliseconds, and an optional index, for
    disambiguating events which fall on the same offset.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_index', '_offset')


    ### INITIALIZER ###

    @abstractmethod
    def __init__(self, offset, index=None):
        offset = durationtools.Offset(offset)
        self._offset = offset
        self._index = index

    ### SPECIAL METHODS ###

    def __repr__(self):
        return '\n'.join(self._get_tools_package_qualified_repr_pieces())

    def __lt__(self, other):
        if type(self) == type(self):
            if self.offset < other.offset:
                return True
        return False

    ### PRIVATE PROPERTIES ###

    @property
    def index(self):
        '''The optional index, for sorting QEvents with identical offsets.'''
        return self._index

    @property
    def offset(self):
        '''The offset in milliseconds of the event.'''
        return self._offset
