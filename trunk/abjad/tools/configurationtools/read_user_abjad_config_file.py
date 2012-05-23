from abjad.cfg.cfg import ABJADCONFIG


def read_user_abjad_config_file(attribute_name=None):
    '''Read the content of the config file ``$HOME/.abjad/config.py``.

    Returns a dictionary of var : value entries.
    '''
    from abjad.tools import configurationtools

    configurationtools.verify_abjad_config_file()

    config_file_dict = configurationtools.get_default_abjad_config_file_as_dict()

    if attribute_name is not None:
        return config_file_dict[attribute_name]['value']
    else:
        return config_file_dict
