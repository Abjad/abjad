import abc
import copy
from abjad.tools import durationtools
from abjad.tools import timerelationtools 
from abjad.tools import timespantools 
from abjad.tools.abctools.AbjadObject import AbjadObject
from experimental.tools import helpertools 


class RegionCommand(AbjadObject):
    '''RegionCommand.

    Timespan-scoped command.

    Interpreter byproduct.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta

    ### INTIAILIZER ###

    def __init__(self, request, context_name, timespan, fresh=None):
        from experimental.tools import requesttools 
        from experimental.tools import settingtools 
        from experimental.tools import timeexpressiontools
        assert isinstance(request, (
            settingtools.PayloadCallbackMixin, timeexpressiontools.TimespanExpression)), repr(request)
        assert isinstance(context_name, (str, type(None))), repr(context_name)
        assert isinstance(timespan, timespantools.Timespan), repr(timespan)
        assert isinstance(fresh, (bool, type(None))), repr(fresh)
        self._request = request
        self._context_name = context_name
        self._timespan = timespan
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

    ### PRIVATE METHODS ###

    @abc.abstractmethod
    def _can_fuse(self, expr):
        pass

    ### READ-ONLY PUBLIC PROPERTIES ###

    @abc.abstractproperty
    def attribute(self):
        '''RegionCommand attribute.

        Return string.
        '''
        pass

    @property
    def context_name(self):
        '''RegionCommand context name.
    
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
        '''RegionCommand request.
        
        Return request object.
        ''' 
        return self._request

    @property
    def timespan(self):
        '''RegionCommand timespan.
        '''
        return self._timespan

    ### PUBLIC METHODS ###

    # TODO: change name to self.__or__()
    #def fuse(self, command):
    def __or__(self, command):
        '''Fuse `command` to the end of self.

        Return newly constructed division command.

        Raise exception when self can not fuse with `division_command`.
        '''
        assert self._can_fuse(command)
        stop_offset = self.timespan.stop_offset + command.timespan.duration
        timespan = self.timespan.new(stop_offset=stop_offset) 
        fused_command = self.new(timespan=timespan)
        #return fused_command
        return timespantools.TimespanInventory([fused_command])

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
