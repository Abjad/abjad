# -*- encoding: utf-8 -*-
import collections
from abjad.tools.datastructuretools.TypedCollection import TypedCollection


class TypedCounter(TypedCollection):

    ### CLASS VARIABLES ### 

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self, tokens=None, item_class=None, name=None, **kwargs):
        TypedCollection.__init__(self, 
            item_class=item_class, 
            name=name,
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
    __setitem__
    '''

    def __add__(self, expr):
        if not isinstance(expr, type(self)) \
            or not self.item_class == expr.item_class:
            return NotImplemented
        result = type(self)()
        result._collection = self._collection + expr._collection
        return result

    def __and__(self, expr):
        if not isinstance(expr, type(self)) \
            or not self.item_class == expr.item_class:
            return NotImplemented
        result = type(self)()
        result._collection = self._collection & expr._collection
        return result

    def __delitem__(self, token):
        item = self._item_callable(token)
        if item in self._collection:
            dict.__delitem__(self._collection, item)

    def __getitem__(self, token):
        item = self._item_callable(token)
        return self._collection[item]

    def __missing__(self, token):
        return 0

    def __or__(self, expr):
        if not isinstance(expr, type(self)) \
            or not self.item_class == expr.item_class:
            return NotImplemented
        result = type(self)()
        result._collection = self._collection | expr._collection
        return result

    def __reduce__(self):
        return self.__class__, (dict(self._collection),)

    def __setitem__(self, token, value):
        item = self._item_callable(token)
        self._collection.__setitem__(item, value)

    def __sub__(self, expr):
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
        self._collection.clear()

    def copy(self):
        return self.__class__(self)

    def elements(self):
            return self._collection.elements()

    @classmethod
    def fromkeys(cls, iterable, v=None):
        message = '{}.fromkeys() is undefined. Use {}(iterable) instead.'
        message = message.format(cls.__name__, cls.__name__)
        raise NotImplementedError(message)

    def items(self):
        return self._collection.items()

    def iteritems(self):
        return self._collection.iteritems()

    def iterkeys(self):
        return self._collection.iterkeys()

    def itervalues(self):
        return self._collection.itervalues()

    def keys(self):
        return self._collection.keys()

    def most_common(self, n=None):
        return self._collection(n=n)

    def subtract(self, iterable=None, **kwargs):
        items, itemdict = self._coerce_arguments(iterable, **kwargs)
        self._collection.subtract(items, **itemdict)

    def update(self, iterable=None, **kwargs):
        items, itemdict = self._coerce_arguments(iterable, **kwargs)
        self._collection.update(items, **itemdict)

    def values(self):
        return self._collection.values()

    def viewitems(self):
        return self._collection.viewitems()

    def viewkeys(self):
        return self._collection.viewkeys()

    def viewvalues(self):
        return self._collection.viewvalues()


collections.MutableMapping.register(TypedCounter)
