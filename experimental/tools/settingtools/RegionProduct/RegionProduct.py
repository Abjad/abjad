import abc
import copy
from abjad.tools import componenttools
from abjad.tools import containertools
from abjad.tools import durationtools
from abjad.tools import timespantools
from abjad.tools import wellformednesstools
from abjad.tools.abctools.AbjadObject import AbjadObject


class RegionProduct(AbjadObject):
    r'''Region expression.

    Timespan-positioned payload.

    Interpreter byproduct.
    ''' 

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, payload=None, voice_name=None, timespan=None):
        assert isinstance(voice_name, (str, type(None))), repr(voice_name)
        timespan = timespan or timespantools.Timespan(0)
        assert isinstance(timespan, (timespantools.Timespan)), repr(timespan)
        self._payload = payload
        self._voice_name = voice_name
        self._start_offset = timespan.start_offset

    ### SPECIAL METHODS ###

    def __lt__(self, expr):
        return self.timespan.start_offset < expr.timespan.start_offset

    def __sub__(self, timespan):
        '''Subtract `timespan` from rhythm region product.

        Example 1. Subtract from left:

        ::

            >>> payload = [Container("c'8 d'8 e'8 f'8")]
            >>> product = settingtools.RhythmRegionProduct(payload, 'Voice 1', timespantools.Timespan(0))
            >>> result = product - timespantools.Timespan(0, Offset(1, 8))

        ::

                >>> z(result)
                timespantools.TimespanInventory([
                    settingtools.RhythmRegionProduct(
                        payload=containertools.Container(
                            music=({d'8, e'8, f'8},)
                            ),
                        voice_name='Voice 1',
                        timespan=timespantools.Timespan(
                            start_offset=durationtools.Offset(1, 8),
                            stop_offset=durationtools.Offset(1, 2)
                            )
                        )
                    ])

            Example 2. Subtract from right:

            ::

                >>> payload = [Container("c'8 d'8 e'8 f'8")]
                >>> product = settingtools.RhythmRegionProduct(payload, 'Voice 1', timespantools.Timespan(0))
                >>> result = product - timespantools.Timespan(Offset(3, 8), 100)

            ::

                >>> z(result)
                timespantools.TimespanInventory([
                    settingtools.RhythmRegionProduct(
                        payload=containertools.Container(
                            music=({c'8, d'8, e'8},)
                            ),
                        voice_name='Voice 1',
                        timespan=timespantools.Timespan(
                            start_offset=durationtools.Offset(0, 1),
                            stop_offset=durationtools.Offset(3, 8)
                            )
                        )
                    ])

            Example 3. Subtract from middle:

            ::

                >>> payload = [Container("c'8 d'8 e'8 f'8")]
                >>> product = settingtools.RhythmRegionProduct(payload, 'Voice 1', timespantools.Timespan(0))
                >>> result = product - timespantools.Timespan(Offset(1, 8), Offset(3, 8))

            ::

                >>> z(result)
                timespantools.TimespanInventory([
                    settingtools.RhythmRegionProduct(
                        payload=containertools.Container(
                            music=({c'8},)
                            ),
                        voice_name='Voice 1',
                        timespan=timespantools.Timespan(
                            start_offset=durationtools.Offset(0, 1),
                            stop_offset=durationtools.Offset(1, 8)
                            )
                        ),
                    settingtools.RhythmRegionProduct(
                        payload=containertools.Container(
                            music=({f'8},)
                            ),
                        voice_name='Voice 1',
                        timespan=timespantools.Timespan(
                            start_offset=durationtools.Offset(3, 8),
                            stop_offset=durationtools.Offset(1, 2)
                            )
                        )
                    ])

            Example 4. Subtract nothing:

            ::

                >>> payload = [Container("c'8 d'8 e'8 f'8")]
                >>> product = settingtools.RhythmRegionProduct(payload, 'Voice 1', timespantools.Timespan(0))
                >>> result = product - timespantools.Timespan(100, 200)

            ::

                >>> z(result)
                timespantools.TimespanInventory([
                    settingtools.RhythmRegionProduct(
                        payload=containertools.Container(
                            music=({c'8, d'8, e'8, f'8},)
                            ),
                        voice_name='Voice 1',
                        timespan=timespantools.Timespan(
                            start_offset=durationtools.Offset(0, 1),
                            stop_offset=durationtools.Offset(1, 2)
                            )
                        )
                    ])

        Operate in place and return timespan inventory.
        '''
        if timespan.delays_timespan(self):
            split_offset = durationtools.Offset(timespan.stop_offset)
            duration_to_trim = split_offset - self.start_offset
            result = self._split_payload_at_offsets([duration_to_trim])
            trimmed_payload = result[-1][0]
            self._payload = trimmed_payload
            self._start_offset = split_offset
            result = timespantools.TimespanInventory([self])
        elif timespan.curtails_timespan(self):
            split_offset = durationtools.Offset(timespan.start_offset)
            duration_to_trim = self.stop_offset - split_offset
            duration_to_keep = self.payload.prolated_duration - duration_to_trim
            result = self._split_payload_at_offsets([duration_to_keep])
            trimmed_payload = result[0][0]
            self._payload = trimmed_payload
            result = timespantools.TimespanInventory([self])
        elif timespan.trisects_timespan(self):
            split_offsets = []
            split_offsets.append(timespan.start_offset - self.start_offset)
            split_offsets.append(timespan.duration)
            result = self._split_payload_at_offsets(split_offsets)
            left_payload = result[0][0]
            right_payload = result[-1][0]
            left_timespan = timespantools.Timespan(self.start_offset)
            left_product = type(self)(
                payload=None, voice_name=self.voice_name, timespan=left_timespan)
            left_product._payload = left_payload
            right_timespan = timespantools.Timespan(timespan.stop_offset)
            right_product = type(self)(
                payload=None, voice_name=self.voice_name, timespan=right_timespan)
            right_product._payload = right_payload
            products = [left_product, right_product]
            result = timespantools.TimespanInventory(products)
        else:
            result = timespantools.TimespanInventory([self])
        return result

    ### READ-ONLY PRIVATE PROPERTIES ###

    @abc.abstractproperty
    def _duration(self):
        pass

    @property
    def _stop_offset(self):
        return self._start_offset + self._duration

    ### PRIVATE METHODS ###

    def _can_fuse(self, expr):
        if isinstance(expr, type(self)):
            if self.timespan.stops_when_timespan_starts(expr):
                return self.voice_name == expr.voice_name
        return False
        
    @abc.abstractmethod
    def _set_start_offset(self, start_offset):
        pass

    @abc.abstractmethod
    def _set_stop_offset(self, stop_offset):
        pass

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def payload(self):
        return self._payload

    @property
    def start_offset(self):
        return self.timespan.start_offset

    @property
    def stop_offset(self):
        return self.timespan.stop_offset

    @property
    def timespan(self):
        return timespantools.Timespan(self._start_offset, self._stop_offset)

    @property
    def voice_name(self):
        return self._voice_name

    ### PUBLIC METHODS ###
    
    def new(self, **kwargs):
        positional_argument_dictionary = self._positional_argument_dictionary
        keyword_argument_dictionary = self._keyword_argument_dictionary
        for key, value in kwargs.iteritems():
            if key in positional_argument_dictionary:
                positional_argument_dictionary[key] = value
            elif key in keyword_argument_dictionary:
                keyword_argument_dictionary[key] = value
            else:
                raise KeyError(key)
        positional_argument_values = []
        for positional_argument_name in self._positional_argument_names:
            positional_argument_value = positional_argument_dictionary[positional_argument_name]
            positional_argument_values.append(positional_argument_value)
        result = type(self)(*positional_argument_values, **keyword_argument_dictionary)
        return result

    # TODO: change to __sub__
    def set_offsets(self, start_offset=None, stop_offset=None):
        '''Operate in place and return self.
        '''
        if stop_offset is not None:
            stop_offset = durationtools.Offset(stop_offset)
            if stop_offset < self.timespan.stop_offset:
                self._set_stop_offset(stop_offset)
        if start_offset is not None:
            start_offset = durationtools.Offset(start_offset)
            if self.timespan.start_offset < start_offset:
                self._set_start_offset(start_offset)
        return self
        # TODO: use this implementation instead
        #assert start_offset < stop_offset
        #if self.timespan.start_offset < stop_offset < self.timespan.stop_offset:
        #    stop_offset = durationtools.Offset(stop_offset)
        #    if stop_offset < self.timespan.stop_offset:
        #        self._set_stop_offset(stop_offset)
        #if self.timespan.start_offset < start_offset < self.timespan.stop_offset:
        #    start_offset = durationtools.Offset(start_offset)
        #    if self.timespan.start_offset < start_offset:
        #        self._set_start_offset(start_offset)
        #return self
