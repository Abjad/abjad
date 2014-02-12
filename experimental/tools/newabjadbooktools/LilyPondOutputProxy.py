# -*- encoding: utf-8 -*-
import copy
import os
from abjad.tools import systemtools
from abjad.tools import lilypondfiletools
from experimental.tools.newabjadbooktools.ImageOutputProxy \
    import ImageOutputProxy


class LilyPondOutputProxy(ImageOutputProxy):
    r'''Output proxy for LilyPond notation:

    ::

        >>> payload = Staff("c'4 d'4 e'4 f'4")
        >>> output_proxy = newabjadbooktools.LilyPondOutputProxy(payload)
        >>> print output_proxy
        LilyPondOutputProxy('\\version "2.19.0"\n\\language "english"\n\n\\header {}\n\n\\layout {}\n\n\\paper {}\n\n\\score {\n\t\\new Staff {\n\t\tc\'4\n\t\td\'4\n\t\te\'4\n\t\tf\'4\n\t}\n}')

    Returns output proxy.
    '''

    ### INITIALIZER ###

    def __init__(self, payload):
        from abjad import abjad_configuration
        if isinstance(payload, str):
            self._payload = payload
        else:
            payload = copy.deepcopy(payload)
            manager = systemtools.IOManager
            lilypond_file = manager._insert_expr_into_lilypond_file(payload)
            lilypond_file.file_initial_system_comments[:] = []
            token = lilypondfiletools.LilyPondVersionToken(
                abjad_configuration.get_lilypond_minimum_version_string(),
                )
            lilypond_file.file_initial_system_includes[0] = token
            lilypond_format = format(lilypond_file)
            self._payload = lilypond_format
             
    ### PUBLIC METHODS ###

    def handle_html_document_environment(self, document_handler):
        r'''Handle an HTML document environment:

        ::

            >>> document_handler = newabjadbooktools.HTMLDocumentHandler([])
            >>> output_proxy.handle_html_document_environment(document_handler)
            ['<img alt="" src="assets/lilypond-....png"/>']

        Returns list.
        '''
        return ImageOutputProxy.handle_html_document_environment(
            self,
            document_handler,
            )

    def handle_latex_document_environment(self, document_handler):
        r'''Handle a LaTeX document environment:

        ::

            >>> document_handler = newabjadbooktools.LaTeXDocumentHandler([])
            >>> output_proxy.handle_latex_document_environment(document_handler)
            ['\\includegraphics{assets/lilypond-....pdf}']

        Returns list.
        '''
        return ImageOutputProxy.handle_latex_document_environment(
            self,
            document_handler,
            )

    def handle_rest_document_environment(self, document_handler):
        r'''Handle an ReST document environment:

        ::

            >>> document_handler = newabjadbooktools.ReSTDocumentHandler([])
            >>> output_proxy.handle_rest_document_environment(document_handler)
            ['.. image:: assets/lilypond-....png']

        Returns list.
        '''
        return ImageOutputProxy.handle_rest_document_environment(
            self,
            document_handler,
            )
