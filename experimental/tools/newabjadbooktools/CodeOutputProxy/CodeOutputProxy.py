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
    
    ### READ-ONLY PRIVATE ATTRIBUTES ###

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

    def handle_rest_document_environment(self, document_handler):
        '''ReST output:

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
            ''

        Return list.
        '''

        result = [
            '::',
            '',
            ]
        for line in self.payload:
            result.append('\t{}'.format(line))
        result.append('')
        return result

