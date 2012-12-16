from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import sequencetools
from abjad.tools.mathtools.BoundedObject import BoundedObject


class Timespan(BoundedObject):
    r'''.. versionadded:: 2.11

    Timespan ``[1/2, 3/2)``::

        >>> timespan = timespantools.Timespan((1, 2), (3, 2)) 

    ::

        >>> timespan
        Timespan(start_offset=Offset(1, 2), stop_offset=Offset(3, 2))

    ::
    
        >>> z(timespan)
        timespantools.Timespan(
            start_offset=durationtools.Offset(1, 2),
            stop_offset=durationtools.Offset(3, 2)
            )

    Timespans are object-modeled offset pairs.

    Timespans are immutable and treated as value objects.
    '''

    ### INITIALIZER ###

    def __init__(self, start_offset=None, stop_offset=None):
        BoundedObject.__init__(self)
        start_offset = self._initialize_offset(start_offset)
        stop_offset = self._initialize_offset(stop_offset)
        self._start_offset = start_offset
        self._stop_offset = stop_offset

    ### PRIVATE METHODS ###

    def _initialize_offset(self, offset):
        if offset is not None:
            return durationtools.Offset(offset)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def duration(self):
        '''Get timespan duration::

            >>> timespan.duration
            Duration(1, 1)

        Return duration.
        '''
        return self.stop_offset - self.start_offset

    @property
    def is_well_formed(self):
        '''True when timespan start offset preceeds timespan stop offset.
        Otherwise false.

            >>> timespan.is_well_formed
            True

        Return boolean.
        '''
        return self.start_offset < self.stop_offset

    @property
    def offsets(self):
        '''Timespan offsets::

            >>> timespan.offsets
            (Offset(1, 2), Offset(3, 2))

        Return offset pair.
        '''
        return self.start_offset, self.stop_offset

    @property
    def start_offset(self):
        '''Timespan start offset::

            >>> timespan.start_offset
            Offset(1, 2)

        Return offset.
        '''
        return self._start_offset

    @property
    def stop_offset(self):
        '''Timespan stop offset::

            >>> timespan.stop_offset
            Offset(3, 2)
            
        Return offset.
        '''
        return self._stop_offset

    ### PUBLIC METHODS ###

    def divide_by_ratio(self, ratio):
        '''Divide timespan by `ratio`::

            >>> for x in timespan.divide_by_ratio((1, 2, 1)):
            ...     x
            Timespan(start_offset=Offset(1, 2), stop_offset=Offset(3, 4))
            Timespan(start_offset=Offset(3, 4), stop_offset=Offset(5, 4))
            Timespan(start_offset=Offset(5, 4), stop_offset=Offset(3, 2))

        Return tuple of newly constructed timespans.
        '''
        if isinstance(ratio, int):
            ratio = ratio * (1, )
        ratio = mathtools.Ratio(ratio)
        unit_duration = self.duration / sum(ratio) 
        part_durations = [numerator * unit_duration for numerator in ratio]
        start_offsets = mathtools.cumulative_sums([self.start_offset] + part_durations)
        offset_pairs = sequencetools.iterate_sequence_pairwise_strict(start_offsets)
        result = [type(self)(*offset_pair) for offset_pair in offset_pairs]
        return tuple(result)

    def scale(self, multiplier):
        '''Scale timespan by `multiplier`::

            >>> timespan.scale(Multiplier(1, 2))
            Timespan(start_offset=Offset(1, 2), stop_offset=Offset(1, 1))

        Return newly constructed timespan.
        '''
        multiplier = durationtools.Multiplier(multiplier)
        new_start_offset = self.start_offset
        new_duration = multiplier * self.duration
        new_stop_offset = self.start_offset + new_duration
        result = type(self)(new_start_offset, new_stop_offset)
        return result

    def set_duration(self, duration):
        '''Set timespan duration to `duration`::

            >>> timespan.set_duration(Duration(3, 5))
            Timespan(start_offset=Offset(1, 2), stop_offset=Offset(11, 10))

        Return newly constructed timespan.
        '''
        duration = durationtools.Duration(duration)
        new_stop_offset = self.start_offset + duration
        result = type(self)(self.start_offset, new_stop_offset)
        return result

    def set_offsets(self, start_offset=None, stop_offset=None):
        '''Set timespan start offset to `start_offset` and
        stop offset to `stop_offset`::

            >>> timespan.set_offsets(stop_offset=Offset(7, 8))
            Timespan(start_offset=Offset(1, 2), stop_offset=Offset(7, 8))

        Return newly constructed timespan.
        '''
        if start_offset is not None:
            new_start_offset = start_offset
        else:
            new_start_offset = self.start_offset
        if stop_offset is not None:
            new_stop_offset = stop_offset
        else:
            new_stop_offset = self.stop_offset
        result = type(self)(new_start_offset, new_stop_offset)
        return result

    def translate_offsets(self, start_offset_translation=None, stop_offset_translation=None):
        '''Translate timespan start offset by `start_offset_translation` and
        stop offset by `stop_offset_translation`::

            >>> timespan.translate_offsets(start_offset_translation=Duration(-1, 8))
            Timespan(start_offset=Offset(3, 8), stop_offset=Offset(3, 2))

        Return newly constructed timespan.
        '''
        start_offset_translation = start_offset_translation or 0
        stop_offset_translation = stop_offset_translation or 0
        start_offset_translation = durationtools.Duration(start_offset_translation)
        stop_offset_translation = durationtools.Duration(stop_offset_translation)
        new_start_offset = self.start_offset + start_offset_translation
        new_stop_offset = self.stop_offset + stop_offset_translation
        result = type(self)(new_start_offset, new_stop_offset)
        return result
