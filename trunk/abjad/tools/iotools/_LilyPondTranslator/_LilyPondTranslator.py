from abjad.tools.iotools._LilyPondLexer._LilyPondLexer import _LilyPondLexer
from abjad.tools.iotools._LilyPondParser._LilyPondParser import _LilyPondParser


class _LilyPondTranslator(object):

    def __init__(self):
        self._lexer = _LilyPondLexer( )
        self._parser = _LilyPondParser( )

    ### OVERRIDES ###

    def __call__(self, lily_string):
        tokens = self._lexer(lily_string)
        objects = self._parser(tokens, lily_string)
        # components = self._translate_objects(objects, lily_string)
        return objects

