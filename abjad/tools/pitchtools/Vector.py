# -*- encoding: utf-8 -*-
import abc
import collections
import types
from abjad.tools import datastructuretools
from abjad.tools.datastructuretools import TypedCounter
from abjad.tools.topleveltools import new


class Vector(TypedCounter):
    '''Music-theoretic vector base class.
    '''

    ### CLASS VARIABLES ##

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(self, items=None, item_class=None):
        from abjad.tools import datastructuretools
        from abjad.tools import pitchtools
        if isinstance(items, str):
            items = items.split()
        elif isinstance(items, (
            collections.Iterator,
            types.GeneratorType,
            )):
            items = [item for item in items]
        if isinstance(items, (TypedCounter, collections.Counter)):
            new_tokens = []
            for item, count in items.iteritems():
                new_tokens.extend(count * [item])
            items = new_tokens
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
            for key, value in self.iteritems()]
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
        for key, value in self:
            items[str(key)] = value
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
        r'''Makes vector from `selection`.

        Returns vector.
        '''
        raise NotImplementedError
