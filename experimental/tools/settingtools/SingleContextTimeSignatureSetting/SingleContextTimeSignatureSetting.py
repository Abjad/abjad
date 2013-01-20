from experimental.tools.settingtools.SingleContextSetting import SingleContextSetting


class SingleContextTimeSignatureSetting(SingleContextSetting):
    r'''Single-context time signature setting.
    '''

    ### INITIALIZER ###

    def __init__(self, expression=None, anchor=None, context_name=None, fresh=True, persist=True):
        SingleContextSetting.__init__(self, attribute='time_signatures', expression=expression, 
            anchor=anchor, context_name=context_name, fresh=fresh, persist=persist)

    ### PUBLIC METHODS ###

    def make_time_signatures(self, score_specification):
        if hasattr(self.expression, '_evaluate_early'):
            time_signatures = self.expression._evaluate_early(score_specification)
        else:
            time_signatures = self.expression._evaluate(score_specification)
        if time_signatures:
            segment_specification = score_specification.get_start_segment_specification(self.anchor)
            segment_specification._time_signatures = time_signatures[:]
            return time_signatures

    def to_command(self, score_specification, voice_name):
        '''Change single-context time signature setting to command.

        Return command.
        '''
        from experimental.tools import settingtools
        anchor_timespan = score_specification.get_anchor_timespan(self, voice_name)
        command = settingtools.TimeSignatureRegionCommand(
            self.expression, self.context_name, anchor_timespan, fresh=self.fresh)
        return command
