from abjad.cfg.cfg import ABJADCONFIG


def _config_file_to_dict( ):
    globals = { }
    locals = { }
    execfile(ABJADCONFIG, globals, locals)
    return locals
