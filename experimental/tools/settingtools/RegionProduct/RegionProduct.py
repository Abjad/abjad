import abc
from abjad.tools import durationtools
from abjad.tools import timespantools
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
    def __init__(self, voice_name, timespan=None):
        assert isinstance(voice_name, (str, type(None))), repr(voice_name)
        self._voice_name = voice_name
        timespan = timespan or timespantools.Timespan(0)
        assert isinstance(timespan, (timespantools.Timespan)), repr(timespan)
        self._start_offset = timespan.start_offset

    ### SPECIAL METHODS ###

    def __lt__(self, expr):
        return self.timespan.start_offset < expr.timespan.start_offset

    ### READ-ONLY PRIVATE PROPERTIES ###

    @abc.abstractproperty
    def _duration(self):
        pass

    @property
    def _stop_offset(self):
        return self._start_offset + self._duration

    ### PRIVATE METHODS ###

    @abc.abstractmethod
    def _set_start_offset(self, start_offset):
        pass

    @abc.abstractmethod
    def _set_stop_offset(self, stop_offset):
        pass

    ### READ-ONLY PUBLIC PROPERTIES ###

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

    def set_offsets(self, start_offset=None, stop_offset=None):
        if stop_offset is not None:
            stop_offset = durationtools.Offset(stop_offset)
            if stop_offset < self.timespan.stop_offset:
                self._set_stop_offset(stop_offset)
        if start_offset is not None:
            start_offset = durationtools.Offset(start_offset)
            if self.timespan.start_offset < start_offset:
                self._set_start_offset(start_offset)
