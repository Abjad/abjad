import abc

from abjad.system.FormatSpecification import FormatSpecification
from abjad.system.StorageFormatManager import StorageFormatManager


class TypedCollection(object):
    """
    Abstract typed collection.
    """

    ### CLASS VARIABLES ###

    __slots__ = ("_collection", "_item_class")

    _is_abstract = True

    _publish_storage_format = True

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, items=None, item_class=None):
        assert isinstance(item_class, (type(None), type))
        self._item_class = item_class

    ### SPECIAL METHODS ###

    def __contains__(self, item):
        """
        Is true when typed collection contains ``item``.

        Returns true or false.
        """
        try:
            item = self._coerce_item(item)
        except ValueError:
            return False
        return self._collection.__contains__(item)

    def __eq__(self, argument):
        """
        Is true when ``argument`` is a typed collection with items that
        compare equal to those of this typed collection.

        Returns true or false.
        """
        if issubclass(type(argument), type(self)):
            return self._collection == argument._collection
        elif isinstance(argument, type(self._collection)):
            return self._collection == argument
        return False

    def __format__(self, format_specification="") -> str:
        """
        Formats object.
        """
        return StorageFormatManager(self).get_storage_format()

    def __hash__(self):
        """
        Hashes typed collection.

        Redefined in tandem with __eq__.
        """
        return object.__hash__(self)

    def __iter__(self):
        """
        Iterates typed collection.

        Returns generator.
        """
        return self._collection.__iter__()

    def __len__(self):
        """
        Gets length of typed collection.

        Returns nonnegative integer.
        """
        return len(self._collection)

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return StorageFormatManager(self).get_repr_format()

    ### PRIVATE METHODS ###

    def _coerce_item(self, item):
        def coerce_(x):
            if isinstance(x, self._item_class):
                return x
            return self._item_class(x)

        if self._item_class is None:
            return item
        return coerce_(item)

    def _get_format_specification(self):
        manager = StorageFormatManager(self)
        names = list(manager.signature_keyword_names)
        if "items" in names:
            names.remove("items")
        return FormatSpecification(
            self,
            repr_is_indented=False,
            storage_format_args_values=[self._collection],
            storage_format_kwargs_names=names,
        )

    def _on_insertion(self, item):
        """
        Override to operate on item after insertion into collection.
        """
        pass

    def _on_removal(self, item):
        """
        Override to operate on item after removal from collection.
        """
        pass

    ### PUBLIC PROPERTIES ###

    @property
    def item_class(self):
        """
        Gets item class of collection.

        Collection coerces items according to ``item_class``.

        Returns class.
        """
        return self._item_class

    @property
    def items(self):
        """
        Gets items in collection.

        Returns list.
        """
        return [_ for _ in self]
