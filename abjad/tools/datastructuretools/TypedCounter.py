# -*- encoding: utf-8 -*-
import collections
from abjad.tools.datastructuretools.TypedCollection import TypedCollection


class TypedCounter(TypedCollection):
    r'''A typed counter.

    ::

        >>> counter = datastructuretools.TypedCounter(
        ...     [0, "c'", 1, True, "cs'", "df'"],
        ...     item_class=pitchtools.NumberedPitch,
        ...     )

    ::

        >>> print format(counter)
        datastructuretools.TypedCounter(
            {
                pitchtools.NumberedPitch(0): 2,
                pitchtools.NumberedPitch(1): 4,
                },
            item_class=pitchtools.NumberedPitch,
            )

    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(
        self, 
        tokens=None, 
        item_class=None, 
        custom_identifier=None, 
        **kwargs
        ):
        TypedCollection.__init__(
            self,
            item_class=item_class,
            custom_identifier=custom_identifier,
            tokens=tokens,
            )
        self._collection = collections.Counter()
        self.update(tokens, **kwargs)

    ### SPECIAL METHODS ###

    '''
    __cmp__
    __ge__
    __getattribute__
    __gt__
    __hash__
    __le__
    __lt__
    '''

    def __add__(self, expr):
        r'''Adds typed counter to `expr`.

        Returns new typed counter.
        '''
        if not isinstance(expr, type(self)) \
            or not self.item_class == expr.item_class:
            return NotImplemented
        result = type(self)()
        result._collection = self._collection + expr._collection
        return result

    def __and__(self, expr):
        r'''Logical AND of typed counter and `expr`.

        Returns new typed counter.
        '''
        if not isinstance(expr, type(self)) \
            or not self.item_class == expr.item_class:
            return NotImplemented
        result = type(self)()
        result._collection = self._collection & expr._collection
        return result

    def __delitem__(self, token):
        r'''Deletes `token` from typed counter.

        Returns none.
        '''
        item = self._item_callable(token)
        if item in self._collection:
            dict.__delitem__(self._collection, item)

    def __getitem__(self, token):
        r'''Gets `token` from typed counter.

        Returns item.
        '''
        item = self._item_callable(token)
        return self._collection[item]

    def __missing__(self, token):
        r'''Returns zero.

        Returns zero.
        '''
        return 0

    def __or__(self, expr):
        r'''Logical OR of typed counter and `expr`.

        Returns new typed counter.
        '''
        if not isinstance(expr, type(self)) \
            or not self.item_class == expr.item_class:
            return NotImplemented
        result = type(self)()
        result._collection = self._collection | expr._collection
        return result

    def __reduce__(self):
        r'''Reduces typed counter.

        Returns new typed counter.
        '''
        return type(self), (dict(self._collection),)

    def __setitem__(self, token, value):
        r'''Sets typed counter `token` to `value`.

        Returns none.
        '''
        item = self._item_callable(token)
        self._collection.__setitem__(item, value)

    def __sub__(self, expr):
        r'''Subtracts `expr` from typed counter.

        Returns new typed counter.
        '''
        if not isinstance(expr, type(self)) \
            or not self.item_class == expr.item_class:
            return NotImplemented
        result = type(self)()
        result._collection = self._collection - expr._collection
        return result

    ### PRIVATE METHODS ###

    def _coerce_arguments(self, tokens=None, **kwargs):
        def _coerce_mapping(tokens):
            items = {}
            for token, count in tokens.iteritems():
                item = self._item_callable(token)
                if item not in items:
                    items[item] = 0
                items[item] += count
            return items
        items = []
        if tokens is not None:
            if isinstance(tokens, collections.Mapping):
                items = _coerce_mapping(tokens)
            else:
                items = []
                for token in tokens:
                    items.append(self._item_callable(token))
        itemdict = _coerce_mapping(kwargs)
        return items, itemdict

    ### PUBLIC METHODS ###

    '''
    get
    has_key
    pop
    popitem
    setdefault
    '''

    def clear(self):
        r'''Clears typed counter.

        Returns none.
        '''
        self._collection.clear()

    def copy(self):
        r'''Copies typed counter.

        Returns new typed counter.
        '''
        return type(self)(self)

    def elements(self):
        r'''Elements in typed counter.
        '''
        return self._collection.elements()

    @classmethod
    def fromkeys(cls, iterable, v=None):
        r'''Makes new typed counter from `iterable`.

        Not yet impelemented.

        Will return new typed counter.
        '''
        message = '{}.fromkeys() is undefined. Use {}(iterable) instead.'
        message = message.format(cls.__name__, cls.__name__)
        raise NotImplementedError(message)

    def items(self):
        r'''Items in typed counter.

        Returns tuple.
        '''
        return self._collection.items()

    def iteritems(self):
        r'''Iterates items in typed counter.
        
        Yields items.
        '''
        return self._collection.iteritems()

    def iterkeys(self):
        r'''Iterates keys in typed counter.
        '''
        return self._collection.iterkeys()

    def itervalues(self):
        r'''Iterates values in typed counter.
        '''
        return self._collection.itervalues()

    def keys(self):
        r'''Keys in typed counter.
        '''
        return self._collection.keys()

    def most_common(self, n=None):
        r'''Please document.
        '''
        return self._collection(n=n)

    def subtract(self, iterable=None, **kwargs):
        r'''Stracts `iterable` from typed counter.
        '''
        items, itemdict = self._coerce_arguments(iterable, **kwargs)
        self._collection.subtract(items, **itemdict)

    def update(self, iterable=None, **kwargs):
        r'''Updates typed counter with `iterable`.
        '''
        items, itemdict = self._coerce_arguments(iterable, **kwargs)
        self._collection.update(items, **itemdict)

    def values(self):
        r'''Values of typed counter.
        '''
        return self._collection.values()

    def viewitems(self):
        r'''Please document.
        '''
        return self._collection.viewitems()

    def viewkeys(self):
        r'''Please document.
        '''
        return self._collection.viewkeys()

    def viewvalues(self):
        r'''Please document.
        '''
        return self._collection.viewvalues()


collections.MutableMapping.register(TypedCounter)
