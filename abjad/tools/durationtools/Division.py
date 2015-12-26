# -*- coding: utf-8 -*-
from abjad.tools import mathtools
from abjad.tools.abctools.AbjadObject import AbjadObject
from abjad.tools.topleveltools.override import override
from abjad.tools.topleveltools.set_ import set_


class Division(AbjadObject):
    r'''A division.

    ..  container:: example

        **Example 1.** Division with duration, start offset and payload:

        ::

            >>> division = durationtools.Division(
            ...     duration=Duration((3, 8)),
            ...     payload=rhythmmakertools.NoteRhythmMaker(),
            ...     start_offset=Offset((5, 4)),
            ...     )

        ::

            >>> print(format(division))
            durationtools.Division(
                duration=durationtools.Duration(3, 8),
                payload=rhythmmakertools.NoteRhythmMaker(),
                start_offset=durationtools.Offset(5, 4),
                )

    ..  container:: example

        **Example 2.** Division with duration and start offset:

        ::

            >>> division = durationtools.Division(
            ...     duration=Duration((3, 8)),
            ...     start_offset=Offset((5, 4)),
            ...     )

        ::

            >>> print(format(division))
            durationtools.Division(
                duration=durationtools.Duration(3, 8),
                start_offset=durationtools.Offset(5, 4),
                )

    ..  container:: example

        **Example 3.** Division with duration:

        ::

            >>> division = durationtools.Division(
            ...     duration=Duration((3, 8)),
            ...     )

        ::

            >>> print(format(division))
            durationtools.Division(
                duration=durationtools.Duration(3, 8),
                )

    ..  container:: example

        **Example 4.** Makes divisions from durations:

        ::

            >>> durations = 10 * [Duration(1, 8)]
            >>> start_offsets = mathtools.cumulative_sums(durations)[:-1]
            >>> divisions = []
            >>> for duration, start_offset in zip(durations, start_offsets):
            ...     division = durationtools.Division(
            ...         duration=duration,
            ...         start_offset=start_offset,
            ...         )
            ...     divisions.append(division)

        ::

            >>> for division in divisions:
            ...     print(division)
            Division(duration=Duration(1, 8), start_offset=Offset(0, 1))
            Division(duration=Duration(1, 8), start_offset=Offset(1, 8))
            Division(duration=Duration(1, 8), start_offset=Offset(1, 4))
            Division(duration=Duration(1, 8), start_offset=Offset(3, 8))
            Division(duration=Duration(1, 8), start_offset=Offset(1, 2))
            Division(duration=Duration(1, 8), start_offset=Offset(5, 8))
            Division(duration=Duration(1, 8), start_offset=Offset(3, 4))
            Division(duration=Duration(1, 8), start_offset=Offset(7, 8))
            Division(duration=Duration(1, 8), start_offset=Offset(1, 1))
            Division(duration=Duration(1, 8), start_offset=Offset(9, 8))

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
            Division(duration=Duration(1, 8), start_offset=Offset(3, 8))
            Division(duration=Duration(1, 8), start_offset=Offset(1, 2))
            Division(duration=Duration(1, 8), start_offset=Offset(5, 8))
            Division(duration=Duration(1, 8), start_offset=Offset(3, 4))

        Gets start offset of middle third:

        ::

            >>> parts[1][0].start_offset
            Offset(3, 8)
            
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_duration',
        '_payload',
        '_start_offset',
        )

    ### INITIALIZER ###

    def __init__(
        self, 
        duration=None, 
        payload=None, 
        start_offset=None,
        ):
        from abjad.tools import durationtools
        if duration is not None:
            duration = durationtools.Duration(duration)
        self._duration = duration
        self._payload = payload
        if start_offset is not None:
            start_offset = durationtools.Offset(start_offset)
        self._start_offset = start_offset

    ### PUBLIC PROPERTIES ###

    @property
    def duration(self):
        r'''Gets duration of division.

        ..  container:: example

            **Example 1.** Division with duration:

            ::

                >>> division = durationtools.Division(
                ...     duration=Duration((3, 8)),
                ...     )

            ::

                >>> division.duration
                Duration(3, 8)

        ..  container:: example

            **Example 2.** Division without duration:

            ::

                >>> division = durationtools.Division()

            ::

                >>> division.duration is None
                True

        Set to duration or none.

        Defaults to none.

        Returns duration or none.
        '''
        return self._duration        

    @property
    def payload(self):
        r'''Gets payload of division.

        ..  container:: example

            **Example 1.** Division with payload:

            ::

                >>> division = durationtools.Division(
                ...     duration=Duration((3, 8)),
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
                ...     duration=Duration((3, 8)),
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
                ...     duration=Duration((3, 8)),
                ...     start_offset=Offset((5, 4)),
                ...     )

            ::

                >>> division.start_offset
                Offset(5, 4)

        ..  container:: example

            **Example 2.** Division without start offset:

            ::

                >>> division = durationtools.Division(
                ...     duration=Duration((3, 8)),
                ...     )

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
                ...     duration=Duration((3, 8)),
                ...     start_offset=Offset((5, 4)),
                ...     )

            ::

                >>> division.stop_offset
                Offset(13, 8)

        ..  container:: example

            **Example 2.** Division without start offset:

            ::

                >>> division = durationtools.Division(
                ...     duration=Duration((3, 8)),
                ...     )

            ::

                >>> division.stop_offset is None
                True

            Returns none when start offset is none.

        ..  container:: example

            **Example 3.** Division without duration

            ::

                >>> division = durationtools.Division(
                ...     start_offset=Offset((5, 4)),
                ...     )

            ::

                >>> division.stop_offset is None
                True

            Returns none when duration is none.

        Returns offset or none.
        '''
        if self.duration is None:
            return
        if self.start_offset is None:
            return
        return self.start_offset + self.duration