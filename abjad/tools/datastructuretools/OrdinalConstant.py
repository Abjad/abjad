# -*- encoding: utf-8 -*-
import functools
from abjad.tools.abctools.AbjadObject import AbjadObject


@functools.total_ordering
class OrdinalConstant(AbjadObject):
    r'''An ordinal constant.

    Initializes with `dimension`, `value` and `representation`:

    ::

        >>> Left = datastructuretools.OrdinalConstant('x', -1, 'Left')
        >>> Left
        Left

    ::

        >>> Right = datastructuretools.OrdinalConstant('x', 1, 'Right')
        >>> Right
        Right

    ::

        >>> Left < Right
        True

    Comparing like-dimensioned ordinal constants is allowed:

    ::

        >>> Up = datastructuretools.OrdinalConstant('y', 1, 'Up')
        >>> Up
        Up

    ::

        >>> Down = datastructuretools.OrdinalConstant('y', -1, 'Down')
        >>> Down
        Down

    ::

        >>> Down < Up
        True

    Comparing differently dimensioned ordinal constants raises an exception:

    ::

        >>> import pytest

    ::

        >>> bool(pytest.raises(Exception, 'Left < Up'))
        True

    The ``Left``, ``Right``, ``Center``, ``Up`` and ``Down`` constants 
    shown here load into Python's built-in namespace on Abjad import.

    These four objects can be used as constant values supplied to keywords.

    This behavior is similar to True, False and None.

    Ordinal constants are immutable.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_dimension',
        '_representation',
        '_value',
        )

    ### CONSTRUCTOR ###

    def __new__(
        cls, 
        dimension=None, 
        value=0, 
        representation=None,
        ):
        dimension = dimension or ''
        representation = representation or ''
        assert isinstance(dimension, str), repr(dimension)
        assert isinstance(representation, str), repr(representation)
        self = object.__new__(cls)
        self._dimension = dimension
        self._value = value
        self._representation = representation
        return self

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        r'''Is true when `expr` is an ordinal constant with dimension and value
        equal to those of this ordinal constant. Otherwise false.

        Returns boolean.
        '''
        if isinstance(expr, type(self)):
            if self._dimension == expr._dimension:
                return self._value == expr._value
        return False

    def __format__(self, format_specification=''):
        r'''Formats ordinal constant.

        Set `format_specification` to `''` or `'storage'`.
        Interprets `''` equal to `'storage'`.

        Returns string.
        '''
        from abjad.tools import systemtools
        if format_specification in ('', 'storage'):
            return systemtools.StorageFormatManager.get_storage_format(self)
        return str(self)

    def __getnewargs__(self):
        r'''Gets new arguments.

        Returns tuple.
        '''
        return (
            self._dimension,
            self._value,
            self._representation,
            )

    def __lt__(self, expr):
        r'''Is true when `expr` is an ordinal with value greater than that of this
        ordinal constant. Otherwise false.

        Returns boolean.
        '''
        self._check_comparator(expr)
        return self._value < expr._value

    ### PRIVATE PROPERTIES ###

    @property
    def _repr_specification(self):
        return self._storage_format_specification

    @property
    def _storage_format_specification(self):
        from abjad.tools import systemtools
        return systemtools.StorageFormatSpecification(
            self,
            storage_format_pieces=(
                self._representation,
                ),
            )

    ### PRIVATE METHODS ###

    # can only compare like-dimensioned ordinal constants
    def _check_comparator(self, expr):
        if not isinstance(expr, type(self)) or \
            not self._dimension == expr._dimension:
            message = 'can only compare like-dimensioned ordinal constants.'
            raise Exception(message)
