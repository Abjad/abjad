class ExtraSettingError(Exception):
    '''More than one setting found.
    '''
    pass


class MissingSettingError(Exception):
    '''No setting found.
    '''
    pass
