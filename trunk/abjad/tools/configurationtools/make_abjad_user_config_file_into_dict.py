from abjad.cfg.cfg import ABJADCONFIG


def make_abjad_user_config_file_into_dict():
    globals = {}
    locals = {}
    execfile(ABJADCONFIG, globals, locals)
    return locals
