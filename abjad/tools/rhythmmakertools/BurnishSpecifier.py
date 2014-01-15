# -*- encoding: utf-8 -*-
from abjad.tools import sequencetools
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
        assert lefts is None or all(x in (-1, 0, 1) for x in lefts)
        assert middles is None or all(x in (-1, 0, 1) for x in middles)
        assert rights is None or all(x in (-1, 0, 1) for x in rights)
        assert left_lengths is None or \
            sequencetools.all_are_nonnegative_integer_equivalent_numbers(
            left_lengths)
        assert right_lengths is None or \
            sequencetools.all_are_nonnegative_integer_equivalent_numbers(
            right_lengths)
        self._lefts = lefts
        self._middles = middles
        self._rights = rights
        self._left_lengths = left_lengths
        self._right_lengths = right_lengths

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        r'''Is true when `expr` is a burnish specifier with input parameters
        equal to those of this burnish specifier. Otherwise false.

        Returns boolean.
        '''
        if isinstance(expr, type(self)) and \
            self.lefts == expr.lefts and \
            self.middles == expr.middles and \
            self.rights == expr.rights and \
            self.left_lengths == expr.left_lengths and \
            self.right_lengths == expr.right_lengths:
            return True
        return False

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

    ### PUBLIC METHODS ###

    def reverse(self):
        r'''Reverses burnish specification.

        Returns new burnish specification.
        '''
        lefts = self.lefts
        if lefts is not None:
            lefts = tuple(reversed(lefts))
        middles = self.middles
        if middles is not None:
            middles = tuple(reversed(middles))
        rights = self.rights
        if rights is not None:
            rights = tuple(reversed(rights))
        left_lengths = self.left_lengths
        if left_lengths is not None:
            left_lengths = tuple(reversed(left_lengths))
        right_lengths = self.right_lengths
        if right_lengths is not None:
            right_lengths = tuple(reversed(right_lengths))
        new = type(self)(
            lefts=lefts,
            middles=middles,
            rights=rights,
            left_lengths=left_lengths,
            right_lengths=right_lengths,
            )
        return new
