from collections import Iterable
from numbers import Number
from abjad.tools.abctools import AbjadObject


class QEvent(AbjadObject):
    '''A utility class for quantization comprising an offset time in milliseconds,
    and some pitch information: a Number representing a single pitch, None representing silence,
    or an Iterable comprised of Numbers representing a chord.

    `QEvents` are immutable.
    '''

    __slots__ = ('_offset', '_value')

    def __init__(self, *args):

        if len(args) == 2:
            offset = args[0]
            value = args[1]
            assert isinstance(offset, Number)
            assert isinstance(value, (Number, Iterable, type(None)))
            if isinstance(value, Iterable):
                assert all([isinstance(x, Number) for x in value])
                value = tuple(sorted(set(value)))

        elif len(args) == 1 and isinstance(args[0], type(self)):
            offset = args[0].offset
            value = args[0].value

        object.__setattr__(self, '_value', value)
        object.__setattr__(self, '_offset', offset)

    ### OVERRIDES ###

    def __eq__(self, other):
        if type(self) == type(other):
            if self.offset == other.offset:
                if self.value == other.value:
                    return True
        return False

    def __getnewargs__(self):
        return self.offset, self.value

    def __repr__(self):
        return '%s(%s)' % (type(self).__name__, self._format_string)

    ### PRIVATE PROPERTIES ###

    @property
    def _format_string(self):
        return ', '.join([repr(x) for x in
            [self.offset, self.value]])

    ### PUBLIC PROPERTIES ###

    @property
    def offset(self):
        '''The offset in milliseconds of the event.'''
        return self._offset

    @property
    def value(self):
        '''The pitch information of the event.'''
        return self._value
