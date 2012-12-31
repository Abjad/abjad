import abc
import copy
from abjad.tools import durationtools
from abjad.tools import timerelationtools 
from abjad.tools import timespantools 
from abjad.tools.timespantools.Timespan import Timespan
from experimental.tools import helpertools 


class Command(Timespan):
    '''

    Command indicating period of time to which request will apply.

    Composers do not create commands because command arise
    as a byproduct of interpretation.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta

    ### INTIAILIZER ###

    def __init__(self, request, context_name, start_offset, stop_offset, fresh=None):
        from experimental.tools import requesttools 
        from experimental.tools import timeexpressiontools
        assert isinstance(request, (requesttools.Request, timeexpressiontools.TimespanExpression)), repr(request)
        assert isinstance(context_name, (str, type(None))), repr(context_name)
        start_offset = durationtools.Offset(start_offset)
        stop_offset = durationtools.Offset(stop_offset)
        assert start_offset <= stop_offset
        assert isinstance(fresh, (bool, type(None))), repr(fresh)
        Timespan.__init__(self, start_offset=start_offset, stop_offset=stop_offset)
        self._request = request
        self._context_name = context_name
        self._fresh = fresh

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        if isinstance(expr, type(self)):
            for my_value, expr_value in zip(
                self._positional_argument_values, expr._positional_argument_values):
                if not my_value == expr_value:
                    return False
            else:
                return True
        return False

    def __lt__(self, expr):
        return timerelationtools.timespan_2_starts_before_timespan_1_starts(expr, self)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @abc.abstractproperty
    def attribute(self):
        '''Command attribute.

        Return string.
        '''
        pass

    @property
    def context_name(self):
        '''Command context name.
    
        Return string.
        '''
        return self._context_name

    @property
    def fresh(self):
        '''True when command was generated in response 
        to an explicit user command. Otherwise false.

        Return boolean.
        '''
        return self._fresh

    @property
    def request(self):
        '''Command request.
        
        Return request object.
        ''' 
        return self._request

    @property
    def timespan(self):
        return timespantools.Timespan(self.start_offset, self.stop_offset)

    ### PUBLIC METHODS ###

    @abc.abstractmethod
    def can_fuse(self, expr):
        pass

    def fuse(self, command):
        '''Fuse `command` to the end of self.

        Return newly constructed division command.

        Raise exception when self can not fuse with `division_command`.
        '''
        assert self.can_fuse(command)
        stop_offset = self.stop_offset + command.duration
        fused_command = self.new(stop_offset=stop_offset)
        return fused_command

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
