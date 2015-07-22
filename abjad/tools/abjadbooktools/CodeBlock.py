# -*- encoding: utf-8 -*-
from __future__ import print_function
import types
import importlib
import inspect
import textwrap
from abjad.tools import abctools
from abjad.tools import systemtools
from sphinx.util.console import bold, red


class CodeBlock(abctools.AbjadValueObject):
    r'''A code block.

    ::

        >>> from abjad.tools import abjadbooktools
        >>> console = abjadbooktools.AbjadBookConsole()
        >>> input_file_contents = [
        ...     'staff = Staff(r"\clef bass c4 d4 e4 f4")',
        ...     'show(staff)',
        ...     'print(len(staff))'
        ...     ]
        >>> code_block = abjadbooktools.CodeBlock(input_file_contents)
        >>> code_block.interpret(console)
        >>> for output_proxy in code_block.output_proxies:
        ...     print(format(output_proxy))
        ...
        abjadbooktools.CodeOutputProxy(
            (
                '>>> staff = Staff(r"\\clef bass c4 d4 e4 f4")',
                '>>> show(staff)',
                )
            )
        abjadbooktools.LilyPondOutputProxy(
            lilypondfiletools.LilyPondFile()
            )
        abjadbooktools.CodeOutputProxy(
            ('>>> print(len(staff))', '4')
            )

    ::

        >>> input_file_contents = [
        ...     'for leaf in staff:',
        ...     '    print(format(leaf))',
        ...     '    show(leaf)',
        ...     '',
        ...     ]
        >>> code_block = abjadbooktools.CodeBlock(input_file_contents)
        >>> code_block.interpret(console)
        >>> for output_proxy in code_block.output_proxies:
        ...     print(format(output_proxy))
        ...
        abjadbooktools.CodeOutputProxy(
            (
                '>>> for leaf in staff:',
                '...     print(format(leaf))',
                '...     show(leaf)',
                '... ',
                '\\clef "bass"',
                'c4',
                )
            )
        abjadbooktools.LilyPondOutputProxy(
            lilypondfiletools.LilyPondFile()
            )
        abjadbooktools.CodeOutputProxy(
            ('d4',)
            )
        abjadbooktools.LilyPondOutputProxy(
            lilypondfiletools.LilyPondFile()
            )
        abjadbooktools.CodeOutputProxy(
            ('e4',)
            )
        abjadbooktools.LilyPondOutputProxy(
            lilypondfiletools.LilyPondFile()
            )
        abjadbooktools.CodeOutputProxy(
            ('f4',)
            )
        abjadbooktools.LilyPondOutputProxy(
            lilypondfiletools.LilyPondFile()
            )

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_allow_exceptions',
        '_current_lines',
        '_document_source',
        '_executed_lines',
        '_hide',
        '_output_proxies',
        '_options',
        '_source_lines',
        '_starting_line_number',
        '_strip_prompt',
        '_stylesheet',
        '_text_width',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        input_file_contents,
        allow_exceptions=None,
        document_source=None,
        executed_lines=None,
        hide=None,
        starting_line_number=None,
        strip_prompt=None,
        stylesheet=None,
        text_width=None,
        **options
        ):
        if allow_exceptions is not None:
            allow_exceptions = bool(allow_exceptions)
        self._allow_exceptions = allow_exceptions
        self._document_source = document_source
        if executed_lines is not None:
            executed_lines = tuple(executed_lines)
        self._executed_lines = executed_lines
        if hide is not None:
            hide = bool(hide)
        self._hide = hide
        self._output_proxies = []
        self._source_lines = tuple(input_file_contents)
        if strip_prompt is not None:
            strip_prompt = bool(strip_prompt)
        self._starting_line_number = starting_line_number
        self._strip_prompt = strip_prompt
        self._current_lines = []
        self._stylesheet = stylesheet
        if text_width is not None:
            if text_width is True:
                text_width = 80
            text_width = abs(int(text_width))
            if text_width < 1:
                text_width = None
        self._text_width = text_width
        self._options = options

    ### PUBLIC METHODS ###

    def as_docutils(
        self,
        configuration=None,
        output_directory=None,
        ):
        result = []
        if self.output_proxies:
            for output_proxy in self.output_proxies:
                subresult = output_proxy.as_docutils(
                    configuration=configuration,
                    output_directory=output_directory,
                    )
                result.extend(subresult)
        return result

    def as_latex(
        self,
        configuration=None,
        output_directory=None,
        relative_output_directory=None,
        ):
        from abjad.tools import abjadbooktools
        result = []
        configuration = configuration or {}
        latex_configuration = configuration.get('latex', {})
        output_start_delimiter = latex_configuration.get(
            'output-start-delimiter',
            ('%%% ABJADBOOK START %%%',),
            )
        output_stop_delimiter = latex_configuration.get(
            'output-stop-delimiter',
            ('%%% ABJADBOOK END %%%',),
            )
        if self.output_proxies:
            result.extend(output_start_delimiter)
            before = latex_configuration.get('before-code-block', ())
            result.extend(before)
            for i, output_proxy in enumerate(self.output_proxies):
                lines = output_proxy.as_latex(
                    configuration=configuration,
                    output_directory=output_directory,
                    relative_output_directory=relative_output_directory,
                    )
                string = '\n'.join(lines)
                if isinstance(output_proxy, abjadbooktools.ImageOutputProxy):
                    if i < len(self.output_proxies) - 1:
                        next_proxy = self.output_proxies[i + 1]
                        if isinstance(next_proxy, abjadbooktools.ImageOutputProxy):
                            string += r'\\'
                result.append(string)
            after = latex_configuration.get('after-code-block', ())
            result.extend(after)
            result.extend(output_stop_delimiter)
            result = '\n'.join(result)
            result = [result]
        return result

    def flush(self):
        pass

    @staticmethod
    def from_latex_abjadextract_block(
        source_line,
        starting_line_number=None,
        **options
        ):
        from abjad.tools import abjadbooktools
        code_address = source_line.partition('<abjadextract ')[-1].split()[0]
        module_name, sep, attr_name = code_address.rpartition(':')
        module = importlib.import_module(module_name)
        attr = getattr(module, attr_name)
        input_file_contents = inspect.getsource(attr).splitlines()
        executed_lines = 'from {} import {}'.format(
            module_name,
            attr_name,
            )
        executed_lines = (executed_lines,)
        code_block = abjadbooktools.CodeBlock(
            executed_lines=executed_lines,
            input_file_contents=input_file_contents,
            starting_line_number=starting_line_number,
            **options
            )
        return code_block

    @staticmethod
    def from_latex_abjad_block(
        input_file_contents,
        starting_line_number=None,
        **options
        ):
        from abjad.tools import abjadbooktools
        code_block = abjadbooktools.CodeBlock(
            input_file_contents=input_file_contents,
            starting_line_number=starting_line_number,
            **options
            )
        return code_block

    @staticmethod
    def from_docutils_abjad_import_block(block):
        from abjad.tools import abjadbooktools
        code_address = block['path']
        module_name, sep, attr_name = code_address.rpartition(':')
        module = importlib.import_module(module_name)
        attr = getattr(module, attr_name)
        input_file_contents = inspect.getsource(attr).splitlines()
        executed_lines = 'from {} import {}'.format(
            module_name,
            attr_name,
            )
        executed_lines = (executed_lines,)
        options = {}
        for key, value in block.attlist():
            key = key.replace('-', '_')
            options[key] = value
        code_block = abjadbooktools.CodeBlock(
            executed_lines=executed_lines,
            input_file_contents=input_file_contents,
            starting_line_number=block.line,
            **options
            )
        return code_block

    @staticmethod
    def from_docutils_abjad_input_block(block):
        from abjad.tools import abjadbooktools
        input_file_contents = block[0][0].splitlines()
        input_file_contents = (str(_) for _ in input_file_contents)
        options = {}
        for key, value in block.attlist():
            key = key.replace('-', '_')
            options[key] = value
        code_block = abjadbooktools.CodeBlock(
            input_file_contents=input_file_contents,
            starting_line_number=block.line,
            **options
            )
        return code_block

    @staticmethod
    def from_docutils_literal_block(block):
        from abjad.tools import abjadbooktools
        input_file_contents = []
        for line in block[0].splitlines():
            if line.startswith(('>>>', '...')):
                input_file_contents.append(line[4:])
        document_source = None
        parent = block.parent
        while not document_source and getattr(parent, 'parent'):
            document_source = getattr(parent, 'source', None)
            parent = parent.parent
        code_block = abjadbooktools.CodeBlock(
            input_file_contents=input_file_contents,
            starting_line_number=block.line,
            document_source=document_source,
            )
        return code_block

    def interpret(self, console):
        from abjad.tools import abjadbooktools
        is_incomplete_statement = False
        input_file_contents = self.input_file_contents
        self.output_proxies[:] = []
        self.current_lines[:] = []
        self.setup_capture_hooks(console)
        if self.executed_lines:
            for executed_line in self.executed_lines:
                is_incomplete_statement = console.push(executed_line)
            code_output_proxy = abjadbooktools.CodeOutputProxy(input_file_contents)
            self.output_proxies.insert(0, code_output_proxy)
        else:
            result = '>>> '
            for i, line in enumerate(input_file_contents):
                result += line
                self.current_lines.append(result)
                with systemtools.RedirectedStreams(self, self):
                    is_incomplete_statement = console.push(line)
                if console.errored:
                    if self.allow_exceptions:
                        console.unregister_error()
                    else:
                        message = 'Abjad-book error on '
                        if self.document_source:
                            message += str(self.document_source)
                            message += ':{}'
                        else:
                            message += 'line number {}'
                        message = message.format(self.starting_line_number + i)
                        message = bold(red(message))
                        message += '\n    '
                        message = message + '\n    '.join(self.current_lines)
                        raise abjadbooktools.AbjadBookError(message)
                if not is_incomplete_statement:
                    result = '>>> '
                    self.setup_capture_hooks(console)
                else:
                    result = '... '
        if is_incomplete_statement:
            with systemtools.RedirectedStreams(self, self):
                is_incomplete_statement = console.push('\n')
        self.push_code_output_proxy()
        if self.hide:
            self.output_proxies[:] = [
                _ for _ in self.output_proxies
                if not isinstance(_, abjadbooktools.CodeOutputProxy)
                ]

    def push_asset_output_proxy(self, asset_output_proxy):
        self.push_code_output_proxy()
        self.output_proxies.append(asset_output_proxy)

    def push_code_output_proxy(self):
        from abjad.tools import abjadbooktools
        if not self.current_lines:
            return
        if self.strip_prompt:
            self.current_lines[:] = [
                _[4:].rstrip() for _ in self.current_lines
                if _.startswith(('>>> ', '... '))
                ]
            while not self.current_lines[-1]:
                self.current_lines.pop()
        code_output_proxy = abjadbooktools.CodeOutputProxy(self.current_lines)
        self.output_proxies.append(code_output_proxy)
        self.current_lines[:] = []

    def setup_capture_hooks(self, console):
        prototype = (types.MethodType, types.FunctionType)
        if isinstance(console.locals['graph'], prototype):
            console.locals['graph'] = self.graph
        console.locals['show'] = self.show
        console.locals['quit'] = self.quit
        topleveltools = console.locals['topleveltools']
        topleveltools.__dict__['graph'] = self.graph
        topleveltools.__dict__['show'] = self.show

    def write(self, string):
        if string:
            if string.endswith('\n'):
                string = string[:-1]
            lines = string.splitlines()
            if self.text_width is None:
                self.current_lines.extend(lines)
            else:
                for line in lines:
                    wrapped_lines = textwrap.wrap(line, self.text_width)
                    self.current_lines.extend(wrapped_lines)

    ### PROXIES ###

    def graph(
        self,
        expr,
        layout='dot',
        graph_attributes=None,
        node_attributes=None,
        edge_attributes=None,
        **kwargs
        ):
        r'''Proxies Abjad's toplevel `graph()` function.

        ::

            >>> from abjad.tools import abjadbooktools
            >>> console = abjadbooktools.AbjadBookConsole()
            >>> input_file_contents = [
            ...     'meter = metertools.Meter((4, 4))',
            ...     'graph(meter)',
            ...     'print(format(meter))',
            ...     ]
            >>> code_block = abjadbooktools.CodeBlock(input_file_contents)
            >>> code_block.interpret(console)
            >>> for output_proxy in code_block.output_proxies:
            ...     print(format(output_proxy))
            ...
            abjadbooktools.CodeOutputProxy(
                (
                    '>>> meter = metertools.Meter((4, 4))',
                    '>>> graph(meter)',
                    )
                )
            abjadbooktools.GraphvizOutputProxy(
                documentationtools.GraphvizGraph(
                    attributes={
                        'bgcolor': 'transparent',
                        'fontname': 'Arial',
                        'penwidth': 2,
                        'truecolor': True,
                        },
                    children=(
                        documentationtools.GraphvizNode(
                            attributes={
                                'label': '4/4',
                                'shape': 'triangle',
                                },
                            ),
                        documentationtools.GraphvizNode(
                            attributes={
                                'label': '1/4',
                                'shape': 'box',
                                },
                            ),
                        documentationtools.GraphvizNode(
                            attributes={
                                'label': '1/4',
                                'shape': 'box',
                                },
                            ),
                        documentationtools.GraphvizNode(
                            attributes={
                                'label': '1/4',
                                'shape': 'box',
                                },
                            ),
                        documentationtools.GraphvizNode(
                            attributes={
                                'label': '1/4',
                                'shape': 'box',
                                },
                            ),
                        documentationtools.GraphvizSubgraph(
                            attributes={
                                'style': 'rounded',
                                },
                            children=(
                                documentationtools.GraphvizNode(
                                    attributes={
                                        'color': 'white',
                                        'fillcolor': 'black',
                                        'fontcolor': 'white',
                                        'fontname': 'Arial bold',
                                        'shape': 'Mrecord',
                                        'style': 'filled',
                                        },
                                    children=(
                                        documentationtools.GraphvizGroup(
                                            children=(
                                                documentationtools.GraphvizField(
                                                    label='0',
                                                    ),
                                                documentationtools.GraphvizField(
                                                    label='++',
                                                    ),
                                                ),
                                            ),
                                        ),
                                    ),
                                documentationtools.GraphvizNode(
                                    attributes={
                                        'color': 'white',
                                        'fillcolor': 'black',
                                        'fontcolor': 'white',
                                        'fontname': 'Arial bold',
                                        'shape': 'Mrecord',
                                        'style': 'filled',
                                        },
                                    children=(
                                        documentationtools.GraphvizGroup(
                                            children=(
                                                documentationtools.GraphvizField(
                                                    label='1/4',
                                                    ),
                                                documentationtools.GraphvizField(
                                                    label='+',
                                                    ),
                                                ),
                                            ),
                                        ),
                                    ),
                                documentationtools.GraphvizNode(
                                    attributes={
                                        'color': 'white',
                                        'fillcolor': 'black',
                                        'fontcolor': 'white',
                                        'fontname': 'Arial bold',
                                        'shape': 'Mrecord',
                                        'style': 'filled',
                                        },
                                    children=(
                                        documentationtools.GraphvizGroup(
                                            children=(
                                                documentationtools.GraphvizField(
                                                    label='1/2',
                                                    ),
                                                documentationtools.GraphvizField(
                                                    label='+',
                                                    ),
                                                ),
                                            ),
                                        ),
                                    ),
                                documentationtools.GraphvizNode(
                                    attributes={
                                        'color': 'white',
                                        'fillcolor': 'black',
                                        'fontcolor': 'white',
                                        'fontname': 'Arial bold',
                                        'shape': 'Mrecord',
                                        'style': 'filled',
                                        },
                                    children=(
                                        documentationtools.GraphvizGroup(
                                            children=(
                                                documentationtools.GraphvizField(
                                                    label='3/4',
                                                    ),
                                                documentationtools.GraphvizField(
                                                    label='+',
                                                    ),
                                                ),
                                            ),
                                        ),
                                    ),
                                documentationtools.GraphvizNode(
                                    attributes={
                                        'shape': 'Mrecord',
                                        },
                                    children=(
                                        documentationtools.GraphvizGroup(
                                            children=(
                                                documentationtools.GraphvizField(
                                                    label='1',
                                                    ),
                                                documentationtools.GraphvizField(
                                                    label='++',
                                                    ),
                                                ),
                                            ),
                                        ),
                                    ),
                                ),
                            edge_attributes={
                                },
                            is_cluster=True,
                            name='cluster_offsets',
                            node_attributes={
                                },
                            ),
                        ),
                    edge_attributes={
                        'penwidth': 2,
                        },
                    is_digraph=True,
                    name='G',
                    node_attributes={
                        'fontname': 'Arial',
                        'fontsize': 12,
                        'penwidth': 2,
                        },
                    ),
                layout='dot',
                )
            abjadbooktools.CodeOutputProxy(
                (
                    '>>> print(format(meter))',
                    'metertools.Meter(',
                    "    '(4/4 (1/4 1/4 1/4 1/4))'",
                    '    )',
                    )
                )

        '''
        from abjad.tools import abjadbooktools
        graph = expr.__graph__(**kwargs)
        if graph_attributes:
            graph.attributes.update(graph_attributes)
        if node_attributes:
            graph.node_attributes.update(node_attributes)
        if edge_attributes:
            graph.edge_attributes.update(edge_attributes)
        output_proxy = abjadbooktools.GraphvizOutputProxy(
            graph,
            layout=layout,
            )
        self.push_asset_output_proxy(output_proxy)

    def play(self, expr):
        r'''Proxies Abjad's toplevel `play()` function.
        '''
        pass

    def quit(self):
        r'''Proxies Python's builtin `quit()` function.
        '''
        pass

    def show(self, expr, return_timing=False, **kwargs):
        r'''Proxies Abjad's toplevel `show()` function.

        ::

            >>> from abjad.tools import abjadbooktools
            >>> console = abjadbooktools.AbjadBookConsole()
            >>> input_file_contents = [
            ...     'staff = Staff(r"\clef bass c4 d4 e4 f4")',
            ...     'show(staff)',
            ...     'print(len(staff))'
            ...     ]
            >>> code_block = abjadbooktools.CodeBlock(input_file_contents)
            >>> code_block.interpret(console)
            >>> for output_proxy in code_block.output_proxies:
            ...     print(format(output_proxy))
            ...
            abjadbooktools.CodeOutputProxy(
                (
                    '>>> staff = Staff(r"\\clef bass c4 d4 e4 f4")',
                    '>>> show(staff)',
                    )
                )
            abjadbooktools.LilyPondOutputProxy(
                lilypondfiletools.LilyPondFile()
                )
            abjadbooktools.CodeOutputProxy(
                ('>>> print(len(staff))', '4')
                )

        '''
        from abjad.tools import abjadbooktools
        illustration = expr.__illustrate__(**kwargs)
        output_proxy = abjadbooktools.LilyPondOutputProxy(
            illustration,
            stylesheet=self.stylesheet,
            )
        self.push_asset_output_proxy(output_proxy)

    ### PUBLIC PROPERTIES ###

    @property
    def allow_exceptions(self):
        return self._allow_exceptions

    @property
    def current_lines(self):
        return self._current_lines

    @property
    def document_source(self):
        return self._document_source

    @property
    def executed_lines(self):
        return self._executed_lines

    @property
    def hide(self):
        return self._hide

    @property
    def output_proxies(self):
        return self._output_proxies

    @property
    def input_file_contents(self):
        return self._source_lines

    @property
    def starting_line_number(self):
        return self._starting_line_number

    @property
    def strip_prompt(self):
        return self._strip_prompt

    @property
    def stylesheet(self):
        return self._stylesheet

    @property
    def text_width(self):
        return self._text_width