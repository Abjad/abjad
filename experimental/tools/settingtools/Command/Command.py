import abc
import copy
from abjad.tools import datastructuretools
from abjad.tools import durationtools
from abjad.tools.abctools.AbjadObject import AbjadObject
from experimental.tools import helpertools 
from experimental.tools import requesttools 
from abjad.tools import timerelationtools 


class Command(AbjadObject):
    '''.. versionadded:: 1.0

    Command indicating period of time to which request will apply.

    Composers do not create commands because command arise
    as a byproduct of interpretation.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta

    ### INTIAILIZER ###

    def __init__(self, request, context_name, start_offset, stop_offset, modifications=None, fresh=None):
        from experimental.tools import symbolictimetools
        assert isinstance(request, (requesttools.Request, symbolictimetools.SymbolicTimespan)), repr(request)
        assert isinstance(context_name, (str, type(None))), repr(context_name)
        start_offset = durationtools.Offset(start_offset)
        stop_offset = durationtools.Offset(stop_offset)
        assert start_offset <= stop_offset
        assert isinstance(fresh, (bool, type(None))), repr(fresh)
        self._request = request
        self._context_name = context_name
        self._start_offset = start_offset
        self._stop_offset = stop_offset
        modifications = modifications or []
        self._modifications = datastructuretools.ObjectInventory(modifications)
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

    ### PRIVATE READ-ONLY PROPERTIES ###

    @property
    def _keyword_argument_name_value_strings(self):
        result = AbjadObject._keyword_argument_name_value_strings.fget(self)
        if 'modifications=ObjectInventory([])' in result:
            result = list(result)
            result.remove('modifications=ObjectInventory([])')
        return tuple(result)

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
    def duration(self):
        '''Command duration.
            
        Return duration.
        ''' 
        return self.stop_offset - self.start_offset

    @property
    def fresh(self):
        '''True when command was generated in response 
        to an explicit user command. Otherwise false.

        Return boolean.
        '''
        return self._fresh

    @property
    def modifications(self):
        return self._modifications

    @property
    def offsets(self):
        '''Return pair.
        '''
        return self.start_offset, self.stop_offset

    @property
    def request(self):
        '''Command request.
        
        Return request object.
        ''' 
        return self._request

    @property
    def start_offset(self):
        '''Score start offset of command.

        Return offset.
        '''
        return self._start_offset

    @property
    def stop_offset(self):
        '''Score stop offset of command.

        Return offset.
        '''
        return self._stop_offset

    @property
    def vector(self):
        '''Command mandatory argument values.

        Return tuple.
        '''
        return self._positional_argument_values

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
        duration = self.duration + command.duration
        fused_command = copy.deepcopy(self)
        fused_command._stop_offset = stop_offset
        fused_command._duration = duration 
        return fused_command
