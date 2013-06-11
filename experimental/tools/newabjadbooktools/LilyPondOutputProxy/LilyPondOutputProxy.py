import copy
from experimental.tools.newabjadbooktools.ImageOutputProxy import ImageOutputProxy
from abjad.tools.iotools._insert_expr_into_lilypond_file import _insert_expr_into_lilypond_file


class LilyPondOutputProxy(ImageOutputProxy):

    ### CLASS VARIABLES ###

    def __init__(self, payload):
        if isinstance(payload, str):
            self._payload = payload
        else:
            payload = copy.deepcopy(payload)
            lilypond_file = _insert_expr_into_lilypond_file(payload)
            lilypond_file.file_initial_system_comments[:] = []
            lilypond_format = lilypond_file.lilypond_format
            self._payload = lilypond_format
             
    ### PUBLIC METHODS ###

    def handle_rest_document_environment(self, document_handler):
        result = []
        result.append('.. image:: {}.png'.format(
            self.file_name_without_extension,
            ))
        result.append('')
        return result
