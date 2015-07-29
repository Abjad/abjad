# -*- encoding: utf-8 -*-
from __future__ import print_function
import importlib
import inspect
import sys
import textwrap
import types
from abjad.tools import abctools
from abjad.tools import systemtools
from sphinx.util.console import bold, red


class CodeBlock(abctools.AbjadValueObject):
    r'''A code block.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_console',
        '_current_lines',
        '_document_source',
        '_executed_lines',
        '_options',
        '_output_proxies',
        '_source_lines',
        '_starting_line_number',
        )
    __slots__ += (
        '_allow_exceptions',
        '_hide',
        '_strip_prompt',
        '_no_stylesheet',
        '_stylesheet',
        '_text_width',
        )
    __slots__ += (
        '_no_strip',
        '_pages',
        '_with_columns',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        input_file_contents,
        allow_exceptions=None,
        document_source=None,
        executed_lines=None,
        hide=None,
        no_stylesheet=None,
        pages=None,
        starting_line_number=None,
        strip_prompt=None,
        stylesheet=None,
        text_width=None,
        **options
        ):
        self._allow_exceptions = bool(allow_exceptions) or None
        self._document_source = document_source
        if executed_lines is not None:
            executed_lines = tuple(executed_lines)
        self._executed_lines = executed_lines
        self._hide = bool(hide) or None
        self._no_stylesheet = bool(no_stylesheet) or None
        self._output_proxies = []
        self._pages = pages or None
        self._source_lines = tuple(input_file_contents)
        self._starting_line_number = starting_line_number
        self._strip_prompt = bool(strip_prompt) or None
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
        input_file_contents = inspect.getsource(attr)
        if sys.version_info[0] == 2:
            input_file_contents = input_file_contents.decode('utf-8')
        input_file_contents = input_file_contents.splitlines()
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
        input_file_contents = tuple(block[0][0].splitlines())
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
        self._console = console
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
            for line_number, line in enumerate(input_file_contents):
                result += line
                self.current_lines.append(result)

                is_incomplete_statement = self.push_line_to_console(
                    line, console, line_number)

                if not is_incomplete_statement:
                    result = '>>> '
                    self.setup_capture_hooks(console)
                else:
                    result = '... '
        if is_incomplete_statement:
            is_incomplete_statement = self.push_line_to_console(
                '\n', console, line_number)
        self.push_code_output_proxy()
        if self.hide:
            self.output_proxies[:] = [
                _ for _ in self.output_proxies
                if not isinstance(_, abjadbooktools.CodeOutputProxy)
                ]
        self._console = None

    def push_line_to_console(self, line, console, line_number):
        from abjad.tools import abjadbooktools
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
                line_number += self.starting_line_number
                message = message.format(line_number)
                message = bold(red(message))
                message += '\n    '
                message = message + '\n    '.join(self.current_lines)
                raise abjadbooktools.AbjadBookError(message)
        return is_incomplete_statement

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
        console.locals['play'] = self.play
        console.locals['quit'] = self.quit
        console.locals['show'] = self.show
        topleveltools = console.locals['topleveltools']
        topleveltools.__dict__['graph'] = self.graph
        topleveltools.__dict__['play'] = self.play
        topleveltools.__dict__['show'] = self.show

    def write(self, string):
        if not string:
            return
        if sys.version_info[0] == 2:
            string = string.decode('utf-8')
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
        '''
        from abjad.tools import abjadbooktools
        illustration = expr.__illustrate__(**kwargs)
        if (
            self._console is not None and
            self._console.document_handler is not None
            ):
            handler = self._console.document_handler
            default_stylesheet = handler.get_default_stylesheet()
        stylesheet = self.stylesheet or default_stylesheet
        if self.no_stylesheet:
            stylesheet = None
        output_proxy = abjadbooktools.LilyPondOutputProxy(
            illustration,
            pages=self.pages,
            stylesheet=stylesheet,
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
    def no_stylesheet(self):
        return self._no_stylesheet

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

    @property
    def pages(self):
        return self._pages