# -*- encoding: utf-8 -*-
import abc
from abjad.tools.abctools.AttributeEqualityAbjadObject \
	import AttributeEqualityAbjadObject


class SortableAttributeEqualityAbjadObject(AttributeEqualityAbjadObject):
    '''note:: deprecated.

    Abstact base class to confer sortable attribute-equality 
    to any custom class.

    Sortable attribute-equality comparators implement ``__eq__``, ``__ne__``,
    ``__gt__``, ``__ge__``, ``__lt__``, ``__le__`` against a single comparison
    attribute.
    '''

    ### CLASS VARIABLES ###

    __metaclass__ = abc.ABCMeta

    __slots__ = (
        '_comparison_attribute',
        )

    ### SPECIAL METHODS ###

    def __ge__(self, arg):
        r'''Initialize new object from `arg` and evaluate 
        comparison attributes.

        Return boolean.
        '''
        arg = self._massage_comparison_arg(arg)
        return arg and self._comparison_attribute >= arg._comparison_attribute

    def __gt__(self, arg):
        r'''Initialize new object from `arg` and evaluate 
        comparison attributes.

        Return boolean.
        '''
        arg = self._massage_comparison_arg(arg)
        return arg and self._comparison_attribute > arg._comparison_attribute

    def __le__(self, arg):
        r'''Initialize new object from `arg` and evaluate 
        comparison attributes.

        Return boolean.
        '''
        arg = self._massage_comparison_arg(arg)
        return arg and self._comparison_attribute <= arg._comparison_attribute

    def __lt__(self, arg):
        r'''Initialize new object from `arg` and evaluate 
        comparison attributes.

        Return boolean.
        '''
        arg = self._massage_comparison_arg(arg)
        return arg and self._comparison_attribute < arg._comparison_attribute
