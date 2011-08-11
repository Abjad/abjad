from abjad.cfg._config_file_to_dict import _config_file_to_dict
from abjad.cfg._verify_config_file import _verify_config_file
from abjad.cfg.cfg import ABJADCONFIG


def _read_config_file( ):
    '''Read the content of the config file ``$HOME/.abjad/config.py``.
    Returns a dictionary of var : value entries.'''

    _verify_config_file( )
    return _config_file_to_dict( )
