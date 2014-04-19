# -*- encoding: utf-8 -*-
import copy
from abjad.tools import durationtools
from abjad.tools import sequencetools
from experimental.tools.musicexpressiontools.StartPositionedPayloadExpression \
    import StartPositionedPayloadExpression


class StartPositionedDivisionPayloadExpression(
    StartPositionedPayloadExpression):
    r'''Start-positioned division payload expression.

    ::

        >>> payload = [(6, 8), (6, 8), (3, 4)]
        >>> expression = \
        ...     musicexpressiontools.StartPositionedDivisionPayloadExpression(
        ...     payload, Offset(0))

    ::

        >>> print(format(expression))
        musicexpressiontools.StartPositionedDivisionPayloadExpression(
            payload=musicexpressiontools.DivisionList(
                [
                    musicexpressiontools.Division(
                        '[6, 8]',
                        start_offset=durationtools.Offset(0, 1),
                        ),
                    musicexpressiontools.Division(
                        '[6, 8]',
                        start_offset=durationtools.Offset(3, 4),
                        ),
                    musicexpressiontools.Division(
                        '[3, 4]',
                        start_offset=durationtools.Offset(3, 2),
                        ),
                    ],
                start_offset=durationtools.Offset(0, 1),
                ),
            start_offset=durationtools.Offset(0, 1),
            )

    Start-positioned division payload expressions are immutable.
    '''

    ### INITIALIZER ###

    def __init__(self, payload=None, start_offset=None, voice_name=None):
        from experimental.tools import musicexpressiontools
        payload = musicexpressiontools.DivisionList(
            payload,
            start_offset=start_offset,
            voice_name=voice_name,
            )
        StartPositionedPayloadExpression.__init__(
            self,
            payload=payload,
            start_offset=start_offset,
            voice_name=voice_name,
            )

    ### SPECIAL METHODS ###

    def __and__(self, timespan):
        r'''Keep intersection of start-positioned
        division payload expression and `timespan`.

        Example 1. Intersection on the left:

        ::

            >>> payload = [(6, 8), (6, 8), (3, 4)]
            >>> expression = musicexpressiontools.StartPositionedDivisionPayloadExpression(
            ...     payload, Offset(0))
            >>> result = expression & timespantools.Timespan(0, Offset(1, 8))

        ::

            >>> print(format(result))
            timespantools.TimespanInventory(
                [
                    musicexpressiontools.StartPositionedDivisionPayloadExpression(
                        payload=musicexpressiontools.DivisionList(
                            [
                                musicexpressiontools.Division(
                                    '[1, 8]',
                                    start_offset=durationtools.Offset(0, 1),
                                    ),
                                ],
                            start_offset=durationtools.Offset(0, 1),
                            ),
                        start_offset=durationtools.Offset(0, 1),
                        ),
                    ]
                )

        Example 2. Intersection on the right:

        ::

            >>> payload = [(6, 8), (6, 8), (3, 4)]
            >>> expression = musicexpressiontools.StartPositionedDivisionPayloadExpression(
            ...     payload, Offset(0))
            >>> result = expression & timespantools.Timespan(Offset(17, 8), 100)

        ::

            >>> print(format(result))
            timespantools.TimespanInventory(
                [
                    musicexpressiontools.StartPositionedDivisionPayloadExpression(
                        payload=musicexpressiontools.DivisionList(
                            [
                                musicexpressiontools.Division(
                                    '[1, 8]',
                                    start_offset=durationtools.Offset(17, 8),
                                    ),
                                ],
                            start_offset=durationtools.Offset(17, 8),
                            ),
                        start_offset=durationtools.Offset(17, 8),
                        ),
                    ]
                )

        Example 3. Trisection:

        ::

            >>> payload = [(6, 8), (6, 8), (3, 4)]
            >>> expression = musicexpressiontools.StartPositionedDivisionPayloadExpression(
            ...     payload, Offset(0))
            >>> result = expression & timespantools.Timespan(Offset(1, 8), Offset(17, 8))

        ::

            >>> print(format(result))
            timespantools.TimespanInventory(
                [
                    musicexpressiontools.StartPositionedDivisionPayloadExpression(
                        payload=musicexpressiontools.DivisionList(
                            [
                                musicexpressiontools.Division(
                                    '[5, 8]',
                                    start_offset=durationtools.Offset(1, 8),
                                    ),
                                musicexpressiontools.Division(
                                    '[6, 8]',
                                    start_offset=durationtools.Offset(3, 4),
                                    ),
                                musicexpressiontools.Division(
                                    '[5, 8]',
                                    start_offset=durationtools.Offset(3, 2),
                                    ),
                                ],
                            start_offset=durationtools.Offset(1, 8),
                            ),
                        start_offset=durationtools.Offset(1, 8),
                        ),
                    ]
                )

        Example 4. No intersection:

        ::

            >>> payload = [(6, 8), (6, 8), (3, 4)]
            >>> expression = musicexpressiontools.StartPositionedDivisionPayloadExpression(
            ...     payload, Offset(0))
            >>> result = expression & timespantools.Timespan(100, 200)

        ::

            >>> print(format(result))
            timespantools.TimespanInventory(
                []
                )

        Operates in place and returns timespan inventory.
        '''
        return StartPositionedPayloadExpression.__and__(self, timespan)

    def __format__(self, format_specification=''):
        r'''Formats start-positioned division payload expression.

        Set `format_specification` to `''` or `'storage'`.
        Interprets `''` equal to `'storage'`.

        ::

            >>> print(format(expression))
            musicexpressiontools.StartPositionedDivisionPayloadExpression(
                payload=musicexpressiontools.DivisionList(
                    [
                        musicexpressiontools.Division(
                            '[6, 8]',
                            start_offset=durationtools.Offset(0, 1),
                            ),
                        musicexpressiontools.Division(
                            '[6, 8]',
                            start_offset=durationtools.Offset(3, 4),
                            ),
                        musicexpressiontools.Division(
                            '[3, 4]',
                            start_offset=durationtools.Offset(3, 2),
                            ),
                        ],
                    start_offset=durationtools.Offset(0, 1),
                    ),
                start_offset=durationtools.Offset(0, 1),
                )

        Returns string.
        '''
        superclass = super(StartPositionedPayloadExpression, self)
        return superclass.__format__(format_specification=format_specification)

    def __getitem__(self, expr):
        r'''Get start-positioned division payload expression item.

        ::

            >>> result = expression[:2]

        ::

            >>> print(format(result))
            musicexpressiontools.StartPositionedDivisionPayloadExpression(
                payload=musicexpressiontools.DivisionList(
                    [
                        musicexpressiontools.Division(
                            '[6, 8]',
                            start_offset=durationtools.Offset(0, 1),
                            ),
                        musicexpressiontools.Division(
                            '[6, 8]',
                            start_offset=durationtools.Offset(3, 4),
                            ),
                        ],
                    start_offset=durationtools.Offset(0, 1),
                    ),
                start_offset=durationtools.Offset(0, 1),
                )

        Returns newly constructed start-positioned division payload expression.
        '''
        from experimental.tools import musicexpressiontools
        assert isinstance(expr, (slice, int)), repr(expr)
        result = self.payload.__getitem__(expr)
        if isinstance(result, list):
            divisions = result
        elif isinstance(result, musicexpressiontools.Division):
            divisions = [result]
        else:
            raise TypeError(result)
        if divisions:
            start_offset = divisions[0].start_offset
        else:
            start_offset = durationtools.Offset(0)
        result = type(self)(
            payload=divisions,
            voice_name=self.voice_name,
            start_offset=start_offset,
            )
        return result

    def __or__(self, expr):
        r'''Logical OR of two start-positioned division payload expressions:

        ::

            >>> expression_1 = musicexpressiontools.StartPositionedDivisionPayloadExpression(
            ...     2 * [(3, 16)], Offset(0))
            >>> timespan = timespantools.Timespan(Offset(6, 16))
            >>> expression_2 = musicexpressiontools.StartPositionedDivisionPayloadExpression(
            ...     2 * [(2, 16)], Offset(6, 16))

        ::

            >>> expression_1.timespan.stops_when_timespan_starts(expression_2)
            True

        ::

            >>> result = expression_1 | expression_2

        ::

            >>> print(format(result))
            timespantools.TimespanInventory(
                [
                    musicexpressiontools.StartPositionedDivisionPayloadExpression(
                        payload=musicexpressiontools.DivisionList(
                            [
                                musicexpressiontools.Division(
                                    '[3, 16]',
                                    start_offset=durationtools.Offset(0, 1),
                                    ),
                                musicexpressiontools.Division(
                                    '[3, 16]',
                                    start_offset=durationtools.Offset(3, 16),
                                    ),
                                musicexpressiontools.Division(
                                    '[2, 16]',
                                    start_offset=durationtools.Offset(3, 8),
                                    ),
                                musicexpressiontools.Division(
                                    '[2, 16]',
                                    start_offset=durationtools.Offset(1, 2),
                                    ),
                                ],
                            start_offset=durationtools.Offset(0, 1),
                            ),
                        start_offset=durationtools.Offset(0, 1),
                        ),
                    ]
                )

        Returns timespan inventory.
        '''
        return StartPositionedPayloadExpression.__or__(self, expr)

    def __sub__(self, timespan):
        r'''Subtract `timespan` from start-positioned division
        payload expression.

        Example 1. Subtract from left:

        ::

            >>> payload = [(6, 8), (6, 8), (3, 4)]
            >>> expression = musicexpressiontools.StartPositionedDivisionPayloadExpression(
            ...     payload, Offset(0))
            >>> result = expression - timespantools.Timespan(0, Offset(1, 8))

        ::

            >>> print(format(result))
            timespantools.TimespanInventory(
                [
                    musicexpressiontools.StartPositionedDivisionPayloadExpression(
                        payload=musicexpressiontools.DivisionList(
                            [
                                musicexpressiontools.Division(
                                    '[5, 8]',
                                    start_offset=durationtools.Offset(1, 8),
                                    ),
                                musicexpressiontools.Division(
                                    '[6, 8]',
                                    start_offset=durationtools.Offset(3, 4),
                                    ),
                                musicexpressiontools.Division(
                                    '[3, 4]',
                                    start_offset=durationtools.Offset(3, 2),
                                    ),
                                ],
                            start_offset=durationtools.Offset(1, 8),
                            ),
                        start_offset=durationtools.Offset(1, 8),
                        ),
                    ]
                )

        Example 2. Subtract from right:

        ::

            >>> payload = [(6, 8), (6, 8), (3, 4)]
            >>> expression = musicexpressiontools.StartPositionedDivisionPayloadExpression(
            ...     payload, Offset(0))
            >>> result = expression - timespantools.Timespan(Offset(17, 8), 100)

        ::

            >>> print(format(result))
            timespantools.TimespanInventory(
                [
                    musicexpressiontools.StartPositionedDivisionPayloadExpression(
                        payload=musicexpressiontools.DivisionList(
                            [
                                musicexpressiontools.Division(
                                    '[6, 8]',
                                    start_offset=durationtools.Offset(0, 1),
                                    ),
                                musicexpressiontools.Division(
                                    '[6, 8]',
                                    start_offset=durationtools.Offset(3, 4),
                                    ),
                                musicexpressiontools.Division(
                                    '[5, 8]',
                                    start_offset=durationtools.Offset(3, 2),
                                    ),
                                ],
                            start_offset=durationtools.Offset(0, 1),
                            ),
                        start_offset=durationtools.Offset(0, 1),
                        ),
                    ]
                )

        Example 3. Subtract from middle:

        ::

            >>> payload = [(6, 8), (6, 8), (3, 4)]
            >>> expression = musicexpressiontools.StartPositionedDivisionPayloadExpression(
            ...     payload, Offset(0))
            >>> result = expression - timespantools.Timespan(Offset(1, 8), Offset(17, 8))

        ::

            >>> print(format(result))
            timespantools.TimespanInventory(
                [
                    musicexpressiontools.StartPositionedDivisionPayloadExpression(
                        payload=musicexpressiontools.DivisionList(
                            [
                                musicexpressiontools.Division(
                                    '[1, 8]',
                                    start_offset=durationtools.Offset(0, 1),
                                    ),
                                ],
                            start_offset=durationtools.Offset(0, 1),
                            ),
                        start_offset=durationtools.Offset(0, 1),
                        ),
                    musicexpressiontools.StartPositionedDivisionPayloadExpression(
                        payload=musicexpressiontools.DivisionList(
                            [
                                musicexpressiontools.Division(
                                    '[1, 8]',
                                    start_offset=durationtools.Offset(17, 8),
                                    ),
                                ],
                            start_offset=durationtools.Offset(17, 8),
                            ),
                        start_offset=durationtools.Offset(17, 8),
                        ),
                    ]
                )

        Example 4. Subtract from nothing:

        ::

            >>> payload = [(6, 8), (6, 8), (3, 4)]
            >>> expression = musicexpressiontools.StartPositionedDivisionPayloadExpression(
            ...     payload, Offset(0))
            >>> result = expression - timespantools.Timespan(100, 200)

        ::

            >>> print(format(result))
            timespantools.TimespanInventory(
                [
                    musicexpressiontools.StartPositionedDivisionPayloadExpression(
                        payload=musicexpressiontools.DivisionList(
                            [
                                musicexpressiontools.Division(
                                    '[6, 8]',
                                    start_offset=durationtools.Offset(0, 1),
                                    ),
                                musicexpressiontools.Division(
                                    '[6, 8]',
                                    start_offset=durationtools.Offset(3, 4),
                                    ),
                                musicexpressiontools.Division(
                                    '[3, 4]',
                                    start_offset=durationtools.Offset(3, 2),
                                    ),
                                ],
                            start_offset=durationtools.Offset(0, 1),
                            ),
                        start_offset=durationtools.Offset(0, 1),
                        ),
                    ]
                )

        Operates in place and returns timespan inventory.
        '''
        return StartPositionedPayloadExpression.__sub__(self, timespan)

    ### PRIVATE METHODS ###

    def _split_payload_at_offsets(self, offsets):
        from experimental.tools import musicexpressiontools
        divisions = self.payload.divisions
        self._payload = musicexpressiontools.DivisionList(
            [], voice_name=self.voice_name, start_offset=self.start_offset)
        shards = sequencetools.split_sequence(
            divisions, offsets, cyclic=False, overhang=True)
        result, total_duration = [], durationtools.Duration(0)
        for shard in shards:
            shard = musicexpressiontools.DivisionList(
                shard, voice_name=self.voice_name, start_offset=total_duration)
            result.append(shard)
            total_duration += shard.duration
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def elements(self):
        r'''Start-positioned division payload expression elements.

        ::

            >>> expression.elements
            [Division('[6, 8]', start_offset=Offset(0, 1)),
            Division('[6, 8]', start_offset=Offset(3, 4)),
            Division('[3, 4]', start_offset=Offset(3, 2))]

        Returns list.
        '''
        return self.payload.divisions

    @property
    def elements_are_time_contiguous(self):
        r'''Is true when start-positioned division payload expression elements
        are time-contiguous. Otherwise false:

        ::

            >>> expression.elements_are_time_contiguous
            True

        Returns boolean.
        '''
        return StartPositionedPayloadExpression.elements_are_time_contiguous.fget(self)

    @property
    def payload(self):
        r'''Start-positioned division payload expression payload.

        ::

            >>> expression.payload
            DivisionList('[6, 8], [6, 8], [3, 4]')

        Returns division list.
        '''
        return StartPositionedPayloadExpression.payload.fget(self)

    @property
    def start_offset(self):
        r'''Start-positioned division payload expression start offset.

        ::

            >>> expression.start_offset
            Offset(0, 1)

        Returns offset.
        '''
        return StartPositionedPayloadExpression.start_offset.fget(self)

    @property
    def stop_offset(self):
        r'''Start-positioned division payload expression stop offset.

        ::

            >>> expression.stop_offset
            Offset(9, 4)

        Returns offset.
        '''
        return StartPositionedPayloadExpression.stop_offset.fget(self)

    @property
    def timespan(self):
        r'''Start-positioned division payload expression timespan.

        ::

            >>> expression.timespan
            Timespan(start_offset=Offset(0, 1), stop_offset=Offset(9, 4))

        Returns timespan.
        '''
        return StartPositionedPayloadExpression.timespan.fget(self)

    @property
    def voice_name(self):
        r'''Start-positioned division payload expression voice name.

        ::

            >>> expression.voice_name is None
            True

        Returns string.
        '''
        return StartPositionedPayloadExpression.voice_name.fget(self)

    ### PUBLIC METHODS ###

    def partition_by_ratio(self, ratio):
        r'''Partition start-positioned division payload expression by `ratio`.

        ::

            >>> payload = [(6, 8), (6, 8), (6, 8), (6, 8), (6, 4), (6, 4)]
            >>> expression = musicexpressiontools.StartPositionedDivisionPayloadExpression(
            ...     payload, Offset(0))

        ::

            >>> result = expression.partition_by_ratio((1, 1))

        ::

            >>> print(format(result))
            musicexpressiontools.TimespanScopedSingleContextSetExpressionInventory(
                [
                    musicexpressiontools.StartPositionedDivisionPayloadExpression(
                        payload=musicexpressiontools.DivisionList(
                            [
                                musicexpressiontools.Division(
                                    '[6, 8]',
                                    start_offset=durationtools.Offset(0, 1),
                                    ),
                                musicexpressiontools.Division(
                                    '[6, 8]',
                                    start_offset=durationtools.Offset(3, 4),
                                    ),
                                musicexpressiontools.Division(
                                    '[6, 8]',
                                    start_offset=durationtools.Offset(3, 2),
                                    ),
                                ],
                            start_offset=durationtools.Offset(0, 1),
                            ),
                        start_offset=durationtools.Offset(0, 1),
                        ),
                    musicexpressiontools.StartPositionedDivisionPayloadExpression(
                        payload=musicexpressiontools.DivisionList(
                            [
                                musicexpressiontools.Division(
                                    '[6, 8]',
                                    start_offset=durationtools.Offset(9, 4),
                                    ),
                                musicexpressiontools.Division(
                                    '[6, 4]',
                                    start_offset=durationtools.Offset(3, 1),
                                    ),
                                musicexpressiontools.Division(
                                    '[6, 4]',
                                    start_offset=durationtools.Offset(9, 2),
                                    ),
                                ],
                            start_offset=durationtools.Offset(9, 4),
                            ),
                        start_offset=durationtools.Offset(9, 4),
                        ),
                    ]
                )

        Operates in place and returns newly constructed inventory.
        '''
        return StartPositionedPayloadExpression.partition_by_ratio(self, ratio)

    def partition_by_ratio_of_durations(self, ratio):
        r'''Partition start-positioned division payload expression by
        `ratio` of durations.

        ::

            >>> payload = [(6, 8), (6, 8), (6, 8), (6, 8), (6, 4), (6, 4)]
            >>> expression = musicexpressiontools.StartPositionedDivisionPayloadExpression(
            ...     payload, Offset(0))

        ::

            >>> result = expression.partition_by_ratio_of_durations((1, 1))

        ::

            >>> print(format(result))
            musicexpressiontools.TimespanScopedSingleContextSetExpressionInventory(
                [
                    musicexpressiontools.StartPositionedDivisionPayloadExpression(
                        payload=musicexpressiontools.DivisionList(
                            [
                                musicexpressiontools.Division(
                                    '[6, 8]',
                                    start_offset=durationtools.Offset(0, 1),
                                    ),
                                musicexpressiontools.Division(
                                    '[6, 8]',
                                    start_offset=durationtools.Offset(3, 4),
                                    ),
                                musicexpressiontools.Division(
                                    '[6, 8]',
                                    start_offset=durationtools.Offset(3, 2),
                                    ),
                                musicexpressiontools.Division(
                                    '[6, 8]',
                                    start_offset=durationtools.Offset(9, 4),
                                    ),
                                ],
                            start_offset=durationtools.Offset(0, 1),
                            ),
                        start_offset=durationtools.Offset(0, 1),
                        ),
                    musicexpressiontools.StartPositionedDivisionPayloadExpression(
                        payload=musicexpressiontools.DivisionList(
                            [
                                musicexpressiontools.Division(
                                    '[6, 4]',
                                    start_offset=durationtools.Offset(3, 1),
                                    ),
                                musicexpressiontools.Division(
                                    '[6, 4]',
                                    start_offset=durationtools.Offset(9, 2),
                                    ),
                                ],
                            start_offset=durationtools.Offset(3, 1),
                            ),
                        start_offset=durationtools.Offset(3, 1),
                        ),
                    ]
                )

        Operates in place and returns newly constructed inventory.
        '''
        return StartPositionedPayloadExpression.partition_by_ratio_of_durations(self, ratio)

    def reflect(self):
        r'''Reflect start-positioned division payload expression about axis.

        ::

            >>> payload = [(6, 8), (6, 8), (3, 4)]
            >>> expression = musicexpressiontools.StartPositionedDivisionPayloadExpression(
            ...     payload, Offset(0))

        ::

            >>> result = expression.reflect()

        ::

            >>> print(format(expression))
            musicexpressiontools.StartPositionedDivisionPayloadExpression(
                payload=musicexpressiontools.DivisionList(
                    [
                        musicexpressiontools.Division(
                                '[3, 4]',
                                start_offset=durationtools.Offset(0, 1),
                                ),
                        musicexpressiontools.Division(
                                '[6, 8]',
                                start_offset=durationtools.Offset(3, 4),
                                ),
                        musicexpressiontools.Division(
                                '[6, 8]',
                                start_offset=durationtools.Offset(3, 2),
                                ),
                        ],
                    start_offset=durationtools.Offset(0, 1),
                    ),
                start_offset=durationtools.Offset(0, 1),
                )

        Operates in place and returns division payload expression.
        '''
        return StartPositionedPayloadExpression.reflect(self)

    def repeat_to_duration(self, duration):
        r'''Repeat start-positioned division payload expression to `duration`.

        ::

            >>> payload = [(6, 8), (6, 8), (3, 4)]
            >>> expression = musicexpressiontools.StartPositionedDivisionPayloadExpression(
            ...     payload, Offset(0))

        ::

            >>> result = expression.repeat_to_duration(Duration(13, 4))

        ::

            >>> print(format(result))
            musicexpressiontools.StartPositionedDivisionPayloadExpression(
                payload=musicexpressiontools.DivisionList(
                    [
                        musicexpressiontools.Division(
                                '[6, 8]',
                                start_offset=durationtools.Offset(0, 1),
                                ),
                        musicexpressiontools.Division(
                                '[6, 8]',
                                start_offset=durationtools.Offset(3, 4),
                                ),
                        musicexpressiontools.Division(
                                '[3, 4]',
                                start_offset=durationtools.Offset(3, 2),
                                ),
                        musicexpressiontools.Division(
                                '[6, 8]',
                                start_offset=durationtools.Offset(9, 4),
                                ),
                        musicexpressiontools.Division(
                                '[2, 8]',
                                start_offset=durationtools.Offset(3, 1),
                                ),
                        ],
                    start_offset=durationtools.Offset(0, 1),
                    ),
                start_offset=durationtools.Offset(0, 1),
                )

        Returns newly constructed start-positioned division payload expression.
        '''
        divisions = sequencetools.repeat_sequence_to_weight(self.payload, duration)
        result = type(self)(payload=divisions, voice_name=self.voice_name, start_offset=self.start_offset)
        return result

    def repeat_to_length(self, length):
        r'''Repeat start-positioned division payload expression to `length`.

        ::

            >>> payload = [(6, 8), (6, 8), (3, 4)]
            >>> expression = musicexpressiontools.StartPositionedDivisionPayloadExpression(
            ...     payload, Offset(0))

        ::

            >>> result = expression.repeat_to_length(5)

        ::

            >>> print(format(result))
            musicexpressiontools.StartPositionedDivisionPayloadExpression(
                payload=musicexpressiontools.DivisionList(
                    [
                        musicexpressiontools.Division(
                                '[6, 8]',
                                start_offset=durationtools.Offset(0, 1),
                                ),
                        musicexpressiontools.Division(
                                '[6, 8]',
                                start_offset=durationtools.Offset(3, 4),
                                ),
                        musicexpressiontools.Division(
                                '[3, 4]',
                                start_offset=durationtools.Offset(3, 2),
                                ),
                        musicexpressiontools.Division(
                                '[6, 8]',
                                start_offset=durationtools.Offset(9, 4),
                                ),
                        musicexpressiontools.Division(
                                '[6, 8]',
                                start_offset=durationtools.Offset(3, 1),
                                ),
                        ],
                    start_offset=durationtools.Offset(0, 1),
                    ),
                start_offset=durationtools.Offset(0, 1),
                )

        Returns newly constructed start-positioned division payload expression.
        '''
        divisions = sequencetools.repeat_sequence_to_length(self.payload, length)
        result = type(self)(payload=divisions, voice_name=self.voice_name, start_offset=self.start_offset)
        return result

    def rotate(self, rotation):
        r'''Rotate start-positioned division payload expression by `rotation`.

        ::

            >>> payload = [(6, 8), (6, 8), (3, 4)]
            >>> expression = musicexpressiontools.StartPositionedDivisionPayloadExpression(
            ...     payload, Offset(0))

        ::

            >>> result = expression.rotate(-1)

        ::

            >>> print(format(expression))
            musicexpressiontools.StartPositionedDivisionPayloadExpression(
                payload=musicexpressiontools.DivisionList(
                    [
                        musicexpressiontools.Division(
                                '[6, 8]',
                                start_offset=durationtools.Offset(0, 1),
                                ),
                        musicexpressiontools.Division(
                                '[3, 4]',
                                start_offset=durationtools.Offset(3, 4),
                                ),
                        musicexpressiontools.Division(
                                '[6, 8]',
                                start_offset=durationtools.Offset(3, 2),
                                ),
                        ],
                    start_offset=durationtools.Offset(0, 1),
                    ),
                start_offset=durationtools.Offset(0, 1),
                )

        Operates in place and returns division payload expression.
        '''
        return StartPositionedPayloadExpression.rotate(self, rotation)

    def translate(self, translation):
        r'''Translate division payload expression by `translation`.

        ::

            >>> payload = [(6, 8), (6, 8), (3, 4)]
            >>> expression = musicexpressiontools.StartPositionedDivisionPayloadExpression(
            ...     payload, Offset(0))

        ::

            >>> result = expression.translate(10)

        ::

            >>> print(format(result))
            musicexpressiontools.StartPositionedDivisionPayloadExpression(
                payload=musicexpressiontools.DivisionList(
                    [
                        musicexpressiontools.Division(
                            '[6, 8]',
                            start_offset=durationtools.Offset(10, 1),
                            ),
                        musicexpressiontools.Division(
                            '[6, 8]',
                            start_offset=durationtools.Offset(43, 4),
                            ),
                        musicexpressiontools.Division(
                            '[3, 4]',
                            start_offset=durationtools.Offset(23, 2),
                            ),
                        ],
                    start_offset=durationtools.Offset(10, 1),
                    ),
                start_offset=durationtools.Offset(10, 1),
                )

        Operates in place and returns division payload expression.
        '''
        new_start_offset = self.start_offset + translation
        result = type(self)(
            self.payload.divisions,
            voice_name=self.voice_name,
            start_offset=new_start_offset,
            )
        return result
