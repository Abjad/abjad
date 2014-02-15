# -*- encoding: utf-8 -*-
import abc
import collections
from abjad.tools.datastructuretools.TypedCollection import TypedCollection
from abjad.tools.topleveltools import new


class TypedOrderedDict(TypedCollection):
    r'''A typed ordered dictionary.

    ..  note:: doctests not included because class is used as an abstract
        base class. Doctests here would put weird examples in child classes.
        See child classes for doctests.

    '''

    ### CLASS VARIABLES ###

    __metaclass__ = abc.ABCMeta

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(self, tokens=None, item_class=None):
        TypedCollection.__init__(
            self,
            item_class=item_class,
            tokens=tokens,
            )
        tokens = tokens or []
        items = []
        for token in tokens:
            assert len(token) == 2, repr(token)
            key = token[0]
            value = self._item_callable(token[1])
            item = (key, value)
            items.append(item)
        self._collection = collections.OrderedDict(items)

    ### SPECIAL METHODS ###

    def __cmp__(self, expr):
        r'''Aliases OrderedDict.__cmp__().

        Returns boolean.
        '''
        assert isinstance(expr, type(self))
        ordered_dictionary = expr._collection
        return self._collection.__cmp__(ordered_dictionary)

    def __contains__(self, key):
        r'''Aliases OrderedDict.__contains__().

        Returns boolean.
        '''
        return key in self._collection

    def __delitem__(self, i):
        r'''Aliases OrderedDict.__delitem__().

        Returns none.
        '''
        self._on_removal(self._collection[i])
        del(self._collection[i])

    def __getitem__(self, i):
        r'''Aliases OrderedDict.__getitem__().

        Returns item.
        '''
        return self._collection[i]

    def __ge__(self, expr):
        r'''Is true when typed ordered dictionary is greater than or equal 
        to `expr`. Otherwise false.

        Returns boolean.
        '''
        expr = type(self)(expr)
        return self._collection.__ge__(expr._collection)

    def __gt__(self, expr):
        r'''Is true when typed ordered dictionary is greater than `expr`. 
        Otherwise false.

        Returns boolean.
        '''
        expr = type(self)(expr)
        return self._collection.__gt__(expr._collection)

    def __hash__(self):
        r'''Hashes typed ordered dictionary.

        Returns integer.
        '''
        return hash((
            type(self), 
            self._collection,
            self.item_class,
            self.name,
            ))

    def __le__(self, expr):
        r'''Is true when typed ordered dictionary is less than or equal 
        to `expr`. Otherwise false.

        Returns boolean.
        '''
        expr = type(self)(expr)
        return self._collection.__le__(expr._collection)

    def __lt__(self, expr):
        r'''Is true when typed ordered dictionary is less than `expr`. 
        Otherwise false.

        Returns boolean.
        '''
        expr = type(self)(expr)
        return self._collection.__lt__(expr._collection)

    def __ne__(self, expr):
        r'''Is true when typed ordered dictionary is not equal to `expr`. 
        Otherwise false.

        Returns boolean.
        '''
        return not self == expr

    def __reversed__(self):
        r'''Aliases OrderedDict.__reversed__().

        Returns generatos.
        '''
        return self._collection.__reversed__()

    def __setitem__(self, i, expr):
        r'''Changes tokens in `expr` to items and sets.

        Returns none.
        '''
        new_item = self._item_callable(expr)
        self._collection[i] = new_item


    ### PUBLIC METHODS ###

    def clear(self):
        r'''Clears typed ordered dictionary.

        Returns none.
        '''
        self._collection.clear()

    def copy(self):
        r'''Copies typed ordered dictionary.

        Returns new typed ordered dictionary.
        '''
        ordered_dictionary = self._collection.copy()
        items = ordered_dictionary.items()
        return type(self)(
            item_class=self.item_class,
            tokens=items,
            )

    def get(self, i, default=None):
        r'''Alias OrderedDict.get().

        Returns item or raises key error.
        '''
        return self._collection.get(i, default)

    def items(self):
        r'''Alias OrderedDict.items().

        Returns list.
        '''
        return self._collection.items()


collections.MutableMapping.register(TypedOrderedDict)
