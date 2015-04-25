# -*- encoding: utf-8 -*-
from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import sequencetools
from abjad.tools.pitchtools.Segment import Segment
from abjad.tools.topleveltools import new


class IntervalSegment(Segment):
    r'''An interval segment.

    ::

        >>> intervals = 'm2 M10 -aug4 P5'
        >>> pitchtools.IntervalSegment(intervals)
        IntervalSegment(['+m2', '+M10', '-aug4', '+P5'])

    ::

        >>> pitch_segment = pitchtools.PitchSegment("c d e f g a b c'")
        >>> pitchtools.IntervalSegment(pitch_segment)
        IntervalSegment(['+M2', '+M2', '+m2', '+M2', '+M2', '+M2', '+m2'])

    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(
        self,
        items=None,
        item_class=None,
        ):
        from abjad.tools import pitchtools
        if isinstance(items, pitchtools.PitchSegment):
            intervals = []
            for one, two in sequencetools.iterate_sequence_nwise(items):
                intervals.append(one - two)
            items = intervals
        Segment.__init__(
            self,
            items=items,
            item_class=item_class,
            )

    ### PRIVATE PROPERTIES ###

    @property
    def _named_item_class(self):
        from abjad.tools import pitchtools
        return pitchtools.NamedInterval

    @property
    def _numbered_item_class(self):
        from abjad.tools import pitchtools
        return pitchtools.NumberedInterval

    @property
    def _parent_item_class(self):
        from abjad.tools import pitchtools
        return pitchtools.Interval

    @property
    def _repr_specification(self):
        items = []
        if self.item_class.__name__.startswith('Named'):
            items = [str(x) for x in self]
        else:
            items = [x.number for x in self]
        return new(
            self._storage_format_specification,
            is_indented=False,
            keyword_argument_names=(),
            positional_argument_values=(
                items,
                ),
            )

    ### PUBLIC METHODS ###

    @classmethod
    def from_selection(
        cls,
        selection,
        item_class=None,
        ):
        r'''Makes interval segment from component `selection`.

        ::

            >>> staff = Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
            >>> pitchtools.IntervalSegment.from_selection(
            ...     staff, item_class=pitchtools.NumberedInterval)
            IntervalSegment([2, 2, 1, 2, 2, 2, 1])

        Returns interval segment.
        '''
        from abjad.tools import pitchtools
        pitch_segment = pitchtools.PitchSegment.from_selection(selection)
        intervals = (-x for x in mathtools.difference_series(pitch_segment))
        return cls(
            items=intervals,
            item_class=item_class,
            )

    def rotate(self, n):
        r'''Rotates interval segment by `n`.

        Returns new interval segment.
        '''
        return new(self, self[-n:] + self[:-n])

    ### PUBLIC PROPERTIES ###

    @property
    def has_duplicates(self):
        r'''True if segment has duplicate items. Otherwise false.

        ::

            >>> intervals = 'm2 M3 -aug4 m2 P5'
            >>> segment = pitchtools.IntervalSegment(intervals)
            >>> segment.has_duplicates
            True

        ::

            >>> intervals = 'M3 -aug4 m2 P5'
            >>> segment = pitchtools.IntervalSegment(intervals)
            >>> segment.has_duplicates
            False

        Returns boolean.
        '''
        from abjad.tools import pitchtools
        return len(pitchtools.IntervalSet(self)) < len(self)

    @property
    def slope(self):
        r'''Slope of interval segment.

        The slope of a interval segment is the sum of its
        intervals divided by its length:

        ::

            >>> pitchtools.IntervalSegment([1, 2]).slope
            Multiplier(3, 2)

        Returns multiplier.
        '''
        return durationtools.Multiplier.from_float(
            sum([x.number for x in self])) / len(self)

    @property
    def spread(self):
        r'''Spread of interval segment.

        The maximum interval spanned by any combination of
        the intervals within a numbered interval segment.

        ::

            >>> pitchtools.IntervalSegment([1, 2, -3, 1, -2, 1]).spread
            NumberedInterval(4.0)

        ::

            >>> pitchtools.IntervalSegment([1, 1, 1, 2, -3, -2]).spread
            NumberedInterval(5.0)

        Returns numbered interval.
        '''
        from abjad.tools import pitchtools
        current = maximum = minimum = 0
        for x in self:
            current += float(x)
            if maximum < current:
                maximum = current
            if current < minimum:
                minimum = current
        return pitchtools.NumberedInterval(maximum - minimum)