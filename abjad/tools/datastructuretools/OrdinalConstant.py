# -*- coding: utf-8 -*-
import functools
from abjad.tools.abctools.AbjadObject import AbjadObject


@functools.total_ordering
class OrdinalConstant(AbjadObject):
    r'''An ordinal constant.

    ..  container:: example

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

    ..  container:: example

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

    ..  container:: example

        Comparing differently dimensioned ordinal constants raises an exception:

        ::

            >>> import pytest

        ::

            >>> bool(pytest.raises(Exception, 'Left < Up'))
            True

    Abjad adds the following constants to Python's built-in namespace
    when Abjad is first imported:

    * ``Left``
    * ``Right``
    * ``Center``
    * ``Up``
    * ``Down``
    * ``Less``
    * ``More``
    * ``Exact``

    These eight objects can be used as constant values supplied to keywords.

    This behavior is similar to built-in ``True``, ``False`` and ``None``.

    ..  note:: Use ``==`` to compare Abjad ordinal constants.
        Do not use ``is``.

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
        class_,
        dimension=None,
        value=0,
        representation=None,
        ):
        dimension = dimension or ''
        representation = representation or ''
        assert isinstance(dimension, str), repr(dimension)
        assert isinstance(representation, str), repr(representation)
        self = object.__new__(class_)
        self._dimension = dimension
        self._value = value
        self._representation = representation
        return self

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        r'''Is true when `expr` is an ordinal constant with dimension and value
        equal to those of this ordinal constant. Otherwise false.

        Returns true or false.
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
            if self._representation:
                return systemtools.StorageFormatManager.get_storage_format(
                    self)
            else:
                result = 'datastructuretools.{}()'
                result = result.format(type(self).__name__)
                return result
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

    def __hash__(self):
        r'''Hashes ordinal constant.

        Returns int.
        '''
        hash_values = (
            type(self),
            self._dimension,
            self._representation,
            self._value,
            )
        return hash(hash_values)

    def __lt__(self, expr):
        r'''Is true when `expr` is an ordinal with value greater than that of
        this ordinal constant. Otherwise false.

        Returns true or false.
        '''
        self._check_comparator(expr)
        return self._value < expr._value

    def __repr__(self):
        r'''Gets interpreter representation of ordinal constant.

        Returns string.
        '''
        if self._representation:
            return AbjadObject.__repr__(self)
        string = 'datastructuretools.{}()'
        string = string.format(type(self).__name__)
        return string

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