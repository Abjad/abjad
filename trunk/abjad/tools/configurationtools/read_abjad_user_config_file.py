def read_abjad_user_config_file(attribute_name):
    '''Read the content of the config file ``$HOME/.abjad/config.py``.

    Returns a dictionary of var : value entries.

    .. versionchanged:: 2.10
        renamed ``configurationtools.read_user_abjad_config_file()`` to
        ``ABJCFG()``.
    '''
    from abjad import ABJCFG

    return ABJCFG[attribute_name]
