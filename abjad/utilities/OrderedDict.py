import collections
from .TypedCollection import TypedCollection


class OrderedDict(TypedCollection, collections.MutableMapping):
    r"""
    Ordered dictionary.

    ..  container:: example

        Initializes from list of pairs:

        >>> dictionary = abjad.OrderedDict([
        ...     ('color', 'red'),
        ...     ('directive', abjad.Markup(r'\italic Allegretto')),
        ...     ])

        >>> abjad.f(dictionary)
        abjad.OrderedDict(
            [
                ('color', 'red'),
                (
                    'directive',
                    abjad.Markup(
                        contents=[
                            abjad.MarkupCommand(
                                'italic',
                                'Allegretto'
                                ),
                            ],
                        ),
                    ),
                ]
            )

    ..  container:: example

        Initializes from built-in dictionary:

        >>> dictionary = {
        ...     'color': 'red',
        ...     'directive': abjad.Markup(r'\italic Allegretto'),
        ...     }
        >>> dictionary = abjad.OrderedDict(
        ...     dictionary
        ...     )

        >>> abjad.f(dictionary)
        abjad.OrderedDict(
            [
                ('color', 'red'),
                (
                    'directive',
                    abjad.Markup(
                        contents=[
                            abjad.MarkupCommand(
                                'italic',
                                'Allegretto'
                                ),
                            ],
                        ),
                    ),
                ]
            )

    ..  container:: example

        Initializes from other ordered dictionary:

        >>> dictionary_1 = abjad.OrderedDict([
        ...     ('color', 'red'),
        ...     ('directive', abjad.Markup(r'\italic Allegretto')),
        ...     ])
        >>> dictionary_2 = abjad.OrderedDict(
        ...     dictionary_1
        ...     )

        >>> abjad.f(dictionary_2)
        abjad.OrderedDict(
            [
                ('color', 'red'),
                (
                    'directive',
                    abjad.Markup(
                        contents=[
                            abjad.MarkupCommand(
                                'italic',
                                'Allegretto'
                                ),
                            ],
                        ),
                    ),
                ]
            )

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(self, items=None, item_class=None):
        TypedCollection.__init__(
            self,
            item_class=item_class,
            )
        if isinstance(items, dict):
            items = sorted(items.items())
        elif isinstance(items, collections.Mapping):
            items = list(items.items())
        items = items or []
        the_items = []
        for item in items:
            assert len(item) == 2, repr(item)
            key = item[0]
            value = self._item_coercer(item[1])
            the_item = (key, value)
            the_items.append(the_item)
        self._collection = collections.OrderedDict(the_items)

    ### SPECIAL METHODS ###

    def __cmp__(self, argument):
        """
        Aliases OrderedDict.__cmp__().

        Returns true or false.
        """
        assert isinstance(argument, type(self))
        ordered_dictionary = argument._collection
        return self._collection.__cmp__(ordered_dictionary)

    def __contains__(self, key):
        """
        Aliases OrderedDict.__contains__().

        Returns true or false.
        """
        return key in self._collection

    def __delitem__(self, i):
        """
        Aliases OrderedDict.__delitem__().

        Returns none.
        """
        del(self._collection[i])

    def __ge__(self, argument):
        """
        Is true when typed ordered dictionary is greater than or equal
        to ``argument``.

        Returns true or false.
        """
        argument = type(self)(argument)
        return self._collection.__ge__(argument._collection)

    def __getitem__(self, argument):
        """
        Gets item or slice identified by ``argument``.

        Returns item or slice.
        """
        return self._collection.__getitem__(argument)

    def __gt__(self, argument):
        """
        Is true when typed ordered dictionary is greater than ``argument``.

        Returns true or false.
        """
        argument = type(self)(argument)
        return self._collection.__gt__(argument._collection)

    def __le__(self, argument):
        """
        Is true when typed ordered dictionary is less than or equal
        to ``argument``.

        Returns true or false.
        """
        argument = type(self)(argument)
        return self._collection.__le__(argument._collection)

    def __lt__(self, argument):
        """
        Is true when typed ordered dictionary is less than ``argument``.

        Returns true or false.
        """
        argument = type(self)(argument)
        return self._collection.__lt__(argument._collection)

    def __reversed__(self):
        """
        Aliases OrderedDict.__reversed__().

        Returns generatos.
        """
        return self._collection.__reversed__()

    def __setitem__(self, i, argument):
        """
        Changes items in ``argument`` to items and sets.

        Returns none.
        """
        new_item = self._item_coercer(argument)
        self._collection[i] = new_item

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        import abjad
        agent = abjad.StorageFormatManager(self)
        names = list(agent.signature_keyword_names)
        if 'items' in names:
            names.remove('items')
        values = [list(self._collection.items())]
        return abjad.FormatSpecification(
            self,
            repr_is_indented=False,
            storage_format_args_values=values,
            storage_format_kwargs_names=names,
            )

    ### PUBLIC METHODS ###

    def clear(self):
        """
        Clears typed ordered dictionary.

        Returns none.
        """
        self._collection.clear()

    def copy(self):
        """
        Copies typed ordered dictionary.

        Returns new typed ordered dictionary.
        """
        ordered_dictionary = self._collection.copy()
        items = list(ordered_dictionary.items())
        return type(self)(
            item_class=self.item_class,
            items=items,
            )

    def get(self, i, default=None):
        """
        Aliases OrderedDict.get().

        Returns item or raises key error.
        """
        return self._collection.get(i, default)

    def has_key(self, key):
        """
        Aliases OrderdDict.has_key().

        Returns true or false.
        """
        return key in self._collection

    def items(self):
        """
        Aliases OrderedDict.items().

        Returns generator.
        """
        return iter(self._collection.items())

    def keys(self):
        """
        Aliases OrderedDict.keys().

        Returns generator.
        """
        return iter(self._collection.keys())

    def pop(self, key, default=None):
        """
        Aliases OrderedDict.pop().

        Returns items.
        """
        return self._collection.pop(key, default)

    def popitem(self):
        """
        Aliases OrderedDict.popitem().

        Returns generator.
        """
        return self._collection.popitem()

    def setdefault(self, key, default=None):
        """
        Aliases OrderedDict.setdefault().

        Returns items.
        """
        return self._collection.setdefault(key, default)

    def sort(self, recurse=False) -> None:
        """
        Sorts ordered dictionary (in place).

        ..  container:: example

            >>> dictionary = abjad.OrderedDict()
            >>> dictionary['flavor'] = 'cherry'
            >>> dictionary['colors'] = abjad.OrderedDict()
            >>> dictionary['colors']['red'] = 3
            >>> dictionary['colors']['green'] = 2
            >>> dictionary['colors']['blue'] = 1
            >>> abjad.f(dictionary)
            abjad.OrderedDict(
                [
                    ('flavor', 'cherry'),
                    (
                        'colors',
                        abjad.OrderedDict(
                            [
                                ('red', 3),
                                ('green', 2),
                                ('blue', 1),
                                ]
                            ),
                        ),
                    ]
                )

            >>> dictionary.sort()
            >>> abjad.f(dictionary)
            abjad.OrderedDict(
                [
                    (
                        'colors',
                        abjad.OrderedDict(
                            [
                                ('red', 3),
                                ('green', 2),
                                ('blue', 1),
                                ]
                            ),
                        ),
                    ('flavor', 'cherry'),
                    ]
                )

            >>> dictionary.sort(recurse=True)
            >>> abjad.f(dictionary)
            abjad.OrderedDict(
                [
                    (
                        'colors',
                        abjad.OrderedDict(
                            [
                                ('blue', 1),
                                ('green', 2),
                                ('red', 3),
                                ]
                            ),
                        ),
                    ('flavor', 'cherry'),
                    ]
                )

        """
        items = list(self.items())
        items.sort()
        self.clear()
        for key, value in items:
            if recurse is True and isinstance(value, OrderedDict):
                value.sort(recurse=True)
            self[key] = value

    def update(self, *arguments, **keywords):
        """
        Aliases OrderedDict.update().

        Returns none.
        """
        return self._collection.update(*arguments, **keywords)

    def values(self):
        """
        Aliases OrderedDict.values().

        Returns generator.
        """
        return iter(self._collection.values())
