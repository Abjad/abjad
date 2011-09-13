from abjad.core._StrictComparator import _StrictComparator


class _FlexEqualityComparator(_StrictComparator):
    '''Mix-in base class to confer a certain type of comparator behavior to any custom class.
    Flex equality comparators raise not implemented error on gt, lt, ge, le.
    Flex equality comparators attempt type coercion on eq, ne.
    '''

    __slots__ = ('_comparison_attribute', '_format_string')

    ### OVERLOADS ###

    def __eq__(self, arg):
        arg = self._massage_comparison_arg(arg)
        return arg and self._comparison_attribute == arg._comparison_attribute

    def __ne__(self, arg):
        return not self == arg

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, self._format_string)

    ### PRIVATE METHODS ###

    def _massage_comparison_arg(self, arg):
        if not isinstance(arg, type(self)):
            try:
                arg = type(self)(arg)
            except (ValueError, TypeError):
                return False
        return arg
