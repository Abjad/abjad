from abjad.cfg.cfg import ABJADCONFIG


def get_user_abjad_config_file_as_dict():
    globals = {}
    locals = {}
    execfile(ABJADCONFIG, globals, locals)
    return locals
