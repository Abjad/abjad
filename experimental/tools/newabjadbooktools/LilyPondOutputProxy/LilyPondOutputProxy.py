import copy
from experimental.tools.newabjadbooktools.ImageOutputProxy import ImageOutputProxy


class LilyPondOutputProxy(ImageOutputProxy):

    ### CLASS VARIABLES ###

    def __init__(self, payload):
        if isinstance(payload, str):
            self._payload = payload
        else:
            from abjad.tools.iotools._insert_expr_into_lilypond_file import _insert_expr_into_lilypond_file
            lilypond_file = _insert_expr_into_lilypond_file(payload)
            lilypond_format = lilypond_file.lilypond_format
            self._payload = lilypond_format
             
