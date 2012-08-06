from experimental.selectortools.Selector import Selector


class TimespanSelector(Selector):
    r'''.. versionadded:: 1.0

    Timespan selector.
    '''
    
    ### INTIALIZER ###

    def __init__(self, timespan):
        from experimental import timespantools
        timespan = timespantools.expr_to_timespan(timespan)
        Selector.__init__(self)
        self._timespan = timespan

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        if isinstance(expr, type(self)):
            if self.timespan == expr.timespan:
                return True
        return False

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def context_name(self):
        raise Exception('do not use.')

    @property
    def context_names(self):
        raise Exception('do not use.')

    @property
    def segment_identifier(self):
        '''Delegate to ``self.timespan.segment_identifier``.
        '''
        return self.timespan.segment_identifier
    
    @property
    def timespan(self):
        '''Timespan of timespan selector.
    
        Return timespan or none.
        '''
        return self._timespan

    ### PUBLIC METHODS ###

    def get_duration(self, score_specification):
        '''Delegate to ``self.timespan.get_duration()``.
        '''
        return self.timespan.get_duration(score_specification)

    def get_segment_start_offset(self, score_specification):
        '''Delegate to ``self.timespan.get_segment_start_offset()``.
        '''
        return self.timespan.get_segment_start_offset(score_specification)

    def get_segment_stop_offset(self, score_specification):
        '''Delegate to ``self.timespan.get_segment_stop_offset()``.
        '''
        return self.timespan.get_segment_stop_offset(score_specification)
