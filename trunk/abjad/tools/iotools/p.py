def p(*args):
    from abjad.tools.lilypondparsertools import LilyPondParser
    if 1 < len(args):
        return LilyPondParser(default_language=args[1])(args[0])
    return LilyPondParser()(args[0])
