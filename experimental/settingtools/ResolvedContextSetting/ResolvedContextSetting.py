from experimental.settingtools.SingleContextSetting import SingleContextSetting


class ResolvedContextSetting(SingleContextSetting):
    
    ### INITIALIZER ###

    def __init__(self, target, attribute, source, value, persistent=True, truncate=False, fresh=True):
        SingleContextSetting.__init__(self, target, attribute, source, persistent=persistent, truncate=truncate)
        assert value is not None, repr(value)
        assert isinstance(fresh, bool), repr(fresh)
        self._value = value
        self._fresh = fresh

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def value(self):
        return self._value
