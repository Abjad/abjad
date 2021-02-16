import abc
import collections.abc

from .new import new
from .storage import FormatSpecification, StorageFormatManager


class TypedCollection:
    """
    Abstract typed collection.
    """

    ### CLASS VARIABLES ###

    __slots__ = ("_collection", "_item_class")

    _is_abstract = True

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
        names = list(StorageFormatManager(self).signature_keyword_names)
        if "items" in names:
            names.remove("items")
        return FormatSpecification(
            self,
            repr_is_indented=False,
            storage_format_args_values=[self._collection],
            storage_format_keyword_names=names,
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


class TypedCounter(TypedCollection, collections.abc.MutableMapping):
    """
    Typed counter.

    ..  container:: example

        >>> counter = abjad.TypedCounter(
        ...     [0, "c'", 1, True, "cs'", "df'"],
        ...     item_class=abjad.NumberedPitch,
        ...     )

        >>> string = abjad.storage(counter)
        >>> print(string)
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

    ### INITIALIZER ###

    def __init__(self, items=None, item_class=None, **keywords):
        TypedCollection.__init__(self, item_class=item_class, items=items)
        self._collection = collections.Counter()
        self.update(items, **keywords)

    ### SPECIAL METHODS ###

    def __add__(self, argument):
        """
        Adds typed counter to ``argument``.

        Returns new typed counter.
        """
        if (
            not isinstance(argument, type(self))
            or not self.item_class == argument.item_class
        ):
            return NotImplemented
        result = type(self)()
        result._collection = self._collection + argument._collection
        return result

    def __and__(self, argument):
        """
        Logical AND of typed counter and ``argument``.

        Returns new typed counter.
        """
        if (
            not isinstance(argument, type(self))
            or not self.item_class == argument.item_class
        ):
            return NotImplemented
        result = type(self)()
        result._collection = self._collection & argument._collection
        return result

    def __delitem__(self, item):
        """
        Deletes ``item`` from typed counter.

        Returns none.
        """
        item = self._coerce_item(item)
        if item in self._collection:
            dict.__delitem__(self._collection, item)

    def __getitem__(self, argument):
        """
        Gets item or slice identified by ``argument``.

        Returns item or slice.
        """
        argument = self._coerce_item(argument)
        return self._collection.__getitem__(argument)

    def __or__(self, argument):
        """
        Logical OR of typed counter and ``argument``.

        Returns new typed counter.
        """
        if (
            not isinstance(argument, type(self))
            or not self.item_class == argument.item_class
        ):
            return NotImplemented
        result = type(self)()
        result._collection = self._collection | argument._collection
        return result

    def __radd__(self, argument):
        """
        Adds ``argument`` to typed counter.

        Returns new typed counter.
        """
        if (
            not isinstance(argument, type(self))
            or not self.item_class == argument.item_class
        ):
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
        item = self._coerce_item(item)
        self._collection.__setitem__(item, value)

    def __sub__(self, argument):
        """
        Subtracts ``argument`` from typed counter.

        Returns new typed counter.
        """
        if (
            not isinstance(argument, type(self))
            or not self.item_class == argument.item_class
        ):
            return NotImplemented
        result = type(self)()
        result._collection = self._collection - argument._collection
        return result

    ### PRIVATE METHODS ###

    def _coerce_arguments(self, items=None, **keywords):
        def _coerce_mapping(items):
            the_items = {}
            for item, count in items.items():
                item = self._coerce_item(item)
                if item not in the_items:
                    the_items[item] = 0
                the_items[item] += count
            return the_items

        the_items = []
        if items is not None:
            if isinstance(items, collections.abc.Mapping):
                items = _coerce_mapping(items)
            else:
                the_items = []
                for item in items:
                    the_items.append(self._coerce_item(item))
        itemdict = _coerce_mapping(keywords)
        return the_items, itemdict

    def _get_format_specification(self):
        names = list(StorageFormatManager(self).signature_keyword_names)
        if "items" in names:
            names.remove("items")
        return FormatSpecification(
            self,
            repr_is_indented=False,
            storage_format_args_values=[self._collection],
            storage_format_keyword_names=names,
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
        name = class_.__name__
        message = f"{name}.fromkeys() is undefined. Use {name}(iterable) instead."
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


class TypedFrozenset(TypedCollection, collections.abc.Set):
    """
    Typed fozen set.
    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self, items=None, item_class=None):
        TypedCollection.__init__(self, item_class=item_class, items=items)
        items = items or []
        items = [self._coerce_item(_) for _ in items]
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
        hash_values = StorageFormatManager(self).get_hash_values()
        try:
            result = hash(hash_values)
        except TypeError:
            raise TypeError(f"unhashable type: {self}")
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


class TypedList(TypedCollection, collections.abc.MutableSequence):
    """
    Typed list.

    ..  container:: example

        No item coercion:

        >>> list_ = abjad.TypedList()
        >>> list_.append(23)
        >>> list_.append('foo')
        >>> list_.append(False)
        >>> list_.append((1, 2, 3))
        >>> list_.append(3.14159)

        >>> string = abjad.storage(list_)
        >>> print(string)
        abjad.TypedList(
            [
                23,
                'foo',
                False,
                (1, 2, 3),
                3.14159,
                ]
            )

    ..  container:: example

        Named pitch item coercion:

        >>> pitch_list = abjad.TypedList(
        ...     item_class=abjad.NamedPitch,
        ...     )
        >>> pitch_list.append(0)
        >>> pitch_list.append("d'")
        >>> pitch_list.append(('e', 4))
        >>> pitch_list.append(abjad.NamedPitch("f'"))

        >>> string = abjad.storage(pitch_list)
        >>> print(string)
        abjad.TypedList(
            [
                abjad.NamedPitch("c'"),
                abjad.NamedPitch("d'"),
                abjad.NamedPitch("e'"),
                abjad.NamedPitch("f'"),
                ],
            item_class=abjad.NamedPitch,
            )

    Ordered collection with optional item coercion.

    Implements the list interface.
    """

    ### CLASS VARIABLES ###

    __slots__ = ("_keep_sorted",)

    ### INITIALIZER ###

    def __init__(self, items=None, item_class=None, keep_sorted=False):
        TypedCollection.__init__(self, item_class=item_class, items=items)
        self._collection = []
        if keep_sorted is not None:
            assert isinstance(keep_sorted, bool), repr(keep_sorted)
        self._keep_sorted = keep_sorted
        items = items or []
        the_items = []
        for item in items:
            the_items.append(self._coerce_item(item))
        self.extend(the_items)

    ### SPECIAL METHODS ###

    def __delitem__(self, i):
        """
        Aliases list.__delitem__().

        Returns none.
        """
        self._on_removal(self._collection[i])
        del self._collection[i]

    def __getitem__(self, argument):
        """
        Gets item or slice identified  by ``argument``.

        Returns item or slice.
        """
        return self._collection.__getitem__(argument)

    def __iadd__(self, argument):
        """
        Adds ``argument`` in place to typed list.

        ..  container:: example

            >>> dynamic_list = abjad.TypedList(item_class=abjad.Dynamic)
            >>> dynamic_list.append('ppp')
            >>> dynamic_list += ['p', 'mp', 'mf', 'fff']

            >>> string = abjad.storage(dynamic_list)
            >>> print(string)
            abjad.TypedList(
                [
                    abjad.Dynamic('ppp'),
                    abjad.Dynamic('p'),
                    abjad.Dynamic('mp'),
                    abjad.Dynamic('mf'),
                    abjad.Dynamic('fff'),
                    ],
                item_class=abjad.Dynamic,
                )

        Returns typed list.
        """
        self.extend(argument)
        return self

    def __reversed__(self):
        """
        Aliases list.__reversed__().

        Returns generator.
        """
        return self._collection.__reversed__()

    def __setitem__(self, i, argument):
        """
        Sets item ``i`` equal to ``argument``.

        ..  container:: example

            Sets item:

            >>> pitch_list = abjad.TypedList(
            ...     item_class=abjad.NamedPitch,
            ...     )
            >>> pitch_list.append(0)
            >>> pitch_list.append("d'")
            >>> pitch_list.append(('e', 4))
            >>> pitch_list.append(abjad.NamedPitch("f'"))

            >>> pitch_list[-1] = 'gqs,'
            >>> string = abjad.storage(pitch_list)
            >>> print(string)
            abjad.TypedList(
                [
                    abjad.NamedPitch("c'"),
                    abjad.NamedPitch("d'"),
                    abjad.NamedPitch("e'"),
                    abjad.NamedPitch('gqs,'),
                    ],
                item_class=abjad.NamedPitch,
                )

        ..  container:: example

            Sets slice:

            >>> pitch_list[-1:] = ["f'", "g'", "a'", "b'", "c''"]
            >>> string = abjad.storage(pitch_list)
            >>> print(string)
            abjad.TypedList(
                [
                    abjad.NamedPitch("c'"),
                    abjad.NamedPitch("d'"),
                    abjad.NamedPitch("e'"),
                    abjad.NamedPitch("f'"),
                    abjad.NamedPitch("g'"),
                    abjad.NamedPitch("a'"),
                    abjad.NamedPitch("b'"),
                    abjad.NamedPitch("c''"),
                    ],
                item_class=abjad.NamedPitch,
                )

        Returns none.
        """
        if isinstance(i, int):
            new_item = self._coerce_item(argument)
            old_item = self._collection[i]
            self._on_removal(old_item)
            self._on_insertion(new_item)
            self._collection[i] = new_item
        elif isinstance(i, slice):
            new_items = [self._coerce_item(item) for item in argument]
            old_items = self._collection[i]
            for old_item in old_items:
                self._on_removal(old_item)
            for new_item in new_items:
                self._on_insertion(new_item)
            self._collection[i] = new_items
        if self.keep_sorted:
            self.sort()

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        names = list(StorageFormatManager(self).signature_keyword_names)
        if "items" in names:
            names.remove("items")
        if "keep_sorted" in names:
            names.remove("keep_sorted")
        return FormatSpecification(
            self,
            repr_is_indented=False,
            storage_format_args_values=[self._collection],
            storage_format_keyword_names=names,
        )

    ### PUBLIC METHODS ###

    def append(self, item):
        """
        Appends ``item`` to typed list.

        ..  container:: example

            >>> integer_list = abjad.TypedList(item_class=int)
            >>> integer_list.append('1')
            >>> integer_list.append(2)
            >>> integer_list.append(3.4)
            >>> integer_list[:]
            [1, 2, 3]

        Returns none.
        """
        item = self._coerce_item(item)
        self._on_insertion(item)
        self._collection.append(item)
        if self.keep_sorted:
            self.sort()

    def count(self, item):
        """
        Gets count of ``item`` in typed list.

        ..  container:: example

            >>> integer_list = abjad.TypedList(item_class=int)
            >>> integer_list.extend([0, 0., '0', 99])

            >>> integer_list.count(0)
            3
            >>> integer_list.count(1)
            0
            >>> integer_list.count(99)
            1

        Returns nonnegative integer.
        """
        item = self._coerce_item(item)
        return self._collection.count(item)

    def extend(self, items):
        """
        Extends typed list with ``items``.

        ..  container:: example

            >>> integer_list = abjad.TypedList(item_class=int)
            >>> integer_list.extend(['0', 1.0, 2, 3.14159])
            >>> integer_list
            TypedList([0, 1, 2, 3], item_class=int)

        Returns none.
        """
        for item in items:
            self.append(item)
        if self.keep_sorted:
            self.sort()

    def index(self, item):
        """
        Gets index of ``item`` in typed list.

        ..  container:: example

            >>> pitch_list = abjad.TypedList(
            ...     item_class=abjad.NamedPitch,
            ...     )
            >>> pitch_list.extend(['cqf', "as'", 'b,', 'dss'])

            >>> pitch_list.index(abjad.NamedPitch('cqf'))
            0
            >>> pitch_list.index(abjad.NamedPitch("as'"))
            1
            >>> pitch_list.index('b,')
            2
            >>> pitch_list.index('dss')
            3

        Returns nonnegative integer.
        """
        item = self._coerce_item(item)
        return self._collection.index(item)

    def insert(self, i, item):
        """
        Insert ``item`` into typed list.

        ..  container:: example

            Inserts into typed list.

            >>> integer_list = abjad.TypedList(item_class=int)
            >>> integer_list.extend(['1', 2, 4.3])
            >>> integer_list
            TypedList([1, 2, 4], item_class=int)

            >>> integer_list.insert(0, '0')
            >>> integer_list
            TypedList([0, 1, 2, 4], item_class=int)

            >>> integer_list.insert(1, '9')
            >>> integer_list
            TypedList([0, 9, 1, 2, 4], item_class=int)

        Returns none.
        """
        item = self._coerce_item(item)
        self._on_insertion(item)
        result = self._collection.insert(i, item)
        if self.keep_sorted:
            self.sort()
        return result

    def pop(self, i=-1):
        """
        Pops item ``i`` from typed list.

        Returns item.
        """
        result = self._collection.pop(i)
        self._on_removal(result)
        if self.keep_sorted:
            self.sort()
        return result

    def remove(self, item):
        """
        Removes ``item`` from typed list.

        ..  container:: example

            >>> integer_list = abjad.TypedList(item_class=int)
            >>> integer_list.extend(('0', 1.0, 2, 3.14159))
            >>> integer_list[:]
            [0, 1, 2, 3]

            >>> integer_list.remove('1')
            >>> integer_list[:]
            [0, 2, 3]

        Returns none.
        """
        item = self._coerce_item(item)
        index = self._collection.index(item)
        item = self._collection[index]
        self._on_removal(item)
        del self._collection[index]
        if self.keep_sorted:
            self.sort()

    def reverse(self):
        """
        Reverses items in typed list.
        """
        self._collection.reverse()

    def sort(self, cmp=None, key=None, reverse=False):
        """
        Sorts items in typed list.
        """
        if cmp is not None:

            def cmp_to_key(comparator):
                """
                Convert a ``cmp`` function into a ``key`` function for use
                with ``sort()``.
                """

                class CmpToKey:
                    def __init__(self, argument):
                        self.argument = argument

                    def __lt__(self, other):
                        return comparator(self.argument, other.argument) < 0

                    def __gt__(self, other):
                        return comparator(self.argument, other.argument) > 0

                    def __eq__(self, other):
                        return comparator(self.argument, other.argument) == 0

                    def __le__(self, other):
                        return comparator(self.argument, other.argument) <= 0

                    def __ge__(self, other):
                        return comparator(self.argument, other.argument) >= 0

                    def __ne__(self, other):
                        return comparator(self.argument, other.argument) != 0

                return CmpToKey

            key = cmp_to_key(cmp)
        self._collection.sort(key=key, reverse=reverse)

    ### PUBLIC PROPERTIES ###

    @property
    def keep_sorted(self):
        """
        Is true when typed list keeps items sorted.

        Defaults to none.

        Set to true, false or none.

        Returns true, false or none.
        """
        return self._keep_sorted

    @keep_sorted.setter
    def keep_sorted(self, argument):
        assert isinstance(argument, (bool, type(None)))
        self._keep_sorted = argument


class TypedTuple(TypedCollection, collections.abc.Sequence):
    """
    Typed tuple.
    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self, items=None, item_class=None):
        TypedCollection.__init__(self, item_class=item_class, items=items)
        items = items or []
        self._collection = tuple(self._coerce_item(item) for item in items)

    ### SPECIAL METHODS ###

    def __add__(self, argument):
        """
        Adds typed tuple to ``argument``.

        Returns new typed tuple.
        """

        if isinstance(argument, type(self)):
            items = argument._collection
            return new(self, items=self._collection[:] + items)
        elif isinstance(argument, type(self._collection)):
            items = argument[:]
            return new(self, items=self._collection[:] + items)
        raise NotImplementedError

    def __contains__(self, item):
        """
        Is true if typed tuple contains ``item``.

        Coerces ``item``.

        Returns none.
        """
        try:
            item = self._coerce_item(item)
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
        hash_values = StorageFormatManager(self).get_hash_values()
        try:
            result = hash(hash_values)
        except TypeError:
            raise TypeError(f"unhashable type: {self}")
        return result

    def __mul__(self, argument):
        """
        Multiplies typed tuple by ``argument``.

        Returns new typed tuple.
        """
        items = self._collection * argument
        return new(self, items=items)

    def __radd__(self, argument):
        """
        Right-adds ``argument`` to typed tuple.
        """
        items = argument + self._collection
        return new(self, items=items)

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
            item = self._coerce_item(item)
        except (ValueError, TypeError):
            return 0
        return self._collection.count(item)

    def index(self, item):
        """
        Gets index of ``item`` in collection.

        Coerces ``item``.

        Returns nonnegative integer.
        """
        item = self._coerce_item(item)
        return self._collection.index(item)
