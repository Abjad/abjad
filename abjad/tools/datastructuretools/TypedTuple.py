# -*- encoding: utf-8 -*-
import collections
from abjad.tools.datastructuretools.TypedCollection import TypedCollection


class TypedTuple(TypedCollection):

    ### CLASS VARIABLES ### 

    __slots__ = ()

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
        if isinstance(expr, type(self)):
            tokens = expr._collection
            return self.new(tokens=self._collection[:] + tokens)
        elif isinstance(expr, type(self._collection)):
            tokens = expr[:]
            return self.new(tokens=self._collection[:] + tokens)
        raise NotImplementedError

    def __contains__(self, token):
        r'''Change `token` to item and return true if item exists in
        collection.
        '''
        try:
            item = self._item_callable(token)
        except ValueError:
            return False
        return self._collection.__contains__(item)

    def __getitem__(self, i):
        '''Aliases tuple.__getitem__().
        '''
        return self._collection[i]

    def __getslice__(self, start, stop):
        return self.new(tokens=self._collection[start:stop])

    def __hash__(self):
        return hash((
            type(self), 
            self._collection,
            self.item_class,
            self.name,
            ))

    def __mul__(self, expr):
        tokens = self._collection * expr
        return self.new(tokens=tokens)

    def __rmul__(self, expr):
        return self.__mul__(expr)

    ### PUBLIC METHODS ###

    def count(self, token):
        r'''Change `token` to item and return count in collection.
        '''
        item = self._item_callable(token)
        return self._collection.count(item)

    def index(self, token):
        r'''Change `token` to item and return index in collection.
        '''
        item = self._item_callable(token)
        return self._collection.index(item)


collections.Sequence.register(TypedTuple)
