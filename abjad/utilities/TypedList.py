import collections
from .TypedCollection import TypedCollection


class TypedList(TypedCollection, collections.MutableSequence):
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

        >>> abjad.f(list_)
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

        >>> abjad.f(pitch_list)
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

    __slots__ = (
        '_keep_sorted',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        items=None,
        item_class=None,
        keep_sorted=False,
        ):
        TypedCollection.__init__(
            self,
            item_class=item_class,
            items=items,
            )
        self._collection = []
        if keep_sorted is not None:
            assert isinstance(keep_sorted, bool), repr(keep_sorted)
        self._keep_sorted = keep_sorted
        items = items or []
        the_items = []
        for item in items:
            the_items.append(self._item_coercer(item))
        self.extend(the_items)

    ### SPECIAL METHODS ###

    def __delitem__(self, i):
        """
        Aliases list.__delitem__().

        Returns none.
        """
        self._on_removal(self._collection[i])
        del(self._collection[i])

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

            >>> abjad.f(dynamic_list)
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
            >>> abjad.f(pitch_list)
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
            >>> abjad.f(pitch_list)
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
            new_item = self._item_coercer(argument)
            old_item = self._collection[i]
            self._on_removal(old_item)
            self._on_insertion(new_item)
            self._collection[i] = new_item
        elif isinstance(i, slice):
            new_items = [self._item_coercer(item) for item in argument]
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
        import abjad
        agent = abjad.StorageFormatManager(self)
        names = list(agent.signature_keyword_names)
        if 'items' in names:
            names.remove('items')
        if 'keep_sorted' in names:
            names.remove('keep_sorted')
        return abjad.FormatSpecification(
            self,
            repr_is_indented=False,
            storage_format_args_values=[self._collection],
            storage_format_kwargs_names=names,
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
        item = self._item_coercer(item)
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
        item = self._item_coercer(item)
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
        item = self._item_coercer(item)
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
        item = self._item_coercer(item)
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
        item = self._item_coercer(item)
        index = self._collection.index(item)
        item = self._collection[index]
        self._on_removal(item)
        del(self._collection[index])
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
                class CmpToKey(object):

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
