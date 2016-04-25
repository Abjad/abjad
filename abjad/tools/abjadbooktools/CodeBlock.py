# -*- coding: utf-8 -*-
from __future__ import print_function
import importlib
import inspect
import sys
import textwrap
import types
from abjad.tools import abctools
from abjad.tools import systemtools
from abjad.tools.topleveltools import new
from sphinx.util.console import bold, red


class CodeBlock(abctools.AbjadValueObject):
    r'''A code block.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Internals'

    ### CLASS VARIABLES ###

    __slots__ = (
        '_code_block_specifier',
        '_console',
        '_current_lines',
        '_document_source',
        '_executed_lines',
        '_image_layout_specifier',
        '_image_render_specifier',
        '_options',
        '_output_proxies',
        '_source_lines',
        '_starting_line_number',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        input_file_contents,
        code_block_specifier=None,
        document_source=None,
        executed_lines=None,
        image_layout_specifier=None,
        image_render_specifier=None,
        starting_line_number=None,
        ):
        self._code_block_specifier = code_block_specifier
        self._current_lines = []
        self._document_source = document_source
        if executed_lines is not None:
            executed_lines = tuple(executed_lines)
        self._executed_lines = executed_lines
        self._image_layout_specifier = image_layout_specifier
        self._image_render_specifier = image_render_specifier
        self._output_proxies = []
        self._source_lines = tuple(input_file_contents)
        self._starting_line_number = starting_line_number

    ### PUBLIC METHODS ###

    def as_docutils(
        self,
        configuration=None,
        output_directory=None,
        ):
        output_proxies = self.filter_output_proxies()
        result = []
        if output_proxies:
            for output_proxy in output_proxies:
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
        output_proxies = self.filter_output_proxies()
        if output_proxies:
            result.extend(output_start_delimiter)
            before = latex_configuration.get('before-code-block', ())
            result.extend(before)
            for i, output_proxy in enumerate(output_proxies):
                lines = output_proxy.as_latex(
                    configuration=configuration,
                    output_directory=output_directory,
                    relative_output_directory=relative_output_directory,
                    )
                string = '\n'.join(lines)
                if isinstance(output_proxy, abjadbooktools.ImageOutputProxy):
                    if i < len(output_proxies) - 1:
                        next_proxy = output_proxies[i + 1]
                        if isinstance(next_proxy, abjadbooktools.ImageOutputProxy):
                            string += r'\\'
                result.append(string)
            after = latex_configuration.get('after-code-block', ())
            result.extend(after)
            result.extend(output_stop_delimiter)
            result = '\n'.join(result)
            result = [result]
        return result

    def filter_output_proxies(self):
        from abjad.tools import abjadbooktools
        code_block_specifier = self.code_block_specifier
        if code_block_specifier is None:
            code_block_specifier = abjadbooktools.CodeBlockSpecifier()
        output_proxies = list(self.output_proxies)
        if code_block_specifier.hide:
            output_proxies = [
                _ for _ in output_proxies
                if not isinstance(_, abjadbooktools.CodeOutputProxy)
                ]
        return output_proxies

    def flush(self):
        pass

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
        cleaned_options = {}
        for key, value in block.attlist():
            key = key.replace('-', '_')
            cleaned_options[key] = value
        code_block_specifier = abjadbooktools.CodeBlockSpecifier.from_options(
            **cleaned_options)
        image_layout_specifier = abjadbooktools.ImageLayoutSpecifier.from_options(
            **cleaned_options)
        image_render_specifier = abjadbooktools.ImageRenderSpecifier.from_options(
            **cleaned_options)
        code_block = abjadbooktools.CodeBlock(
            code_block_specifier=code_block_specifier,
            executed_lines=executed_lines,
            image_layout_specifier=image_layout_specifier,
            image_render_specifier=image_render_specifier,
            input_file_contents=input_file_contents,
            starting_line_number=block.line,
            )
        return code_block

    @staticmethod
    def from_docutils_abjad_input_block(block):
        from abjad.tools import abjadbooktools
        literal_block = block[0]
        text_node = literal_block[0]
        input_file_contents = tuple(text_node.splitlines())
        cleaned_options = {}
        for key, value in block.attlist():
            key = key.replace('-', '_')
            cleaned_options[key] = value
        code_block_specifier = abjadbooktools.CodeBlockSpecifier.from_options(
            **cleaned_options)
        image_layout_specifier = abjadbooktools.ImageLayoutSpecifier.from_options(
            **cleaned_options)
        image_render_specifier = abjadbooktools.ImageRenderSpecifier.from_options(
            **cleaned_options)
        code_block = abjadbooktools.CodeBlock(
            code_block_specifier=code_block_specifier,
            image_layout_specifier=image_layout_specifier,
            image_render_specifier=image_render_specifier,
            input_file_contents=input_file_contents,
            starting_line_number=literal_block.line,
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
        code_block_specifier = abjadbooktools.CodeBlockSpecifier(
            allow_exceptions=True,
            )
        code_block = abjadbooktools.CodeBlock(
            code_block_specifier=code_block_specifier,
            document_source=document_source,
            input_file_contents=input_file_contents,
            starting_line_number=block.line,
            )
        return code_block

    @staticmethod
    def from_latex_abjad_block(
        input_file_contents,
        starting_line_number=None,
        **options
        ):
        from abjad.tools import abjadbooktools
        cleaned_options = {}
        for key, value in options.items():
            key = key.replace('-', '_')
            cleaned_options[key] = value
        code_block_specifier = abjadbooktools.CodeBlockSpecifier.from_options(
            **cleaned_options)
        image_layout_specifier = abjadbooktools.ImageLayoutSpecifier.from_options(
            **cleaned_options)
        image_render_specifier = abjadbooktools.ImageRenderSpecifier.from_options(
            **cleaned_options)
        code_block = abjadbooktools.CodeBlock(
            code_block_specifier=code_block_specifier,
            image_layout_specifier=image_layout_specifier,
            image_render_specifier=image_render_specifier,
            input_file_contents=input_file_contents,
            starting_line_number=starting_line_number,
            )
        return code_block

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
        cleaned_options = {}
        for key, value in options.items():
            key = key.replace('-', '_')
            cleaned_options[key] = value
        code_block_specifier = abjadbooktools.CodeBlockSpecifier.from_options(
            **cleaned_options)
        image_layout_specifier = abjadbooktools.ImageLayoutSpecifier.from_options(
            **cleaned_options)
        image_render_specifier = abjadbooktools.ImageRenderSpecifier.from_options(
            **cleaned_options)
        code_block = abjadbooktools.CodeBlock(
            code_block_specifier=code_block_specifier,
            executed_lines=executed_lines,
            image_layout_specifier=image_layout_specifier,
            image_render_specifier=image_render_specifier,
            input_file_contents=input_file_contents,
            starting_line_number=starting_line_number,
            )
        return code_block

    def interpret(self, console):
        from abjad.tools import abjadbooktools
        code_block_specifier = self.code_block_specifier
        if code_block_specifier is None:
            code_block_specifier = abjadbooktools.CodeBlockSpecifier()
        self._console = console
        is_incomplete_statement = False
        input_file_contents = self.input_file_contents
        self.output_proxies[:] = []
        self.current_lines[:] = []
        self.setup_capture_hooks(console)
        if self.executed_lines:
            for executed_line in self.executed_lines:
                is_incomplete_statement = console.push(executed_line)
            code_output_proxy = abjadbooktools.CodeOutputProxy(
                input_file_contents,
                code_block_specifier=self.code_block_specifier,
                )
            self.output_proxies.insert(0, code_output_proxy)
        else:
            result = '>>> '
            for line_number, line in enumerate(input_file_contents, 1):
                result += line
                self.current_lines.append(result)
                if code_block_specifier.strip_prompt and line.strip() == '':
                    continue
                else:
                    is_incomplete_statement = self.push_line_to_console(
                        line, console, line_number)
                if not is_incomplete_statement:
                    result = '>>> '
                    self.setup_capture_hooks(console)
                else:
                    result = '... '
        if is_incomplete_statement:
            self.current_lines.append(result)
            is_incomplete_statement = self.push_line_to_console(
                '\n', console, line_number)
        self.push_code_output_proxy()
        if code_block_specifier.hide:
            self.output_proxies[:] = [
                _ for _ in self.output_proxies
                if not isinstance(_, abjadbooktools.CodeOutputProxy)
                ]
        self._console = None

    def push_asset_output_proxy(self, asset_output_proxy):
        self.push_code_output_proxy()
        self.output_proxies.append(asset_output_proxy)

    def push_code_output_proxy(self):
        from abjad.tools import abjadbooktools
        strip_prompt = None
        if self.code_block_specifier is not None:
            strip_prompt = self.code_block_specifier.strip_prompt
        if not self.current_lines:
            return
        if strip_prompt:
            self.current_lines[:] = [
                _[4:].rstrip() for _ in self.current_lines
                if _.startswith(('>>> ', '... '))
                ]
            while not self.current_lines[-1]:
                self.current_lines.pop()
        code_output_proxy = abjadbooktools.CodeOutputProxy(
            self.current_lines,
            code_block_specifier=self.code_block_specifier,
            )
        self.output_proxies.append(code_output_proxy)
        self.current_lines[:] = []

    def push_line_to_console(self, line, console, line_number):
        from abjad.tools import abjadbooktools
        allow_exceptions = None
        if self.code_block_specifier is not None:
            allow_exceptions = self.code_block_specifier.allow_exceptions
        with systemtools.RedirectedStreams(self, self):
            is_incomplete_statement = console.push(line)
        if console.errored:
            if allow_exceptions:
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

    def setup_capture_hooks(self, console):
        prototype = (types.MethodType, types.FunctionType)
        if isinstance(console.locals['graph'], prototype):
            console.locals['graph'] = self.graph
        console.locals['play'] = self.play
        console.locals['__builtins__']['print'] = self.print
        console.locals['__builtins__']['quit'] = self.quit
        console.locals['show'] = self.show
        topleveltools = console.locals['topleveltools']
        topleveltools.__dict__['graph'] = self.graph
        topleveltools.__dict__['play'] = self.play
        topleveltools.__dict__['show'] = self.show

    def write(self, string):
        text_width = None
        if self.code_block_specifier is not None:
            text_width = self.code_block_specifier.text_width
        if not string:
            return
        if sys.version_info[0] == 2:
            string = string.decode('utf-8')
        if string.endswith('\n'):
            string = string[:-1]
        lines = string.splitlines()
        if text_width is None:
            self.current_lines.extend(lines)
        else:
            for line in lines:
                wrapped_lines = textwrap.wrap(line, text_width)
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
            image_layout_specifier=self.image_layout_specifier,
            image_render_specifier=self.image_render_specifier,
            )
        self.push_asset_output_proxy(output_proxy)

    def play(self, expr):
        r'''Proxies Abjad's toplevel `play()` function.
        '''
        pass

    def print(self, *args, **kwargs):
        r'''Proxies Python's builtin `print()` function.

        Proxying `print()` is necessary because the original print function
        makes multiple calls to `sys.stdout.write()` rather than one. In the
        context of abjad-book code block interpretation, each write operation
        adds a new line, hence the necessity of joining the `print()` arguments
        into a single string and then writing that.

        Note that this will produce unexpected results if attempting to do
        fancy operations like overwriting the current line.
        '''
        self.write(' '.join(str(_) for _ in args))

    def quit(self):
        r'''Proxies Python's builtin `quit()` function.
        '''
        pass

    def show(self, expr, return_timing=False, **kwargs):
        r'''Proxies Abjad's toplevel `show()` function.
        '''
        from abjad.tools import abjadbooktools
        illustration = expr.__illustrate__(**kwargs)
        default_stylesheet = None
        if (
            self._console is not None and
            self._console.document_handler is not None
            ):
            handler = self._console.document_handler
            default_stylesheet = handler.get_default_stylesheet()
        image_render_specifier = self.image_render_specifier
        if image_render_specifier is None:
            image_render_specifier = abjadbooktools.ImageRenderSpecifier()
        if image_render_specifier.stylesheet is None:
            image_render_specifier = new(
                image_render_specifier,
                stylesheet=default_stylesheet,
                )
        output_proxy = abjadbooktools.LilyPondOutputProxy(
            illustration,
            image_layout_specifier=self.image_layout_specifier,
            image_render_specifier=image_render_specifier,
            )
        self.push_asset_output_proxy(output_proxy)

    ### PUBLIC PROPERTIES ###

    @property
    def code_block_specifier(self):
        return self._code_block_specifier

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
    def image_layout_specifier(self):
        return self._image_layout_specifier

    @property
    def image_render_specifier(self):
        return self._image_render_specifier

    @property
    def input_file_contents(self):
        return self._source_lines

    @property
    def output_proxies(self):
        return self._output_proxies

    @property
    def starting_line_number(self):
        return self._starting_line_number
