# -*- coding: utf-8 -*-
import collections
from abjad.tools.datastructuretools.TypedCollection import TypedCollection
from abjad.tools.topleveltools import new


class TypedFrozenset(TypedCollection):
    r'''A typed fozen set.
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
        items = [self._item_coercer(_) for _ in items]
        self._collection = frozenset(items)

    ### SPECIAL METHODS ###

    def __and__(self, expr):
        r'''Logical AND of typed frozen set and `expr`.

        Returns new typed frozen set.
        '''
        expr = type(self)(expr)
        result = self._collection.__and__(expr._collection)
        result = type(self)(result)
        return result

    def __ge__(self, expr):
        r'''Is true when typed frozen set is greater than or equal to `expr`.
        Otherwise false.

        Returns true or false.
        '''
        expr = type(self)(expr)
        return self._collection.__ge__(expr._collection)

    def __gt__(self, expr):
        r'''Is true when typed frozen set is greater than `expr`. Otherwise false.

        Returns true or false.
        '''
        expr = type(self)(expr)
        return self._collection.__gt__(expr._collection)

    def __hash__(self):
        r'''Hashes typed frozen set.

        Returns integer.
        '''
        return hash((
            type(self),
            self._collection,
            self.item_class,
            ))

    def __le__(self, expr):
        r'''Is true when typed frozen set is less than or equal to `expr`.
        Otherwise false.

        Returns true or false.
        '''
        expr = type(self)(expr)
        return self._collection.__le__(expr._collection)

    def __lt__(self, expr):
        r'''Is true when typed frozen set is less than `expr`. Otherwise false.

        Returns true or false.
        '''
        expr = type(self)(expr)
        return self._collection.__lt__(expr._collection)

    def __ne__(self, expr):
        r'''Is true when typed frozen set is not equal to `expr`. Otherwise
        false.

        Returns true or false.
        '''
        expr = type(self)(expr)
        return self._collection.__ne__(expr._collection)

    def __or__(self, expr):
        r'''Logical OR of typed frozen set and `expr`.

        Returns new typed frozen set.
        '''
        expr = type(self)(expr)
        result = self._collection.__or__(expr._collection)
        result = type(self)(result)
        return result

    def __sub__(self, expr):
        r'''Subtracts `expr` from typed frozen set.

        Returns new typed frozen set.
        '''
        expr = type(self)(expr)
        result = self._collection.__sub__(expr._collection)
        result = type(self)(result)
        return result

    def __xor__(self, expr):
        r'''Logical XOR of typed frozen set and `expr`.

        Returns new typed frozen set.
        '''
        expr = type(self)(expr)
        result = self._collection.__xor__(expr._collection)
        result = type(self)(result)
        return result

    ### PUBLIC METHODS ###

    def copy(self):
        r'''Copies typed frozen set.

        Returns new typed frozen set.
        '''
        return type(self)(self._collection.copy())

    def difference(self, expr):
        r'''Typed frozen set set-minus `expr`.

        Returns new typed frozen set.
        '''
        expr = type(self)(expr)
        result = self._collection.difference(expr._collection)
        result = type(self)(result)
        return result

    def intersection(self, expr):
        r'''Set-theoretic intersection of typed frozen set and `expr`.

        Returns new typed frozen set.
        '''
        expr = type(self)(expr)
        result = self._collection.intersection(expr._collection)
        result = type(self)(result)
        return result

    def isdisjoint(self, expr):
        r'''Is true when typed frozen set shares no elements with `expr`.
        Otherwise false.

        Returns true or false.
        '''
        expr = type(self)(expr)
        return self._collection.isdisjoint(expr._collection)

    def issubset(self, expr):
        r'''Is true when typed frozen set is a subset of `expr`. Otherwise
        false.

        Returns true or false.
        '''
        expr = type(self)(expr)
        return self._collection.issubset(expr._collection)

    def issuperset(self, expr):
        r'''Is true when typed frozen set is a superset of `expr`. Otherwise
        false.

        Returns true or false.
        '''
        expr = type(self)(expr)
        return self._collection.issuperset(expr._collection)

    def symmetric_difference(self, expr):
        r'''Symmetric difference of typed frozen set and `expr`.

        Returns new typed frozen set.
        '''
        expr = type(self)(expr)
        result = self._collection.symmetric_difference(expr._collection)
        result = type(self)(result)
        return result

    def union(self, expr):
        r'''Union of typed frozen set and `expr`.

        Returns new typed frozen set.
        '''
        expr = type(self)(expr)
        result = self._collection.union(expr._collection)
        result = type(self)(result)
        return result


collections.Set.register(TypedFrozenset)
