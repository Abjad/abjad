# -*- coding: utf-8 -*-
from abjad.tools import mathtools
from abjad.tools import systemtools
from abjad.tools.mathtools.NonreducedFraction import NonreducedFraction


class Division(NonreducedFraction):
    r'''Division.

    ..  container:: example

        **Example 1.** Division with duration, start offset and payload:

        ::

            >>> division = durationtools.Division(
            ...     (3, 8),
            ...     payload=rhythmmakertools.NoteRhythmMaker(),
            ...     start_offset=Offset((5, 4)),
            ...     )

        ::

            >>> print(format(division))
            durationtools.Division(
                (3, 8),
                payload=rhythmmakertools.NoteRhythmMaker(),
                start_offset=durationtools.Offset(5, 4),
                )

    ..  container:: example

        **Example 2.** Division with duration and start offset:

        ::

            >>> division = durationtools.Division(
            ...     (3, 8),
            ...     start_offset=Offset((5, 4)),
            ...     )

        ::

            >>> print(format(division))
            durationtools.Division(
                (3, 8),
                start_offset=durationtools.Offset(5, 4),
                )

    ..  container:: example

        **Example 3.** Division with duration:

        ::

            >>> division = durationtools.Division((3, 8))

        ::

            >>> print(format(division))
            durationtools.Division(
                (3, 8)
                )

    ..  container:: example

        **Example 4.** Initializes from other division:

        ::

            >>> division = durationtools.Division(
            ...     (3, 8),
            ...     payload=rhythmmakertools.NoteRhythmMaker(),
            ...     start_offset=Offset((5, 4)),
            ...     )
            >>> new_division = durationtools.Division(division)

        ::

            >>> print(format(new_division))
            durationtools.Division(
                (3, 8),
                payload=rhythmmakertools.NoteRhythmMaker(),
                start_offset=durationtools.Offset(5, 4),
                )

    ..  container:: example

        **Example 5.** Initializes from nonreduced fraction:

        ::

            >>> fraction = mathtools.NonreducedFraction((6, 4))
            >>> division = durationtools.Division(
            ...     fraction,
            ...     payload=rhythmmakertools.NoteRhythmMaker(),
            ...     start_offset=Offset((5, 4)),
            ...     )
            >>> new_division = durationtools.Division(division)

        ::

            >>> print(format(new_division))
            durationtools.Division(
                (6, 4),
                payload=rhythmmakertools.NoteRhythmMaker(),
                start_offset=durationtools.Offset(5, 4),
                )

    ..  container:: example

        **Example 6.** Empty initialization:

        ::

            >>> division = durationtools.Division()

        ::

            >>> print(format(division))
            durationtools.Division(
                (0, 1)
                )

    ..  container:: example

        **Example 7.** Makes divisions from durations:

        ::

            >>> durations = 10 * [Duration(1, 8)]
            >>> start_offsets = mathtools.cumulative_sums(durations)[:-1]
            >>> divisions = []
            >>> for duration, start_offset in zip(durations, start_offsets):
            ...     division = durationtools.Division(
            ...         duration,
            ...         start_offset=start_offset,
            ...         )
            ...     divisions.append(division)
            >>> divisions = Sequence(divisions)

        ::

            >>> for division in divisions:
            ...     print(division)
            Division((1, 8), start_offset=Offset(0, 1))
            Division((1, 8), start_offset=Offset(1, 8))
            Division((1, 8), start_offset=Offset(1, 4))
            Division((1, 8), start_offset=Offset(3, 8))
            Division((1, 8), start_offset=Offset(1, 2))
            Division((1, 8), start_offset=Offset(5, 8))
            Division((1, 8), start_offset=Offset(3, 4))
            Division((1, 8), start_offset=Offset(7, 8))
            Division((1, 8), start_offset=Offset(1, 1))
            Division((1, 8), start_offset=Offset(9, 8))

        Partitions divisions into thirds:

        ::

            >>> ratio = mathtools.Ratio((1, 1, 1))
            >>> parts = divisions.partition_by_ratio_of_lengths(ratio)

        Gets middle third:

        ::

            >>> for division in parts[1]:
            ...     division
            Division((1, 8), start_offset=Offset(3, 8))
            Division((1, 8), start_offset=Offset(1, 2))
            Division((1, 8), start_offset=Offset(5, 8))
            Division((1, 8), start_offset=Offset(3, 4))

        Gets start offset of middle third:

        ::

            >>> parts[1][0].start_offset
            Offset(3, 8)

    ..  container:: example

        **Example 8.** Makes divisions from durations:

        ::

            >>> durations = 10 * [Duration(1, 8)]
            >>> start_offsets = mathtools.cumulative_sums(durations)[:-1]
            >>> divisions = []
            >>> for duration, start_offset in zip(durations, start_offsets):
            ...     division = durationtools.Division(
            ...         duration,
            ...         start_offset=start_offset,
            ...         )
            ...     divisions.append(division)
            >>> divisions = Sequence(divisions)

        ::

            >>> for division in divisions:
            ...     print(division)
            Division((1, 8), start_offset=Offset(0, 1))
            Division((1, 8), start_offset=Offset(1, 8))
            Division((1, 8), start_offset=Offset(1, 4))
            Division((1, 8), start_offset=Offset(3, 8))
            Division((1, 8), start_offset=Offset(1, 2))
            Division((1, 8), start_offset=Offset(5, 8))
            Division((1, 8), start_offset=Offset(3, 4))
            Division((1, 8), start_offset=Offset(7, 8))
            Division((1, 8), start_offset=Offset(1, 1))
            Division((1, 8), start_offset=Offset(9, 8))

        Splits divisions every five sixteenths:

        ::

            >>> parts = divisions.split([Fraction(5, 16)], cyclic=True)
            >>> for i, part in enumerate(parts):
            ...     message = 'part {}'.format(i)
            ...     print(message)
            ...     for division in part:
            ...         print('\t' + str(division))
            part 0
                Division((1, 8), start_offset=Offset(0, 1))
                Division((1, 8), start_offset=Offset(1, 8))
                Division((1, 16), start_offset=Offset(1, 4))
            part 1
                Division((1, 16), start_offset=Offset(5, 16))
                Division((1, 8), start_offset=Offset(3, 8))
                Division((1, 8), start_offset=Offset(1, 2))
            part 2
                Division((1, 8), start_offset=Offset(5, 8))
                Division((1, 8), start_offset=Offset(3, 4))
                Division((1, 16), start_offset=Offset(7, 8))
            part 3
                Division((1, 16), start_offset=Offset(15, 16))
                Division((1, 8), start_offset=Offset(1, 1))
                Division((1, 8), start_offset=Offset(9, 8))

        Gets start offset of first division of last part:

        ::

            >>> parts[-1][0].start_offset
            Offset(15, 16)

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_payload',
        '_start_offset',
        )

    ### INITIALIZER ###

    def __new__(
        class_,
        argument=None,
        payload=None,
        start_offset=None,
        ):
        from abjad.tools import durationtools
        argument = argument or (0, 1)
        if isinstance(argument, str):
            division = eval(argument)
            argument = division
            if payload is None:
                payload = argument.payload
            if start_offset is None:
                start_offset = argument.start_offset
        if isinstance(argument, mathtools.NonreducedFraction):
            if payload is None:
                payload = getattr(argument, 'payload', None)
            if start_offset is None:
                start_offset = getattr(argument, 'start_offset', None)
        self = NonreducedFraction.__new__(class_, argument)
        self._payload = payload
        if start_offset is not None:
            start_offset = durationtools.Offset(start_offset)
        self._start_offset = start_offset
        return self

    ### SPECIAL METHODS###

    def __add__(self, expr):
        r'''Adds `expr` to division.

        ..  container:: example

            **Example 1.** No start offsets:

            ::

                >>> division_1 = durationtools.Division((2, 4))
                >>> division_2 = durationtools.Division((4, 4))
                >>> division_1 + division_2
                Division((6, 4))

        ..  container:: example

            **Example 2.** One start offset:

            ::

                >>> division_1 = durationtools.Division(
                ...     (2, 4),
                ...     start_offset=Offset(1),
                ...     )
                >>> division_2 = durationtools.Division((4, 4))
                >>> division_1 + division_2
                Division((6, 4), start_offset=Offset(1, 1))

        ..  container:: example

            **Example 3.** Contiguous start offsets:

            ::

                >>> division_1 = durationtools.Division(
                ...     (2, 4),
                ...     start_offset=Offset(1),
                ...     )
                >>> division_2 = durationtools.Division(
                ...     (4, 4),
                ...     start_offset=Offset((3, 2)),
                ...     )
                >>> division_1 + division_2
                Division((6, 4), start_offset=Offset(1, 1))

        ..  container:: example

            **Example 4.** Noncontiguous start offsets:

            ::

                >>> division_1 = durationtools.Division(
                ...     (2, 4),
                ...     start_offset=Offset(1),
                ...     )
                >>> division_2 = durationtools.Division(
                ...     (4, 4),
                ...     start_offset=Offset(10),
                ...     )
                >>> division_1 + division_2
                Division((40, 4), start_offset=Offset(1, 1))

        ..  container:: example

            **Example 5.** Identical start offsets:

            ::

                >>> division_1 = durationtools.Division(
                ...     (2, 4),
                ...     start_offset=Offset(1),
                ...     )
                >>> division_2 = durationtools.Division(
                ...     (4, 4),
                ...     start_offset=Offset(1),
                ...     )
                >>> division_1 + division_2
                Division((4, 4), start_offset=Offset(1, 1))

        ..  container:: example

            **Example 6.** Overlapping start offsets:

            ::

                >>> division_1 = durationtools.Division(
                ...     (2, 4),
                ...     start_offset=Offset(1),
                ...     )
                >>> division_2 = durationtools.Division(
                ...     (4, 4),
                ...     start_offset=Offset((5, 4)),
                ...     )
                >>> division_1 + division_2
                Division((5, 4), start_offset=Offset(1, 1))

        Returns new division.
        '''
        if not isinstance(expr, type(self)):
            expr = type(self)(expr)
        start_offsets = []
        stop_offsets = []
        if self.start_offset is not None:
            start_offsets.append(self.start_offset)
            stop_offsets.append(self.stop_offset)
        if expr.start_offset is not None:
            start_offsets.append(expr.start_offset)
            stop_offsets.append(expr.stop_offset)
        superclass = super(Division, self)
        sum_ = superclass.__add__(expr)
        if not start_offsets:
            division = type(self)(sum_)
        elif len(start_offsets) == 1:
            start_offset = start_offsets[0]
            division = type(self)(sum_, start_offset=start_offset)
        elif len(start_offsets) == 2:
            start_offset = min(start_offsets)
            stop_offset = max(stop_offsets)
            duration = stop_offset - start_offset
            division = type(self)(duration)
            division = division.with_denominator(self.denominator)
            if not division.denominator == self.denominator:
                division = division.with_denominator(expr.denominator)
            division = type(self)(division, start_offset=start_offset)
        else:
            raise Exception
        return division

    def __copy__(self, *args):
        r'''Copies division.

        Returns new division.
        '''
        arguments = self.__getnewargs__()
        return type(self)(*arguments)

    def __deepcopy__(self, *args):
        r'''Deep copies division.

        Returns new division.
        '''
        return self.__copy__(*args)

    def __getnewargs__(self):
        r'''Gets new arguments.

        Returns tuple.
        '''
        return (self.pair, self.payload, self.start_offset)

    def __str__(self):
        r'''Gets string representation of division.

        Returns string.
        '''
        return repr(self)

    def __sub__(self, expr):
        r'''Subtracts `expr` from division.

        ..  container:: example

            **Example 1.** No timespans:

            ::

                >>> division_1 = durationtools.Division((6, 2))
                >>> division_2 = durationtools.Division((4, 2))

            ::

                >>> division_1 - division_2
                Division((2, 2))

            ::

                >>> division_2 - division_1
                Division((-2, 2))

        ..  container:: example

            **Example 2.** Overlapping timespans that start at the same time:

            ::

                >>> division_1 = durationtools.Division(
                ...     (4, 1),
                ...     start_offset=Offset(10),
                ...     )
                >>> division_2 = durationtools.Division(
                ...     (2, 1),
                ...     start_offset=Offset(10),
                ...     )

            ::

                >>> division_1 - division_2
                Division((2, 1), start_offset=Offset(12, 1))

            ::

                >>> division_2 - division_1
                Division((-2, 1), start_offset=Offset(12, 1))

        ..  container:: example

            **Example 3.** Overlapping timespans that start at different times:

            ::

                >>> division_1 = durationtools.Division(
                ...     (4, 1),
                ...     start_offset=Offset(10),
                ...     )
                >>> division_2 = durationtools.Division(
                ...     (4, 1),
                ...     start_offset=Offset(12),
                ...     )

            ::

                >>> division_1 - division_2
                Division((2, 1), start_offset=Offset(10, 1))

            ::

                >>> division_2 - division_1
                Division((2, 1), start_offset=Offset(14, 1))

        ..  container:: example

            **Example 4.** Nonoverlapping timespans:

            ::

                >>> division_1 = durationtools.Division(
                ...     (6, 2),
                ...     start_offset=Offset(0),
                ...     )
                >>> division_2 = durationtools.Division(
                ...     (4, 2),
                ...     start_offset=Offset(20),
                ...     )

            ::

                >>> division_1 - division_2
                Division((6, 2), start_offset=Offset(0, 1))

            ::

                >>> division_2 - division_1
                Division((4, 2), start_offset=Offset(20, 1))

        ..  container:: example

            **Exceptions.** Raises exception when one division has a start
            offset and the other does not:

            ::

                >>> division_1 = durationtools.Division(
                ...     (6, 4),
                ...     start_offset=Offset(5),
                ...     )
                >>> division_2 = durationtools.Division((2, 4))

            ::

                >>> division_1 - division_2
                Traceback (most recent call last):
                ...
                Exception: both divisions must have (or not have) start offsets.

            ::

                >>> division_2 - division_1
                Traceback (most recent call last):
                ...
                Exception: both divisions must have (or not have) start offsets.

        Uses timespan arithmetic when both divisions have a start offset.

        Returns new division.
        '''
        if not isinstance(expr, type(self)):
            expr = type(self)(expr, start_offset=self.start_offset)

        self_has_start_offset = bool(self.start_offset is not None)
        expr_has_start_offset = bool(expr.start_offset is not None)
        if not self_has_start_offset == expr_has_start_offset:
            message = 'both divisions must have (or not have) start offsets.'
            raise Exception(message)

        if self.start_offset is expr.start_offset is None:
            superclass = super(Division, self)
            difference = superclass.__sub__(expr)
            return self._from_pair(difference)

        my_timespan = self._to_timespan()
        expr_timespan = expr._to_timespan()
        inventory = my_timespan - expr_timespan

        negate_result = False
        if len(inventory) == 0:
            #message = 'subtraction destroys division.'
            #raise Exception(message)
            inventory = expr_timespan - my_timespan
            negate_result = True

        assert 0 < len(inventory), repr(inventory)
        if len(inventory) == 1:
            result_timespan = inventory[0]
            duration = result_timespan.duration
            nonreduced_fraction = duration.with_denominator(self.denominator)
            pair = nonreduced_fraction.pair
            start_offset = result_timespan.start_offset
            division = type(self)(pair, start_offset=start_offset)
            if negate_result:
                division = -division
            return division
        else:
            message = 'timespan subtraction creates more than one division.'
            raise Exception(message)

    ### PRIVATE METHODS ###

    def _from_pair(self, pair):
        return type(self)(pair, start_offset=self.start_offset)

    def _get_format_specification(self):
        return systemtools.FormatSpecification(
            client=self,
            repr_is_indented=False,
            storage_format_args_values=[self.pair],
            storage_format_kwargs_names=[
                'payload',
                'start_offset',
                ],
            )

    def _to_timespan(self):
        from abjad.tools import timespantools
        if self.start_offset is None:
            message = 'division must have start offset: {!r}.'
            message = message.format(self)
            raise Exception(message)
        stop_offset = self.start_offset + self
        return timespantools.Timespan(
            start_offset=self.start_offset,
            stop_offset=stop_offset,
            )

    ### PUBLIC PROPERTIES ###

    @property
    def duration(self):
        r'''Gets duration of division.

        ..  container:: example

            **Example 1.** Gets duration:

            ::

                >>> division = durationtools.Division((3, 8))

            ::

                >>> division.duration
                Duration(3, 8)

        ..  container:: example

            **Example 2.** Gets duration:

            ::

                >>> division = durationtools.Division((6, 4))

            ::

                >>> division.duration
                Duration(3, 2)

        Returns duration.
        '''
        from abjad.tools import durationtools
        return durationtools.Duration(self)

    @property
    def payload(self):
        r'''Gets payload of division.

        ..  container:: example

            **Example 1.** Division with payload:

            ::

                >>> division = durationtools.Division(
                ...     (3, 8),
                ...     payload=rhythmmakertools.NoteRhythmMaker(),
                ...     start_offset=Offset((5, 4)),
                ...     )

            ::

                >>> division.payload
                NoteRhythmMaker()

        ..  container:: example

            **Example 2.** Division without duration:

            ::

                >>> division = durationtools.Division(
                ...     (3, 8),
                ...     start_offset=Offset((5, 4)),
                ...     )

            ::

                >>> division.payload is None
                True

        Set to object or none.

        Defaults to none.

        Returns object or none.
        '''
        return self._payload

    @property
    def start_offset(self):
        r'''Gets start offset of division.

        ..  container:: example

            **Example 1.** Division with start offset:

            ::

                >>> division = durationtools.Division(
                ...     (3, 8),
                ...     start_offset=Offset((5, 4)),
                ...     )

            ::

                >>> division.start_offset
                Offset(5, 4)

        ..  container:: example

            **Example 2.** Division without start offset:

            ::

                >>> division = durationtools.Division((3, 8))

            ::

                >>> division.start_offset is None
                True

        Set to offset or none.

        Defaults to none.

        Returns offset or none.
        '''
        return self._start_offset

    @property
    def stop_offset(self):
        r'''Gets stop offset of division.

        ..  container:: example

            **Example 1.** Division with start offset:

            ::

                >>> division = durationtools.Division(
                ...     (3, 8),
                ...     start_offset=Offset((5, 4)),
                ...     )

            ::

                >>> division.stop_offset
                Offset(13, 8)

        ..  container:: example

            **Example 2.** Division without start offset:

            ::

                >>> division = durationtools.Division((3, 8))

            ::

                >>> division.stop_offset is None
                True

            Returns none when start offset is none.

        Returns offset or none.
        '''
        if self.start_offset is None:
            return
        return self.start_offset + self.duration
