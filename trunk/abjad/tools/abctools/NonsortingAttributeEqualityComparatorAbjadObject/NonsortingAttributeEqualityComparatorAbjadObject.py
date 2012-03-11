from abc import ABCMeta
from abjad.tools.abctools.NonsortingIdEqualityComparatorAbjadObject import NonsortingIdEqualityComparatorAbjadObject


# TODO: inherit from AbjadObject directly
class NonsortingAttributeEqualityComparatorAbjadObject(NonsortingIdEqualityComparatorAbjadObject):
    '''.. versionadded:: 2.0

    Abstract base class to confer nonsorting attribute-equality comparability to any custom class.

    Nonsorting objects raise exceptions on gt, ge, lt, le.

    Attribute-equality comparators compare equal only with equal comparison attributes.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = ABCMeta
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
