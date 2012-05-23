from abjad.cfg.cfg import ABJADCONFIG


def read_user_abjad_config_file(attribute_name):
    '''Read the content of the config file ``$HOME/.abjad/config.py``.

    Returns a dictionary of var : value entries.
    '''
    from abjad.tools import configurationtools

    configurationtools.verify_abjad_config_file()

    return configurationtools.make_abjad_user_config_file_into_dict()[attribute_name]
