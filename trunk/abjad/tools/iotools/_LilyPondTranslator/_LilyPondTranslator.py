from abjad.tools.iotools._LilyPondLexer._LilyPondLexer import _LilyPondLexer
from abjad.tools.iotools._LilyPondTokenGrouper._LilyPondTokenGrouper import _LilyPondTokenGrouper


class _LilyPondTranslator(object):

    def __init__(self):
        self._lexer = _LilyPondLexer( )
        self._grouper = _LilyPondTokenGrouper( )

    ### OVERRIDES ###

    def __call__(self, lily_string):
        tokens = self._lexer(lily_string)
        objects = self._grouper(tokens, lily_string)
        # components = self._parse_objects(objects, lily_string)
        return objects

