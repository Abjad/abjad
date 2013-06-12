import abc
import hashlib
from abjad.tools.abctools import AbjadObject


class OutputProxy(AbjadObject):

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, payload):
        raise NotImplemented
        
    ### READ-ONLY PRIVATE ATTRIBUTES ###

    @property
    def _contents_repr_string(self):
        return ''

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def payload(self):
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


