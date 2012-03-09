from abc import ABCMeta
from abjad.mixins._ImmutableAbjadObject import _ImmutableAbjadObject


class _UnaryComparator(_ImmutableAbjadObject):
    '''Mix-in abstact base class to confer unary comparison behavior to any custom class.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = ABCMeta
    __slots__ = ('_comparison_attribute', '_format_string')

    ### OVERLOADS ###

    def __eq__(self, arg):
        arg = self._massage_comparison_arg(arg)
        return arg and self._comparison_attribute == arg._comparison_attribute

    def __ge__(self, arg):
        arg = self._massage_comparison_arg(arg)
        return arg and self._comparison_attribute >= arg._comparison_attribute

    def __gt__(self, arg):
        arg = self._massage_comparison_arg(arg)
        return arg and self._comparison_attribute > arg._comparison_attribute

    def __le__(self, arg):
        arg = self._massage_comparison_arg(arg)
        return arg and self._comparison_attribute <= arg._comparison_attribute

    def __lt__(self, arg):
        arg = self._massage_comparison_arg(arg)
        return arg and self._comparison_attribute < arg._comparison_attribute

    def __ne__(self, arg):
        return not self == arg

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, self._comparison_attribute)

    ### PRIVATE METHODS ###

    def _massage_comparison_arg(self, arg):
        if not isinstance(arg, type(self)):
            try:
                arg = type(self)(arg)
            except (ValueError, TypeError):
                return False
        return arg
