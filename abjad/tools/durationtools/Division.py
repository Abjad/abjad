# -*- coding: utf-8 -*-
from abjad.tools import mathtools
from abjad.tools.mathtools.NonreducedFraction import NonreducedFraction
from abjad.tools.topleveltools.override import override
from abjad.tools.topleveltools.set_ import set_


class Division(NonreducedFraction):
    r'''A division.

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
            >>> parts = sequencetools.partition_sequence_by_ratio_of_lengths(
            ...     divisions,
            ...     ratio,
            ...     )

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
        r'''Add `expr` to division.

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

    def __repr__(self):
        r'''Gets interpreter representation of division.

        Returns string.
        '''
        from abjad.tools import systemtools
        return systemtools.StorageFormatManager.get_repr_format(self)

    def __str__(self):
        r'''Gets string representation of division.

        Returns string.
        '''
        return repr(self)

    ### PRIVATE PROPERTIES ###

    @property
    def _storage_format_specification(self):
        from abjad.tools import systemtools
        return systemtools.StorageFormatSpecification(
            self,
            keyword_argument_names=(
                'payload',
                'start_offset',
                ),
            positional_argument_values=(
                self.pair,
                ),
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