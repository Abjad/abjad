import abc
from abjad.tools import durationtools
from abjad.tools import timespantools
from abjad.tools.timespantools.Timespan import Timespan


class OffsetPositionedExpression(Timespan):
    r'''Offset-positioned expression.

    Base class from which concrete expressions inherit.

    Composers do not create offset-positioned expression objects
    because offset-positioned expressions arise as a byproduct
    of interpretation.
    ''' 

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, voice_name, start_offset=None, stop_offset=None):
        assert isinstance(voice_name, (str, type(None))), repr(voice_name)
        self._voice_name = voice_name
        if start_offset is None:
            start_offset = durationtools.Offset(0)
        else:
            start_offset = durationtools.Offset(start_offset)
        Timespan.__init__(self, start_offset=start_offset)

    ### SPECIAL METHODS ###

    def __lt__(self, expr):
        return self.timespan.start_offset < expr.timespan.start_offset

    ### PRIVATE METHODS ###

    @abc.abstractmethod
    def _set_start_offset(self, start_offset):
        '''Trim to start offset.

        Adjust start offset.
          
        Operate in place and return none.
        '''
        pass

    @abc.abstractmethod
    def _set_stop_offset(self, stop_offset):
        '''Trim to stop offset.

        Adjust stop offset.
          
        Operate in place and return none.
        '''
        pass

    ### READ-ONLY PUBLIC PROPERTIES ###

    @abc.abstractproperty
    def duration(self):
        pass

    @property
    def stop_offset(self):
        '''Offset-positioned expression stop offset.
        
        Defined equal to expression start offset 
        plus expression duration.

        Return offset.
        '''
        return self.start_offset + self.duration

    @property
    def timespan(self):
        return timespantools.Timespan(self.start_offset, self.stop_offset)

    @property
    def voice_name(self):
        '''Offset-positioned expression voice name.

        Return string.
        '''
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
        '''Adjust to offsets.

        Operate in place and return none.
        '''
        if stop_offset is not None:
            stop_offset = durationtools.Offset(stop_offset)
            if stop_offset < self.timespan.stop_offset:
                self._set_stop_offset(stop_offset)
        if start_offset is not None:
            start_offset = durationtools.Offset(start_offset)
            if self.timespan.start_offset < start_offset:
                self._set_start_offset(start_offset)
