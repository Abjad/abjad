# -*- encoding: utf-8 -*-
import abc
import hashlib
from abjad.tools.abctools import AbjadObject


class OutputProxy(AbjadObject):
    r'''Abstact base class for all abjad-book output managers.

    An output proxy handles generating a document representation for a given
    structure in different documentation environments:

    ::

        >>> staff = Staff("c'4-> \f d'4 ( e'4 f'4 )")
        >>> output_proxy = newabjadbooktools.LilyPondOutputProxy(staff)
        >>> print output_proxy
        LilyPondOutputProxy('\\version "2.19.0"\n\\language "english"\n\n\\score {\n\t\\new Staff {\n\t\tc\'4\n\t\td\'4 (\n\t\te\'4\n\t\tf\'4 )\n\t}\n}')

    ::

        >>> html_handler = newabjadbooktools.HTMLDocumentHandler([])
        >>> output_proxy.generate_document_representation(html_handler)
        ['<img alt="" src="assets/lilypond-....png"/>']

    ::

        >>> latex_handler = newabjadbooktools.LaTeXDocumentHandler([])
        >>> output_proxy.generate_document_representation(latex_handler)
        ['\\includegraphics{assets/lilypond-....pdf}']

    ::

        >>> rest_handler = newabjadbooktools.ReSTDocumentHandler([])
        >>> output_proxy.generate_document_representation(rest_handler)
        ['.. image:: assets/lilypond-....png']

    Returns output proxy.
    '''

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, payload):
        raise NotImplemented
        
    ### PRIVATE ATTRIBUTES ###

    @property
    def _contents_repr_string(self):
        return ''

    ### PUBLIC ATTRIBUTES ###

    @property
    def payload(self):
        r'''The document-environment-agnostic payload of an output proxy.
        '''
        return self._payload

    ### PUBLIC METHODS ###

    def generate_document_representation(self, document_handler):
        from experimental.tools import newabjadbooktools
        document_handler_mapping = {
            newabjadbooktools.DoctreeDocumentHandler:
                self.handle_doctree_document_environment,
            newabjadbooktools.HTMLDocumentHandler:
                self.handle_html_document_environment,
            newabjadbooktools.LaTeXDocumentHandler:
                self.handle_latex_document_environment,
            newabjadbooktools.ReSTDocumentHandler:
                self.handle_rest_document_environment,
            }
        assert type(document_handler) in document_handler_mapping
        procedure = document_handler_mapping[type(document_handler)]
        return procedure(document_handler)

    def handle_doctree_document_environment(self, document_handler):
        raise NotImplemented

    @abc.abstractmethod
    def handle_html_document_environment(self, document_handler):
        raise NotImplemented

    @abc.abstractmethod
    def handle_latex_document_environment(self, document_handler):
        raise NotImplemented

    @abc.abstractmethod
    def handle_rest_document_environment(self, document_handler):
        raise NotImplemented
