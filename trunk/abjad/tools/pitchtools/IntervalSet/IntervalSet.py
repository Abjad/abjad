# -*- encoding: utf-8 -*-
from abjad.tools.datastructuretools import TypedFrozenset


class IntervalSet(TypedFrozenset):
    r'''Abjad model of an interval set.
    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self, tokens=None, item_class=None, name=None):
        from abjad.tools import pitchtools 
        if isinstance(tokens, str):
            tokens = tokens.split()
        if item_class is None and tokens is not None:
            if isinstance(tokens, type(self)):
                item_class = tokens.item_class
            elif len(tokens):
                if isinstance(tokens[0], str):
                    item_class = pitchtools.NamedInterval 
                elif isinstance(tokens[0], (int, float)):
                    item_class = pitchtools.NumberedInterval
        elif item_class is None:
            item_class = pitchtools.NamedInterval
        assert issubclass(item_class, pitchtools.Interval)
        TypedFrozenset.__init__(
            self,
            tokens=tokens,
            item_class=item_class,
            )
