def read_abjad_user_config_file(attribute_name):
    '''Read the content of the config file ``$home/.abjad/config.py``.

    Returns a dictionary of var : value entries.
    '''
    from abjad import ABJCFG

    return ABJCFG[attribute_name]
