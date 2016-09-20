# -*- coding: utf-8 -*-
import abc
import collections
import types
from abjad.tools import datastructuretools
from abjad.tools import systemtools
from abjad.tools.datastructuretools import TypedFrozenset


class Set(TypedFrozenset):
    '''Set base class.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(self, items=None, item_class=None):
        if isinstance(items, str):
            items = items.split()
        elif isinstance(items, (
            collections.Iterator,
            types.GeneratorType,
            )):
            items = [item for item in items]
        if item_class is None:
            item_class = self._named_item_class
            if items is not None:
                if isinstance(items, datastructuretools.TypedCollection) and \
                    issubclass(items.item_class, self._parent_item_class):
                    item_class = items.item_class
                elif len(items):
                    if isinstance(items, collections.Set):
                        items = tuple(items)
                    if isinstance(items[0], str):
                        item_class = self._named_item_class
                    elif isinstance(items[0], (int, float)):
                        item_class = self._numbered_item_class
                    elif isinstance(items[0], self._parent_item_class):
                        item_class = type(items[0])
        assert issubclass(item_class, self._parent_item_class)
        TypedFrozenset.__init__(
            self,
            items=items,
            item_class=item_class,
            )

    ### SPECIAL METHODS ###

    def __str__(self):
        r'''String representation of set.

        Returns string.
        '''
        parts = [str(x) for x in self]
        return '<{}>'.format(', '.join(parts))

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        items = sorted(self, key=lambda x: (float(x), str(x)))
        if self.item_class.__name__.startswith('Named'):
            repr_items = [str(x) for x in items]
        elif hasattr(self.item_class, 'pitch_number'):
            repr_items = [x.pitch_number for x in items]
        elif hasattr(self.item_class, 'pitch_class_number'):
            repr_items = [x.pitch_class_number for x in items]
        elif hasattr(self.item_class, '__abs__'):
            repr_items = [abs(x) for x in items]
        else:
            raise ValueError
        return systemtools.FormatSpecification(
            client=self,
            repr_is_indented=False,
            repr_args_values=[repr_items],
            storage_format_args_values=[repr_items],
            storage_format_kwargs_names=[],
            )

    def _sort_self(self):
        return tuple(self)

    ### PUBLIC METHODS ###

    @abc.abstractmethod
    def from_selection(
        class_,
        selection,
        item_class=None,
        ):
        r'''Makes set from `selection`.

        Returns set.
        '''
        raise NotImplementedError

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
