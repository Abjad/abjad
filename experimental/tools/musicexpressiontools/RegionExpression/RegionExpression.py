# -*- encoding: utf-8 -*-
import abc
from abjad.tools import durationtools
from experimental.tools.musicexpressiontools.Expression import Expression


class RegionExpression(Expression):
    r'''Region expression.
    '''

    ### CLASS VARIABLES ###

    __metaclass__ = abc.ABCMeta

    ### INITIALIZER ###

    def __init__(
        self, 
        source_expression=None, 
        start_offset=None, 
        total_duration=None, 
        voice_name=None,
        ):
        assert isinstance(voice_name, str), repr(voice_name)
        start_offset = durationtools.Offset(start_offset)
        total_duration = durationtools.Duration(total_duration)
        self._source_expression = source_expression
        self._start_offset = start_offset
        self._total_duration = total_duration
        self._voice_name = voice_name

    ### PUBLIC PROPERTIES ###

    @property
    def source_expression(self):
        r'''Region expression source expression.

        Return expression.
        '''
        return self._source_expression

    @property
    def start_offset(self):
        r'''Region expression start offset.

        Return offset.
        '''
        return self._start_offset

    @property
    def total_duration(self):
        r'''Region expression total duration.

        Return duration.
        '''
        return self._total_duration

    @property
    def voice_name(self):
        r'''Region expression voice name.

        Return string.
        '''
        return self._voice_name
