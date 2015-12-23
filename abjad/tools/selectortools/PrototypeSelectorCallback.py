# -*- coding: utf-8 -*-
import collections
from abjad.tools.abctools import AbjadValueObject
from abjad.tools.topleveltools import iterate
from abjad.tools.topleveltools import select


class PrototypeSelectorCallback(AbjadValueObject):
    r'''A prototype selector callback.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Callbacks'

    __slots__ = (
        '_flatten',
        '_prototype',
        )

    ### INITIALIZER ###

    def __init__(self, prototype=None, flatten=None):
        prototype = prototype or ()
        if isinstance(prototype, collections.Sequence):
            prototype = tuple(prototype)
            assert all(isinstance(x, type) for x in prototype)
        assert isinstance(prototype, (tuple, type))
        self._prototype = prototype
        if flatten is not None:
            flatten = bool(flatten)
        self._flatten = flatten

    ### SPECIAL METHODS ###

    def __call__(self, expr, start_offset=None):
        r'''Iterates tuple `expr`.

        Returns tuple of selections.
        '''
        assert isinstance(expr, tuple), repr(tuple)
        new_start_offset = start_offset
        result = []
        prototype = self.prototype
        if not isinstance(prototype, tuple):
            prototype = (prototype,)
        for subexpr in expr:
            subresult = iterate(subexpr).by_class(prototype)
            subresult = select(subresult)
            if subresult:
                if self.flatten:
                    result.extend(subresult)
                else:
                    result.append(subresult)
        # TODO: calculate new_start_offset in a non-naive way;
        #       this naive assignment will fail in some cases
        return tuple(result), new_start_offset

    ### PUBLIC PROPERTIES ###

    @property
    def flatten(self):
        r'''Is true if selector callback returns a single, rather than nested
        selection. Otherwise false.

        Returns true or false.
        '''
        return self._flatten

    @property
    def prototype(self):
        r'''Gets prototype selector callback prototype.

        Return tuple of classes.
        '''
        return self._prototype