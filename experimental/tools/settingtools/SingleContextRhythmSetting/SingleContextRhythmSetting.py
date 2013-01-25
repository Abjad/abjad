from experimental.tools.settingtools.SingleContextSetting import SingleContextSetting


class SingleContextRhythmSetting(SingleContextSetting):
    r'''Single-context time signature setting.
    '''

    ### INITIALIZER ###

    def __init__(self, expression=None, anchor=None, context_name=None, fresh=True, persist=True):
        SingleContextSetting.__init__(self, attribute='rhythm', expression=expression, 
            anchor=anchor, context_name=context_name, fresh=fresh, persist=persist)

    ### PUBLIC METHODS ###

    def to_timespan_scoped_setting(self):
        '''Evaluate timespan of single-context rhythm setting.

        Return timespan-scoped single-context rhythm setting.
        '''
        from experimental.tools import settingtools
        timespan = self.get_anchor_timespan()
        command = settingtools.TimespanScopedSingleContextRhythmSetting(
            expression=self.expression, timespan=timespan, context_name=self.context_name, fresh=self.fresh)
        return command
