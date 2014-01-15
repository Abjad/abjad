# -*- encoding: utf-8 -*-
from abjad.tools.abctools import AbjadObject


class BurnishSpecifier(AbjadObject):
    r'''Burnish specifier.
    '''

    ### INITIALIZER ###

    def __init__(
        self,
        lefts=None, 
        middles=None, 
        rights=None, 
        left_lengths=None, 
        right_lengths=None,
        ):
        lefts = self._to_tuple(lefts)
        middles = self._to_tuple(middles)
        rights = self._to_tuple(rights)
        left_lengths = self._to_tuple(left_lengths)
        right_lengths = self._to_tuple(right_lengths)
        prototype = (tuple, type(None))
        assert isinstance(lefts, prototype)
        assert isinstance(middles, prototype)
        assert isinstance(rights, prototype)
        assert isinstance(left_lengths, prototype)
        assert isinstance(right_lengths, prototype)
        self._lefts = lefts
        self._middles = middles
        self._rights = rights
        self._left_lengths = left_lengths
        self._right_lengths = right_lengths

    ### PRIVATE METHODS ###

    @staticmethod
    def _to_tuple(expr):
        if isinstance(expr, list):
            expr = tuple(expr)
        return expr

    ### PUBLIC PROPERTIES ###

    @property
    def left_lengths(self):
        r'''Gets left lengths of burnish specifier.

        Returns tuple or none.
        '''
        return self._left_lengths

    @property
    def lefts(self):
        r'''Gets lefts of burnish specifier.

        Returns tuple or none.
        '''
        return self._lefts

    @property
    def middles(self):
        r'''Gets middles of burnish specifier.

        Returns tuple or none.
        '''
        return self._middles

    @property
    def right_lengths(self):
        r'''Gets right lengths of burnish specifier.

        Returns tuple or none.
        '''
        return self._right_lengths

    @property
    def rights(self):
        r'''Gets rights of burnish specifier.

        Returns tuple or none.
        '''
        return self._rights
