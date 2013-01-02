from experimental.tools.settingtools.SingleContextSetting import SingleContextSetting


class SingleContextTimeSignatureSetting(SingleContextSetting):
    r'''Single-context time signature setting.
    '''

    ### INITIALIZER ###

    def __init__(self, request=None, anchor=None, context_name=None, fresh=True, persist=True):
        SingleContextSetting.__init__(self, attribute='time_signatures', request=request, 
            anchor=anchor, context_name=context_name, fresh=fresh, persist=persist)

    ### PUBLIC METHODS ###

    def to_command(self, score_specification, voice_name):
        '''Change single-context time signature setting to command.

        Return command.
        '''
        from experimental.tools import settingtools
        anchor_timespan = score_specification.get_anchor_timespan(self, voice_name)
        command = settingtools.TimeSignatureRegionCommand(
            self.request, self.context_name, anchor_timespan, fresh=self.fresh)
        return command

    def make_time_signatures(self, score_specification):
        from experimental.tools import requesttools
        from experimental.tools import selectortools
        if isinstance(self.request, requesttools.AbsoluteRequest):
            time_signatures = self.request.get_payload(score_specification)
        elif isinstance(self.request, requesttools.TimeSignatureCommandRequest):
            time_signatures = self.request.get_payload(score_specification)
        # TODO: Maybe extend BackgroundMeasureSelector.get_payload() method 
        #       This will parallel TimeSignatureCommandRequest.get_payload() method.
        elif isinstance(self.request, selectortools.BackgroundMeasureSelector):
            time_signatures = self.request._get_time_signatures_without_timespan(score_specification)
        else:
            raise TypeError(self.request)
        if time_signatures:
            segment_specification = score_specification.get_start_segment_specification(self.anchor)
            segment_specification._time_signatures = time_signatures[:]
            return time_signatures
