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

    # TODO: remove voice_name altogether
    def to_command(self, score_specification, voice_name):
        '''Change single-context time signature setting to command.

        Return command.
        '''
        from experimental.tools import settingtools
        anchor_timespan = score_specification.get_anchor_timespan(self)
        command = settingtools.DivisionRegionCommand(
            self.expression, self.context_name, anchor_timespan, fresh=self.fresh, truncate=self.truncate)
        return command
