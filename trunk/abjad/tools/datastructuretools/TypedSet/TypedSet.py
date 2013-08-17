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

    ### SPECIAL METHODS ###

    '''
    __and__
    __contains__
    __ge__
    __gt__
    __iand__
    __ior__
    __isub__
    __ixor__
    __le__
    __lt__
    __ne__
    __or__
    __sub__
    __xor__
    '''

    ### PUBLIC METHODS ###

    '''
    add
    clear
    copy
    difference
    difference_update
    discard
    intersection
    intersection_update
    isdisjoint
    issubset
    issuperset
    pop
    remove
    symmetric_difference
    symmetric_difference_update
    union
    update
    '''
