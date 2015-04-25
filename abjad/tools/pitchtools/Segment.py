# -*- encoding: utf-8 -*-
import abc
import collections
import types
from abjad.tools.datastructuretools import TypedTuple
from abjad.tools.topleveltools import new


class Segment(TypedTuple):
    r'''Music-theoretic segment base class.
    '''

    ### CLASS VARIABLES ##

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(
        self,
        items=None,
        item_class=None,
        ):
        from abjad.tools import datastructuretools
        prototype = (
            collections.Iterator,
            types.GeneratorType,
            )
        if isinstance(items, str):
            items = items.split()
        elif isinstance(items, prototype):
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
        TypedTuple.__init__(
            self,
            items=items,
            item_class=item_class,
            )

    ### SPECIAL METHODS ###

    def __str__(self):
        r'''String representation of segment.

        Returns string.
        '''
        parts = [str(x) for x in self]
        return '<{}>'.format(', '.join(parts))

    ### PRIVATE PROPERTIES ###

    @property
    def _item_coercer(self):
        return self._item_class

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
        items = []
        if self.item_class.__name__.startswith('Named'):
            items = [str(x) for x in self]
        elif hasattr(self.item_class, 'pitch_number'):
            items = [x.pitch_number for x in self]
        elif hasattr(self.item_class, 'pitch_class_number'):
            items = [x.pitch_class_number for x in self]
        elif hasattr(self.item_class, '__abs__'):
            items = [abs(x) for x in self]
        else:
            raise ValueError
        return new(
            self._storage_format_specification,
            is_indented=False,
            keyword_argument_names=(),
            positional_argument_values=(
                items,
                ),
            )

    ### PUBLIC METHODS ###

    @abc.abstractmethod
    def from_selection(
        cls,
        selection,
        item_class=None,
        ):
        r'''Makes segment from `selection`.

        Returns new segment.
        '''
        raise NotImplementedError

    ### PUBLIC PROPERTIES ###

    @abc.abstractproperty
    def has_duplicates(self):
        r'''Is true when segment has duplicates. Otherwise false.

        Returns boolean.
        '''
        raise NotImplementedError