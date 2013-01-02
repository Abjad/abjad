from experimental.tools.settingtools.SingleContextSetting import SingleContextSetting


class SingleContextDivisionSetting(SingleContextSetting):
    r'''Single-context division setting.
    '''

    ### INITIALIZER ###

    def __init__(self, request=None, anchor=None, context_name=None, fresh=True, persist=True, truncate=None):
        SingleContextSetting.__init__(self, attribute='divisions', request=request, 
            anchor=anchor, context_name=context_name, fresh=fresh, persist=persist)
        self._truncate = truncate

    ### PUBLIC METHODS ###

    def to_command(self, score_specification, voice_name):
        '''Change single-context time signature setting to command.

        Return command.
        '''
        from experimental.tools import settingtools
        anchor_timespan = score_specification.get_anchor_timespan(self, voice_name)
        command = settingtools.DivisionRegionCommand(
            self.request, self.context_name, anchor_timespan, fresh=self.fresh, truncate=self.truncate)
        return command
