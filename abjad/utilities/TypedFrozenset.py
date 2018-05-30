import collections
from .TypedCollection import TypedCollection


class TypedFrozenset(TypedCollection, collections.Set):
    """
    Typed fozen set.
    """

    ### CLASS VARIABLES ###

    __slots__ = ()

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

    def __and__(self, argument):
        """
        Logical AND of typed frozen set and ``argument``.

        Returns new typed frozen set.
        """
        argument = type(self)(argument)
        result = self._collection.__and__(argument._collection)
        result = type(self)(result)
        return result

    def __ge__(self, argument):
        """
        Is true when typed frozen set is greater than or equal to ``argument``.

        Returns true or false.
        """
        argument = type(self)(argument)
        return self._collection.__ge__(argument._collection)

    def __gt__(self, argument):
        """
        Is true when typed frozen set is greater than ``argument``.

        Returns true or false.
        """
        argument = type(self)(argument)
        return self._collection.__gt__(argument._collection)

    def __hash__(self):
        """
        Hashes typed frozen set.

        Returns integer.
        """
        import abjad
        hash_values = abjad.StorageFormatManager(self).get_hash_values()
        try:
            result = hash(hash_values)
        except TypeError:
            message = 'unhashable type: {}'.format(self)
            raise TypeError(message)
        return result

    def __le__(self, argument):
        """
        Is true when typed frozen set is less than or equal to ``argument``.

        Returns true or false.
        """
        argument = type(self)(argument)
        return self._collection.__le__(argument._collection)

    def __lt__(self, argument):
        """
        Is true when typed frozen set is less than ``argument``.

        Returns true or false.
        """
        argument = type(self)(argument)
        return self._collection.__lt__(argument._collection)

    def __or__(self, argument):
        """
        Logical OR of typed frozen set and ``argument``.

        Returns new typed frozen set.
        """
        argument = type(self)(argument)
        result = self._collection.__or__(argument._collection)
        result = type(self)(result)
        return result

    def __sub__(self, argument):
        """
        Subtracts ``argument`` from typed frozen set.

        Returns new typed frozen set.
        """
        argument = type(self)(argument)
        result = self._collection.__sub__(argument._collection)
        result = type(self)(result)
        return result

    def __xor__(self, argument):
        """
        Logical XOR of typed frozen set and ``argument``.

        Returns new typed frozen set.
        """
        argument = type(self)(argument)
        result = self._collection.__xor__(argument._collection)
        result = type(self)(result)
        return result

    ### PUBLIC METHODS ###

    def copy(self):
        """
        Copies typed frozen set.

        Returns new typed frozen set.
        """
        return type(self)(self._collection.copy())

    def difference(self, argument):
        """
        Typed frozen set set-minus ``argument``.

        Returns new typed frozen set.
        """
        argument = type(self)(argument)
        result = self._collection.difference(argument._collection)
        result = type(self)(result)
        return result

    def intersection(self, argument):
        """
        Set-theoretic intersection of typed frozen set and ``argument``.

        Returns new typed frozen set.
        """
        argument = type(self)(argument)
        result = self._collection.intersection(argument._collection)
        result = type(self)(result)
        return result

    def isdisjoint(self, argument):
        """
        Is true when typed frozen set shares no elements with ``argument``.

        Returns true or false.
        """
        argument = type(self)(argument)
        return self._collection.isdisjoint(argument._collection)

    def issubset(self, argument):
        """
        Is true when typed frozen set is a subset of ``argument``.

        Returns true or false.
        """
        argument = type(self)(argument)
        return self._collection.issubset(argument._collection)

    def issuperset(self, argument):
        """
        Is true when typed frozen set is a superset of ``argument``.

        Returns true or false.
        """
        argument = type(self)(argument)
        return self._collection.issuperset(argument._collection)

    def symmetric_difference(self, argument):
        """
        Symmetric difference of typed frozen set and ``argument``.

        Returns new typed frozen set.
        """
        argument = type(self)(argument)
        result = self._collection.symmetric_difference(argument._collection)
        result = type(self)(result)
        return result

    def union(self, argument):
        """
        Union of typed frozen set and ``argument``.

        Returns new typed frozen set.
        """
        argument = type(self)(argument)
        result = self._collection.union(argument._collection)
        result = type(self)(result)
        return result
