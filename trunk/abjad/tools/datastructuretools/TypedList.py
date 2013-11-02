# -*- encoding: utf-8 -*-
import collections
from abjad.tools.datastructuretools.TypedCollection import TypedCollection


class TypedList(TypedCollection):
    '''Ordered collection of objects, which optionally coerces its contents
    to the same type:

    ::

        >>> object_collection = datastructuretools.TypedList()
        >>> object_collection.append(23)
        >>> object_collection.append('foo')
        >>> object_collection.append(False)
        >>> object_collection.append((1, 2, 3))
        >>> object_collection.append(3.14159)

    ::

        >>> print object_collection.storage_format
        datastructuretools.TypedList([
            23,
            'foo',
            False,
            (1, 2, 3),
            3.14159,
            ])

    ::

        >>> pitch_collection = datastructuretools.TypedList(
        ...     item_class=pitchtools.NamedPitch)
        >>> pitch_collection.append(0)
        >>> pitch_collection.append("d'")
        >>> pitch_collection.append(('e', 4))
        >>> pitch_collection.append(pitchtools.NamedPitch("f'"))

    ::

        >>> print pitch_collection.storage_format
        datastructuretools.TypedList([
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
        '_collection',
        '_item_class',
        '_name',
        )

    ### INITIALIZER ###

    def __init__(self, tokens=None, item_class=None, name=None):
        TypedCollection.__init__(self, 
            item_class=item_class, 
            name=name,
            tokens=tokens,
            )
        self._collection = []
        if isinstance(tokens, type(self)):
            for token in tokens:
                self.append(self._item_callable(token))
        else:
            tokens = tokens or []
            items = []
            for token in tokens:
                items.append(self._item_callable(token))
            self.extend(items)

    ### SPECIAL METHODS ###

    def __delitem__(self, i):
        '''Aliases list.__delitem__().
        '''
        del(self._collection[i])

    def __getitem__(self, i):
        '''Aliases list.__getitem__().
        '''
        return self._collection[i]

    def __iadd__(self, expr):
        '''Change tokens in `expr` to items and extend:

        ::

            >>> dynamic_collection = datastructuretools.TypedList(
            ...     item_class=marktools.DynamicMark)
            >>> dynamic_collection.append('ppp')
            >>> dynamic_collection += ['p', 'mp', 'mf', 'fff']

        ::

            >>> print dynamic_collection.storage_format
            datastructuretools.TypedList([
                marktools.DynamicMark(
                    'ppp',
                    target_context=scoretools.Staff
                    ),
                marktools.DynamicMark(
                    'p',
                    target_context=scoretools.Staff
                    ),
                marktools.DynamicMark(
                    'mp',
                    target_context=scoretools.Staff
                    ),
                marktools.DynamicMark(
                    'mf',
                    target_context=scoretools.Staff
                    ),
                marktools.DynamicMark(
                    'fff',
                    target_context=scoretools.Staff
                    ),
                ],
                item_class=marktools.DynamicMark,
                )

        Returns collection.
        '''
        self.extend(expr)
        return self

    def __reversed__(self):
        '''Aliases list.__reversed__().
        '''
        return self._collection.__reversed__()

    def __setitem__(self, i, expr):
        '''Change tokens in `expr` to items and set:

        ::

            >>> pitch_collection[-1] = 'gqs,'
            >>> print pitch_collection.storage_format
            datastructuretools.TypedList([
                pitchtools.NamedPitch("c'"),
                pitchtools.NamedPitch("d'"),
                pitchtools.NamedPitch("e'"),
                pitchtools.NamedPitch('gqs,'),
                ],
                item_class=pitchtools.NamedPitch,
                )

        ::

            >>> pitch_collection[-1:] = ["f'", "g'", "a'", "b'", "c''"]
            >>> print pitch_collection.storage_format
            datastructuretools.TypedList([
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

        '''
        if isinstance(i, int):
            item = self._item_callable(expr)
            self._collection[i] = item
        elif isinstance(i, slice):
            items = [self._item_callable(token) for token in expr]
            self._collection[i] = items

    ### PUBLIC METHODS ###

    def append(self, token):
        r'''Change `token` to item and append:

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
        item = self._item_callable(token)
        self._collection.append(item)

    def count(self, token):
        r'''Change `token` to item and return count.

        ::

            >>> integer_collection = datastructuretools.TypedList(
            ...     tokens=[0, 0., '0', 99],
            ...     item_class=int)
            >>> integer_collection[:]
            [0, 0, 0, 99]

        ::

            >>> integer_collection.count(0)
            3

        Returns count.
        '''
        item = self._item_callable(token)
        return self._collection.count(item)

    def extend(self, tokens):
        r'''Change `tokens` to items and extend.

        ::

            >>> integer_collection = datastructuretools.TypedList(
            ...     item_class=int)
            >>> integer_collection.extend(('0', 1.0, 2, 3.14159))
            >>> integer_collection[:]
            [0, 1, 2, 3]

        Returns none.
        '''
        for token in tokens:
            self.append(token)

    def index(self, token):
        r'''Change `token` to item and return index.

        ::

            >>> pitch_collection = datastructuretools.TypedList(
            ...     tokens=('cqf', "as'", 'b,', 'dss'),
            ...     item_class=pitchtools.NamedPitch)
            >>> pitch_collection.index("as'")
            1

        Returns index.
        '''
        item = self._item_callable(token)
        return self._collection.index(item)

    def insert(self, i, token):
        r'''Change `token` to item and insert.

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
        item = self._item_callable(token)
        return self._collection.insert(i, item)

    def pop(self, i=-1):
        r'''Aliases list.pop().
        '''
        return self._collection.pop(i)

    def remove(self, token):
        r'''Change `token` to item and remove.

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
        item = self._item_callable(token)
        self._collection.remove(item)

    def reverse(self):
        r'''Aliases list.reverse().
        '''
        self._collection.reverse()

    def sort(self, cmp=None, key=None, reverse=False):
        r'''Aliases list.sort().
        '''
        self._collection.sort(cmp=cmp, key=key, reverse=reverse)


collections.MutableSequence.register(TypedList)
