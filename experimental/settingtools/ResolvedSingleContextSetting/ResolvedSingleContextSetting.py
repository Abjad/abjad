from experimental.settingtools.SingleContextSetting import SingleContextSetting


class ResolvedSingleContextSetting(SingleContextSetting):
    
    ### INITIALIZER ###

    def __init__(self, attribute, source, value, target, persist=True, truncate=False, fresh=True):
        SingleContextSetting.__init__(self, attribute, source, target, persist=persist, truncate=truncate)
        assert value is not None, repr(value)
        assert isinstance(fresh, bool), repr(fresh)
        self._value = value
        self._fresh = fresh

    ### READ-ONLY PUBLIC PROPERTIES ###

    # TODO: change name to self.resolved_value
    @property
    def value(self):
        '''Value of resolved source.
        '''
        return self._value
