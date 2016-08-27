# -*- coding: utf-8 -*-
import functools
from abjad.tools import systemtools
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


@functools.total_ordering
class OrdinalConstant(AbjadValueObject):
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

    def __lt__(self, expr):
        r'''Is true when `expr` is an ordinal with value greater than that of
        this ordinal constant. Otherwise false.

        Returns true or false.
        '''
        self._check_comparator(expr)
        return self._value < expr._value

    ### PRIVATE METHODS ###

    # can only compare like-dimensioned ordinal constants
    def _check_comparator(self, expr):
        if not isinstance(expr, type(self)) or \
            self._dimension != expr._dimension:
            message = 'can only compare like-dimensioned ordinal constants.'
            raise Exception(message)

    def _get_format_specification(self):
        storage_format_text = repr_text = self._representation or None
        return systemtools.FormatSpecification(
            client=self,
            repr_text=repr_text,
            storage_format_text=storage_format_text,
            )
