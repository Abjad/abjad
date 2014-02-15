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

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(
        self, 
        tokens=None, 
        item_class=None, 
        ):
        from abjad.tools import datastructuretools
        from abjad.tools import pitchtools 
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
        TypedTuple.__init__(
            self,
            tokens=tokens,
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
            tokens = [str(x) for x in self]
        elif hasattr(self.item_class, 'pitch_number'):
            tokens = [x.pitch_number for x in self]
        elif hasattr(self.item_class, 'pitch_class_number'):
            tokens = [x.pitch_class_number for x in self]
        elif hasattr(self.item_class, '__abs__'):
            tokens = [abs(x) for x in self]
        else:
            raise ValueError
        return new(
            self._storage_format_specification,
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
