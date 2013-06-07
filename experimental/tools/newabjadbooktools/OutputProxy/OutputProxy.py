from abjad.tools.abctools import AbjadObject


class OutputProxy(AbjadObject):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_payload',
        )

    ### INITIALIZER ###

    def __init__(self, payload):
        self._payload = payload
        
    ### READ-ONLY PUBLIC ATTRIBUTES ###

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

