from abjad.cfg.cfg import ABJADCONFIG


def abjad_config_file_to_dict():
    globals = {}
    locals = {}
    execfile(ABJADCONFIG, globals, locals)
    return locals
