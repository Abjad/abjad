# -*- coding: utf-8 -*-
import abc
from abjad.tools.abctools.AbjadObject import AbjadObject


class TypedCollection(AbjadObject):
    r'''Abstract base class for typed collections.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_collection',
        '_item_class',
        )

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, items=None, item_class=None):
        assert isinstance(item_class, (type(None), type))
        self._item_class = item_class

    ### SPECIAL METHODS ###

    def __contains__(self, item):
        r'''Is true when typed collection container `item`.
        Otherwise false.

        Returns true or false.
        '''
        try:
            item = self._item_coercer(item)
        except ValueError:
            return False
        return self._collection.__contains__(item)

    def __eq__(self, expr):
        r'''Is true when `expr` is a typed collection with items that compare
        equal to those of this typed collection. Otherwise false.

        Returns true or false.
        '''
        if isinstance(expr, type(self)):
            return self._collection == expr._collection
        elif isinstance(expr, type(self._collection)):
            return self._collection == expr
        return False

    def __format__(self, format_specification=''):
        r'''Formats typed collection.

        Set `format_specification` to `''` or `'storage'`.
        Interprets `''` equal to `'storage'`.

        Returns string.
        '''
        from abjad.tools import systemtools
        if format_specification in ('', 'storage'):
            return systemtools.StorageFormatManager.get_storage_format(self)
        return str(self)

    def __getnewargs__(self):
        r'''Gets new arguments.

        Returns tuple.
        '''
        return (self._collection, self.item_class)

    def __hash__(self):
        r'''Hashes typed collection.

        Required to be explicitly redefined on Python 3 if __eq__ changes.

        Returns integer.
        '''
        return super(TypedCollection, self).__hash__()

    def __iter__(self):
        r'''Iterates typed collection.

        Returns generator.
        '''
        return self._collection.__iter__()

    def __len__(self):
        r'''Length of typed collection.

        Returns nonnegative integer.
        '''
        return len(self._collection)

    def __ne__(self, expr):
        r'''Is true when `expr` is not a typed collection with items equal to
        this typed collection. Otherwise false.

        Returns true or false.
        '''
        return not self.__eq__(expr)

    ### PRIVATE METHODS ###

    def _on_insertion(self, item):
        r'''Override to operate on item after insertion into collection.
        '''
        pass

    def _on_removal(self, item):
        r'''Override to operate on item after removal from collection.
        '''
        pass

    ### PRIVATE PROPERTIES ###

    @property
    def _item_coercer(self):
        def coerce_(x):
            if isinstance(x, self._item_class):
                return x
            return self._item_class(x)
        if self._item_class is None:
            return lambda x: x
        return coerce_

    @property
    def _repr_specification(self):
        from abjad.tools import systemtools
        manager = systemtools.StorageFormatManager
        names = manager.get_signature_keyword_argument_names(self)
        keyword_argument_names = list(names)
        if 'items' in keyword_argument_names:
            keyword_argument_names.remove('items')
        keyword_argument_names = tuple(keyword_argument_names)
        positional_argument_values = (
            self._collection,
            )
        return systemtools.StorageFormatSpecification(
            self,
            is_indented=False,
            keyword_argument_names=keyword_argument_names,
            positional_argument_values=positional_argument_values,
            )

    @property
    def _storage_format_specification(self):
        from abjad.tools import systemtools
        manager = systemtools.StorageFormatManager
        names = manager.get_signature_keyword_argument_names(self)
        keyword_argument_names = list(names)
        if 'items' in keyword_argument_names:
            keyword_argument_names.remove('items')
        keyword_argument_names = tuple(keyword_argument_names)
        positional_argument_values = (
            self._collection,
            )
        return systemtools.StorageFormatSpecification(
            self,
            keyword_argument_names=keyword_argument_names,
            positional_argument_values=positional_argument_values,
            )

    ### PUBLIC PROPERTIES ###

    @property
    def item_class(self):
        r'''Item class to coerce items into.
        '''
        return self._item_class

    @property
    def items(self):
        r'''Gets collection items.
        '''
        return [x for x in self]
