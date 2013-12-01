# -*- encoding: utf-8 -*-
import collections
from abjad.tools.datastructuretools.TypedCollection import TypedCollection


class TypedFrozenset(TypedCollection):
    r'''A typed fozen set.
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
        self._collection = frozenset(self._item_callable(token) 
            for token in tokens)

    ### SPECIAL METHODS ###

    def __and__(self, expr):
        r'''Logical AND of typed frozen set and `expr`.

        Returns new typed frozen set.
        '''
        expr = self.__makenew__(expr)
        result = self._collection.__and__(expr._collection)
        return self.__makenew__(result)

    def __ge__(self, expr):
        r'''True when typed frozen set is greater than or equal to `expr`.
        Otherwise false.

        Returns boolean.
        '''
        expr = self.__makenew__(expr)
        return self._collection.__ge__(expr._collection)

    def __gt__(self, expr):
        r'''True when typed frozen set is greater than `expr`. Otherwise false.

        Returns boolean.
        '''
        expr = self.__makenew__(expr)
        return self._collection.__gt__(expr._collection)

    def __hash__(self):
        r'''Hashes typed frozen set.

        Returns integer.
        '''
        return hash((
            type(self), 
            self._collection,
            self.item_class,
            self.name,
            ))

    def __le__(self, expr):
        r'''True when typed frozen set is less than or equal to `expr`.
        Otherwise false.

        Returns boolean.
        '''
        expr = self.__makenew__(expr)
        return self._collection.__le__(expr._collection)

    def __lt__(self, expr):
        r'''True when typed frozen set is less than `expr`. Otherwise false.

        Returns boolean.
        '''
        expr = self.__makenew__(expr)
        return self._collection.__lt__(expr._collection)

    def __ne__(self, expr):
        r'''True when typed frozen set is not equal to `expr`. Otherwise false.

        Returns boolean.
        '''
        expr = self.__makenew__(expr)
        return self._collection.__ne__(expr._collection)

    def __or__(self, expr):
        r'''Logical OR of typed frozen set and `expr`.

        Returns new typed frozen set.
        '''
        expr = self.__makenew__(expr)
        result = self._collection.__or__(expr._collection)
        return self.__makenew__(result)

    def __sub__(self, expr):
        r'''Subtracts `expr` from typed frozen set.

        Returns new typed frozen set.
        '''
        expr = self.__makenew__(expr)
        result = self._collection.__sub__(expr._collection)
        return self.__makenew__(result)

    def __xor__(self, expr):
        r'''Logical XOR of typed frozen set and `expr`.

        Returns new typed frozen set.
        '''
        expr = self.__makenew__(expr)
        result = self._collection.__xor__(expr._collection)
        return self.__makenew__(result)

    ### PUBLIC METHODS ###

    def copy(self):
        r'''Copies typed frozen set.

        Returns new typed frozen set.
        '''
        return self.__makenew__(self._collection.copy())

    def difference(self, expr):
        r'''Typed frozen set set-minus `expr`.

        Returns new typed frozen set.
        '''
        expr = self.__makenew__(expr)
        result = self._collection.difference(expr._collection)
        return self.__makenew__(result)

    def intersection(self, expr):
        r'''Set-theoretic intersection of typed frozen set and `expr`.

        Returns new typed frozen set.
        '''
        expr = self.__makenew__(expr)
        result = self._collection.intersection(expr._collection)
        return self.__makenew__(result)

    def isdisjoint(self, expr):
        r'''True when typed frozen set shares no elements with `expr`.
        Otherwise false.

        Returns boolean.
        '''
        expr = self.__makenew__(expr)
        return self._collection.isdisjoint(expr._collection)

    def issubset(self, expr):
        r'''True when typed frozen set is a subset of `expr`. Otherwise false.

        Returns boolean.
        '''
        expr = self.__makenew__(expr)
        return self._collection.issubset(expr._collection)

    def issuperset(self, expr):
        r'''True when typed frozen set is a superset of `expr`. Otherwise
        false.

        Returns boolean.
        '''
        expr = self.__makenew__(expr)
        return self._collection.issuperset(expr._collection)

    def symmetric_difference(self, expr):
        r'''Symmetric difference of typed frozen set and `expr`.

        Returns new typed frozen set.
        '''
        expr = self.__makenew__(expr)
        result = self._collection.symmetric_difference(expr._collection)
        return self.__makenew__(result)

    def union(self, expr):
        r'''Union of typed frozen set and `expr`.

        Returns new typed frozen set.
        '''
        expr = self.__makenew__(expr)
        result = self._collection.union(expr._collection)
        return self.__makenew__(result)


collections.Set.register(TypedFrozenset)
