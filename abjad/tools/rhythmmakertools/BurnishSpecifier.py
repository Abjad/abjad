# -*- encoding: utf-8 -*-
from abjad.tools import mathtools
from abjad.tools.abctools import AbjadValueObject


class BurnishSpecifier(AbjadValueObject):
    r'''Burnish specifier.

    ..  container:: example

        Forces first leaf of each division to be a rest:

        ::

            >>> burnish_specifier = rhythmmakertools.BurnishSpecifier(
            ...     left_classes=[Rest],
            ...     left_counts=[1],
            ...     )

    ..  container:: example

        Forces the first three leaves of each division to be rests:

        ::

            >>> burnish_specifier = rhythmmakertools.BurnishSpecifier(
            ...     left_classes=[Rest],
            ...     left_counts=[3],
            ...     )

    ..  container:: example

        Forces last leaf of each division to be a rest:

        ::

            >>> burnish_specifier = rhythmmakertools.BurnishSpecifier(
            ...     right_classes=[Rest],
            ...     right_counts=[1],
            ...     )

    ..  container:: example

        Forces the last three leaves of each division to be rests:

        ::

            >>> burnish_specifier = rhythmmakertools.BurnishSpecifier(
            ...     right_classes=[Rest],
            ...     right_counts=[3],
            ...     )

    ..  container:: example

        Forces the first leaf of every even-numbered division to be a rest;
        forces the first leaf of every odd-numbered division to be a note.

        ::

            >>> burnish_specifier = rhythmmakertools.BurnishSpecifier(
            ...     left_classes=[Rest, Note],
            ...     left_counts=[1],
            ...     )

    ..  container:: example

        Forces the last leaf of every even-numbered division to be a rest;
        forces the last leaf of every odd-numbered division to be a note.

        ::

            >>> burnish_specifier = rhythmmakertools.BurnishSpecifier(
            ...     right_classes=[Rest, Note],
            ...     right_counts=[1],
            ...     )

    ..  container:: example

        Forces the first leaf of every even-numbered division to be a rest;
        leave the first leaf of every odd-numbered division unchanged.

        ::

            >>> burnish_specifier = rhythmmakertools.BurnishSpecifier(
            ...     left_classes=[Rest, 0],
            ...     left_counts=[1],
            ...     )

    ..  container:: example

        Forces the last leaf of every even-numbered division to be a rest;
        leave the last leaf of every odd-numbered division unchanged.

        ::

            >>> burnish_specifier = rhythmmakertools.BurnishSpecifier(
            ...     right_classes=[Rest, 0],
            ...     right_counts=[1],
            ...     )

    Burnish specifiers are immutable.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Specifiers'

    __slots__ = (
        '_left_lengths',
        '_lefts',
        '_middles',
        '_outer_divisions_only',
        '_right_lengths',
        '_rights',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        left_classes=None,
        middle_classes=None,
        right_classes=None,
        left_counts=None,
        right_counts=None,
        outer_divisions_only=False,
        ):
        assert isinstance(outer_divisions_only, bool)
        self._outer_divisions_only = outer_divisions_only
        left_classes = self._to_tuple(left_classes)
        middle_classes = self._to_tuple(middle_classes)
        if middle_classes == (0,):
            middle_classes = ()
        right_classes = self._to_tuple(right_classes)
        left_counts = self._to_tuple(left_counts)
        right_counts = self._to_tuple(right_counts)
        assert self._is_sign_tuple(left_classes)
        assert self._is_sign_tuple(middle_classes)
        assert self._is_sign_tuple(right_classes)
        assert self._is_length_tuple(left_counts)
        assert self._is_length_tuple(right_counts)
        self._lefts = left_classes
        self._middles = middle_classes
        self._rights = right_classes
        self._left_lengths = left_counts
        self._right_lengths = right_counts
#        if outer_divisions_only and left_counts:
#            assert len(left_counts) <= 1, repr(left_counts)
#        if outer_divisions_only and right_counts:
#            assert len(right_counts) <= 1, repr(right_counts)

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        r'''Is true when `expr` is a burnish specifier with input parameters
        equal to those of this burnish specifier. Otherwise false.

        ..  container:: example

            ::

                >>> burnish_specifier_1 = rhythmmakertools.BurnishSpecifier(
                ...     left_classes=[Rest, 0],
                ...     left_counts=[1],
                ... )
                >>> burnish_specifier_2 = rhythmmakertools.BurnishSpecifier(
                ...     left_classes=[Rest, 0],
                ...     left_counts=[1],
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
                ...     left_classes=[Rest, 0],
                ...     left_counts=[1],
                ...     )

            ::

                >>> print(format(burnish_specifier))
                rhythmmakertools.BurnishSpecifier(
                    left_classes=(
                        scoretools.Rest,
                        0,
                        ),
                    left_counts=(1,),
                    )

        Returns string.
        '''
        return AbjadValueObject.__format__(
            self,
            format_specification=format_specification,
            )

    def __hash__(self):
        r'''Hashes burnish specifier.

        Required to be explicitly re-defined on Python 3 if __eq__ changes.

        Returns integer.
        '''
        return super(BurnishSpecifier, self).__hash__()

    def __ne__(self, expr):
        r'''Is true when `expr` does not equal burnish specifier.

        ..  container:: example

            ::

                >>> burnish_specifier_1 = rhythmmakertools.BurnishSpecifier(
                ...     left_classes=[Rest, 0],
                ...     left_counts=[1],
                ... )
                >>> burnish_specifier_2 = rhythmmakertools.BurnishSpecifier(
                ...     left_classes=[Rest, 0],
                ...     left_counts=[1],
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
        return AbjadValueObject.__ne__(self, expr)

    def __repr__(self):
        r'''Gets interpreter representation of burnish specifier.

        ..  container:: example

            ::

                >>> burnish_specifier = rhythmmakertools.BurnishSpecifier(
                ...     left_classes=[Rest, 0],
                ...     left_counts=[1],
                ...     )

            ::

                >>> burnish_specifier
                BurnishSpecifier(left_classes=(Rest, 0), left_counts=(1,))

        Returns string.
        '''
        return AbjadValueObject.__repr__(self)

    ### PRIVATE PROPERTIES ###

    @property
    def _storage_format_specification(self):
        from abjad.tools import systemtools
        manager = systemtools.StorageFormatManager
        keyword_argument_names = \
            manager.get_signature_keyword_argument_names(self)
        keyword_argument_names = list(keyword_argument_names)
        if not self.left_classes:
            keyword_argument_names.remove('left_classes')
        if not self.middle_classes:
            keyword_argument_names.remove('middle_classes')
        if not self.right_classes:
            keyword_argument_names.remove('right_classes')
        if not self.left_counts:
            keyword_argument_names.remove('left_counts')
        if not self.right_counts:
            keyword_argument_names.remove('right_counts')
        if self.outer_divisions_only == False:
            keyword_argument_names.remove('outer_divisions_only')
        return systemtools.StorageFormatSpecification(
            self,
            keyword_argument_names=keyword_argument_names,
            )

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
        from abjad.tools import scoretools
        if expr is None:
            return True
        if isinstance(expr, tuple):
            prototype = (-1, 0, 1, scoretools.Note, scoretools.Rest)
            return all(_ in prototype for _ in expr)
        return False

    @staticmethod
    def _to_tuple(expr):
        if isinstance(expr, list):
            expr = tuple(expr)
        return expr

    ### PUBLIC PROPERTIES ###

    @property
    def left_classes(self):
        r'''Gets left_classes of burnish specifier.

        ..  container:: example

            ::

                >>> burnish_specifier = rhythmmakertools.BurnishSpecifier(
                ...     left_classes=[Rest, 0],
                ...     right_classes=[Rest, Rest, 0],
                ...     left_counts=[2],
                ...     right_counts=[1],
                ...     )

            ::

                >>> burnish_specifier.left_classes
                (<class 'abjad.tools.scoretools.Rest.Rest'>, 0)

        Returns tuple or none.
        '''
        return self._lefts

    @property
    def left_counts(self):
        r'''Gets left lengths of burnish specifier.

        ..  container:: example

            ::

                >>> burnish_specifier = rhythmmakertools.BurnishSpecifier(
                ...     left_classes=[Rest, 0],
                ...     right_classes=[Rest, Rest, 0],
                ...     left_counts=[2],
                ...     right_counts=[1],
                ...     )

            ::

                >>> burnish_specifier.left_counts
                (2,)

        Returns tuple or none.
        '''
        return self._left_lengths

    @property
    def middle_classes(self):
        r'''Gets middle_classes of burnish specifier.

        ..  container:: example

            ::

                >>> burnish_specifier = rhythmmakertools.BurnishSpecifier(
                ...     left_classes=[Rest, 0],
                ...     right_classes=[Rest, Rest, 0],
                ...     left_counts=[2],
                ...     right_counts=[1],
                ...     )

            ::

                >>> burnish_specifier.middle_classes is None
                True

        Returns tuple or none.
        '''
        return self._middles

    @property
    def outer_divisions_only(self):
        r'''Is true when rhythm-maker should burnish only first and last 
        division in output.
        
        Is false when rhythm-maker should burnish all divisions.

        Defaults to false.

        Set to true or false.
        '''
        return self._outer_divisions_only

    @property
    def right_classes(self):
        r'''Gets right_classes of burnish specifier.

        ..  container:: example

            ::

                >>> burnish_specifier = rhythmmakertools.BurnishSpecifier(
                ...     left_classes=[Rest, 0],
                ...     right_classes=[Rest, Rest, 0],
                ...     left_counts=[2],
                ...     right_counts=[1],
                ...     )

            ::

                >>> burnish_specifier.right_classes
                (<class 'abjad.tools.scoretools.Rest.Rest'>, <class 'abjad.tools.scoretools.Rest.Rest'>, 0)

        Returns tuple or none.
        '''
        return self._rights

    @property
    def right_counts(self):
        r'''Gets right lengths of burnish specifier.

        ..  container:: example

            ::

                >>> burnish_specifier = rhythmmakertools.BurnishSpecifier(
                ...     left_classes=[Rest, 0],
                ...     right_classes=[Rest, Rest, 0],
                ...     left_counts=[2],
                ...     right_counts=[1],
                ...     )

            ::

                >>> burnish_specifier.right_counts
                (1,)

        Returns tuple or none.
        '''
        return self._right_lengths