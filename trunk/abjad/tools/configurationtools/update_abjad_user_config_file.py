from abjad.cfg.cfg import ABJADCONFIG


def update_abjad_user_config_file(default_dict, user_dict):
    '''
    Default dict is drawn from Abjad config file dict.

    User dict is drawn from reading Abjad config file.
    '''
    from abjad.tools import configurationtools

    default_keyset = set(default_dict.keys())
    user_keyset = set(user_dict.keys())

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

    configurationtools.write_abjad_user_config_file(ABJADCONFIG, default_dict)
