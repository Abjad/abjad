from abc import ABCMeta, abstractmethod
from abjad.tools import abctools


class QEvent(tuple, abctools.ImmutableAbjadObject):
    '''A utility class for quantization comprising an offset time in milliseconds,
    and some pitch information: a Number representing a single pitch, None representing silence,
    or an Iterable comprised of Numbers representing a chord.

    `QEvents` are immutable.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = ABCMeta
    __slots__ = ()

    ### INITIALIZER ###

    @abstractmethod
    def __new__(cls, *args, **kwargs):
        raise Exception("Not implemented.")

    ### SPECIAL METHODS ###

    def __getnewargs__(self):
        'Return self as a plain tuple.  Used by copy and pickle.'
        return tuple(self)

    def __repr__(self):
        return '\n'.join(self._get_tools_package_qualified_repr_pieces())

    def __lt__(self, other):
        if type(self) == type(self):
            if self.offset < other.offset:
                return True
        return False

    ### SPECIAL PROPERTIES ###

    @property
    def __dict__(self):
        return OrderedDict(zip(self._fields, self))

    ### PRIVATE PROPERTIES ###

    @property
    def offset(self):
        '''The offset in milliseconds of the event.'''
        return self[0]

