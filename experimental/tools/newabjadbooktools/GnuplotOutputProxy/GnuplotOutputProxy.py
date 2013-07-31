from experimental.tools.newabjadbooktools.ImageOutputProxy \
    import ImageOutputProxy


class GnuplotOutputProxy(ImageOutputProxy):
    r'''Output proxy for Gnuplot images of Abjad datastructures:

    ::

        >>> bpf = datastructuretools.BreakPointFunction({
        ...     0.:   0.,  
        ...     0.75: (-1, 1.),
        ...     1.:   0.25,
        ...     })

    ::

        >>> output_proxy = newabjadbooktools.GnuplotOutputProxy(bpf)

    Return output proxy.
    '''

    ### INITIALIZER ###

    def __init__(self, payload):
        if isinstance(payload, str):
            self._payload = payload
        else:
            gnuplot_format = payload.gnuplot_format
            self._payload = gnuplot_format

    ### PUBLIC METHODS ###
             
    def handle_html_document_environment(self, document_handler):
        r'''Handle an HTML document environment:

        ::

            >>> document_handler = newabjadbooktools.HTMLDocumentHandler([])
            >>> output_proxy.handle_html_document_environment(document_handler)
            ['<img alt="" src="assets/gnuplot-14219af1a9b714fc222091106ca83f50.png"/>']

        Return list.
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
            ['\\includegraphics{assets/gnuplot-14219af1a9b714fc222091106ca83f50.pdf}']

        Return list.
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
            ['.. image:: assets/gnuplot-14219af1a9b714fc222091106ca83f50.png']

        Return list.
        '''
        return ImageOutputProxy.handle_rest_document_environment(
            self,
            document_handler,
            )
