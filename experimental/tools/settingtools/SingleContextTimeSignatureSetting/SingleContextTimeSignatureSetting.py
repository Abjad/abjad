from experimental.tools.settingtools.SingleContextSetting import SingleContextSetting


class SingleContextTimeSignatureSetting(SingleContextSetting):
    r'''Single-context time signature setting.
    '''

    ### INITIALIZER ###

    def __init__(self, request=None, anchor=None, context_name=None, fresh=True, persist=True):
        Setting.__init__(self, attribute='time_signatures', request=request, anchor=anchor,
            fresh=fresh, persist=persist)

    ### PUBLIC METHODS ###

    def to_command(self, score_specification, voice_name):
        '''Change single-context time signature setting to command.

        Return command.
        '''
        anchor_timespan = score_specification.get_anchor_timespan(self, voice_name)
        command = TimeSignatureRegionCommand(self.request, self.context_name, anchor_timespan, fresh=self.fresh)
        return command
