# -*- encoding: utf-8 -*-
import abc
import collections
import types
from abjad.tools import datastructuretools
from abjad.tools.datastructuretools import TypedFrozenset
from abjad.tools.topleveltools import new


class Set(TypedFrozenset):
    '''Music-theoretic set base class.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    #def __init__(self, tokens=None, item_class=None, custom_identifier=None):
    def __init__(self, tokens=None, item_class=None):
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
#            custom_identifier=custom_identifier,
            )

    ### SPECIAL METHODS ###

    def __str__(self):
        r'''String representation of set.

        Returns string.
        '''
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
        elif hasattr(self.item_class, 'pitch_number'):
            tokens = sorted([x.pitch_number for x in self])
        elif hasattr(self.item_class, 'pitch_class_number'):
            tokens = sorted([x.pitch_class_number for x in self])
        elif hasattr(self.item_class, '__abs__'):
            tokens = sorted([abs(x) for x in self])
        else:
            raise ValueError
        positional_argument_values=(
            tokens,
            )
        return new(
            self._storage_format_specification,
            is_indented=False,
            keyword_argument_names=(),
            positional_argument_values=positional_argument_values,
            )

    ### PUBLIC METHODS ###

    @abc.abstractmethod
    def from_selection(
        cls, 
        selection, 
        item_class=None, 
#        custom_identifier=None,
        ):
        r'''Makes set from `selection`.

        Returns set.
        '''
        raise NotImplementedError
