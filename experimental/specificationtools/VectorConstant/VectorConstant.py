from abjad.tools.abctools.ImmutableAbjadObject import ImmutableAbjadObject


class VectorConstant(ImmutableAbjadObject):
    r'''.. versionadded:: 1.0

    Dimensioned constant with user-specifiable repr::

        >>> from experimental import specificationtools

    ::

        >>> left = specificationtools.VectorConstant('x', -1, 'left')
        >>> left
        left

    ::

        >>> right = specificationtools.VectorConstant('x', 1, 'right')
        >>> right
        right

    ::

        >>> left < right
        True

    Comparing like-dimensioned vector constants is allowed::

        >>> up = specificationtools.VectorConstant('y', 1, 'up')
        >>> up
        up

    ::

        >>> down = specificationtools.VectorConstant('y', -1, 'down')
        >>> down
        down

    ::

        >>> down < up
        True

    Comparing differently dimensioned vector constants raises an exception::

        >>> import py.test
    
    ::

        >>> bool(py.test.raises(Exception, 'left < up'))
        True

    The ``left``, ``right``, ``up`` and ``down`` constants shown here load into Python's built-in namespace
    on ``specificationtools`` import.

    These four objects can be used as constant values supplied to ``specificationtools`` keyword arguments,
    similarly to true, false and none.
    
    Vector constants are immutable.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = (
        '_dimension',
        '_representation', 
        '_value',
        )
   
    ### INITIALIZER ###

    def __new__(klass, dimension, value, representation):
        assert isinstance(dimension, str), repr(dimension)
        assert isinstance(representation, str), repr(representation)
        self = object.__new__(klass)
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

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _mandatory_argument_values(self):
        return (
            self._dimension,
            self._value,
            self._representation,
            )

    ### PRIVATE METHODS ###

    def _check_comparator(self, expr):
        if not isinstance(expr, type(self)) or \
            not self._dimension == expr._dimension:
            raise Exception('can only compare like-dimensioned vector constants.')
