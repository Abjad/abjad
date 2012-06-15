from experimental.specificationtools.Setting import Setting


class ResolvedSetting(Setting):
    
    ### INITIALIZER ###

    def __init__(self, target, attribute_name, source, persistent, truncate, value, fresh=True):
        Setting.__init__(self, target, attribute_name, source, persistent, truncate)
        assert value is not None, repr(value)
        assert isinstance(fresh, bool), repr(fresh)
        self._value = value
        self._fresh = fresh

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def fresh(self):
        return self._fresh

    @property
    def value(self):
        return self._value
