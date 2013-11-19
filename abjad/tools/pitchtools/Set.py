# -*- encoding: utf-8 -*-
import abc
import collections
import types
from abjad.tools import datastructuretools
from abjad.tools.datastructuretools import TypedFrozenset


class Set(TypedFrozenset):
    '''Music-theoretic set base class.
    '''

    ### CLASS METHODS ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self, tokens=None, item_class=None, custom_identifier=None):
        if isinstance(tokens, str):
            tokens = tokens.split()
        elif isinstance(tokens, (
            collections.Iterator,
            types.GeneratorType,
            )):
            tokens = [token for token in tokens]
        if item_class is None:
            item_class = self._named_item_class
            if tokens is not None:
                if isinstance(tokens, datastructuretools.TypedCollection) and \
                    issubclass(tokens.item_class, self._parent_item_class):
                    item_class = tokens.item_class
                elif len(tokens):
                    if isinstance(tokens, collections.Set):
                        tokens = tuple(tokens)
                    if isinstance(tokens[0], str):
                        item_class = self._named_item_class
                    elif isinstance(tokens[0], (int, float)):
                        item_class = self._numbered_item_class
                    elif isinstance(tokens[0], self._parent_item_class):
                        item_class = type(tokens[0])
        assert issubclass(item_class, self._parent_item_class)
        TypedFrozenset.__init__(
            self,
            tokens=tokens,
            item_class=item_class,
            custom_identifier=custom_identifier,
            )

    ### SPECIAL METHODS ###

    def __str__(self):
        parts = [str(x) for x in self]
        return '<{}>'.format(', '.join(parts))

    ### PRIVATE METHODS ###

    def _sort_self(self):
        return tuple(self)

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
        tokens = []
        if self.item_class.__name__.startswith('Named'):
            tokens = [str(x) for x in sorted(self)]
        else:
            tokens = sorted([abs(x) for x in self])
        return self._storage_format_specification.new(
            is_indented=False,
            keyword_argument_names=(),
            positional_argument_values=(
                tokens,
                ),
            )

    ### PUBLIC METHODS ###

    @abc.abstractmethod
    def from_selection(cls, selection, item_class=None, custom_identifier=None):
        raise NotImplementedError
