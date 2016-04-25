# -*- coding: utf-8 -*-
import collections
from abjad.tools.datastructuretools.TypedCollection import TypedCollection
from abjad.tools.topleveltools.new import new


class TypedList(TypedCollection):
    r'''A typed list.

    Ordered collection of objects, which optionally coerces its contents
    to the same type:

    ::

        >>> object_collection = datastructuretools.TypedList()
        >>> object_collection.append(23)
        >>> object_collection.append('foo')
        >>> object_collection.append(False)
        >>> object_collection.append((1, 2, 3))
        >>> object_collection.append(3.14159)

    ::

        >>> print(format(object_collection))
        datastructuretools.TypedList(
            [
                23,
                'foo',
                False,
                (1, 2, 3),
                3.14159,
                ]
            )

    ::

        >>> pitch_collection = datastructuretools.TypedList(
        ...     item_class=NamedPitch)
        >>> pitch_collection.append(0)
        >>> pitch_collection.append("d'")
        >>> pitch_collection.append(('e', 4))
        >>> pitch_collection.append(NamedPitch("f'"))

    ::

        >>> print(format(pitch_collection))
        datastructuretools.TypedList(
            [
                pitchtools.NamedPitch("c'"),
                pitchtools.NamedPitch("d'"),
                pitchtools.NamedPitch("e'"),
                pitchtools.NamedPitch("f'"),
                ],
            item_class=pitchtools.NamedPitch,
            )

    Implements the list interface.
    '''

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
        assert isinstance(keep_sorted, bool), repr(keep_sorted)
        self._keep_sorted = keep_sorted
        items = items or []
        the_items = []
        for item in items:
            the_items.append(self._item_coercer(item))
        self.extend(the_items)

    ### SPECIAL METHODS ###

    def __delitem__(self, i):
        r'''Aliases list.__delitem__().

        Returns none.
        '''
        self._on_removal(self._collection[i])
        del(self._collection[i])

    def __getitem__(self, i):
        r'''Aliases list.__getitem__().

        Returns item.
        '''
        return self._collection[i]

    def __iadd__(self, expr):
        r'''Changes items in `expr` to items and extends.

        ::

            >>> dynamic_collection = datastructuretools.TypedList(
            ...     item_class=Dynamic)
            >>> dynamic_collection.append('ppp')
            >>> dynamic_collection += ['p', 'mp', 'mf', 'fff']

        ::

            >>> print(format(dynamic_collection))
            datastructuretools.TypedList(
                [
                    indicatortools.Dynamic(
                        name='ppp',
                        ),
                    indicatortools.Dynamic(
                        name='p',
                        ),
                    indicatortools.Dynamic(
                        name='mp',
                        ),
                    indicatortools.Dynamic(
                        name='mf',
                        ),
                    indicatortools.Dynamic(
                        name='fff',
                        ),
                    ],
                item_class=indicatortools.Dynamic,
                )

        Returns collection.
        '''
        self.extend(expr)
        return self

    def __reversed__(self):
        r'''Aliases list.__reversed__().

        Returns generator.
        '''
        return self._collection.__reversed__()

    def __setitem__(self, i, expr):
        r'''Changes items in `expr` to items and sets.

        ::

            >>> pitch_collection[-1] = 'gqs,'
            >>> print(format(pitch_collection))
            datastructuretools.TypedList(
                [
                    pitchtools.NamedPitch("c'"),
                    pitchtools.NamedPitch("d'"),
                    pitchtools.NamedPitch("e'"),
                    pitchtools.NamedPitch('gqs,'),
                    ],
                item_class=pitchtools.NamedPitch,
                )

        ::

            >>> pitch_collection[-1:] = ["f'", "g'", "a'", "b'", "c''"]
            >>> print(format(pitch_collection))
            datastructuretools.TypedList(
                [
                    pitchtools.NamedPitch("c'"),
                    pitchtools.NamedPitch("d'"),
                    pitchtools.NamedPitch("e'"),
                    pitchtools.NamedPitch("f'"),
                    pitchtools.NamedPitch("g'"),
                    pitchtools.NamedPitch("a'"),
                    pitchtools.NamedPitch("b'"),
                    pitchtools.NamedPitch("c''"),
                    ],
                item_class=pitchtools.NamedPitch,
                )

        Returns none.
        '''
        if isinstance(i, int):
            new_item = self._item_coercer(expr)
            old_item = self._collection[i]
            self._on_removal(old_item)
            self._on_insertion(new_item)
            self._collection[i] = new_item
        elif isinstance(i, slice):
            new_items = [self._item_coercer(item) for item in expr]
            old_items = self._collection[i]
            for old_item in old_items:
                self._on_removal(old_item)
            for new_item in new_items:
                self._on_insertion(new_item)
            self._collection[i] = new_items
        if self.keep_sorted:
            self.sort()

    ### PRIVATE PROPERTIES ###

    @property
    def _repr_specification(self):
        specification = self._storage_format_specification
        return new(
            specification,
            is_indented=False,
            )

    @property
    def _storage_format_specification(self):
        from abjad.tools import systemtools
        superclass = super(TypedList, self)
        specification = superclass._storage_format_specification
        keyword_argument_names = list(specification.keyword_argument_names)
        if (self.keep_sorted == False and
            'keep_sorted' in keyword_argument_names):
            keyword_argument_names.remove('keep_sorted')
        positional_argument_values = specification.positional_argument_values
        return systemtools.StorageFormatSpecification(
            self,
            keyword_argument_names=keyword_argument_names,
            positional_argument_values=positional_argument_values,
            )

    ### PUBLIC METHODS ###

    def append(self, item):
        r'''Changes `item` to item and appends.

        ::

            >>> integer_collection = datastructuretools.TypedList(
            ...     item_class=int)
            >>> integer_collection[:]
            []

        ::

            >>> integer_collection.append('1')
            >>> integer_collection.append(2)
            >>> integer_collection.append(3.4)
            >>> integer_collection[:]
            [1, 2, 3]

        Returns none.
        '''
        item = self._item_coercer(item)
        self._on_insertion(item)
        self._collection.append(item)
        if self.keep_sorted:
            self.sort()

    def count(self, item):
        r'''Changes `item` to item and returns count.

        ::

            >>> integer_collection = datastructuretools.TypedList(
            ...     items=[0, 0., '0', 99],
            ...     item_class=int)
            >>> integer_collection[:]
            [0, 0, 0, 99]

        ::

            >>> integer_collection.count(0)
            3

        Returns count.
        '''
        item = self._item_coercer(item)
        return self._collection.count(item)

    def extend(self, items):
        r'''Changes `items` to items and extends.

        ::

            >>> integer_collection = datastructuretools.TypedList(
            ...     item_class=int)
            >>> integer_collection.extend(('0', 1.0, 2, 3.14159))
            >>> integer_collection[:]
            [0, 1, 2, 3]

        Returns none.
        '''
        for item in items:
            self.append(item)
        if self.keep_sorted:
            self.sort()

    def index(self, item):
        r'''Changes `item` to item and returns index.

        ::

            >>> pitch_collection = datastructuretools.TypedList(
            ...     items=('cqf', "as'", 'b,', 'dss'),
            ...     item_class=NamedPitch)
            >>> pitch_collection.index("as'")
            1

        Returns index.
        '''
        item = self._item_coercer(item)
        return self._collection.index(item)

    def insert(self, i, item):
        r'''Changes `item` to item and inserts.

        ::

            >>> integer_collection = datastructuretools.TypedList(
            ...     item_class=int)
            >>> integer_collection.extend(('1', 2, 4.3))
            >>> integer_collection[:]
            [1, 2, 4]

        ::

            >>> integer_collection.insert(0, '0')
            >>> integer_collection[:]
            [0, 1, 2, 4]

        ::

            >>> integer_collection.insert(1, '9')
            >>> integer_collection[:]
            [0, 9, 1, 2, 4]

        Returns none.
        '''
        item = self._item_coercer(item)
        self._on_insertion(item)
        result = self._collection.insert(i, item)
        if self.keep_sorted:
            self.sort()
        return result

    def pop(self, i=-1):
        r'''Aliases list.pop().
        '''
        result = self._collection.pop(i)
        self._on_removal(result)
        if self.keep_sorted:
            self.sort()
        return result

    def remove(self, item):
        r'''Changes `item` to item and removes.

        ::

            >>> integer_collection = datastructuretools.TypedList(
            ...     item_class=int)
            >>> integer_collection.extend(('0', 1.0, 2, 3.14159))
            >>> integer_collection[:]
            [0, 1, 2, 3]

        ::

            >>> integer_collection.remove('1')
            >>> integer_collection[:]
            [0, 2, 3]

        Returns none.
        '''
        item = self._item_coercer(item)
        index = self._collection.index(item)
        item = self._collection[index]
        self._on_removal(item)
        del(self._collection[index])
        if self.keep_sorted:
            self.sort()

    def reverse(self):
        r'''Aliases list.reverse().
        '''
        self._collection.reverse()

    def sort(self, cmp=None, key=None, reverse=False):
        r'''Aliases list.sort().
        '''
        if cmp is not None:
            def cmp_to_key(comparator):
                r'''Convert a `cmp` function into a `key` function for use
                with `sort()`.
                '''
                class CmpToKey(object):

                    def __init__(self, object_):
                        self.object_ = object_

                    def __lt__(self, other):
                        return comparator(self.object_, other.object_) < 0

                    def __gt__(self, other):
                        return comparator(self.object_, other.object_) > 0

                    def __eq__(self, other):
                        return comparator(self.object_, other.object_) == 0

                    def __le__(self, other):
                        return comparator(self.object_, other.object_) <= 0

                    def __ge__(self, other):
                        return comparator(self.object_, other.object_) >= 0

                    def __ne__(self, other):
                        return comparator(self.object_, other.object_) != 0

                return CmpToKey
            key = cmp_to_key(cmp)
        self._collection.sort(key=key, reverse=reverse)

    ### PUBLIC PROPERTIES ###

    @property
    def keep_sorted(self):
        r'''Sorts collection on mutation if true.
        '''
        return self._keep_sorted

    @keep_sorted.setter
    def keep_sorted(self, expr):
        assert isinstance(expr, (bool, type(None)))
        self._keep_sorted = expr


collections.MutableSequence.register(TypedList)
