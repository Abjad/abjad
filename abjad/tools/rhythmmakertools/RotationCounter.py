# -*- encoding: utf-8 -*-
from abjad.tools.datastructuretools.TypedCounter import TypedCounter


class RotationCounter(TypedCounter):
    r'''A rotation counter.
    
    ::

        >>> counter = rhythmmakertools.RotationCounter(default=3)

    ::

        >>> counter['talea__counts']
        3

    ::

        >>> counter['talea__counts'] += 1
        >>> counter['talea__counts']
        4

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_autoincrement',
        '_default',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        autoincrement=None,
        default=None,
        items=None,
        **kwargs
        ):
        TypedCounter.__init__(
            self,
            items=items,
            **kwargs
            )
        if autoincrement is not None:
            autoincrement = bool(autoincrement)
        self._autoincrement = autoincrement
        default = default or 0
        self._default = int(default)

    ### SPECIAL METHODS ###

    def __getitem__(self, item):
        r'''Gets `item` from rotation counter.

        Returns item.
        '''
        item = self._item_coercer(item)
        if item not in self._collection:
            self._collection[item] = self._default
        return self._collection[item]

    ### PUBLIC PROPERTIES ###

    @property
    def autoincrement(self):
        r'''Is true if rotation counter should be auto-incremented.
        Otherwise false.

        Returns boolean.
        '''
        return self._autoincrement

    @property
    def default(self):
        r'''Gets default count.

        Returns integer.
        '''
        return self._default