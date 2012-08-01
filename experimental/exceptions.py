class ExtraContextSettingError(Exception):
    '''More than one setting found.
    '''
    pass


class MissingContextSettingError(Exception):
    '''No setting found.
    '''
    pass


class MultipleContextSelectorError(Exception):
    '''Operation should ask for single-context selector
    instead of multiple-context selector.
    '''
    pass


class SingleContextSelectorError(Exception):
    '''Operation should ask for multiple-context selector
    instead of single-context selector.
    '''
    pass
