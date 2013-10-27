# -*- encoding: utf-8 -*-
from abjad.tools.abctools.AbjadObject import AbjadObject


class OrdinalConstant(AbjadObject):
    r'''Ordinal constant.

    Initialize with `dimension`, `value` and `representation`:

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

        >>> import py.test

    ::

        >>> bool(py.test.raises(Exception, 'Left < Up'))
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

    def __new__(cls, dimension, value, representation):
        assert isinstance(dimension, str), repr(dimension)
        assert isinstance(representation, str), repr(representation)
        self = object.__new__(cls)
        self._dimension = dimension
        self._value = value
        self._representation = representation
        return self

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        if isinstance(expr, type(self)):
            if self._dimension == expr._dimension:
                return self._value == expr._value
        return False

    def __ge__(self, expr):
        self._check_comparator(expr)
        return self._value >= expr._value

    def __getnewargs__(self):
        return self._positional_argument_values

    def __gt__(self, expr):
        self._check_comparator(expr)
        return self._value > expr._value

    def __le__(self, expr):
        self._check_comparator(expr)
        return self._value <= expr._value

    def __lt__(self, expr):
        self._check_comparator(expr)
        return self._value < expr._value

    def __repr__(self):
        return self._representation

    ### PRIVATE PROPERTIES ###

    @property
    def _positional_argument_values(self):
        return (
            self._dimension,
            self._value,
            self._representation,
            )

    ### PRIVATE METHODS ###

    # can only compare like-dimensioned ordinal constants
    def _check_comparator(self, expr):
        if not isinstance(expr, type(self)) or \
            not self._dimension == expr._dimension:
            message = 'can only compare like-dimensioned ordinal constants.'
            raise Exception(message)

    # ordinal constants appear as constants in storage format
    def _get_tools_package_qualified_repr_pieces(self, is_indented=True):
        return [repr(self)]

    ### PUBLIC PROPERTIES ###

    @property
    def storage_format(self):
        r'''Storage format of ordinal constant.

        Returns string.
        '''
        return self._tools_package_qualified_indented_repr
