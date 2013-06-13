import abc
import hashlib
from abjad.tools.abctools import AbjadObject


class OutputProxy(AbjadObject):
    r'''Abstact base class for all abjad-book output proxies.

    An output proxy handles generating a document representation for a given
    structure in different documentation environments:

    ::

        >>> staff = Staff("c'4-> \f d'4 ( e'4 f'4 )")
        >>> output_proxy = newabjadbooktools.LilyPondOutputProxy(staff)
        >>> print output_proxy
        LilyPondOutputProxy()

    ::

        >>> html_handler = newabjadbooktools.HTMLDocumentHandler([])
        >>> result = output_proxy.generate_document_representation(html_handler)
        >>> print '\n'.join(result)
        <img alt="" src="assets/lilypond-ec7dff190fe7b4e72b53063e3914670c.png"/>
        <BLANKLINE>

    ::

        >>> latex_handler = newabjadbooktools.LaTeXDocumentHandler([])
        >>> result = output_proxy.generate_document_representation(latex_handler)
        >>> print '\n'.join(result)
        \includegraphics{assets/lilypond-ec7dff190fe7b4e72b53063e3914670c.pdf}
        <BLANKLINE>

    ::

        >>> rest_handler = newabjadbooktools.ReSTDocumentHandler([])
        >>> result = output_proxy.generate_document_representation(rest_handler)
        >>> print '\n'.join(result)
        .. image:: assets/lilypond-ec7dff190fe7b4e72b53063e3914670c.png
        <BLANKLINE>

    Return output proxy.
    '''

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
        '''The document-environment-agnostic payload of an output proxy.
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


