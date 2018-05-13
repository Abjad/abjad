import collections
from .TypedCollection import TypedCollection


class TypedTuple(TypedCollection, collections.Sequence):
    """
    Typed tuple.
    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(
        self,
        items=None,
        item_class=None,
        ):
        TypedCollection.__init__(
            self,
            item_class=item_class,
            items=items,
            )
        items = items or []
        self._collection = tuple(
            self._item_coercer(item) for item in items)

    ### SPECIAL METHODS ###

    def __add__(self, argument):
        """
        Adds typed tuple to ``argument``.

        Returns new typed tuple.
        """
        import abjad
        if isinstance(argument, type(self)):
            items = argument._collection
            return abjad.new(self, items=self._collection[:] + items)
        elif isinstance(argument, type(self._collection)):
            items = argument[:]
            return abjad.new(self, items=self._collection[:] + items)
        raise NotImplementedError

    def __contains__(self, item):
        """
        Is true if typed tuple contains ``item``.

        Coerces ``item``.

        Returns none.
        """
        try:
            item = self._item_coercer(item)
        except ValueError:
            return False
        return self._collection.__contains__(item)

    def __getitem__(self, argument):
        """
        Gets item or slice identified by ``argument``.

        Returns item or new typed tuple.
        """
        item = self._collection.__getitem__(argument)
        try:
            return type(self)(item)
        except TypeError:
            return item

    def __hash__(self):
        """
        Hashes typed tuple.

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

    def __mul__(self, argument):
        """
        Multiplies typed tuple by ``argument``.

        Returns new typed tuple.
        """
        import abjad
        items = self._collection * argument
        return abjad.new(self, items=items)

    def __radd__(self, argument):
        """
        Right-adds ``argument`` to typed tuple.
        """
        items = argument + self._collection
        return abjad.new(self, items=items)

    def __rmul__(self, argument):
        """
        Multiplies ``argument`` by typed tuple.

        Returns new typed tuple.
        """
        return self.__mul__(argument)

    ### PUBLIC METHODS ###

    def count(self, item):
        """
        Counts ``item`` in collection.

        Coerces ``item``.

        Returns nonnegative integer.
        """
        try:
            item = self._item_coercer(item)
        except (ValueError, TypeError):
            return 0
        return self._collection.count(item)

    def index(self, item):
        """
        Gets index of ``item`` in collection.

        Coerces ``item``.

        Returns nonnegative integer.
        """
        item = self._item_coercer(item)
        return self._collection.index(item)
