# -*- coding: utf-8 -*-
from abjad.tools import abctools
from docutils import nodes


class CodeOutputProxy(abctools.AbjadValueObject):
    r'''A code output proxy.

    ::

        >>> from abjad.tools import abjadbooktools
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

    __documentation_section__ = 'Output Proxies'

    __slots__ = (
        '_code_block_specifier',
        '_payload',
        )

    ### INITIALIZER ###

    def __init__(self, payload, code_block_specifier=None):
        self._payload = tuple(payload)
        self._code_block_specifier = code_block_specifier

    ### PUBLIC METHODS ###

    def as_docutils(
        self,
        configuration=None,
        output_directory=None,
        ):
        r'''Creates a docutils node representation of the code output proxy.

        Returns list of docutils nodes.
        '''
        result = []
        try:
            waiting_for_prompt = False
            lines = []
            for line in self.payload:
                if not line.startswith(('>>> ', '... ')):
                    waiting_for_prompt = True
                elif line.startswith('>>> ') and waiting_for_prompt:
                    waiting_for_prompt = False
                    code = u'\n'.join(lines)
                    block = nodes.literal_block(code, code)
                    result.append(block)
                    lines = []
                lines.append(line)
            if lines:
                code = u'\n'.join(lines)
                block = nodes.literal_block(code, code)
                result.append(block)
        except UnicodeDecodeError:
            print()
            print(type(self))
            for line in self.payload:
                print(repr(line))
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

        configuration = configuration or {}
        latex_configuration = configuration.get('latex', {})
        start_command = latex_configuration.get(
            'code-block-start',
            [r'\begin{lstlisting}'],
            )
        start_command = '\n'.join(start_command)
        stop_command = latex_configuration.get(
            'code-block-stop',
            [r'\end{lstlisting}'],
            )
        stop_command = '\n'.join(stop_command)
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
    def code_block_specifier(self):
        r'''Gets code block specifier.
        '''
        return self._code_block_specifier

    @property
    def payload(self):
        r'''Gets code output proxy payload.

        Returns tuple of strings.
        '''
        return self._payload
