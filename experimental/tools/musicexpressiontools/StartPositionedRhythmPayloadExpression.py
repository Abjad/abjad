# -*- encoding: utf-8 -*-
import copy
import math
from abjad.tools import datastructuretools
from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import scoretools
from abjad.tools import sequencetools
from abjad.tools import spannertools
from abjad.tools import timespantools
from abjad.tools.topleveltools import inspect_
from abjad.tools.topleveltools import iterate
from abjad.tools.topleveltools import mutate
from experimental.tools.musicexpressiontools.StartPositionedPayloadExpression \
    import StartPositionedPayloadExpression


class StartPositionedRhythmPayloadExpression(StartPositionedPayloadExpression):
    r'''Start-positioned rhythm payload expression.

    ::

        >>> payload = [Container("c'8 d'8 e'8 f'8")]
        >>> expression = musicexpressiontools.StartPositionedRhythmPayloadExpression(
        ...     payload, Offset(10))

    ::

        >>> print(format(expression))
        musicexpressiontools.StartPositionedRhythmPayloadExpression(
            payload=scoretools.Container(
                "{ c'8 d'8 e'8 f'8 }"
                ),
            start_offset=durationtools.Offset(10, 1),
            )

    Start-positioned rhythm payload expressions are immutable.
    '''

    ### INITIALIZER ###

    def __init__(self, payload=None, start_offset=None, voice_name=None):
        from abjad.tools import lilypondfiletools
        if isinstance(payload, lilypondfiletools.LilyPondFile):
            payload = payload.items[:]
        payload = scoretools.Container(music=payload)
        StartPositionedPayloadExpression.__init__(
            self,
            payload=payload,
            start_offset=start_offset,
            voice_name=voice_name,
            )

    ### SPECIAL METHODS ###

    def __and__(self, timespan):
        r'''Intersection start-positioned rhythm payload expression
        and `timespan`.

        Example 1. Intersection on the left:

        ::

            >>> payload = [Container("c'8 d'8 e'8 f'8")]
            >>> expression = \
            ...     musicexpressiontools.StartPositionedRhythmPayloadExpression(
            ...     payload, Offset(0))
            >>> result = expression & timespantools.Timespan(
            ...     Offset(-1, 8), Offset(3, 8))

        ::

            >>> print(format(result))
            timespantools.TimespanInventory(
                [
                    musicexpressiontools.StartPositionedRhythmPayloadExpression(
                        payload=scoretools.Container(
                            "{ c'8 d'8 e'8 }"
                            ),
                        start_offset=durationtools.Offset(0, 1),
                        ),
                    ]
                )

        Example 2. Intersection on the right:

        ::

            >>> payload = [Container("c'8 d'8 e'8 f'8")]
            >>> expression = \
            ...     musicexpressiontools.StartPositionedRhythmPayloadExpression(
            ...     payload, Offset(0))
            >>> result = expression & timespantools.Timespan(
            ...     Offset(1, 8), Offset(5, 8))

        ::

            >>> print(format(result))
            timespantools.TimespanInventory(
                [
                    musicexpressiontools.StartPositionedRhythmPayloadExpression(
                        payload=scoretools.Container(
                            "{ d'8 e'8 f'8 }"
                            ),
                        start_offset=durationtools.Offset(1, 8),
                        ),
                    ]
                )

        Example 3. Trisection:

        ::

            >>> payload = [Container("c'8 d'8 e'8 f'8")]
            >>> expression = musicexpressiontools.StartPositionedRhythmPayloadExpression(payload, Offset(0))
            >>> result = expression & timespantools.Timespan(Offset(1, 8), Offset(3, 8))

        ::

            >>> print(format(result))
            timespantools.TimespanInventory(
                [
                    musicexpressiontools.StartPositionedRhythmPayloadExpression(
                        payload=scoretools.Container(
                            "{ d'8 e'8 }"
                            ),
                        start_offset=durationtools.Offset(1, 8),
                        ),
                    ]
                )

        Example 4. No intersection:

        ::

            >>> payload = [Container("c'8 d'8 e'8 f'8")]
            >>> expression = musicexpressiontools.StartPositionedRhythmPayloadExpression(payload, Offset(0))
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
        r'''Formats start-positioned rhythm payload expression.

        Set `format_specification` to `''` or `'storage'`.
        Interprets `''` equal to `'storage'`.

        ::

            >>> print(format(expression))
            musicexpressiontools.StartPositionedRhythmPayloadExpression(
                payload=scoretools.Container(
                    "{ c'8 d'8 e'8 f'8 }"
                    ),
                start_offset=durationtools.Offset(0, 1),
                )

        Returns string.
        '''
        superclass = super(StartPositionedPayloadExpression, self)
        return superclass.__format__(format_specification=format_specification)

    def __getitem__(self, expr):
        r'''Get start-positioned rhythm payload expression item.

        ::

            >>> result = expression[:2]

        ::

            >>> print(format(result))
            musicexpressiontools.StartPositionedRhythmPayloadExpression(
                payload=scoretools.Container(
                    "{ c'8 d'8 }"
                    ),
                start_offset=durationtools.Offset(0, 1),
                )

        Returns newly constructed start-positioned rhythm payload expression.
        '''
        assert isinstance(expr, slice), repr(expr)
        leaves = self.payload.select_leaves().__getitem__(expr)
        start_offset = leaves[0]._get_timespan().start_offset
        stop_offset = leaves[-1]._get_timespan().stop_offset
        timespan = timespantools.Timespan(start_offset, stop_offset)
        timespan = timespan.translate(self.start_offset)
        result = self & timespan
        assert len(result) == 1, repr(result)
        result = result[0]
        return result

    def __len__(self):
        r'''Start-positioned rhythm payload expression length.

        ::

            >>> payload = [Container("c'8 d'8 e'8 f'8")]
            >>> expression = \
            ...     musicexpressiontools.StartPositionedRhythmPayloadExpression(
            ...     payload, Offset(10))

        ::

            >>> len(expression)
            4

        Returns nonnegative integer.
        '''
        return len(self.payload.select_leaves())

    def __or__(self, expr):
        r'''Logical OR of two start-positioned rhythm payload expressions:

        ::

            >>> payload = [Container("c'8 d'8 e'8 f'8")]
            >>> expression_1 = \
            ...     musicexpressiontools.StartPositionedRhythmPayloadExpression(
            ...     payload, Offset(0))

        ::

            >>> payload = [Container("g'8 a'8 b'8 c''8")]
            >>> expression_2 = \
            ...     musicexpressiontools.StartPositionedRhythmPayloadExpression(
            ...     payload, Offset(4, 8))

        ::

            >>> expression_1.timespan.stops_when_timespan_starts(expression_2)
            True

        ::

            >>> result = expression_1 | expression_2

        ::

            >>> print(format(result))
            timespantools.TimespanInventory(
                [
                    musicexpressiontools.StartPositionedRhythmPayloadExpression(
                        payload=scoretools.Container(
                            "{ c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8 }"
                            ),
                        start_offset=durationtools.Offset(0, 1),
                        ),
                    ]
                )

        Leave start-positioned rhythm payload expression unchanged:

        ::

            >>> print(format(expression_1))
            musicexpressiontools.StartPositionedRhythmPayloadExpression(
                payload=scoretools.Container(
                    "{ c'8 d'8 e'8 f'8 }"
                    ),
                start_offset=durationtools.Offset(0, 1),
                )

        Leave `expr` unchanged:

        ::

            >>> print(format(expression_2))
            musicexpressiontools.StartPositionedRhythmPayloadExpression(
                payload=scoretools.Container(
                    "{ g'8 a'8 b'8 c''8 }"
                    ),
                start_offset=durationtools.Offset(1, 2),
                )

        Returns timespan inventory.
        '''
        return StartPositionedPayloadExpression.__or__(self, expr)

    def __sub__(self, timespan):
        r'''Subtract `timespan` from start-positioned rhythm payload
        expression.

        Example 1. Subtract from left:

        ::

            >>> payload = [Container("c'8 d'8 e'8 f'8")]
            >>> expression = \
            ...     musicexpressiontools.StartPositionedRhythmPayloadExpression(
            ...     payload, Offset(0))
            >>> result = expression - timespantools.Timespan(0, Offset(1, 8))

        ::

                >>> print(format(result))
                timespantools.TimespanInventory(
                    [
                        musicexpressiontools.StartPositionedRhythmPayloadExpression(
                            payload=scoretools.Container(
                                "{ d'8 e'8 f'8 }"
                                ),
                            start_offset=durationtools.Offset(1, 8),
                            ),
                        ]
                    )

        Example 2. Subtract from right:

        ::

            >>> payload = [Container("c'8 d'8 e'8 f'8")]
            >>> expression = \
            ...     musicexpressiontools.StartPositionedRhythmPayloadExpression(
            ...     payload, Offset(0))
            >>> result = expression - timespantools.Timespan(Offset(3, 8), 100)

        ::

            >>> print(format(result))
            timespantools.TimespanInventory(
                [
                    musicexpressiontools.StartPositionedRhythmPayloadExpression(
                        payload=scoretools.Container(
                            "{ c'8 d'8 e'8 }"
                            ),
                        start_offset=durationtools.Offset(0, 1),
                        ),
                    ]
                )

        Example 3. Subtract from middle:

        ::

            >>> payload = [Container("c'8 d'8 e'8 f'8")]
            >>> expression = \
            ...     musicexpressiontools.StartPositionedRhythmPayloadExpression(
            ...     payload, Offset(0))
            >>> result = expression - timespantools.Timespan(
            ...     Offset(1, 8), Offset(3, 8))

        ::

            >>> print(format(result))
            timespantools.TimespanInventory(
                [
                    musicexpressiontools.StartPositionedRhythmPayloadExpression(
                        payload=scoretools.Container(
                            "{ c'8 }"
                            ),
                        start_offset=durationtools.Offset(0, 1),
                        ),
                    musicexpressiontools.StartPositionedRhythmPayloadExpression(
                        payload=scoretools.Container(
                            "{ f'8 }"
                            ),
                        start_offset=durationtools.Offset(3, 8),
                        ),
                    ]
                )

        Example 4. Subtract nothing:

        ::

            >>> payload = [Container("c'8 d'8 e'8 f'8")]
            >>> expression = \
            ...     musicexpressiontools.StartPositionedRhythmPayloadExpression(
            ...     payload, Offset(0))
            >>> result = expression - timespantools.Timespan(100, 200)

        ::

            >>> print(format(result))
            timespantools.TimespanInventory(
                [
                    musicexpressiontools.StartPositionedRhythmPayloadExpression(
                        payload=scoretools.Container(
                            "{ c'8 d'8 e'8 f'8 }"
                            ),
                        start_offset=durationtools.Offset(0, 1),
                        ),
                    ]
                )

        Operates in place and returns timespan inventory.
        '''
        return StartPositionedPayloadExpression.__sub__(self, timespan)

    ### PRIVATE PROPERTIES ###

    @property
    def _duration(self):
        return self.payload._get_duration()

    ### PRIVATE METHODS ###

    def _clone(self):
        wrapped_component = copy.deepcopy(self.payload)
        new = type(self)(
            [],
            start_offset=self.start_offset,
            voice_name=self.voice_name,
            )
        new._payload = wrapped_component
        return new

    def _split_payload_at_offsets(self, offsets):
        assert isinstance(self.payload, scoretools.Container)
        music = self.payload
        self._payload = scoretools.Container()
        shards = mutate([music]).split(
            offsets,
            cyclic=False,
            fracture_spanners=True,
            )
        shards = [shard[0] for shard in shards]
        for shard in shards:
            if not inspect_(shard).is_well_formed():
                inspect_(shard).tabulate_well_formedness_violations_in_expr()
        return shards

    ### PUBLIC PROPERTIES ###

    @property
    def elements(self):
        r'''Start-positioned rhythm payload expression elements.

        ::

            >>> expression.elements
            ContiguousSelection(Note("c'8"), Note("d'8"), Note("e'8"), Note("f'8"))

        Returns leaf selection.
        '''
        return self.payload.select_leaves()

    @property
    def elements_are_time_contiguous(self):
        r'''Is true when start-positioned rhythm payload expression
        elements are time-contiguous. Otherwise false:

        ::

            >>> expression.elements_are_time_contiguous
            True

        Returns boolean.
        '''
        return StartPositionedPayloadExpression.elements_are_time_contiguous.fget(self)

    @property
    def payload(self):
        r'''Start-positioned rhythm payload expression payload.

        ::

            >>> expression.payload
            Container('Container("c\'8 d\'8 e\'8 f\'8")')

        Returns container.
        '''
        return StartPositionedPayloadExpression.payload.fget(self)

    @property
    def start_offset(self):
        r'''Start-positioned rhythm payload expression start offset.

        ::

            >>> expression.start_offset
            Offset(0, 1)

        Returns offset.
        '''
        return StartPositionedPayloadExpression.start_offset.fget(self)

    @property
    def stop_offset(self):
        r'''Start-positioned rhythm payload expression stop offset.

        ::

            >>> expression.stop_offset
            Offset(1, 2)

        Returns offset.
        '''
        return StartPositionedPayloadExpression.stop_offset.fget(self)

    @property
    def timespan(self):
        r'''Start-positioned rhythm payload expression timespan.

        ::

            >>> expression.timespan
            Timespan(start_offset=Offset(0, 1), stop_offset=Offset(1, 2))

        Returns timespan.
        '''
        return StartPositionedPayloadExpression.timespan.fget(self)

    @property
    def voice_name(self):
        r'''Start-positioned rhythm payload expression voice name.

        ::

            >>> expression.voice_name is None
            True

        Returns string.
        '''
        return StartPositionedPayloadExpression.voice_name.fget(self)

    ### PUBLIC METHODS ###

    def partition_by_ratio(self, ratio):
        r'''Partition start-positioned rhythm payload expression by `ratio`:

        ::

            >>> payload = [Container("c'8 d'8 e'8 f'8")]
            >>> expression = \
            ...     musicexpressiontools.StartPositionedRhythmPayloadExpression(
            ...     payload, Offset(10))

        ::

            >>> result = expression.partition_by_ratio((1, 2, 1))

        ::

            >>> print(format(result))
            musicexpressiontools.TimespanScopedSingleContextSetExpressionInventory(
                [
                    musicexpressiontools.StartPositionedRhythmPayloadExpression(
                        payload=scoretools.Container(
                            "{ c'8 }"
                            ),
                        start_offset=durationtools.Offset(10, 1),
                        ),
                    musicexpressiontools.StartPositionedRhythmPayloadExpression(
                        payload=scoretools.Container(
                            "{ d'8 e'8 }"
                            ),
                        start_offset=durationtools.Offset(81, 8),
                        ),
                    musicexpressiontools.StartPositionedRhythmPayloadExpression(
                        payload=scoretools.Container(
                            "{ f'8 }"
                            ),
                        start_offset=durationtools.Offset(83, 8),
                        ),
                    ]
                )

        Operates in place and returns newly constructed region expression inventory.
        '''
        return StartPositionedPayloadExpression.partition_by_ratio(self, ratio)

    def partition_by_ratio_of_durations(self, ratio):
        r'''Partition start-positioned rhythm payload expression
        by `ratio` of durations.

        ::

            >>> payload = [Container("c'2 d'8 e'8 f'4")]
            >>> expression = \
            ...     musicexpressiontools.StartPositionedRhythmPayloadExpression(
            ...     payload, Offset(10))

        ::

            >>> result = expression.partition_by_ratio_of_durations((1, 1))

        ::

            >>> print(format(result))
            musicexpressiontools.TimespanScopedSingleContextSetExpressionInventory(
                [
                    musicexpressiontools.StartPositionedRhythmPayloadExpression(
                        payload=scoretools.Container(
                            "{ c'2 }"
                            ),
                        start_offset=durationtools.Offset(10, 1),
                        ),
                    musicexpressiontools.StartPositionedRhythmPayloadExpression(
                        payload=scoretools.Container(
                            "{ d'8 e'8 f'4 }"
                            ),
                        start_offset=durationtools.Offset(21, 2),
                        ),
                    ]
                )

        Operates in place and returns newly constructed region
        expression inventory.
        '''
        return StartPositionedPayloadExpression.partition_by_ratio_of_durations(
            self, ratio)

    def reflect(self):
        r'''Reflect start-positioned rhythm payload expression about axis.

        ::

            >>> payload = [Container("c'8 d'8 e'8 f'8")]
            >>> expression = \
            ...     musicexpressiontools.StartPositionedRhythmPayloadExpression(
            ...     payload, Offset(0))

        ::

            >>> result = expression.reflect()

        ::

            >>> print(format(expression))
            musicexpressiontools.StartPositionedRhythmPayloadExpression(
                payload=scoretools.Container(
                    "{ f'8 e'8 d'8 c'8 }"
                    ),
                start_offset=durationtools.Offset(0, 1),
                )

        Operates in place and returns start-positioned rhythm
        payload expression.
        '''
        for container in iterate(self.payload).by_class(scoretools.Container):
            container._music.reverse()
        for spanner in self.payload._get_descendants().get_spanners():
            spanner._reverse_components()
        return self

    def repeat_to_duration(self, duration):
        r'''Repeat start-positioned rhythm payload expression to `duration`.

        Example 1. Repeat to duration less than start-positioned
        rhythm payload expression:

        ::

            >>> payload = [Container("c'8 d'8 e'8 f'8")]
            >>> expression = \
            ...     musicexpressiontools.StartPositionedRhythmPayloadExpression(
            ...     payload, Offset(0))

        ::

            >>> result = expression.repeat_to_duration(Duration(5, 16))

        ::

            >>> print(format(expression))
            musicexpressiontools.StartPositionedRhythmPayloadExpression(
                payload=scoretools.Container(
                    "{ c'8 d'8 e'16 }"
                    ),
                start_offset=durationtools.Offset(0, 1),
                )

        Example 2. Repeat to duration greater than start-positioned
        rhythm payload expression:

        ::

            >>> payload = [Container("c'8 d'8 e'8 f'8")]
            >>> expression = \
            ...     musicexpressiontools.StartPositionedRhythmPayloadExpression(
            ...     payload, Offset(0))

        ::

            >>> result = expression.repeat_to_duration(Duration(13, 16))

        ::

            >>> print(format(expression))
            musicexpressiontools.StartPositionedRhythmPayloadExpression(
                payload=scoretools.Container(
                    "{ c'8 d'8 e'8 f'8 } { c'8 d'8 e'16 }"
                    ),
                start_offset=durationtools.Offset(0, 1),
                )

        Operates in place and returns start-positioned rhythm
        payload expression.
        '''
        if self.timespan.duration < duration:
            stop_offset = self.start_offset + duration
            return self.repeat_to_stop_offset(stop_offset)
        elif duration < self.timespan.duration:
            stop_offset = self.start_offset + duration
            timespan = timespantools.Timespan(self.start_offset, stop_offset)
            result = self & timespan
            assert len(result) == 1, repr(result)
            result = result[0]
            return result
        elif self.timespan.duration == duration:
            return self

    def repeat_to_length(self, length):
        r'''Repeat start-positioned rhythm payload expression to `length`.

        Example 1. Repeat to `length` less than start-positioned
        rhythm payload expression:

        ::

            >>> payload = [Container("c'8 d'8 e'8 f'8")]
            >>> expression = \
            ...     musicexpressiontools.StartPositionedRhythmPayloadExpression(
            ...     payload, Offset(0))

        ::

            >>> result = expression.repeat_to_length(3)

        ::

            >>> print(format(expression))
            musicexpressiontools.StartPositionedRhythmPayloadExpression(
                payload=scoretools.Container(
                    "{ c'8 d'8 e'8 }"
                    ),
                start_offset=durationtools.Offset(0, 1),
                )

        Example 2. Repeat to `length` greater than start-positioned
        rhythm payload expression:

        ::

            >>> payload = [Container("c'8 d'8 e'8 f'8")]
            >>> expression = \
            ...     musicexpressiontools.StartPositionedRhythmPayloadExpression(
            ...     payload, Offset(0))

        ::

            >>> result = expression.repeat_to_length(7)

        ::

            >>> print(format(expression))
            musicexpressiontools.StartPositionedRhythmPayloadExpression(
                payload=scoretools.Container(
                    "{ c'8 d'8 e'8 f'8 } { c'8 d'8 e'8 }"
                    ),
                start_offset=durationtools.Offset(0, 1),
                )

        Operates in place and returns start-positioned rhythm
        payload expression.
        '''
        leaves = datastructuretools.CyclicTuple(self.payload.select_leaves())
        leaves = leaves[:length]
        duration = sum([leaf._get_duration() for leaf in leaves])
        return self.repeat_to_duration(duration)

    def repeat_to_stop_offset(self, stop_offset):
        r'''Repeat start-positioned rhythm payload expression to `stop_offset`.

        ::

            >>> payload = [Container("c'8 d'8 e'8 f'8")]
            >>> expression = \
            ...     musicexpressiontools.StartPositionedRhythmPayloadExpression(
            ...     payload, Offset(0))

        ::

            >>> result = expression.repeat_to_stop_offset(Offset(17, 16))

        ::

            >>> print(format(expression))
            musicexpressiontools.StartPositionedRhythmPayloadExpression(
                payload=scoretools.Container(
                    "{ c'8 d'8 e'8 f'8 } { c'8 d'8 e'8 f'8 } { c'16 }"
                    ),
                start_offset=durationtools.Offset(0, 1),
                )

        Operates in place and returns start-positioned rhythm
        payload expression.
        '''
        stop_offset = durationtools.Offset(stop_offset)
        assert self.stop_offset <= stop_offset
        additional_duration = stop_offset - self.stop_offset
        needed_copies = int(
            math.ceil(additional_duration / self.payload._get_duration()))
        copies = []
        for i in range(needed_copies):
            copies.append(copy.deepcopy(self.payload))
        for element in copies:
            self.payload.extend(element)
        assert stop_offset <= self.stop_offset
        stop_offset = durationtools.Offset(stop_offset)
        assert stop_offset <= self.stop_offset
        assert self.start_offset < stop_offset
        duration_to_trim = self.stop_offset - stop_offset
        duration_to_keep = self.payload._get_duration() - duration_to_trim
        shards = self._split_payload_at_offsets([duration_to_keep])
        assert len(shards) in (1, 2), repr(shards)
        self._payload = shards[0]
        return self

    def rotate(self, n, fracture_spanners=True):
        r'''Rotate start-positioned rhythm payload expression.

        Example 1. Rotate by count:

        ::

            >>> payload = [Container("c'8 d'8 e'8 f'8")]
            >>> expression = \
            ...     musicexpressiontools.StartPositionedRhythmPayloadExpression(
            ...     payload, Offset(0))

        ::

            >>> result = expression.rotate(-1)

        ::

            >>> print(format(expression))
            musicexpressiontools.StartPositionedRhythmPayloadExpression(
                payload=scoretools.Container(
                    "{ d'8 e'8 f'8 } { c'8 }"
                    ),
                start_offset=durationtools.Offset(0, 1),
                )

        Example 2. Rotate by duration:

        ::

            >>> payload = [Container("c'8 d'8 e'8 f'8")]
            >>> expression = \
            ...     musicexpressiontools.StartPositionedRhythmPayloadExpression(
            ...     payload, Offset(0))

        ::

            >>> result = expression.rotate(-Duration(3, 16))

        ::

            >>> print(format(expression))
            musicexpressiontools.StartPositionedRhythmPayloadExpression(
                payload=scoretools.Container(
                    "{ d'16 e'8 f'8 } { c'8 d'16 }"
                    ),
                start_offset=durationtools.Offset(0, 1),
                )

        Operates in place and returns start-positioned rhythm
        payload expression.
        '''
        from experimental.tools import musicexpressiontools
        if isinstance(n, int):
            leaves = datastructuretools.CyclicTuple(self.payload.select_leaves())
            if 0 < n:
                split_offset = leaves[-n]._get_timespan().start_offset
            elif n == 0:
                return self
            else:
                split_offset = leaves[-(n+1)]._get_timespan().stop_offset
        elif isinstance(n, musicexpressiontools.RotationExpression):
            rotation_expression = n
            if rotation_expression.level is None:
                components_at_level = self.payload.select_leaves()
            else:
                components_at_level = []
                for component in \
                    iterate(self.payload).by_class():
                    score_index = component._get_parentage().score_index
                    if len(score_index) == rotation_expression.level:
                        components_at_level.append(component)
            components_at_level = datastructuretools.CyclicTuple(components_at_level)
            if isinstance(rotation_expression.index, int):
                if 0 < rotation_expression.index:
                    split_offset = components_at_level[
                        -rotation_expression.index]._get_timespan().start_offset
                elif n == 0:
                    return self
                else:
                    split_offset = components_at_level[
                        -(rotation_expression.index+1)]._get_timespan().stop_offset
            else:
                index = durationtools.Duration(rotation_expression.index)
                if 0 <= index:
                    split_offset = self.payload._get_duration() - index
                else:
                    split_offset = abs(index)
            if rotation_expression.fracture_spanners is not None:
                fracture_spanners = rotation_expression.fracture_spanners
        else:
            n = durationtools.Duration(n)
            if 0 <= n:
                split_offset = self.payload._get_duration() - n
            else:
                split_offset = abs(n)
        #self._debug(split_offset, 'split offset')
        try:
            payload_duration = getattr(self, 'payload')
        except AttributeError:
            payload_duration = self.payload._get_duration()
        if split_offset == payload_duration:
            return self
        if fracture_spanners:
            result = mutate([self.payload]).split(
                [split_offset],
                cyclic=False,
                fracture_spanners=True,
                tie_split_notes=False,
                )
            left_half, right_half = result[0][0], result[-1][0]
            payload = scoretools.Container()
            payload.extend(right_half)
            payload.extend(left_half)
            assert inspect_(payload).is_well_formed()
            self._payload = payload
        else:
            result = mutate(self.payload[:]).split(
                [split_offset],
                cyclic=False,
                fracture_spanners=False,
                tie_split_notes=False,
                )
            left_half, right_half = result[0], result[-1]
            prototype = (spannertools.DuratedComplexBeam, )
            descendants = self.payload._get_descendants()
            for spanner in descendants.get_spanners(prototype):
                if left_half[-1] in spanner and right_half[0] in spanner:
                    leaf_right_of_split = right_half[0]
                    split_offset_in_beam = spanner._start_offset_in_me(
                        leaf_right_of_split)
                    left_durations, right_durations = \
                        sequencetools.split_sequence(
                            spanner.durations,
                            [split_offset_in_beam],
                            cyclic=False,
                            overhang=True,
                            )
                    new_durations = right_durations + left_durations
                    spanner._durations = new_durations
            new_payload = right_half + left_half
            self.payload._music = new_payload
            for component in new_payload:
                component._update_later(offsets=True)
            for spanner in self.payload._get_descendants().get_spanners():
                spanner._components.sort(
                    key=lambda x: x._get_parentage().score_index
                    )
            assert inspect_(self.payload).is_well_formed()
        return self

    def translate(self, translation):
        r'''Translate start-positioned rhythm payload expression by
        `translation`.

        ::

            >>> payload = [Container("c'8 d'8 e'8 f'8")]
            >>> expression = \
            ...     musicexpressiontools.StartPositionedRhythmPayloadExpression(
            ...     payload, Offset(0))

        ::

            >>> result = expression.translate(10)

        ::

            >>> print(format(expression))
            musicexpressiontools.StartPositionedRhythmPayloadExpression(
                payload=scoretools.Container(
                    "{ c'8 d'8 e'8 f'8 }"
                    ),
                start_offset=durationtools.Offset(10, 1),
                )

        Operates in place and returns start-positioned rhythm payload expression.
        '''
        return StartPositionedPayloadExpression.translate(self, translation)
