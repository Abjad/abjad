# -*- encoding: utf-8 -*-
import abc
import collections
import types
from abjad.tools import datastructuretools
from abjad.tools.datastructuretools import TypedCounter


class Vector(TypedCounter):
    '''Music-theoretic vector base class.
    '''

    ### CLASS VARIABLES ##

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(self, tokens=None, item_class=None, custom_identifier=None):
        from abjad.tools import datastructuretools
        from abjad.tools import pitchtools
        if isinstance(tokens, str):
            tokens = tokens.split()
        elif isinstance(tokens, (
            collections.Iterator,
            types.GeneratorType,
            )):
            tokens = [token for token in tokens]
        if isinstance(tokens, (TypedCounter, collections.Counter)):
            new_tokens = []
            for token, count in tokens.iteritems():
                new_tokens.extend([token] * count)
            tokens = new_tokens
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
        TypedCounter.__init__(
            self,
            tokens=tokens,
            item_class=item_class,
            custom_identifier=custom_identifier,
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
        tokens = {}
        for key, value in self:
            tokens[str(key)] = value
        return self._storage_format_specification.__makenew__(
            is_indented=False,
            keyword_argument_names=(),
            positional_argument_values=(
                tokens,
                ),
            )

    ### PUBLIC METHODS ###

    @abc.abstractmethod
    def from_selection(
        cls, 
        selection, 
        item_class=None, 
        custom_identifier=None,
        ):
        r'''Makes vector from `selection`.

        Returns vector.
        '''
        raise NotImplementedError
