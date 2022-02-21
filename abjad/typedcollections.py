import collections
import dataclasses
import typing


@dataclasses.dataclass(slots=True, unsafe_hash=True)
class TypedCollection:
    """
    Abstract typed collection.
    """

    items: typing.Any = None
    item_class: typing.Any = None

    _is_abstract = True

    def __post_init__(self):
        assert isinstance(self.item_class, (type(None), type)), repr(self.item_class)
        self.items = self.items or []

    def __contains__(self, item):
        """
        Is true when typed collection contains ``item``.

        Returns true or false.
        """
        try:
            item = self._coerce_item(item)
        except ValueError:
            return False
        return self.items.__contains__(item)

    def __eq__(self, argument):
        """
        Compares ``items``.
        """
        if issubclass(type(argument), type(self)):
            return self.items == argument.items
        elif isinstance(argument, type(self.items)):
            return self.items == argument
        return False

    def __iter__(self):
        """
        Iterates typed collection.

        Returns generator.
        """
        return self.items.__iter__()

    def __len__(self):
        """
        Gets length of typed collection.

        Returns nonnegative integer.
        """
        return len(self.items)

    def _coerce_item(self, item):
        def coerce_(x):
            if isinstance(x, self.item_class):
                return x
            return self.item_class(x)

        if self.item_class is None:
            return item
        return coerce_(item)

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


@dataclasses.dataclass(slots=True, unsafe_hash=True)
class TypedFrozenset(TypedCollection, collections.abc.Set):
    """
    Typed fozen set.
    """

    def __post_init__(self):
        TypedCollection.__post_init__(self)
        self.items = self.items or []
        self.items = [self._coerce_item(_) for _ in self.items]
        self.items = frozenset(self.items)

    def __and__(self, argument):
        """
        Logical AND of typed frozen set and ``argument``.

        Returns new typed frozen set.
        """
        argument = type(self)(argument)
        result = self.items.__and__(argument.items)
        result = type(self)(result)
        return result

    def __ge__(self, argument):
        """
        Is true when typed frozen set is greater than or equal to ``argument``.

        Returns true or false.
        """
        argument = type(self)(argument)
        return self.items.__ge__(argument.items)

    def __gt__(self, argument):
        """
        Is true when typed frozen set is greater than ``argument``.

        Returns true or false.
        """
        argument = type(self)(argument)
        return self.items.__gt__(argument.items)

    def __le__(self, argument):
        """
        Is true when typed frozen set is less than or equal to ``argument``.

        Returns true or false.
        """
        argument = type(self)(argument)
        return self.items.__le__(argument.items)

    def __lt__(self, argument):
        """
        Is true when typed frozen set is less than ``argument``.

        Returns true or false.
        """
        argument = type(self)(argument)
        return self.items.__lt__(argument.items)

    def __or__(self, argument):
        """
        Logical OR of typed frozen set and ``argument``.

        Returns new typed frozen set.
        """
        argument = type(self)(argument)
        result = self.items.__or__(argument.items)
        result = type(self)(result)
        return result

    def __repr__(self):
        """
        Gets repr of TypedFrozenset.
        """
        return f"{type(self).__name__}(items={self._get_sorted_repr_items()}, item_class=abjad.{self.item_class.__name__})"

    def __str__(self) -> str:
        """
        Gets string.
        """
        items = self._get_sorted_repr_items()
        items = [str(_) for _ in items]
        string = ", ".join(items)
        return f"{{{string}}}"

    def __sub__(self, argument):
        """
        Subtracts ``argument`` from typed frozen set.

        Returns new typed frozen set.
        """
        argument = type(self)(argument)
        result = self.items.__sub__(argument.items)
        result = type(self)(result)
        return result

    def __xor__(self, argument):
        """
        Logical XOR of typed frozen set and ``argument``.

        Returns new typed frozen set.
        """
        argument = type(self)(argument)
        result = self.items.__xor__(argument.items)
        result = type(self)(result)
        return result

    def _get_sorted_repr_items(self):
        items = sorted(self, key=lambda _: (float(_.number), str(_)))
        if self.item_class.__name__.startswith("Named"):
            repr_items = [str(_) for _ in items]
        elif hasattr(self.item_class, "number"):
            repr_items = [_.number for _ in items]
        elif hasattr(self.item_class, "pitch_class_number"):
            repr_items = [_.pitch_class_number for _ in items]
        elif hasattr(self.item_class, "__abs__"):
            repr_items = [abs(_) for _ in items]
        else:
            raise ValueError(f"invalid item class: {self.item_class!r}.")
        return repr_items

    def copy(self):
        """
        Copies typed frozen set.

        Returns new typed frozen set.
        """
        return type(self)(self.items.copy())

    def difference(self, argument):
        """
        Typed frozen set set-minus ``argument``.

        Returns new typed frozen set.
        """
        argument = type(self)(argument)
        result = self.items.difference(argument.items)
        result = type(self)(result)
        return result

    def intersection(self, argument):
        """
        Set-theoretic intersection of typed frozen set and ``argument``.

        Returns new typed frozen set.
        """
        argument = type(self)(argument)
        result = self.items.intersection(argument.items)
        result = type(self)(result)
        return result

    def isdisjoint(self, argument):
        """
        Is true when typed frozen set shares no elements with ``argument``.

        Returns true or false.
        """
        argument = type(self)(argument)
        return self.items.isdisjoint(argument.items)

    def issubset(self, argument):
        """
        Is true when typed frozen set is a subset of ``argument``.

        Returns true or false.
        """
        argument = type(self)(argument)
        return self.items.issubset(argument.items)

    def issuperset(self, argument):
        """
        Is true when typed frozen set is a superset of ``argument``.

        Returns true or false.
        """
        argument = type(self)(argument)
        return self.items.issuperset(argument.items)

    def symmetric_difference(self, argument):
        """
        Symmetric difference of typed frozen set and ``argument``.

        Returns new typed frozen set.
        """
        argument = type(self)(argument)
        result = self.items.symmetric_difference(argument.items)
        result = type(self)(result)
        return result

    def union(self, argument):
        """
        Union of typed frozen set and ``argument``.

        Returns new typed frozen set.
        """
        argument = type(self)(argument)
        result = self.items.union(argument.items)
        result = type(self)(result)
        return result


@dataclasses.dataclass(slots=True)
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

        >>> list_
        TypedList(items=[23, 'foo', False, (1, 2, 3), 3.14159], item_class=None, keep_sorted=False)

    ..  container:: example

        Named pitch item coercion:

        >>> pitch_list = abjad.TypedList(
        ...     item_class=abjad.NamedPitch,
        ...     )
        >>> pitch_list.append(0)
        >>> pitch_list.append("d'")
        >>> pitch_list.append(('e', 4))
        >>> pitch_list.append(abjad.NamedPitch("f'"))

        >>> pitch_list
        TypedList(items=[NamedPitch("c'"), NamedPitch("d'"), NamedPitch("e'"), NamedPitch("f'")], item_class=<class 'abjad.pitch.NamedPitch'>, keep_sorted=False)

    """

    keep_sorted: bool = False

    def __post_init__(self):
        TypedCollection.__post_init__(self)
        if self.keep_sorted is not None:
            assert isinstance(self.keep_sorted, bool), repr(self.keep_sorted)
        self.items = [self._coerce_item(_) for _ in self.items or []]
        if self.keep_sorted:
            self.sort()

    def __delitem__(self, i):
        """
        Aliases list.__delitem__().

        Returns none.
        """
        self._on_removal(self.items[i])
        del self.items[i]

    def __getitem__(self, argument):
        """
        Gets item or slice identified  by ``argument``.

        Returns item or slice.
        """
        return self.items.__getitem__(argument)

    def __iadd__(self, argument):
        """
        Adds ``argument`` in place to typed list.

        ..  container:: example

            >>> dynamic_list = abjad.TypedList(item_class=abjad.Dynamic)
            >>> dynamic_list.append('ppp')
            >>> dynamic_list += ['p', 'mp', 'mf', 'fff']

            >>> dynamic_list
            TypedList(items=[Dynamic(name='ppp', command=None, direction=None, format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=-4, tweaks=None), Dynamic(name='p', command=None, direction=None, format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=-2, tweaks=None), Dynamic(name='mp', command=None, direction=None, format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=-1, tweaks=None), Dynamic(name='mf', command=None, direction=None, format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=1, tweaks=None), Dynamic(name='fff', command=None, direction=None, format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=4, tweaks=None)], item_class=<class 'abjad.dynamic.Dynamic'>, keep_sorted=False)

        Returns typed list.
        """
        self.extend(argument)
        return self

    def __reversed__(self):
        """
        Aliases list.__reversed__().

        Returns generator.
        """
        return self.items.__reversed__()

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
            >>> pitch_list
            TypedList(items=[NamedPitch("c'"), NamedPitch("d'"), NamedPitch("e'"), NamedPitch('gqs,')], item_class=<class 'abjad.pitch.NamedPitch'>, keep_sorted=False)

        ..  container:: example

            Sets slice:

            >>> pitch_list[-1:] = ["f'", "g'", "a'", "b'", "c''"]
            >>> pitch_list
            TypedList(items=[NamedPitch("c'"), NamedPitch("d'"), NamedPitch("e'"), NamedPitch("f'"), NamedPitch("g'"), NamedPitch("a'"), NamedPitch("b'"), NamedPitch("c''")], item_class=<class 'abjad.pitch.NamedPitch'>, keep_sorted=False)

        Returns none.
        """
        if isinstance(i, int):
            new_item = self._coerce_item(argument)
            old_item = self.items[i]
            self._on_removal(old_item)
            self._on_insertion(new_item)
            self.items[i] = new_item
        elif isinstance(i, slice):
            new_items = [self._coerce_item(item) for item in argument]
            old_items = self.items[i]
            for old_item in old_items:
                self._on_removal(old_item)
            for new_item in new_items:
                self._on_insertion(new_item)
            self.items[i] = new_items
        if self.keep_sorted:
            self.sort()

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
        self.items.append(item)
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
        return self.items.count(item)

    def extend(self, items) -> None:
        """
        Extends typed list with ``items``.

        ..  container:: example

            >>> integer_list = abjad.TypedList(item_class=int)
            >>> integer_list.extend(['0', 1.0, 2, 3.14159])
            >>> integer_list
            TypedList(items=[0, 1, 2, 3], item_class=<class 'int'>, keep_sorted=False)

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
        return self.items.index(item)

    def insert(self, i, item):
        """
        Insert ``item`` into typed list.

        ..  container:: example

            Inserts into typed list.

            >>> integer_list = abjad.TypedList(item_class=int)
            >>> integer_list.extend(['1', 2, 4.3])
            >>> integer_list
            TypedList(items=[1, 2, 4], item_class=<class 'int'>, keep_sorted=False)

            >>> integer_list.insert(0, '0')
            >>> integer_list
            TypedList(items=[0, 1, 2, 4], item_class=<class 'int'>, keep_sorted=False)

            >>> integer_list.insert(1, '9')
            >>> integer_list
            TypedList(items=[0, 9, 1, 2, 4], item_class=<class 'int'>, keep_sorted=False)

        Returns none.
        """
        item = self._coerce_item(item)
        self._on_insertion(item)
        result = self.items.insert(i, item)
        if self.keep_sorted:
            self.sort()
        return result

    def pop(self, i=-1):
        """
        Pops item ``i`` from typed list.

        Returns item.
        """
        result = self.items.pop(i)
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
        index = self.items.index(item)
        item = self.items[index]
        self._on_removal(item)
        del self.items[index]
        if self.keep_sorted:
            self.sort()

    def reverse(self):
        """
        Reverses items in typed list.
        """
        self.items.reverse()

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
        self.items.sort(key=key, reverse=reverse)


@dataclasses.dataclass(slots=True, unsafe_hash=True)
class TypedTuple(TypedCollection, collections.abc.Sequence):
    """
    Typed tuple.
    """

    def __post_init__(self):
        TypedCollection.__post_init__(self)
        self.items = self.items or []
        self.items = tuple(self._coerce_item(item) for item in self.items)

    def __add__(self, argument):
        """
        Adds typed tuple to ``argument``.

        Returns new typed tuple.
        """
        if isinstance(argument, type(self)):
            items = argument.items
            return dataclasses.replace(self, items=self.items[:] + items)
        elif isinstance(argument, type(self.items)):
            items = argument[:]
            return dataclasses.replace(self, items=self.items[:] + items)
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
        return self.items.__contains__(item)

    def __getitem__(self, argument):
        """
        Gets item or slice identified by ``argument``.

        Returns item or new typed tuple.
        """
        item = self.items.__getitem__(argument)
        try:
            return type(self)(item)
        except TypeError:
            return item

    def __mul__(self, argument):
        """
        Multiplies typed tuple by ``argument``.

        Returns new typed tuple.
        """
        items = self.items * argument
        return dataclasses.replace(self, items=items)

    def __radd__(self, argument):
        """
        Right-adds ``argument`` to typed tuple.
        """
        items = argument + self.items
        return dataclasses.replace(self, items=items)

    def __rmul__(self, argument):
        """
        Multiplies ``argument`` by typed tuple.

        Returns new typed tuple.
        """
        return self.__mul__(argument)

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
        return self.items.count(item)

    def index(self, item):
        """
        Gets index of ``item`` in collection.

        Coerces ``item``.

        Returns nonnegative integer.
        """
        item = self._coerce_item(item)
        return self.items.index(item)
