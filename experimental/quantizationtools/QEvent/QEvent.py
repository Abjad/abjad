from abc import ABCMeta, abstractmethod
from abjad.tools import abctools
from abjad.tools import durationtools


class QEvent(abctools.AbjadObject):
    '''A utility class for quantization comprising an offset time in milliseconds,
    and some pitch information: a Number representing a single pitch, None representing silence,
    or an Iterable comprised of Numbers representing a chord.

    `QEvents` are immutable.
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
