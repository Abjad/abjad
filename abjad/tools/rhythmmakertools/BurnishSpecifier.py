# -*- encoding: utf-8 -*-
from abjad.tools import mathtools
from abjad.tools import sequencetools
from abjad.tools.abctools import AbjadObject
from abjad.tools.topleveltools import new


class BurnishSpecifier(AbjadObject):
    r'''Burnish specifier.

    ..  container:: example

        Force first leaf of each division to be a rest:

        ::

            >>> burnish_specifier = rhythmmakertools.BurnishSpecifier(
            ...     lefts=(-1,),
            ...     left_lengths=(1,),
            ...     )

    ..  container:: example

        Force the first three leaves of each division to be rests:

        ::

            >>> burnish_specifier = rhythmmakertools.BurnishSpecifier(
            ...     lefts=(-1,),
            ...     left_lengths=(3,),
            ...     )

    ..  container:: example

        Force last leaf of each division to be a rest:

        ::

            >>> burnish_specifier = rhythmmakertools.BurnishSpecifier(
            ...     rights=(-1,),
            ...     right_lengths=(1,),
            ...     )

    ..  container:: example

        Force the last three leaves of each division to be rests:

        ::

            >>> burnish_specifier = rhythmmakertools.BurnishSpecifier(
            ...     rights=(-1,),
            ...     right_lengths=(3,),
            ...     )

    ..  container:: example

        Force the first leaf of every even-numbered division to be a rest;
        force the first leaf of every odd-numbered division to be a note.

        ::

            >>> burnish_specifier = rhythmmakertools.BurnishSpecifier(
            ...     lefts=(-1, 1),
            ...     left_lengths=(1,),
            ...     )

    ..  container:: example

        Force the last leaf of every even-numbered division to be a rest;
        force the last leaf of every odd-numbered division to be a note.

        ::

            >>> burnish_specifier = rhythmmakertools.BurnishSpecifier(
            ...     rights=(-1, 1),
            ...     right_lengths=(1,),
            ...     )

    ..  container:: example

        Force the first leaf of every even-numbered division to be a rest;
        leave the first leaf of every odd-numbered division unchanged.

        ::

            >>> burnish_specifier = rhythmmakertools.BurnishSpecifier(
            ...     lefts=(-1, 0),
            ...     left_lengths=(1,),
            ...     )

    ..  container:: example

        Force the last leaf of every even-numbered division to be a rest;
        leave the last leaf of every odd-numbered division unchanged.

        ::

            >>> burnish_specifier = rhythmmakertools.BurnishSpecifier(
            ...     rights=(-1, 0),
            ...     right_lengths=(1,),
            ...     )

    Burnish specifiers are immutable.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_burnish_divisions',
        '_burnish_output',
        '_left_lengths',
        '_lefts',
        '_middles',
        '_right_lengths',
        '_rights',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        burnish_divisions=False,
        burnish_output=False,
        lefts=None,
        middles=None,
        rights=None,
        left_lengths=None,
        right_lengths=None,
        ):
        assert isinstance(burnish_divisions, bool)
        assert isinstance(burnish_output, bool)
        self._burnish_divisions = burnish_divisions
        self._burnish_output = burnish_output
        lefts = self._to_tuple(lefts)
        middles = self._to_tuple(middles)
        rights = self._to_tuple(rights)
        left_lengths = self._to_tuple(left_lengths)
        right_lengths = self._to_tuple(right_lengths)
        assert self._is_sign_tuple(lefts)
        assert self._is_sign_tuple(middles)
        assert self._is_sign_tuple(rights)
        assert self._is_length_tuple(left_lengths)
        assert self._is_length_tuple(right_lengths)
        self._lefts = lefts
        self._middles = middles
        self._rights = rights
        self._left_lengths = left_lengths
        self._right_lengths = right_lengths

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        r'''Is true when `expr` is a burnish specifier with input parameters
        equal to those of this burnish specifier. Otherwise false.

        ..  container:: example

            ::

                >>> burnish_specifier_1 = rhythmmakertools.BurnishSpecifier(
                ...     lefts=(-1, 0),
                ...     left_lengths=(1,)
                ... )
                >>> burnish_specifier_2 = rhythmmakertools.BurnishSpecifier(
                ...     lefts=(-1, 0),
                ...     left_lengths=(1,)
                ... )
                >>> burnish_specifier_3 = rhythmmakertools.BurnishSpecifier()

            ::

                >>> burnish_specifier_1 == burnish_specifier_1
                True
                >>> burnish_specifier_1 == burnish_specifier_2
                True
                >>> burnish_specifier_1 == burnish_specifier_3
                False
                >>> burnish_specifier_2 == burnish_specifier_1
                True
                >>> burnish_specifier_2 == burnish_specifier_2
                True
                >>> burnish_specifier_2 == burnish_specifier_3
                False
                >>> burnish_specifier_3 == burnish_specifier_1
                False
                >>> burnish_specifier_3 == burnish_specifier_2
                False
                >>> burnish_specifier_3 == burnish_specifier_3
                True

        Returns boolean.
        '''
        from abjad.tools import systemtools
        return systemtools.StorageFormatManager.compare(self, expr)

    def __format__(self, format_specification=''):
        r'''Formats burnish specifier.

        ..  container:: example

            ::

                >>> burnish_specifier = rhythmmakertools.BurnishSpecifier(
                ...     lefts=(-1, 0),
                ...     left_lengths=(1,),
                ...     )

            ::

                >>> print format(burnish_specifier)
                rhythmmakertools.BurnishSpecifier(
                    burnish_divisions=False,
                    burnish_output=False,
                    lefts=(-1, 0),
                    left_lengths=(1,),
                    )

        Returns string.
        '''
        return AbjadObject.__format__(
            self,
            format_specification=format_specification,
            )

    def __ne__(self, expr):
        r'''Is true when `expr` does not equal burnish specifier.

        ..  container:: example

            ::

                >>> burnish_specifier_1 = rhythmmakertools.BurnishSpecifier(
                ...     lefts=(-1, 0),
                ...     left_lengths=(1,)
                ... )
                >>> burnish_specifier_2 = rhythmmakertools.BurnishSpecifier(
                ...     lefts=(-1, 0),
                ...     left_lengths=(1,)
                ... )
                >>> burnish_specifier_3 = rhythmmakertools.BurnishSpecifier()

            ::

                >>> burnish_specifier_1 != burnish_specifier_1
                False
                >>> burnish_specifier_1 != burnish_specifier_2
                False
                >>> burnish_specifier_1 != burnish_specifier_3
                True
                >>> burnish_specifier_2 != burnish_specifier_1
                False
                >>> burnish_specifier_2 != burnish_specifier_2
                False
                >>> burnish_specifier_2 != burnish_specifier_3
                True
                >>> burnish_specifier_3 != burnish_specifier_1
                True
                >>> burnish_specifier_3 != burnish_specifier_2
                True
                >>> burnish_specifier_3 != burnish_specifier_3
                False

        Returns boolean.
        '''
        return AbjadObject.__ne__(self, expr)

    def __repr__(self):
        r'''Gets interpreter representation of burnish specifier.

        ..  container:: example

            ::

                >>> burnish_specifier = rhythmmakertools.BurnishSpecifier(
                ...     lefts=(-1, 0),
                ...     left_lengths=(1,),
                ...     )

            ::

                >>> burnish_specifier
                BurnishSpecifier(burnish_divisions=False, burnish_output=False, lefts=(-1, 0), left_lengths=(1,))

        Returns string.
        '''
        return AbjadObject.__repr__(self)

    ### PRIVATE METHODS ###

    @staticmethod
    def _is_length_tuple(expr):
        if expr is None:
            return True
        if mathtools.all_are_nonnegative_integer_equivalent_numbers(expr):
            if isinstance(expr, tuple):
                return True
        return False

    @staticmethod
    def _is_sign_tuple(expr):
        if expr is None:
            return True
        if isinstance(expr, tuple):
            return all(x in (-1, 0, 1) for x in expr)
        return False

    @staticmethod
    def _reverse_tuple(expr):
        if expr is not None:
            return tuple(reversed(expr))

    @staticmethod
    def _rotate_tuple(expr, n):
        if expr is not None:
            return tuple(sequencetools.rotate_sequence(expr, n))

    @staticmethod
    def _to_tuple(expr):
        if isinstance(expr, list):
            expr = tuple(expr)
        return expr

    ### PUBLIC PROPERTIES ###

    @property
    def burnish_divisions(self):
        r'''Is true when rhythm-maker should burnish every division in output.
        Otherwise false.

        Defaults to false.

        Returns boolean.
        '''
        return self._burnish_divisions

    @property
    def burnish_output(self):
        r'''Is true when rhythm-maker should burnish first and last division
        in output. Otherwise false.

        Defaults to false.

        Returns boolean.
        '''
        return self._burnish_output

    @property
    def left_lengths(self):
        r'''Gets left lengths of burnish specifier.

        ..  container:: example

            ::

                >>> burnish_specifier = rhythmmakertools.BurnishSpecifier(
                ...     lefts=(-1, 0),
                ...     middles=(0,),
                ...     rights=(-1, -1, 0),
                ...     left_lengths=(2,),
                ...     right_lengths=(1,),
                ...     )

            ::

                >>> burnish_specifier.left_lengths
                (2,)

        Returns tuple or none.
        '''
        return self._left_lengths

    @property
    def lefts(self):
        r'''Gets lefts of burnish specifier.

        ..  container:: example

            ::

                >>> burnish_specifier = rhythmmakertools.BurnishSpecifier(
                ...     lefts=(-1, 0),
                ...     middles=(0,),
                ...     rights=(-1, -1, 0),
                ...     left_lengths=(2,),
                ...     right_lengths=(1,),
                ...     )

            ::

                >>> burnish_specifier.lefts
                (-1, 0)

        Returns tuple or none.
        '''
        return self._lefts

    @property
    def middles(self):
        r'''Gets middles of burnish specifier.

        ..  container:: example

            ::

                >>> burnish_specifier = rhythmmakertools.BurnishSpecifier(
                ...     lefts=(-1, 0),
                ...     middles=(0,),
                ...     rights=(-1, -1, 0),
                ...     left_lengths=(2,),
                ...     right_lengths=(1,),
                ...     )

            ::

                >>> burnish_specifier.middles
                (0,)

        Returns tuple or none.
        '''
        return self._middles

    @property
    def right_lengths(self):
        r'''Gets right lengths of burnish specifier.

        ..  container:: example

            ::

                >>> burnish_specifier = rhythmmakertools.BurnishSpecifier(
                ...     lefts=(-1, 0),
                ...     middles=(0,),
                ...     rights=(-1, -1, 0),
                ...     left_lengths=(2,),
                ...     right_lengths=(1,),
                ...     )

            ::

                >>> burnish_specifier.right_lengths
                (1,)

        Returns tuple or none.
        '''
        return self._right_lengths

    @property
    def rights(self):
        r'''Gets rights of burnish specifier.

        ..  container:: example

            ::

                >>> burnish_specifier = rhythmmakertools.BurnishSpecifier(
                ...     lefts=(-1, 0),
                ...     middles=(0,),
                ...     rights=(-1, -1, 0),
                ...     left_lengths=(2,),
                ...     right_lengths=(1,),
                ...     )

            ::

                >>> burnish_specifier.rights
                (-1, -1, 0)

        Returns tuple or none.
        '''
        return self._rights

    ### PUBLIC METHODS ###

    def reverse(self):
        r'''Reverses burnish specification.

        ..  container:: example

            ::

                >>> burnish_specifier = rhythmmakertools.BurnishSpecifier(
                ...     burnish_divisions=True,
                ...     burnish_output=False,
                ...     lefts=(-1, 0),
                ...     middles=(0,),
                ...     rights=(-1, -1, 0),
                ...     left_lengths=(2,),
                ...     right_lengths=(1,),
                ...     )

            ::

                >>> print format(burnish_specifier.reverse())
                rhythmmakertools.BurnishSpecifier(
                    burnish_divisions=True,
                    burnish_output=False,
                    lefts=(0, -1),
                    middles=(0,),
                    rights=(0, -1, -1),
                    left_lengths=(2,),
                    right_lengths=(1,),
                    )

        Returns new burnish specification.
        '''
        lefts = self._reverse_tuple(self.lefts)
        middles = self._reverse_tuple(self.middles)
        rights = self._reverse_tuple(self.rights)
        left_lengths = self._reverse_tuple(self.left_lengths)
        right_lengths = self._reverse_tuple(self.right_lengths)
        result = new(
            self,
            lefts=lefts,
            middles=middles,
            rights=rights,
            left_lengths=left_lengths,
            right_lengths=right_lengths,
            )
        return result

    def rotate(self, n=0):
        r'''Rotates burnish specification.

        ..  container:: example

            ::

                >>> burnish_specifier = rhythmmakertools.BurnishSpecifier(
                ...     burnish_divisions=True,
                ...     burnish_output=False,
                ...     lefts=(-1, 0),
                ...     middles=(0,),
                ...     rights=(-1, -1, 0),
                ...     left_lengths=(2,),
                ...     right_lengths=(1, 2, 3),
                ...     )

            ::

                >>> print format(burnish_specifier.rotate(1))
                rhythmmakertools.BurnishSpecifier(
                    burnish_divisions=True,
                    burnish_output=False,
                    lefts=(0, -1),
                    middles=(0,),
                    rights=(0, -1, -1),
                    left_lengths=(2,),
                    right_lengths=(3, 1, 2),
                    )

        Returns new burnish specification.
        '''
        lefts = self._rotate_tuple(self.lefts, n)
        middles = self._rotate_tuple(self.middles, n)
        rights = self._rotate_tuple(self.rights, n)
        left_lengths = self._rotate_tuple(self.left_lengths, n)
        right_lengths = self._rotate_tuple(self.right_lengths, n)
        return new(
            self,
            lefts=lefts,
            middles=middles,
            rights=rights,
            left_lengths=left_lengths,
            right_lengths=right_lengths,
            )
