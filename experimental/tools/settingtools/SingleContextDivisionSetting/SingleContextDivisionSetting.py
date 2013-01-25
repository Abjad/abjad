from experimental.tools.settingtools.SingleContextSetting import SingleContextSetting


class SingleContextDivisionSetting(SingleContextSetting):
    r'''Single-context division setting.
    '''

    ### INITIALIZER ###

    def __init__(self, expression=None, anchor=None, context_name=None, fresh=True, persist=True, truncate=None):
        assert isinstance(truncate, (bool, type(None)))
        SingleContextSetting.__init__(self, attribute='divisions', expression=expression, 
            anchor=anchor, context_name=context_name, fresh=fresh, persist=persist)
        self._truncate = truncate

    ### PUBLIC METHODS ###

    def to_command(self):
        '''Change single-context time signature setting to command.

        Return command.
        '''
        from experimental.tools import settingtools
        anchor_timespan = self.get_anchor_timespan()
        command = settingtools.TimespanScopedSingleContextDivisionSetting(
            expression=self.expression, timespan=anchor_timespan, 
            context_name=self.context_name, fresh=self.fresh, truncate=self.truncate)
        return command
