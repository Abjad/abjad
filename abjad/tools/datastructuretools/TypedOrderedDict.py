# -*- encoding: utf-8 -*-
import collections
from abjad.tools.datastructuretools.TypedCollection import TypedCollection
from abjad.tools.topleveltools import new


class TypedOrderedDict(TypedCollection):
    r'''A typed ordered dictionary.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(self, tokens=None, item_class=None):
        TypedCollection.__init__(
            self,
            item_class=item_class,
            tokens=tokens,
            )
        tokens = tokens or []
        tokens = [self._item_callable(_) for _ in tokens]
        self._collection = collections.OrderedDict(tokens)



# TODO: how to declare inheritance?
#collections.OrderedDict.register(TypedOrderedDict)
