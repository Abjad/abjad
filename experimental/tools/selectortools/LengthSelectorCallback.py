# -*- encoding: utf-8 -*-
from abjad.tools.abctools import AbjadObject


class LengthSelectorCallback(AbjadObject):
    r'''A length selector callback.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_length',
        '_parts',
        )

    ### INITIALIZER ###

    def __init__(self, length=1, parts=Exact):
        assert isinstance(length, int) and length
        self._length = length
        assert parts in (None, Exact, More, Less)
        self._parts = parts

    ### SPECIAL METHODS ###

    def __call__(self, expr):
        result = []
        for subexpr in expr:
            if self.parts in (None, Exact):
                if len(subexpr) == self.length:
                    result.append(subexpr)
            elif self.parts == More:
                if self.length <= len(subexpr):
                    result.append(subexpr)
            elif self.parts == Less:
                if len(subexpr) <= self.length:
                    result.append(subexpr)
        return tuple(result)

    ### PUBLIC PROPERTIES ###

    @property
    def length(self):
        r'''Gets length selector callback length.

        Returns length.
        '''
        return self._length

    @property
    def parts(self):
        r'''Gets length selector callback partial-result handling.

        Returns ordinal constant.
        '''
        return self._parts
