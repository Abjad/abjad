# -*- encoding: utf-8 -*-
from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import sequencetools
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class DivisionMaker(AbjadValueObject):
    r'''Division-maker.

    ..  container:: example

        ::

            >>> maker = makertools.DivisionMaker(pattern=[(1, 4)])

        ::

            >>> print(format(maker, 'storage'))
            makertools.DivisionMaker(
                pattern=(
                    durationtools.Division(1, 4),
                    ),
                )

        ::

            >>> lists = maker([(7, 8), (7, 8), (7, 16)])
            >>> for list_ in lists:
            ...     list_
            [Division(1, 4), Division(1, 4), Division(1, 4), Division(1, 8)]
            [Division(1, 4), Division(1, 4), Division(1, 4), Division(1, 8)]
            [Division(1, 4), Division(3, 16)]

    Object model of a partially evaluated function that accepts a (possibly
    empty) list of divisions as input and returns a (possibly empty) nested 
    list of divisions as output (structured one output list per input
    division).

    Follows the two-step configure-once / call-repeatedly pattern shown here.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_cyclic',
        '_pattern',
        '_pattern_rotation_index',
        '_remainder',
        '_remainder_fuse_threshold',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        cyclic=True,
        pattern=(),
        pattern_rotation_index=0,
        remainder=Right,
        remainder_fuse_threshold=None,
        ):
        assert isinstance(cyclic, bool), repr(cyclic)
        self._cyclic = cyclic
        pattern = pattern or ()
        pattern_ = []
        for division in pattern:
            division = durationtools.Division(division)
            pattern_.append(division)
        pattern = tuple(pattern_)
        self._pattern = pattern
        assert remainder in (Left, Right), repr(remainder)
        self._remainder = remainder
        assert isinstance(pattern_rotation_index, int)
        self._pattern_rotation_index = pattern_rotation_index
        if remainder_fuse_threshold is not None:
            remainder_fuse_threshold = durationtools.Duration(
                remainder_fuse_threshold,
                )
        self._remainder_fuse_threshold = remainder_fuse_threshold

    ### SPECIAL METHODS ###

    def __call__(self, divisions=None):
        r'''Calls division-maker on `divisions`.

        ..  container:: example

            Calls division-maker on division with no remainder:

            ::

                >>> maker = makertools.DivisionMaker(
                ...     cyclic=True,
                ...     pattern=[(1, 4)],
                ...     )
                >>> lists = maker([(3, 4)])
                >>> for list_ in lists:
                ...     list_
                [Division(1, 4), Division(1, 4), Division(1, 4)]

        ..  container:: example

            Calls division-maker cyclically on each division.
            Positions remainders to the right of each output list:

            ::

                >>> maker = makertools.DivisionMaker(
                ...     pattern=[(1, 4)],
                ...     )
                >>> lists = maker([(7, 8)])
                >>> for list_ in lists:
                ...     list_ 
                [Division(1, 4), Division(1, 4), Division(1, 4), Division(1, 8)]

            Positions remainder at right of output because divison-maker
            `remainder` defaults to right.

        ..  container:: example

            Calls division-maker with pattern set to none:

            ::

                >>> maker = makertools.DivisionMaker()
                >>> lists = maker([(6, 32)])
                >>> for list_ in lists:
                ...     list_
                [Division(6, 32)]

            Returns input division unchanged.

        ..  container:: example

            Calls division-maker on nothing:

            ::

                >>> maker = makertools.DivisionMaker(pattern=[(1, 4)])
                >>> maker()
                []

            Returns empty list.

        ..  container:: example

            Call division-maker on multiple divisions:

            ::

                >>> maker = makertools.DivisionMaker(
                ...     cyclic=True,
                ...     pattern=[(1, 4)],
                ...     )
                >>> lists = maker([(2, 4), (3, 4)])
                >>> for list_ in lists:
                ...     list_
                [Division(1, 4), Division(1, 4)]
                [Division(1, 4), Division(1, 4), Division(1, 4)]

        Returns possibly empty list of division lists.
        '''
        divisions = divisions or []
        if not divisions:
            return []
        division_lists = []
        for i, division in enumerate(divisions):
            input_division = durationtools.Division(division)
            input_duration = durationtools.Duration(input_division)
            assert 0 < input_division, repr(input_division)
            if not self.pattern:
                division_list = [input_division]
                division_lists.append(division_list)
                continue
            division_list = list(self.pattern)
            pattern_rotation_index = self.pattern_rotation_index or 0
            pattern_rotation_index *= i
            division_list = sequencetools.rotate_sequence(
                division_list,
                pattern_rotation_index,
                )
            if self.cyclic:
                division_list = sequencetools.repeat_sequence_to_weight(
                    division_list,
                    input_division,
                    allow_total=Less,
                    )
            total_duration = durationtools.Duration(sum(division_list))
            if total_duration == input_duration:
                division_lists.append(division_list)
                continue
            if self.remainder is None:
                message = 'can not fill {} from {} exactly.'
                message = message.format(input_division, self.pattern)
                raise Exception(message)
            remainder = input_division - total_duration
            remainder = durationtools.Duration(remainder)
            remainder = durationtools.Division(remainder)
            if self.remainder == Left:
                if self.remainder_fuse_threshold is None:
                    division_list.insert(0, remainder)
                elif remainder <= self.remainder_fuse_threshold:
                    #division_list[0] += remainder
                    fused_value = division_list[0] + remainder
                    fused_value = durationtools.Division(fused_value)
                    division_list[0] = fused_value
                else:
                    division_list.insert(0, remainder)
            elif self.remainder == Right:
                if self.remainder_fuse_threshold is None:
                    division_list.append(remainder)
                elif remainder <= self.remainder_fuse_threshold:
                    #division_list[-1] += remainder
                    fused_value = division_list[-1] + remainder
                    fused_value = durationtools.Division(fused_value)
                    division_list[-1] = fused_value
                else:
                    division_list.append(remainder)
            else:
                raise ValueError((self.remainder, remainder))
            total_duration = durationtools.Duration(sum(division_list))
            pair = total_duration, input_duration
            assert total_duration == input_duration, pair
            division_lists.append(division_list)
        return division_lists

    ### PRIVATE PROPERTIES ###

    @property
    def _storage_format_specification(self):
        from abjad.tools import systemtools
        manager = systemtools.StorageFormatManager
        keyword_argument_names = \
            manager.get_signature_keyword_argument_names(self)
        keyword_argument_names = list(keyword_argument_names)
        if self.cyclic == True:
            keyword_argument_names.remove('cyclic')
        if not self.pattern:
            keyword_argument_names.remove('pattern')
        if self.remainder == Right:
            keyword_argument_names.remove('remainder')
        if self.pattern_rotation_index == 0:
            keyword_argument_names.remove('pattern_rotation_index')
        return systemtools.StorageFormatSpecification(
            self,
            keyword_argument_names=keyword_argument_names,
            )

    ### PUBLIC PROPERTIES ###

    @property
    def cyclic(self):
        r'''Is true when division-maker reads pattern cyclically for each input
        division.
        
        Is false when division-maker reads pattern only once per input
        division.

        ..  container:: example

            **Example 1.** Reads pattern cyclically for each input division:

            ::

                >>> maker = makertools.DivisionMaker(
                ...     pattern=[(1, 4)],
                ...     )

            ::

                >>> lists = maker([(7, 8), (7, 8), (7, 16)])
                >>> for list_ in lists:
                ...     list_
                [Division(1, 4), Division(1, 4), Division(1, 4), Division(1, 8)]
                [Division(1, 4), Division(1, 4), Division(1, 4), Division(1, 8)]
                [Division(1, 4), Division(3, 16)]

            Defaults to ``cyclic=True``.

        ..  container:: example

            **Example 2.** Reads pattern only once per input division:

            ::

                >>> maker = makertools.DivisionMaker(
                ...     cyclic=False,
                ...     pattern=[(1, 4)],
                ...     )

            ::

                >>> lists = maker([(7, 8), (7, 8), (7, 16)])
                >>> for list_ in lists:
                ...     list_
                [Division(1, 4), Division(5, 8)]
                [Division(1, 4), Division(5, 8)]
                [Division(1, 4), Division(3, 16)]

        Set to true or false.
        '''
        return self._cyclic

    @property
    def pattern(self):
        r'''Gets pattern of division-maker.

        ..  container:: example

            **Example 1.** Returns input division unchanged when pattern is
            empty:

                >>> maker = makertools.DivisionMaker()

            ::

                >>> lists = maker([(7, 8), (7, 8), (7, 16)])
                >>> for list_ in lists:
                ...     list_
                [Division(7, 8)]
                [Division(7, 8)]
                [Division(7, 16)]

            Defaults to ``pattern=()``.

        ..  container:: example

            **Example 2.** Applies pattern to each input division:

                >>> maker = makertools.DivisionMaker(
                ...     pattern=[(1, 4)],
                ...     )

            ::

                >>> lists = maker([(7, 8), (7, 8), (7, 16)])
                >>> for list_ in lists:
                ...     list_
                [Division(1, 4), Division(1, 4), Division(1, 4), Division(1, 8)]
                [Division(1, 4), Division(1, 4), Division(1, 4), Division(1, 8)]
                [Division(1, 4), Division(3, 16)]

        Set to list or tuple of divisions.
        '''
        return self._pattern

    @property
    def pattern_rotation_index(self):
        r'''Gets pattern rotation index of division-maker.

        ..  container:: example

            **Example 1.** Does not rotate pattern:

            ::

                >>> maker = makertools.DivisionMaker(
                ...     cyclic=True,
                ...     pattern=[(1, 16), (1, 8), (1, 4)],
                ...     )

            ::

                >>> lists = maker([(7, 16), (7, 16), (7, 16)])
                >>> for list_ in lists:
                ...     list_
                [Division(1, 16), Division(1, 8), Division(1, 4)]
                [Division(1, 16), Division(1, 8), Division(1, 4)]
                [Division(1, 16), Division(1, 8), Division(1, 4)]

            Defaults to ``pattern_rotation_index=0``.

        ..  container:: example

            **Example 2.** Rotates pattern one element to the left on each new
            input division:

            ::

                >>> maker = makertools.DivisionMaker(
                ...     cyclic=True,
                ...     pattern=[(1, 16), (1, 8), (1, 4)],
                ...     pattern_rotation_index=-1,
                ...     )

            ::

                >>> lists = maker([(7, 16), (7, 16), (7, 16)])
                >>> for list_ in lists:
                ...     list_
                [Division(1, 16), Division(1, 8), Division(1, 4)]
                [Division(1, 8), Division(1, 4), Division(1, 16)]
                [Division(1, 4), Division(1, 16), Division(1, 8)]

        ..  container:: example

            **Example 3.** Rotates pattern one element to the right on each new
            input division:

            ::

                >>> maker = makertools.DivisionMaker(
                ...     cyclic=True,
                ...     pattern=[(1, 16), (1, 8), (1, 4)],
                ...     pattern_rotation_index=1,
                ...     )

            ::

                >>> lists = maker([(7, 16), (7, 16), (7, 16)])
                >>> for list_ in lists:
                ...     list_
                [Division(1, 16), Division(1, 8), Division(1, 4)]
                [Division(1, 4), Division(1, 16), Division(1, 8)]
                [Division(1, 8), Division(1, 4), Division(1, 16)]

        Set to integer.
        '''
        return self._pattern_rotation_index

    @property
    def remainder(self):
        r'''Gets direction to which any remainder will be positioned.

        ..  container:: example

            **Example 1.** Positions remainder to right of noncyclic pattern:

            ::

                >>> maker = makertools.DivisionMaker(
                ...     cyclic=False,
                ...     pattern=[(4, 16), (1, 16)],
                ...     )
                >>> lists = maker([(3, 4)])
                >>> for list_ in lists:
                ...     list_
                [Division(4, 16), Division(1, 16), Division(7, 16)]

            Defaults to ``remainder=Right``.

        ..  container:: example

            **Example 2.** Positions remainder to right of cyclic pattern:

            ::

                >>> maker = makertools.DivisionMaker(
                ...     pattern=[(4, 16), (1, 16)],
                ...     )
                >>> lists = maker([(3, 4)])
                >>> for list_ in lists:
                ...     list_
                [Division(4, 16), Division(1, 16), Division(4, 16), Division(1, 16), Division(1, 8)]

            Defaults to ``remainder=Right``.

        ..  container:: example

            **Example 3.** Positions remainder to left of noncyclic pattern:

            ::

                >>> maker = makertools.DivisionMaker(
                ...     cyclic=False,
                ...     pattern=[(1, 4), (1, 16)],
                ...     remainder=Left,
                ...     )
                >>> lists = maker([(3, 4)])
                >>> for list_ in lists:
                ...     list_
                [Division(7, 16), Division(1, 4), Division(1, 16)]

        ..  container:: example

            **Example 4.** Positions remainder to left of cyclic pattern:

            ::

                >>> maker = makertools.DivisionMaker(
                ...     cyclic=True,
                ...     pattern=[(1, 4), (1, 16)],
                ...     remainder=Left,
                ...     )
                >>> lists = maker([(3, 4)])
                >>> for list_ in lists:
                ...     list_
                [Division(1, 8), Division(1, 4), Division(1, 16), Division(1, 4), Division(1, 16)]

        Set to left or right.
        '''
        return self._remainder

    @property
    def remainder_fuse_threshold(self):
        r'''Gets remainder fuse threshold of division-maker.

        ..  container:: example

            **Example 1.** No threshold. Remainder unfused to the right:

            ::

                >>> maker = makertools.DivisionMaker(
                ...     pattern=[(1, 4)],
                ...     remainder_fuse_threshold=None,
                ...     )

            ::

                >>> lists = maker([(5, 8)])
                >>> for list_ in lists:
                ...     list_
                [Division(1, 4), Division(1, 4), Division(1, 8)]

        ..  container:: example

            **Example 2.** Remainder less than or equal to ``1/8`` fused 
            to the right:

            ::

                >>> maker = makertools.DivisionMaker(
                ...     pattern=[(1, 4)],
                ...     remainder_fuse_threshold=Duration(1, 8),
                ...     )

            ::

                >>> lists = maker([(5, 8)])
                >>> for list_ in lists:
                ...     list_
                [Division(1, 4), Division(3, 8)]

        ..  container:: example

            **Example 3.** No threshold. Remainder unfused to the left:

            ::

                >>> maker = makertools.DivisionMaker(
                ...     cyclic=True,
                ...     pattern=[(1, 4)],
                ...     remainder=Left,
                ...     remainder_fuse_threshold=None,
                ...     )

            ::

                >>> lists = maker([(5, 8)])
                >>> for list_ in lists:
                ...     list_
                [Division(1, 8), Division(1, 4), Division(1, 4)]

        ..  container:: example

            **Example 4.** Remainder less than or equal to ``1/8`` fused to the
            left:

            ::

                >>> maker = makertools.DivisionMaker(
                ...     cyclic=True,
                ...     pattern=[(1, 4)],
                ...     remainder=Left,
                ...     remainder_fuse_threshold=Duration(1, 8),
                ...     )

            ::

                >>> lists = maker([(5, 8)])
                >>> for list_ in lists:
                ...     list_
                [Division(3, 8), Division(1, 4)]

        Set to duration or none.
        '''
        return self._remainder_fuse_threshold