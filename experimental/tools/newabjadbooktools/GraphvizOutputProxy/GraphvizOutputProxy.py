# -*- encoding: utf-8 -*-
from experimental.tools.newabjadbooktools.ImageOutputProxy \
    import ImageOutputProxy


class GraphvizOutputProxy(ImageOutputProxy):
    r'''Output proxy for Graphviz images of Abjad datastructures:

    ::

        >>> metrical_hierarchy = timesignaturetools.MetricalHierarchy((4, 4))
        >>> print metrical_hierarchy.graphviz_format
        digraph G {
            node_0 [label="4/4",
                shape=triangle];
            node_1 [label="1/4",
                shape=box];
            node_2 [label="1/4",
                shape=box];
            node_3 [label="1/4",
                shape=box];
            node_4 [label="1/4",
                shape=box];
            node_0 -> node_1;
            node_0 -> node_2;
            node_0 -> node_3;
            node_0 -> node_4;
        }
        >>> iotools.graph(metrical_hierarchy) # doctest: +SKIP

    ::

        >>> output_proxy = \
        ...     newabjadbooktools.GraphvizOutputProxy(metrical_hierarchy)

    Return output proxy.
    '''

    ### INITIALIZER ###

    def __init__(self, payload):
        if isinstance(payload, str):
            self._payload = payload
        else:
            graphviz_format = payload.graphviz_format
            self._payload = graphviz_format
             
    ### PUBLIC METHODS ###

    def handle_html_document_environment(self, document_handler):
        r'''Handle an HTML document environment:

        ::

            >>> document_handler = newabjadbooktools.HTMLDocumentHandler([])
            >>> output_proxy.handle_html_document_environment(document_handler)
            ['<img alt="" src="assets/graphviz-e35e25d3a5dcb97ec2d6c43352727dbf.png"/>']

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
            ['\\includegraphics{assets/graphviz-e35e25d3a5dcb97ec2d6c43352727dbf.pdf}']

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
            ['.. image:: assets/graphviz-e35e25d3a5dcb97ec2d6c43352727dbf.png']

        Return list.
        '''
        return ImageOutputProxy.handle_rest_document_environment(
            self,
            document_handler,
            )

