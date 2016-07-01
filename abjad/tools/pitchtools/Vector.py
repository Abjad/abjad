# -*- coding: utf-8 -*-
import abc
import collections
import types
from abjad.tools import datastructuretools
from abjad.tools.datastructuretools import TypedCounter
from abjad.tools.topleveltools import new


class Vector(TypedCounter):
    '''Vector base class.
    '''

    ### CLASS VARIABLES ##

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(self, items=None, item_class=None):
        from abjad.tools import datastructuretools
        from abjad.tools import pitchtools
        prototype_1 = (collections.Iterator, types.GeneratorType)
        prototype_2 = (TypedCounter, collections.Counter)
        if isinstance(items, str):
            items = items.split()
        elif isinstance(items, prototype_1):
            items = [item for item in items]
        elif isinstance(items, dict):
            items = self._dictionary_to_items(items, item_class)
        if isinstance(items, prototype_2):
            new_tokens = []
            for item, count in items.items():
                new_tokens.extend(count * [item])
            items = new_tokens
        if item_class is None:
            item_class = self._named_item_class
            if items is not None:
                if (isinstance(items, datastructuretools.TypedCollection) and
                    issubclass(items.item_class, self._parent_item_class)):
                    item_class = items.item_class
                elif len(items):
                    if isinstance(items, collections.Set):
                        items = tuple(items)
                    if isinstance(items, dict):
                        item_class = self._dictionary_to_item_class(items)
                    elif isinstance(items[0], str):
                        item_class = self._named_item_class
                    elif isinstance(items[0], (int, float)):
                        item_class = self._numbered_item_class
                    elif isinstance(items[0], self._parent_item_class):
                        item_class = type(items[0])
        assert issubclass(item_class, self._parent_item_class)
        TypedCounter.__init__(
            self,
            items=items,
            item_class=item_class,
            )

    ### SPECIAL METHODS ###

    def __str__(self):
        r'''String representation of vector.

        Returns string.
        '''
        parts = ['{}: {}'.format(key, value)
            for key, value in self.items()]
        return '<{}>'.format(', '.join(parts))

    ### PRIVATE PROPERTIES ###

    @abc.abstractproperty
    def _named_item_class(self):
        raise NotImplementedError

    @abc.abstractproperty
    def _numbered_item_class(self):
        raise NotImplementedError

    @abc.abstractproperty
    def _parent_item_class(self):
        raise NotImplementedError

    @property
    def _repr_specification(self):
        items = {}
        for key, value in self.items():
            items[str(key)] = value
        keyword_argument_names = (
            'item_class',
            )
        positional_argument_values = (
            items,
            )
        return new(
            self._storage_format_specification,
            is_indented=False,
            keyword_argument_names=keyword_argument_names,
            positional_argument_values=positional_argument_values,
            )

    ### PRIVATE METHODS ###

    def _dictionary_to_item_class(self, dictionary):
        if not len(dictionary):
            return self._named_item_class
        keys = dictionary.keys()
        first_key = keys[0]
        assert isinstance(first_key, str), repr(first_key)
        try:
            float(first_key)
            item_class = self._numbered_item_class
        except ValueError:
            item_class = self._named_item_class
        return item_class

    def _dictionary_to_items(self, dictionary, item_class):
        items = []
        for initializer_token, count in dictionary.items():
            for _ in range(count):
                item = item_class(initializer_token)
                items.append(item)
        return items

    ### PUBLIC METHODS ###

    @abc.abstractmethod
    def from_selection(
        class_,
        selection,
        item_class=None,
        ):
        r'''Makes vector from `selection`.

        Returns vector.
        '''
        raise NotImplementedError
