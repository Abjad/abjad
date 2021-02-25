import collections

from .storage import FormatSpecification, StorageFormatManager


class OrderedDict(collections.abc.MutableMapping):
    r"""
    Ordered dictionary.

    ..  container:: example

        Initializes from list of pairs:

        >>> string = r"\markup \italic Allegretto"
        >>> markup = abjad.Markup(string, literal=True)
        >>> dictionary = abjad.OrderedDict([
        ...     ('color', 'red'),
        ...     ('directive', markup),
        ...     ])

        >>> string = abjad.storage(dictionary)
        >>> print(string)
        abjad.OrderedDict(
            [
                ('color', 'red'),
                (
                    'directive',
                    abjad.Markup(
                        contents=['\\markup \\italic Allegretto'],
                        literal=True,
                        ),
                    ),
                ]
            )

    ..  container:: example

        Initializes from built-in dictionary:

        >>> string = r"\markup \italic Allegretto"
        >>> markup = abjad.Markup(string, literal=True)
        >>> dictionary = {
        ...     'color': 'red',
        ...     'directive': markup,
        ...     }
        >>> dictionary = abjad.OrderedDict(
        ...     dictionary
        ...     )

        >>> string = abjad.storage(dictionary)
        >>> print(string)
        abjad.OrderedDict(
            [
                ('color', 'red'),
                (
                    'directive',
                    abjad.Markup(
                        contents=['\\markup \\italic Allegretto'],
                        literal=True,
                        ),
                    ),
                ]
            )

    ..  container:: example

        Initializes from other ordered dictionary:

        >>> string = r"\markup \italic Allegretto"
        >>> markup = abjad.Markup(string, literal=True)
        >>> dictionary_1 = abjad.OrderedDict([
        ...     ('color', 'red'),
        ...     ('directive', markup),
        ...     ])
        >>> dictionary_2 = abjad.OrderedDict(
        ...     dictionary_1
        ...     )

        >>> string = abjad.storage(dictionary_2)
        >>> print(string)
        abjad.OrderedDict(
            [
                ('color', 'red'),
                (
                    'directive',
                    abjad.Markup(
                        contents=['\\markup \\italic Allegretto'],
                        literal=True,
                        ),
                    ),
                ]
            )

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_collection",)

    ### INITIALIZER ###

    def __init__(self, items=None):
        if isinstance(items, dict):
            items = sorted(items.items())
        elif isinstance(items, collections.abc.Mapping):
            items = list(items.items())
        items = items or []
        the_items = []
        for item in items:
            assert len(item) == 2, repr(item)
            key = item[0]
            value = item[1]
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
        del self._collection[i]

    def __eq__(self, argument):
        """
        Is true when ``argument`` is an ordered dict with items that
        compare equal to those of this ordered dict.

        Returns true or false.
        """
        if issubclass(type(argument), type(self)):
            return self._collection == argument._collection
        elif isinstance(argument, type(self._collection)):
            return self._collection == argument
        return False

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

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return StorageFormatManager(self).get_repr_format()

    def __setitem__(self, i, argument):
        """
        Changes items in ``argument`` to items and sets.

        Returns none.
        """
        self._collection[i] = argument

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        names = list(StorageFormatManager(self).signature_keyword_names)
        if "items" in names:
            names.remove("items")
        values = [list(self._collection.items())]
        return FormatSpecification(
            self,
            repr_is_indented=False,
            storage_format_args_values=values,
            storage_format_keyword_names=names,
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
        return type(self)(items=items)

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
            >>> string = abjad.storage(dictionary)
            >>> print(string)
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
            >>> string = abjad.storage(dictionary)
            >>> print(string)
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
            >>> string = abjad.storage(dictionary)
            >>> print(string)
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
