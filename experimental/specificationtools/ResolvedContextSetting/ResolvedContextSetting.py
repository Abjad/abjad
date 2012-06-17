from experimental.specificationtools.ContextSetting import ContextSetting


class ResolvedContextSetting(ContextSetting):
    
    ### INITIALIZER ###

    def __init__(self, target, attribute, source, value, persistent=True, truncate=False, fresh=True):
        ContextSetting.__init__(self, target, attribute, source, persistent=persistent, truncate=truncate)
        assert value is not None, repr(value)
        assert isinstance(fresh, bool), repr(fresh)
        self._value = value
        self._fresh = fresh

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def value(self):
        return self._value
