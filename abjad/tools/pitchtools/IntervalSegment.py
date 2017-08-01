# -*- coding: utf-8 -*-
from abjad.tools import datastructuretools
from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools.pitchtools.Segment import Segment
from abjad.tools.topleveltools import new


class IntervalSegment(Segment):
    r'''Interval segment.

    ::

        >>> import abjad

    ..  container:: example

        Initializes from string:

        ::

            >>> intervals = 'm2 M10 -aug4 P5'
            >>> abjad.IntervalSegment(intervals)
            IntervalSegment(['+m2', '+M10', '-aug4', '+P5'])

    ..  container:: example

        Initializes from pitch segment:

        ::

            >>> pitch_segment = abjad.PitchSegment("c d e f g a b c'")
            >>> abjad.IntervalSegment(pitch_segment)
            IntervalSegment(['+M2', '+M2', '+m2', '+M2', '+M2', '+M2', '+m2'])

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(self, items=None, item_class=None):
        from abjad.tools import pitchtools
        if isinstance(items, pitchtools.PitchSegment):
            intervals = []
            for one, two in datastructuretools.Sequence(items).nwise():
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

    ### PUBLIC PROPERTIES ###

    @property
    def slope(self):
        r'''Slope of interval segment.

        The slope of a interval segment is the sum of its
        intervals divided by its length:

        ::

            >>> abjad.IntervalSegment([1, 2]).slope
            Multiplier(3, 2)

        Returns multiplier.
        '''
        return durationtools.Multiplier.from_float(
            sum([x.number for x in self])) / len(self)

    @property
    def spread(self):
        r'''Gets spread of interval segment.

        The maximum interval spanned by any combination of
        the intervals within a numbered interval segment.

        ::

            >>> abjad.IntervalSegment([1, 2, -3, 1, -2, 1]).spread
            NumberedInterval(4)

        ::

            >>> abjad.IntervalSegment([1, 1, 1, 2, -3, -2]).spread
            NumberedInterval(5)

        Returns numbered interval.
        '''
        from abjad.tools import pitchtools
        current = maximum = minimum = 0
        for x in self:
            current += float(x.number)
            if maximum < current:
                maximum = current
            if current < minimum:
                minimum = current
        return pitchtools.NumberedInterval(maximum - minimum)

    ### PUBLIC METHODS ###

    @classmethod
    def from_selection(
        class_,
        selection,
        item_class=None,
        ):
        r'''Makes interval segment from component `selection`.

        ::

            >>> staff = abjad.Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
            >>> abjad.IntervalSegment.from_selection(
            ...     staff,
            ...     item_class=abjad.NumberedInterval,
            ...     )
            IntervalSegment([2, 2, 1, 2, 2, 2, 1])

        Returns interval segment.
        '''
        from abjad.tools import pitchtools
        pitch_segment = pitchtools.PitchSegment.from_selection(selection)
        pitches = [_ for _ in pitch_segment]
        intervals = (-x for x in mathtools.difference_series(pitches))
        return class_(
            items=intervals,
            item_class=item_class,
            )

    def has_duplicates(self):
        r'''True if segment has duplicate items. Otherwise false.

        ::

            >>> intervals = 'm2 M3 -aug4 m2 P5'
            >>> segment = abjad.IntervalSegment(intervals)
            >>> segment.has_duplicates()
            True

        ::

            >>> intervals = 'M3 -aug4 m2 P5'
            >>> segment = abjad.IntervalSegment(intervals)
            >>> segment.has_duplicates()
            False

        Returns true or false.
        '''
        from abjad.tools import pitchtools
        return len(pitchtools.IntervalSet(self)) < len(self)

    def rotate(self, n=0):
        r'''Rotates interval segment by index `n`.

        Returns new interval segment.
        '''
        return new(self, self[-n:] + self[:-n])
