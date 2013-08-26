# -*- encoding: utf-8 -*-
from abjad.tools.datastructuretools.TypedCollection import TypedCollection


class TypedFrozenset(TypedCollection):

    ### CLASS VARIABLES ### 

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self, tokens=None, item_class=None, name=None):
        TypedCollection.__init__(self, 
            item_class=item_class, 
            name=name,
            tokens=tokens,
            )
        tokens = tokens or []
        self._collection = frozenset(self._item_callable(token) 
            for token in tokens)

    ### SPECIAL METHODS ###

    '''
    __and__
    __contains__
    __ge__
    __gt__
    __iand__
    __ior__
    __isub__
    __ixor__
    __le__
    __lt__
    __ne__
    __or__
    __sub__
    __xor__
    '''

    ### PUBLIC METHODS ###

    def copy(self):
        return self.new(self._collection.copy())

    def difference(self, expr):
        expr = self.new(expr)
        result = self._collection.difference(expr._collection)
        return self.new(result)

    def intersection(self, expr):
        expr = self.new(expr)
        result = self._collection.intersection(expr._collection)
        return self.new(result)

    def isdisjoint(self, expr):
        expr = self.new(expr)
        return self._collection.isdisjoint(expr._collection)

    def issubset(self, expr):
        expr = self.new(expr)
        return self._collection.issubset(expr._collection)

    def issuperset(self, expr):
        expr = self.new(expr)
        return self._collection.issuperset(expr._collection)

    def symmetric_difference(self, expr):
        expr = self.new(expr)
        result = self._collection.symmetric_difference(expr._collection)
        return self.new(result)

    def union(self, expr):
        expr = self.new(expr)
        result = self._collection.union(expr._collection)
        return self.new(result)

