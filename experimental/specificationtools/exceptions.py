class ExtraContextSettingError(Exception):
    '''More than one setting found.
    '''
    pass


class MissingContextSettingError(Exception):
    '''No setting found.
    '''
    pass
