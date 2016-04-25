# -*- coding: utf-8 -*-
import collections
from abjad.tools.datastructuretools.TypedCollection import TypedCollection
from abjad.tools.topleveltools import new


class TypedTuple(TypedCollection):
    r'''A typed tuple.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(self, items=None, item_class=None):
        TypedCollection.__init__(
            self,
            item_class=item_class,
            items=items,
            )
        items = items or []
        self._collection = tuple(
            self._item_coercer(item) for item in items)

    ### SPECIAL METHODS ###

    def __add__(self, expr):
        r'''Adds typed tuple to `expr`.

        Returns new typed tuple.
        '''
        if isinstance(expr, type(self)):
            items = expr._collection
            return new(self, items=self._collection[:] + items)
        elif isinstance(expr, type(self._collection)):
            items = expr[:]
            return new(self, items=self._collection[:] + items)
        raise NotImplementedError

    def __contains__(self, item):
        r'''Change `item` to item and return true if item exists in
        collection.

        Returns none.
        '''
        try:
            item = self._item_coercer(item)
        except ValueError:
            return False
        return self._collection.__contains__(item)

    def __getitem__(self, i):
        '''Gets `i` from type tuple.

        Returns item.
        '''
        if type(i) == slice:
            return self.__getslice__(i.start, i.stop)
        return self._collection[i]

    def __getslice__(self, start, stop):
        r'''Gets slice from `start` to `stop` in typed tuple.

        Returns new typed tuple.
        '''
        return new(self, items=self._collection[start:stop])

    def __hash__(self):
        r'''Hashes typed tuple.

        Returns integer.
        '''
        return hash((
            type(self),
            self._collection,
            self.item_class,
            ))

    def __mul__(self, expr):
        r'''Multiplies typed tuple by `expr`.

        Returns new typed tuple.
        '''
        items = self._collection * expr
        return new(self, items=items)

    def __radd__(self, expr):
        r'''Right-adds `expr` to typed tuple.
        '''
        items = expr + self._collection
        return new(self, items=items)

    def __rmul__(self, expr):
        r'''Multiplies `expr` by typed tuple.

        Returns new typed tuple.
        '''
        return self.__mul__(expr)

    ### PUBLIC METHODS ###

    def count(self, item):
        r'''Changes `item` to item.

        Returns count in collection.
        '''
        item = self._item_coercer(item)
        return self._collection.count(item)

    def index(self, item):
        r'''Changes `item` to item.

        Returns index in collection.
        '''
        item = self._item_coercer(item)
        return self._collection.index(item)


collections.Sequence.register(TypedTuple)
