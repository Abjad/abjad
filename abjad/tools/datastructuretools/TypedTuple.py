# -*- coding: utf-8 -*-
import collections
from abjad.tools.datastructuretools.TypedCollection import TypedCollection
from abjad.tools.topleveltools import new


class TypedTuple(TypedCollection):
    r'''Typed tuple.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(
        self,
        items=None,
        item_class=None,
        ):
        TypedCollection.__init__(
            self,
            item_class=item_class,
            items=items,
            )
        items = items or []
        self._collection = tuple(
            self._item_coercer(item) for item in items)

    ### SPECIAL METHODS ###

    def __add__(self, argument):
        r'''Adds typed tuple to `argument`.

        Returns new typed tuple.
        '''
        if isinstance(argument, type(self)):
            items = argument._collection
            return new(self, items=self._collection[:] + items)
        elif isinstance(argument, type(self._collection)):
            items = argument[:]
            return new(self, items=self._collection[:] + items)
        raise NotImplementedError

    def __contains__(self, item):
        r'''Is true if typed tuple contains `item`.

        Coerces `item`.

        Returns none.
        '''
        try:
            item = self._item_coercer(item)
        except ValueError:
            return False
        return self._collection.__contains__(item)

    def __getitem__(self, argument):
        '''Gets item or slice identified by `argument`.

        Returns item or new typed tuple.
        '''
        item = self._collection.__getitem__(argument)
        try:
            return type(self)(item)
        except TypeError:
            return item

    def __hash__(self):
        r'''Hashes typed tuple.

        Returns integer.
        '''
        return super(TypedTuple, self).__hash__()

    def __mul__(self, argument):
        r'''Multiplies typed tuple by `argument`.

        Returns new typed tuple.
        '''
        items = self._collection * argument
        return new(self, items=items)

    def __radd__(self, argument):
        r'''Right-adds `argument` to typed tuple.
        '''
        items = argument + self._collection
        return new(self, items=items)

    def __rmul__(self, argument):
        r'''Multiplies `argument` by typed tuple.

        Returns new typed tuple.
        '''
        return self.__mul__(argument)

    ### PUBLIC METHODS ###

    def count(self, item):
        r'''Counts `item` in collection.

        Coerces `item`.

        Returns nonnegative integer.
        '''
        try:
            item = self._item_coercer(item)
        except TypeError:
            return 0
        return self._collection.count(item)

    def index(self, item):
        r'''Gets index of `item` in collection.

        Coerces `item`.

        Returns nonnegative integer.
        '''
        item = self._item_coercer(item)
        return self._collection.index(item)


collections.Sequence.register(TypedTuple)
