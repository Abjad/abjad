from abjad.tools.iotools._LilyPondTokenizer._LilyPondTokenizer import _LilyPondTokenizer
from abjad.tools.iotools._LilyPondTokenGrouper._LilyPondTokenGrouper import _LilyPondTokenGrouper


class _LilyPondParser(object):

    def __init__(self):
        self._tokenizer = _LilyPondTokenizer( )
        self._grouper = _LilyPondTokenGrouper( )

    ### OVERRIDES ###

    def __call__(self, lily_string):
        tokens = self._tokenizer(lily_string)
        objects = self._grouper(tokens, lily_string)
        # components = self._parse_objects(objects, lily_string)
        return objects

