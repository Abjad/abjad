# -*- encoding: utf-8 -*-
import abc
import inspect
from abjad.tools import durationtools
from abjad.tools.abctools import AbjadObject


class QEvent(AbjadObject):
    r'''Abstract base class from which concrete ``QEvent`` subclasses 
    inherit.

    Represents an attack point to be quantized.

    All ``QEvents`` possess a rational offset in milliseconds, 
    and an optional index for disambiguating events which fall 
    on the same offset in a ``QGrid``.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_index', 
        '_offset',
        )

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, offset, index=None):
        offset = durationtools.Offset(offset)
        self._offset = offset
        self._index = index

    ### SPECIAL METHODS ###

    def __getstate__(self):
        state = {}
        for current_class in inspect.getmro(self.__class__):
            if hasattr(current_class, '__slots__'):
                for slot in current_class.__slots__:
                    if slot not in state:
                        state[slot] = getattr(self, slot)
        return state

    def __lt__(self, expr):
        if type(self) == type(self):
            if self.offset < expr.offset:
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
        r'''The optional index, for sorting QEvents with identical offsets.
        '''
        return self._index

    @property
    def offset(self):
        r'''The offset in milliseconds of the event.
        '''
        return self._offset

    @property
    def storage_format(self):
        r'''Storage format of q-event.

        Returns string.
        '''
        return self._tools_package_qualified_indented_repr
