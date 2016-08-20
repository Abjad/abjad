# -*- coding: utf-8 -*-
from abjad.tools import datastructuretools
from abjad.tools import mathtools
from abjad.tools import scoretools
from abjad.tools import sequencetools
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
        '_left_counts',
        '_lefts',
        '_middles',
        '_outer_divisions_only',
        '_right_counts',
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
        if left_classes is not None:
            left_classes = tuple(left_classes)
        if middle_classes is not None:
            middle_classes = tuple(middle_classes)
        if middle_classes == (0,):
            middle_classes = ()
        if right_classes is not None:
            right_classes = tuple(right_classes)
        if left_counts is not None:
            left_counts = tuple(left_counts)
        if right_counts is not None:
            right_counts = tuple(right_counts)
        assert self._is_sign_tuple(left_classes)
        assert self._is_sign_tuple(middle_classes)
        assert self._is_sign_tuple(right_classes)
        assert self._is_length_tuple(left_counts)
        assert self._is_length_tuple(right_counts)
        self._lefts = left_classes
        self._middles = middle_classes
        self._rights = right_classes
        self._left_counts = left_counts
        self._right_counts = right_counts

    ### SPECIAL METHODS ###

    def __call__(self, divisions, helper_functions=None, rotation=None):
        r'''Calls burnish specifier on `divisions`.

        Returns list of burnished divisions.
        '''
        input_ = self._rotate_input(helper_functions=None, rotation=None)
        if self.outer_divisions_only:
            return self._burnish_outer_divisions(input_, divisions)
        else:
            return self._burnish_each_division(input_, divisions)

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

    def __repr__(self):
        r'''Gets interpreter representation.

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
        return super(BurnishSpecifier, self).__repr__()

    ### PRIVATE METHODS ###

    @staticmethod
    def _burnish_division_part(division_part, token):
        assert len(division_part) == len(token)
        new_division_part = []
        for number, i in zip(division_part, token):
            if i in (-1, scoretools.Rest):
                new_division_part.append(-abs(number))
            elif i == 0:
                new_division_part.append(number)
            elif i in (1, scoretools.Note):
                new_division_part.append(abs(number))
            else:
                raise ValueError
        new_division_part = type(division_part)(new_division_part)
        return new_division_part

    @classmethod
    def _burnish_each_division(class_, input_, divisions):
        left_classes = input_['left_classes']
        middle_classes = input_['middle_classes']
        right_classes = input_['right_classes']
        left_counts = input_['left_counts']
        left_counts = left_counts or datastructuretools.CyclicTuple([0])
        right_counts = input_['right_counts']
        right_counts = right_counts or datastructuretools.CyclicTuple([0])
        lefts_index, rights_index = 0, 0
        burnished_divisions = []
        for division_index, division in enumerate(divisions):
            left_count = left_counts[division_index]
            left = left_classes[lefts_index:lefts_index + left_count]
            lefts_index += left_count
            right_count = right_counts[division_index]
            right = right_classes[rights_index:rights_index + right_count]
            rights_index += right_count
            available_left_count = len(division)
            left_count = min([left_count, available_left_count])
            available_right_count = len(division) - left_count
            right_count = min([right_count, available_right_count])
            middle_count = len(division) - left_count - right_count
            left = left[:left_count]
            if middle_classes:
                middle = middle_count * [middle_classes[division_index]]
            else:
                middle = middle_count * [0]
            right = right[:right_count]
            left_part, middle_part, right_part = \
                sequencetools.partition_sequence_by_counts(
                    division,
                    [left_count, middle_count, right_count],
                    cyclic=False,
                    overhang=False,
                    )
            left_part = class_._burnish_division_part(left_part, left)
            middle_part = class_._burnish_division_part(middle_part, middle)
            right_part = class_._burnish_division_part(right_part, right)
            burnished_division = left_part + middle_part + right_part
            burnished_divisions.append(burnished_division)
        unburnished_weights = [mathtools.weight(x) for x in divisions]
        burnished_weights = [mathtools.weight(x) for x in burnished_divisions]
        assert burnished_weights == unburnished_weights
        return burnished_divisions

    @classmethod
    def _burnish_outer_divisions(class_, input_, divisions):
        for list_ in divisions:
            assert all(isinstance(_, int) for _ in list_), repr(list_)
        left_classes = input_['left_classes']
        middle_classes = input_['middle_classes']
        right_classes = input_['right_classes']
        left_counts = input_['left_counts']
        left_counts = left_counts or datastructuretools.CyclicTuple([0])
        right_counts = input_['right_counts']
        right_counts = right_counts or datastructuretools.CyclicTuple([0])
        burnished_divisions = []
        left_count = 0
        if left_counts:
            left_count = left_counts[0]
        left = left_classes[:left_count]
        right_count = 0
        if right_counts:
            right_count = right_counts[0]
        right = right_classes[:right_count]
        if len(divisions) == 1:
            available_left_count = len(divisions[0])
            left_count = min([left_count, available_left_count])
            available_right_count = len(divisions[0]) - left_count
            right_count = min([right_count, available_right_count])
            middle_count = len(divisions[0]) - left_count - right_count
            left = left[:left_count]
            if not middle_classes:
                middle_classes = [1]
            middle = [middle_classes[0]]
            middle = middle_count * middle
            right = right[:right_count]
            left_part, middle_part, right_part = \
                sequencetools.partition_sequence_by_counts(
                    divisions[0],
                    [left_count, middle_count, right_count],
                    cyclic=False,
                    overhang=Exact,
                    )
            left_part = class_._burnish_division_part(left_part, left)
            middle_part = class_._burnish_division_part(middle_part, middle)
            right_part = class_._burnish_division_part(right_part, right)
            burnished_division = left_part + middle_part + right_part
            burnished_divisions.append(burnished_division)
        else:
            # first division
            available_left_count = len(divisions[0])
            left_count = min([left_count, available_left_count])
            middle_count = len(divisions[0]) - left_count
            left = left[:left_count]
            if not middle_classes:
                middle_classes = [1]
            middle = [middle_classes[0]]
            middle = middle_count * middle
            left_part, middle_part = \
                sequencetools.partition_sequence_by_counts(
                    divisions[0],
                    [left_count, middle_count],
                    cyclic=False,
                    overhang=Exact,
                    )
            left_part = class_._burnish_division_part(left_part, left)
            middle_part = class_._burnish_division_part(middle_part, middle)
            burnished_division = left_part + middle_part
            burnished_divisions.append(burnished_division)
            # middle divisions
            for division in divisions[1:-1]:
                middle_part = division
                middle = len(division) * [middle_classes[0]]
                middle_part = class_._burnish_division_part(
                    middle_part,
                    middle,
                    )
                burnished_division = middle_part
                burnished_divisions.append(burnished_division)
            # last division:
            available_right_count = len(divisions[-1])
            right_count = min([right_count, available_right_count])
            middle_count = len(divisions[-1]) - right_count
            right = right[:right_count]
            middle = middle_count * [middle_classes[0]]
            middle_part, right_part = \
                sequencetools.partition_sequence_by_counts(
                    divisions[-1],
                    [middle_count, right_count],
                    cyclic=False,
                    overhang=Exact,
                    )
            middle_part = class_._burnish_division_part(middle_part, middle)
            right_part = class_._burnish_division_part(right_part, right)
            burnished_division = middle_part + right_part
            burnished_divisions.append(burnished_division)
        unburnished_weights = [mathtools.weight(x) for x in divisions]
        burnished_weights = [mathtools.weight(x) for x in burnished_divisions]
        #assert burnished_weights == unburnished_weights
        # TODO: make the following work on Python 3:
        #assert tuple(burnished_weights) == tuple(unburnished_weights)
        return burnished_divisions

    def _get_format_specification(self):
        from abjad.tools import systemtools
        agent = systemtools.StorageFormatAgent(self)
        names = list(agent.signature_keyword_names)
        for name in names[:]:
            if not getattr(self, name):
                names.remove(name)
        return systemtools.FormatSpecification(
            client=self,
            storage_format_kwargs_names=names,
            )

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

    def _none_to_trivial_helper(self, expr):
        if expr is None:
            expr = self._trivial_helper
        assert callable(expr)
        return expr

    def _rotate_input(self, helper_functions=None, rotation=None):
        helper_functions = helper_functions or {}
        input_ = {}
        names = (
            'left_classes',
            'left_counts',
            'middle_classes',
            'right_classes',
            'right_counts',
            )
        for name in names:
            value = getattr(self, name)
            value = value or ()
            helper_function = helper_functions.get(name)
            helper_function = self._none_to_trivial_helper(helper_function)
            value = helper_function(value, rotation)
            value = datastructuretools.CyclicTuple(value)
            input_[name] = value
        return input_

    def _trivial_helper(self, sequence_, rotation):
        if isinstance(rotation, int) and len(sequence_):
            return sequencetools.rotate_sequence(sequence_, rotation)
        return sequence_

    ### PUBLIC PROPERTIES ###

    @property
    def left_classes(self):
        r'''Gets left classes.

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
        r'''Gets left counts.

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
        return self._left_counts

    @property
    def middle_classes(self):
        r'''Gets middle_classes.

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
        r'''Gets right classes.

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
        r'''Gets right counts.

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
        return self._right_counts
