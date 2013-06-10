import copy
from abjad.tools import lilypondfiletools
from experimental.tools.newabjadbooktools.AssetOutputProxy import AssetOutputProxy


class MIDIOutputProxy(AssetOutputProxy):

    ### CLASS VARIABLES ###

    def __init__(self, payload):
        if isinstance(payload, str):
            self._payload = payload
        else:
            from abjad.tools.iotools._insert_expr_into_lilypond_file import _insert_expr_into_lilypond_file
            lilypond_file = _insert_expr_into_lilypond_file(payload)
            lilypond_file.score_block.append(lilypondfiletools.MIDIBlock())
            lilypond_format = lilypond_file.lilypond_format
            self._payload = lilypond_format
             
