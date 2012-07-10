from abjad.cfg.cfg import ABJADCONFIG, HOME
import os


def setup_abjad_directory():
    '''Silently setup .abjad/, .abjad/output/ and .abjad/config.py.

    Create directories if they do not already exist.

    Create config.py if it does not already exist.

    Update config.py if it is out of date.
    '''

    from abjad.tools import configurationtools

    # create $HOME/.abjad/
    DOTABJADPATH = os.path.join(HOME, '.abjad')
    if not os.path.exists(DOTABJADPATH):
        os.mkdir(DOTABJADPATH)

    # create $HOME/.abjad/config.py
    default_dict = configurationtools.make_abjad_default_config_file_into_dict()
    try:
        user_dict = configurationtools.make_abjad_user_config_file_into_dict()
        default_keyset = set(default_dict.keys())
        user_keyset = set(user_dict.keys())
        if default_keyset.intersection(user_keyset) != default_keyset:
            configurationtools.update_abjad_user_config_file(default_dict, user_dict)    
    except IOError:
        configurationtools.write_abjad_user_config_file(ABJADCONFIG, default_dict)

    # create output path (user defined in config.py, and $HOME/.abjad/output by default)
    ABJADOUTPUT = configurationtools.read_abjad_user_config_file('abjad_output')
    if not os.path.exists(ABJADOUTPUT):
        os.mkdir(ABJADOUTPUT)

