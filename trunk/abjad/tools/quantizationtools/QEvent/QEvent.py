import abc
import inspect
from abjad.tools import durationtools
from abjad.tools.abctools import AbjadObject


class QEvent(AbjadObject):
    '''Abstract base class from which concrete ``QEvent`` subclasses inherit.

    Represents an attack point to be quantized.

    All ``QEvents`` possess a rational offset in milliseconds, and an optional
    index for disambiguating events which fall on the same offset in a ``QGrid``.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_index', '_offset')

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, offset, index=None):
        offset = durationtools.Offset(offset)
        self._offset = offset
        self._index = index

    ### SPECIAL METHODS ###

    def __getstate__(self):
        state = {}
        for klass in inspect.getmro(self.__class__):
            if hasattr(klass, '__slots__'):
                for slot in klass.__slots__:
                    if slot not in state:
                        state[slot] = getattr(self, slot)
        return state

    def __lt__(self, other):
        if type(self) == type(self):
            if self.offset < other.offset:
                return True
        return False

    def __repr__(self):
        return '\n'.join(self._get_tools_package_qualified_repr_pieces())

    def __setstate__(self, state):
        for key, value in state.iteritems():
            setattr(self, key, value)

    ### PRIVATE PROPERTIES ###

    @property
    def index(self):
        '''The optional index, for sorting QEvents with identical offsets.'''
        return self._index

    @property
    def offset(self):
        '''The offset in milliseconds of the event.'''
        return self._offset
