from abjad.cfg.cfg import ABJADCONFIG


def read_abjad_user_config_file(attribute_name):
    '''Read the content of the config file ``$HOME/.abjad/config.py``.

    Returns a dictionary of var : value entries.

    .. versionchanged:: 2.10
        renamed ``configurationtools.read_user_abjad_config_file()`` to
        ``configurationtools.read_abjad_user_config_file()``.
    '''
    from abjad.tools import configurationtools

    configurationtools.verify_abjad_user_config_file()

    return configurationtools.make_abjad_user_config_file_into_dict()[attribute_name]
