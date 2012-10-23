from fractions import Fraction
from abjad.tools.abctools import ImmutableAbjadObject
from abjad.tools import mathtools


class Duration(ImmutableAbjadObject, Fraction):
    '''.. versionadded:: 2.0

    Abjad model of musical duration.

    Initialize from integer numerator::

        >>> Duration(3)
        Duration(3, 1)

    Initialize from integer numerator and denominator::

        >>> Duration(3, 16)
        Duration(3, 16)

    Initialize from integer-equivalent numeric numerator::

        >>> Duration(3.0)
        Duration(3, 1)

    Initialize from integer-equivalent numeric numerator and denominator::

        >>> Duration(3.0, 16)
        Duration(3, 16)

    Initialize from integer-equivalent singleton::

        >>> Duration((3,))
        Duration(3, 1)

    Initialize from integer-equivalent pair::

        >>> Duration((3, 16))
        Duration(3, 16)

    Initialize from other duration::

        >>> Duration(Duration(3, 16))
        Duration(3, 16)

    Intialize from fraction::

        >>> Duration(Fraction(3, 16))
        Duration(3, 16)

    Initialize from solidus string::
        
        >>> Duration('3/16')
        Duration(3, 16)

    .. versionchanged:: 2.9 
        initialize from LilyPond duration string:

    ::

        >>> Duration('8.')
        Duration(3, 16)

    .. versionchanged:: 2.9
        initialize from nonreduced fraction:

    ::

        >>> from abjad.tools import mathtools

    ::

        >>> Duration(mathtools.NonreducedFraction(3, 16))
        Duration(3, 16)
        
    Durations inherit from built-in fraction::

        >>> isinstance(Duration(3, 16), Fraction)
        True

    Durations are numeric::

        >>> import numbers

    ::

        >>> isinstance(Duration(3, 16), numbers.Number)
        True

    Durations are immutable.
    '''

    def __new__(klass, *args):
        from abjad.tools import durationtools
        from abjad.tools import sequencetools
        if len(args) == 1 and sequencetools.is_integer_equivalent_singleton(args[0]):
            self = Fraction.__new__(klass, int(args[0][0]))
        elif len(args) == 1 and sequencetools.is_fraction_equivalent_pair(args[0]):
            self = Fraction.__new__(klass, int(args[0][0]), int(args[0][1]))
        elif len(args) == 1 and durationtools.is_lilypond_duration_string(args[0]):
            self = Fraction.__new__(klass, durationtools.lilypond_duration_string_to_rational(args[0]))
        elif len(args) == 1 and hasattr(args[0], 'numerator') and hasattr(args[0], 'denominator'):
            self = Fraction.__new__(klass, args[0].numerator, args[0].denominator)
        elif sequencetools.all_are_integer_equivalent_numbers(args):
            self = Fraction.__new__(klass, *[int(x) for x in args])
        else:
            self = Fraction.__new__(klass, *args)
        return self

    ### SPECIAL METHODS ###

    def __abs__(self, *args):
        return type(self)(Fraction.__abs__(self, *args))

    def __add__(self, *args):
        from abjad.tools import mathtools
        if len(args) == 1 and isinstance(args[0], mathtools.NonreducedFraction):
            return args[0].__radd__(self)
        else:
            return type(self)(Fraction.__add__(self, *args))

    def __div__(self, *args):
        from abjad.tools import durationtools
        from abjad.tools import mathtools
        if len(args) == 1 and isinstance(args[0], type(self)):
            return durationtools.Multiplier(Fraction.__div__(self, *args))
        elif len(args) == 1 and isinstance(args[0], mathtools.NonreducedFraction):
            return args[0].__rdiv__(self)
        else:
            return type(self)(Fraction.__div__(self, *args))

    def __divmod__(self, *args):
        return type(self)(Fraction.__divmod__(self, *args))

    def __eq__(self, arg):
        return Fraction.__eq__(self, arg)

    def __ge__(self, arg):
        return Fraction.__ge__(self, arg)

    def __gt__(self, arg):
        return Fraction.__gt__(self, arg)        

    def __le__(self, arg):
        return Fraction.__le__(self, arg)

    def __lt__(self, arg):
        return Fraction.__lt__(self, arg)

    def __mod__(self, *args):
        return type(self)(Fraction.__mod__(self, *args))

    def __mul__(self, *args):
        from abjad.tools import mathtools
        if len(args) == 1 and isinstance(args[0], mathtools.NonreducedFraction):
            return args[0].__rmul__(self)
        else:
            return type(self)(Fraction.__mul__(self, *args))

    def __neg__(self, *args):
        return type(self)(Fraction.__neg__(self, *args))

    def __ne__(self, arg):
        return Fraction.__ne__(self, arg)

    def __pos__(self, *args):
        return type(self)(Fraction.__pos__(self, *args))

    def __pow__(self, *args):
        return type(self)(Fraction.__pow__(self, *args))

    def __radd__(self, *args):
        return type(self)(Fraction.__radd__(self, *args))

    def __rdiv__(self, *args):
        return type(self)(Fraction.__rdiv__(self, *args))

    def __rdivmod__(self, *args):
        return type(self)(Fraction.__rdivmod__(self, *args))

    def __repr__(self):
        return '%s(%s, %s)' % (type(self).__name__, self.numerator, self.denominator)

    def __rmod__(self, *args):
        return type(self)(Fraction.__rmod__(self, *args))

    def __rmul__(self, *args):
        return type(self)(Fraction.__rmul__(self, *args))

    def __rpow__(self, *args):
        return type(self)(Fraction.__rpow__(self, *args))

    def __rsub__(self, *args):
        return type(self)(Fraction.__rsub__(self, *args))

    def __rtruediv__(self, *args):
        return type(self)(Fraction.__rtruediv__(self, *args))

    def __sub__(self, *args):
        from abjad.tools import mathtools
        if len(args) == 1 and isinstance(args[0], mathtools.NonreducedFraction):
            return args[0].__rsub__(self)
        else:
            return type(self)(Fraction.__sub__(self, *args))

    def __truediv__(self, *args):
        return type(self)(Fraction.__truediv__(self, *args))

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _keyword_argument_names(self):
        return ()

    @property
    def _mandatory_argument_values(self):
        result = []
        result.append(self.numerator)
        result.append(self.denominator)
        return tuple(result)

    ### PRIVATE METHODS ###

    # do not indent in storage
    def _get_tools_package_qualified_repr_pieces(self, is_indented=True):
        return [''.join(
            ImmutableAbjadObject._get_tools_package_qualified_repr_pieces(self, is_indented=False))]

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def dot_count(self):
        '''.. versionadded:: 2.11

        Positive integer number of dots required to notate duration.

        Raise assignability error when duration is not assignable::

            >>> for n in range(1, 9):
            ...     try:
            ...         duration = Duration(n, 16)
            ...         print '{}\t{}'.format(duration, duration.dot_count)
            ...     except AssignabilityError:
            ...         pass
            ... 
            1/16    0
            1/8     0
            3/16    1
            1/4     0
            3/8     1
            7/16    2
            1/2     0

        Return positive integer.
        '''
        if not self.is_assignable:
            raise AssignabilityError

        binary_string = mathtools.integer_to_binary_string(self.numerator)
        digit_sum = sum([int(x) for x in list(binary_string)])
        dot_count = digit_sum - 1
        return dot_count

    @property
    def is_assignable(self):
        '''.. versionadded:: 2.11

        True when assignable. Otherwise false::

            >>> for numerator in range(0, 17):
            ...     duration = Duration(numerator, 16)
            ...     print '{}\t{}'.format(duration, duration.is_assignable)
            ... 
            0       False
            1/16    True
            1/8     True
            3/16    True
            1/4     True
            5/16    False
            3/8     True
            7/16    True
            1/2     True
            9/16    False
            5/8     False
            11/16   False
            3/4     True
            13/16   False
            7/8     True
            15/16   True
            1       True

        Return boolean.
        '''
        if 0 < self < 16:
            if mathtools.is_nonnegative_integer_power_of_two(self.denominator):
                if mathtools.is_assignable_integer(self.numerator):
                    return True
        return False

    @property
    def lilypond_duration_string(self):
        '''.. versionadded:: 2.11

        LilyPond duration string of assignable duration.

        Raise assignability error when duration is not assignable::

            >>> Duration(3, 16).lilypond_duration_string
            '8.'

        Return string.
        '''
        from abjad.tools import durationtools

        if not self.is_assignable:
            raise AssignabilityError

        undotted_rational = durationtools.rational_to_equal_or_lesser_binary_rational(self)
        if undotted_rational <= 1:
            undotted_duration_string = str(undotted_rational.denominator)
        elif undotted_rational == type(self)(2, 1):
            undotted_duration_string = r'\breve'
        elif undotted_rational == type(self)(4, 1):
            undotted_duration_string = r'\longa'
        elif undotted_rational == type(self)(8, 1):
            undotted_duration_string = r'\maxima'
        else:
            raise ValueError('can not process undotted rational: %s' % undotted_rational)

        dot_count = self.dot_count
        dot_string = '.' * dot_count
        dotted_duration_string = undotted_duration_string + dot_string
        return dotted_duration_string

    @property
    def pair(self):
        '''.. versionadded:: 2.9

        Read-only pair of duration numerator and denominator::

            >>> duration = Duration(3, 16)

        ::

            >>> duration.pair
            (3, 16)

        Return integer pair.
        '''
        return self.numerator, self.denominator

    ### PUBLIC FUNCTIONS ###

    @staticmethod
    def is_token(expr):
        '''.. versionadded:: 2.11

        True if `expr` correctly initializes a duration.
        Otherwise false.

            >>> Duration.is_token('8.')
            True

        Return boolean.
        '''
        try:
            Duration.__new__(Duration, expr)
            return True
        except:
            return False
