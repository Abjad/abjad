import collections
from .TypedCollection import TypedCollection


class TypedCounter(TypedCollection, collections.MutableMapping):
    """
    Typed counter.

    ..  container:: example

        >>> counter = abjad.TypedCounter(
        ...     [0, "c'", 1, True, "cs'", "df'"],
        ...     item_class=abjad.NumberedPitch,
        ...     )

        >>> abjad.f(counter)
        abjad.TypedCounter(
            {
                abjad.NumberedPitch(0): 2,
                abjad.NumberedPitch(1): 4,
                },
            item_class=abjad.NumberedPitch,
            )

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        items=None,
        item_class=None,
        **keywords
        ):
        TypedCollection.__init__(
            self,
            item_class=item_class,
            items=items,
            )
        self._collection = collections.Counter()
        self.update(items, **keywords)

    ### SPECIAL METHODS ###

    def __add__(self, argument):
        """
        Adds typed counter to ``argument``.

        Returns new typed counter.
        """
        if (not isinstance(argument, type(self)) or
            not self.item_class == argument.item_class):
            return NotImplemented
        result = type(self)()
        result._collection = self._collection + argument._collection
        return result

    def __and__(self, argument):
        """
        Logical AND of typed counter and ``argument``.

        Returns new typed counter.
        """
        if (not isinstance(argument, type(self)) or
            not self.item_class == argument.item_class):
            return NotImplemented
        result = type(self)()
        result._collection = self._collection & argument._collection
        return result

    def __delitem__(self, item):
        """
        Deletes ``item`` from typed counter.

        Returns none.
        """
        item = self._item_coercer(item)
        if item in self._collection:
            dict.__delitem__(self._collection, item)

    def __getitem__(self, argument):
        """
        Gets item or slice identified by ``argument``.

        Returns item or slice.
        """
        argument = self._item_coercer(argument)
        return self._collection.__getitem__(argument)

    def __or__(self, argument):
        """
        Logical OR of typed counter and ``argument``.

        Returns new typed counter.
        """
        if (not isinstance(argument, type(self)) or
            not self.item_class == argument.item_class):
            return NotImplemented
        result = type(self)()
        result._collection = self._collection | argument._collection
        return result

    def __radd__(self, argument):
        """
        Adds ``argument`` to typed counter.

        Returns new typed counter.
        """
        if (not isinstance(argument, type(self)) or
            not self.item_class == argument.item_class):
            return NotImplemented
        result = type(self)()
        result._collection = argument._collection + self._collection
        return result

    def __reduce__(self):
        """
        Reduces typed counter.

        Returns new typed counter.
        """
        return type(self), (dict(self._collection),)

    def __setitem__(self, item, value):
        """
        Sets typed counter ``item`` to ``value``.

        Returns none.
        """
        item = self._item_coercer(item)
        self._collection.__setitem__(item, value)

    def __sub__(self, argument):
        """
        Subtracts ``argument`` from typed counter.

        Returns new typed counter.
        """
        if (not isinstance(argument, type(self)) or
            not self.item_class == argument.item_class):
            return NotImplemented
        result = type(self)()
        result._collection = self._collection - argument._collection
        return result

    ### PRIVATE METHODS ###

    def _coerce_arguments(self, items=None, **keywords):
        def _coerce_mapping(items):
            the_items = {}
            for item, count in items.items():
                item = self._item_coercer(item)
                if item not in the_items:
                    the_items[item] = 0
                the_items[item] += count
            return the_items
        the_items = []
        if items is not None:
            if isinstance(items, collections.Mapping):
                items = _coerce_mapping(items)
            else:
                the_items = []
                for item in items:
                    the_items.append(self._item_coercer(item))
        itemdict = _coerce_mapping(keywords)
        return the_items, itemdict

    def _get_format_specification(self):
        import abjad
        agent = abjad.StorageFormatManager(self)
        names = list(agent.signature_keyword_names)
        if 'items' in names:
            names.remove('items')
        return abjad.FormatSpecification(
            self,
            repr_is_indented=False,
            storage_format_args_values=[self._collection],
            storage_format_kwargs_names=names,
            template_names=names,
            )

    ### PUBLIC METHODS ###

    def clear(self):
        """
        Clears typed counter.

        Returns none.
        """
        self._collection.clear()

    def copy(self):
        """
        Copies typed counter.

        Returns new typed counter.
        """
        return type(self)(self)

    def elements(self):
        """
        Elements in typed counter.
        """
        return self._collection.elements()

    @classmethod
    def fromkeys(class_, iterable, v=None):
        """
        Makes new typed counter from ``iterable``.

        Not yet impelemented.

        Will return new typed counter.
        """
        message = '{}.fromkeys() is undefined. Use {}(iterable) instead.'
        message = message.format(class_.__name__, class_.__name__)
        raise NotImplementedError(message)

    def items(self):
        """
        Items in typed counter.

        Returns tuple.
        """
        return list(self._collection.items())

    def keys(self):
        """
        Iterates keys in typed counter.
        """
        return iter(self._collection.keys())

    def most_common(self, n=None):
        """
        Please document.
        """
        return self._collection(n=n)

    def subtract(self, iterable=None, **keywords):
        """
        Subtracts ``iterable`` from typed counter.
        """
        items, itemdict = self._coerce_arguments(iterable, **keywords)
        self._collection.subtract(items, **itemdict)

    def update(self, iterable=None, **keywords):
        """
        Updates typed counter with ``iterable``.
        """
        items, itemdict = self._coerce_arguments(iterable, **keywords)
        self._collection.update(items, **itemdict)

    def values(self):
        """
        Iterates values in typed counter.
        """
        return iter(self._collection.values())

    def viewitems(self):
        """
        Please document.
        """
        return self._collection.items()

    def viewkeys(self):
        """
        Please document.
        """
        return self._collection.keys()

    def viewvalues(self):
        """
        Please document.
        """
        return self._collection.values()
