from baca.specificationtools.Setting import Setting


class ResolvedSetting(Setting):
    
    ### INITIALIZER ###

    def __init__(self, 
        segment_name, context_name, scope, attribute_name, source, persistent, truncate, value, 
        fresh=True):
        Setting.__init__(self, segment_name, context_name, scope, attribute_name, source, 
        persistent, truncate)
        assert value is not None, value
        assert isinstance(fresh, type(True)), fresh
        self.value = value
        self.fresh = fresh
