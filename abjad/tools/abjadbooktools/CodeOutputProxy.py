# -*- encoding: utf-8 -*-
from abjad.tools import abctools
from docutils import nodes


class CodeOutputProxy(abctools.AbjadValueObject):
    r'''A code output proxy.

    ::

        >>> proxy = abjadbooktools.CodeOutputProxy([
        ...     ">>> print('Hello, world!')",
        ...     'Hello, world!',
        ...     '>>> 1 + 1',
        ...     '2',
        ...     ])
        >>> print(format(proxy))
        abjadbooktools.CodeOutputProxy(
            (
                ">>> print('Hello, world!')",
                'Hello, world!',
                '>>> 1 + 1',
                '2',
                )
            )

    ::

        >>> for line in proxy.as_latex():
        ...     line
        ...
        '\\begin{lstlisting}'
        ">>> print('Hello, world!')"
        'Hello, world!'
        '\\end{lstlisting}'
        '\\begin{lstlisting}'
        '>>> 1 + 1'
        '2'
        '\\end{lstlisting}'

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_payload',
        )

    ### INITIALIZER ###

    def __init__(self, payload):
        self._payload = tuple(payload)

    ### PUBLIC METHODS ###

    def as_docutils(
        self,
        ):
        r'''Creates a docutils node representation of the code output proxy.

        Returns list of docutils nodes.
        '''
        result = []
        waiting_for_prompt = False
        lines = []
        for line in self.payload:
            if not line.startswith(('>>> ', '... ')):
                waiting_for_prompt = True
            elif line.startswith('>>> ') and waiting_for_prompt:
                waiting_for_prompt = False
                code = '\n'.join(lines)
                block = nodes.literal_block(code, code)
                result.append(block)
                lines = []
            lines.append(line)
        if lines:
            code = '\n'.join(lines)
            block = nodes.literal_block(code, code)
            result.append(block)
        return result

    def as_latex(
        self,
        configuration=None,
        output_directory=None,
        relative_output_directory=None,
        ):
        r'''Creates a LaTeX representation of the code output proxy.

        Returns list of strings.
        '''
        #lexer = 'pycon'
        #if not self.payload[0].startswith('>>>'):
        #    lexer = 'python'
        start_command = r'\begin{lstlisting}'
        stop_command = r'\end{lstlisting}'
        result = []
        result.append(start_command)
        waiting_for_prompt = False
        for line in self.payload:
            if not line.startswith(('>>> ', '... ')):
                waiting_for_prompt = True
            elif line.startswith('>>> ') and waiting_for_prompt:
                waiting_for_prompt = False
                result.append(stop_command)
                result.append(start_command)
            result.append(line)
        result.append(stop_command)
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def payload(self):
        r'''Gets code output proxy payload.

        Returns tuple of strings.
        '''
        return self._payload