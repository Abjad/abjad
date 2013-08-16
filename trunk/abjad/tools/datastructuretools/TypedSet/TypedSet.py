# -*- encoding: utf-8 -*-
from abjad.tools.datastructuretools.TypedCollection import TypedCollection


class TypedSet(TypedCollection):

    ### CLASS VARIABLES ### 

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self, tokens=None, item_class=None, name=None):
        TypedCollection.__init__(self, 
            item_class=item_class, 
            name=name,
            tokens=tokens,
            )
        tokens = tokens or []
        self._collection = set(self._item_callable(token) 
            for token in tokens)

    ### PUBLIC METHODS ###


