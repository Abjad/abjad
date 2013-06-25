from experimental.tools.newabjadbooktools.OutputProxy import OutputProxy


class CodeOutputProxy(OutputProxy):
    '''Output proxy for a block of code:

    ::

        >>> payload = [
        ...     '>>> print "hello, world!"',
        ...     'hello, world!',
        ...     ]
        >>> output_proxy = newabjadbooktools.CodeOutputProxy(payload)
        >>> print output_proxy
        CodeOutputProxy((
            '>>> print "hello, world!"',
            'hello, world!',
            ))

    Return output proxy.
    '''

    ### INITIALIZER ###

    def __init__(self, payload):
        self._payload = tuple(payload)
    
    ### PRIVATE ATTRIBUTES ###

    @property
    def _contents_repr_string(self):
        result = ''
        if len(self.payload):
            result = '(\n'
            for x in self._payload:
                result += '\t{!r},\n'.format(x)
            result += '\t)'
        return result

    ### PUBLIC METHODS ###

    def handle_html_document_environment(self, document_handler):
        '''Handle an HTML document environment:

        ::

            >>> document_handler = newabjadbooktools.HTMLDocumentHandler([])
            >>> result = output_proxy.handle_html_document_environment(
            ...     document_handler)
            >>> for x in result:
            ...     x
            '<pre class="abjad">'
            '>>> print "hello, world!"'
            'hello, world!'
            '</pre>'

        Return list.
        '''
        result = []
        result.append('<pre class="abjad">')
        for line in self.payload:
            result.append(line)
        result.append('</pre>')
        return result

    def handle_latex_document_environment(self, document_handler):
        '''Handle a LaTeX document environment:

        ::
        
            >>> document_handler = newabjadbooktools.LaTeXDocumentHandler([])
            >>> result = output_proxy.handle_latex_document_environment(
            ...     document_handler)
            >>> for x in result:
            ...     x
            '\\begin{lstlisting}['
            '\tbasicstyle=\\footnotesize\\ttfamily,'
            '\tbreaklines=true,'
            '\ttabsize=4,'
            '\tshowtabs=false,'
            '\tshowspaces=false'
            '\t]'
            '>>> print "hello, world!"'
            'hello, world!'
            '\\end{lstlisting}'

        Return list.
        '''
        result = []
        result.append('\\begin{lstlisting}[')
        result.append('\tbasicstyle=\\footnotesize\\ttfamily,')
        result.append('\tbreaklines=true,')
        result.append('\ttabsize=4,')
        result.append('\tshowtabs=false,')
        result.append('\tshowspaces=false')
        result.append('\t]')
        for line in self.payload:
            result.append(line)
        result.append('\\end{lstlisting}')
        return result

    def handle_rest_document_environment(self, document_handler):
        '''Handle an ReST document environment:

        ::

            >>> document_handler = newabjadbooktools.ReSTDocumentHandler([])
            >>> result = output_proxy.handle_rest_document_environment(
            ...     document_handler)
            >>> for x in result:
            ...     x
            '::'
            ''
            '\t>>> print "hello, world!"'
            '\thello, world!'

        Return list.
        '''
        result = [
            '::',
            '',
            ]
        for line in self.payload:
            result.append('\t{}'.format(line))
        return result

