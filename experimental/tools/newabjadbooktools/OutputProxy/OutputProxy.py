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
    def file_name_prefix(self):
        return self.__class__.__name__.strip('OutputProxy').lower()

    @property
    def file_name_without_extension(self):
        md5 = hashlib.md5(self.payload).hexdigest()
        return '-'.join((self._file_name_prefix, md5))

    @property
    def payload(self):
        return self._payload

    ### PUBLIC METHODS ###

    def handle_doctree_document_environment(self, document_handler):
        raise NotImplemented

    def handle_html_document_environment(self, document_handler):
        raise NotImplemented

    def handle_latex_document_environment(self, document_handler):
        raise NotImplemented

    def handle_rest_document_environment(self, document_handler):
        raise NotImplemented

    def handle_text_document_environment(self, document_handler):
        raise NotImplemented

