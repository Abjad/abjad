from abjad.cfg._write_config_file import _write_config_file
from abjad.cfg.cfg import ABJADCONFIG


def _update_config_file(default_dict, user_dict):
    '''
    default_dict is drawn from abjad.cfg._config_file_dict.
    user_dict is drawn from abjad.cfg._read_config_file.
    '''

    default_keyset = set(default_dict.keys( ))
    user_keyset = set(user_dict.keys( ))

    all_keys = sorted(list(default_keyset.union(user_keyset)))

    for key in all_keys:
        if key in default_keyset.intersection(user_keyset):
            default_dict[key]['value'] = user_dict[key]
        elif key in user_keyset:
            default_dict[key] = {}
            default_dict[key]['comment'] = ''
            default_dict[key]['value'] = user_dict[key]
        else:
            pass

    _write_config_file(ABJADCONFIG, default_dict)
