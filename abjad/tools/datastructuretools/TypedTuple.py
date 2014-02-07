# -*- encoding: utf-8 -*-
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

    def __init__(self, tokens=None, item_class=None, custom_identifier=None):
        TypedCollection.__init__(self, 
            item_class=item_class, 
            custom_identifier=custom_identifier,
            tokens=tokens,
            )
        tokens = tokens or []
        self._collection = tuple(self._item_callable(token) 
            for token in tokens)

    ### SPECIAL METHODS ###

    def __add__(self, expr):
        r'''Adds typed tuple to `expr`.

        Returns new typed tuple.
        '''
        if isinstance(expr, type(self)):
            tokens = expr._collection
            return new(self, tokens=self._collection[:] + tokens)

        elif isinstance(expr, type(self._collection)):
            tokens = expr[:]
            return new(self, tokens=self._collection[:] + tokens)
        raise NotImplementedError

    def __contains__(self, token):
        r'''Change `token` to item and return true if item exists in
        collection.

        Returns none.
        '''
        try:
            item = self._item_callable(token)
        except ValueError:
            return False
        return self._collection.__contains__(item)

    def __getitem__(self, i):
        '''Gets `i` from type tuple.

        Returns item.
        '''
        return self._collection[i]

    def __getslice__(self, start, stop):
        r'''Gets slice from `start` to `stop` in typed tuple.

        Returns new typed tuple.
        '''
        return new(self, tokens=self._collection[start:stop])

    def __hash__(self):
        r'''Hashes typed tuple.

        Returns integer.
        '''
        return hash((
            type(self), 
            self._collection,
            self.item_class,
            self.name,
            ))

    def __mul__(self, expr):
        r'''Multiplies typed tuple by `expr`.

        Returns new typed tuple.
        '''
        tokens = self._collection * expr
        return new(self, tokens=tokens)

    def __rmul__(self, expr):
        r'''Multiplies `expr` by typed tuple.

        Returns new typed tuple.
        '''
        return self.__mul__(expr)

    ### PUBLIC METHODS ###

    def count(self, token):
        r'''Changes `token` to item.
        
        Returns count in collection.
        '''
        item = self._item_callable(token)
        return self._collection.count(item)

    def index(self, token):
        r'''Changes `token` to item.
        
        Returns index in collection.
        '''
        item = self._item_callable(token)
        return self._collection.index(item)


collections.Sequence.register(TypedTuple)
