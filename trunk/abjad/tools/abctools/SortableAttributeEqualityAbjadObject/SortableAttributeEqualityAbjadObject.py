from abc import ABCMeta
from abjad.tools.abctools.AbjadObject import AbjadObject


# TODO: inherit from AttributeEqualityAbjadObject
class SortableAttributeEqualityAbjadObject(AbjadObject):
    '''.. versionadded:: 2.0

    Abstact base class to confer sortable attribute-equality to any custom class.

    Sortable attribute-equality comparators implement ``__eq__``, ``__ne__``, 
    ``__gt__``, ``__ge__``, ``__lt__``, ``__le__`` against a single comparison attribute.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = ABCMeta
    __slots__ = ('_comparison_attribute', '_format_string')

    ### OVERLOADS ###

    def __eq__(self, arg):
        '''Initialize new object from `arg` and evaluate comparison attributes.

        Return boolean.
        '''
        arg = self._massage_comparison_arg(arg)
        return arg and self._comparison_attribute == arg._comparison_attribute

    def __ge__(self, arg):
        '''Initialize new object from `arg` and evaluate comparison attributes.

        Return boolean.
        '''
        arg = self._massage_comparison_arg(arg)
        return arg and self._comparison_attribute >= arg._comparison_attribute

    def __gt__(self, arg):
        '''Initialize new object from `arg` and evaluate comparison attributes.

        Return boolean.
        '''
        arg = self._massage_comparison_arg(arg)
        return arg and self._comparison_attribute > arg._comparison_attribute

    def __le__(self, arg):
        '''Initialize new object from `arg` and evaluate comparison attributes.

        Return boolean.
        '''
        arg = self._massage_comparison_arg(arg)
        return arg and self._comparison_attribute <= arg._comparison_attribute

    def __lt__(self, arg):
        '''Initialize new object from `arg` and evaluate comparison attributes.

        Return boolean.
        '''
        arg = self._massage_comparison_arg(arg)
        return arg and self._comparison_attribute < arg._comparison_attribute

    def __ne__(self, arg):
        '''Initialize new object from `arg` and evaluate comparison attributes.

        Return boolean.
        '''
        return not self == arg

    def __repr__(self):
        '''Interpreter representation of object defined equal to class name and comparison attribute.

        Return string.
        '''
        return '%s(%s)' % (self.__class__.__name__, self._comparison_attribute)

    ### PRIVATE METHODS ###

    def _massage_comparison_arg(self, arg):
        if not isinstance(arg, type(self)):
            try:
                arg = type(self)(arg)
            except (ValueError, TypeError):
                return False
        return arg
