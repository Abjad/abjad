# -*- coding: utf-8 -*-
from __future__ import print_function
import collections
import os
from abjad.tools import abctools
from abjad.tools import systemtools


class LaTeXDocumentHandler(abctools.AbjadObject):
    r"""A LaTeX document handler.

    ::

        >>> input_file_contents = '''Let's print something:
        ...
        ... \\begin{comment}
        ... <abjad>
        ... print("hello, world!")
        ... </abjad>
        ... \\end{comment}
        ...
        ... This is just a simple Python string:
        ...
        ... \\begin{comment}
        ... <abjad>
        ... just_a_string = \'\'\'
        ... show(Nothing!)
        ... \'\'\'
        ... </abjad>
        ... \\end{comment}
        ...
        ... And let's show some music too:
        ...
        ... \\begin{comment}
        ... <abjad>
        ... show(Note("c'4"))
        ... </abjad>
        ... \\end{comment}
        ...
        ... That's it!
        ... '''

    ::

        >>> from abjad.tools import abjadbooktools
        >>> document_handler = abjadbooktools.LaTeXDocumentHandler(
        ...     input_file_contents=input_file_contents,
        ...     input_file_path='test.tex.raw',
        ...     assets_directory='images',
        ...     )

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Document Handlers'

    __slots__ = (
        '_assets_directory',
        '_errored',
        '_input_file_contents',
        '_input_file_path',
        '_latex_root_directory',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        assets_directory=None,
        input_file_contents=None,
        input_file_path=None,
        latex_root_directory=None,
        ):
        self._assets_directory = assets_directory
        self._errored = False
        input_file_contents = input_file_contents or ()
        if isinstance(input_file_contents, str):
            input_file_contents = input_file_contents.rstrip().splitlines()
        self._input_file_contents = tuple(input_file_contents)
        self._input_file_path = input_file_path
        self._latex_root_directory = latex_root_directory

    ### SPECIAL METHODS ###

    def __call__(
        self,
        clean=None,
        configuration=None,
        output_file_path=None,
        return_source=None,
        skip_rendering=None,
        stylesheet=None,
        verbose=None,
        ):
        import abjad
        from abjad.tools import abjadbooktools
        configuration = configuration or {}
        if output_file_path:
            output_file_path = os.path.abspath(output_file_path)
            _, output_file_path = os.path.split(output_file_path)
            output_directory, _ = os.path.split(self.input_file_path)
            output_file_path = os.path.join(output_directory, output_file_path)
        else:
            output_file_path = self.input_file_path
        if stylesheet is not None:
            stylesheet = os.path.abspath(stylesheet)
            stylesheet = os.path.relpath(
                stylesheet,
                self.assets_directory,
                )
        self.report(
            output_file_path=output_file_path,
            stylesheet=stylesheet,
            verbose=verbose,
            )
        self._errored = False
        console = abjadbooktools.AbjadBookConsole(
            document_handler=self,
            locals=abjad.__dict__.copy(),
            )
        output_blocks = self.collect_output_blocks(
            self.input_file_contents,
            configuration=configuration,
            )
        if clean:
            input_blocks = {}
        else:
            input_blocks = self.collect_input_blocks(
                self.input_file_contents,
                stylesheet=stylesheet,
                )
            self.interpret_input_blocks(input_blocks, console)
        if not skip_rendering and not clean and not return_source:
            self.render_asset_output_proxies(
                input_blocks=input_blocks,
                )
        rebuilt_source = self.rebuild_source(
            configuration=configuration,
            input_blocks=input_blocks,
            output_blocks=output_blocks,
            input_file_contents=self.input_file_contents,
            )
        if return_source:
            return rebuilt_source
        self.write_rebuilt_source(
            rebuilt_source,
            output_file_path=output_file_path,
            )

    ### PUBLIC METHODS ###

    def collect_asset_output_proxies(self, input_blocks):
        from abjad.tools import abjadbooktools
        asset_output_proxies = []
        for code_block in input_blocks.values():
            for output_proxy in code_block.output_proxies:
                if isinstance(output_proxy, abjadbooktools.CodeOutputProxy):
                    continue
                asset_output_proxies.append(output_proxy)
        return asset_output_proxies

    def collect_input_blocks(self, input_file_contents, stylesheet=None):
        r"""Collects input blocks.

        ::

            >>> input_blocks = document_handler.collect_input_blocks(
            ...     input_file_contents.splitlines())

        ::

            >>> for source_line_range in input_blocks.keys():
            ...     print(source_line_range)
            ...
            (3, 5)
            (11, 15)
            (21, 23)

        ::

            >>> for input_block in input_blocks.values():
            ...     print(format(input_block))
            ...
            abjadbooktools.CodeBlock(
                ('print("hello, world!")',),
                starting_line_number=5,
                )
            abjadbooktools.CodeBlock(
                ("just_a_string = '''", 'show(Nothing!)', "'''"),
                starting_line_number=15,
                )
            abjadbooktools.CodeBlock(
                ('show(Note("c\'4"))',),
                starting_line_number=23,
                )

        """
        from abjad.tools import abjadbooktools
        input_blocks = collections.OrderedDict()
        in_input_block = False
        starting_line_number = None
        current_block_lines = None
        current_block_options = None
        for i, line in enumerate(input_file_contents):
            if line.startswith('<abjad'):
                if in_input_block:
                    message = 'Extra opening tag at line {}.'.format(i + 1)
                    raise ValueError(message)
                current_block_options = {'stylesheet': stylesheet}
                current_block_options.update(
                    self.extract_code_block_options(line),
                    )
                if line.startswith('<abjad>'):
                    in_input_block = True
                    current_block_lines = []
                    starting_line_number = i
                elif line.startswith('<abjadextract '):
                    starting_line_number = stopping_line_number = i
                    code_block = abjadbooktools.CodeBlock.from_latex_abjadextract_block(
                        line,
                        starting_line_number=i,
                        **current_block_options
                        )
                    source_line_range = (
                        starting_line_number,
                        stopping_line_number,
                        )
                    input_blocks[source_line_range] = code_block
            elif line.startswith('</abjad>'):
                if not in_input_block:
                    message = 'Extra closing tag at line {}'.format(i + 1)
                    raise ValueError(message)
                in_input_block = False
                stopping_line_number = i
                source_line_range = (
                    starting_line_number,
                    stopping_line_number,
                    )
                code_block = abjadbooktools.CodeBlock.from_latex_abjad_block(
                    current_block_lines,
                    starting_line_number=i,
                    **current_block_options
                    )
                input_blocks[source_line_range] = code_block
            elif in_input_block:
                current_block_lines.append(line)
        if in_input_block:
            raise ValueError('Unterminated tag at EOF.')
        return input_blocks

    def collect_output_blocks(self, input_file_contents, configuration=None):
        configuration = configuration or {}
        latex_configuration = configuration.get('latex', {})
        output_start_delimiter = latex_configuration.get(
            'output-start-delimiter',
            ('%%% ABJADBOOK START %%%',),
            )
        output_start_delimiter = output_start_delimiter[0]
        output_stop_delimiter = latex_configuration.get(
            'output-stop-delimiter',
            ('%%% ABJADBOOK END %%%',),
            )
        output_stop_delimiter = output_stop_delimiter[0]
        output_blocks = []
        in_output_block = False
        starting_line_number = None
        for i, line in enumerate(input_file_contents):
            if line.startswith(output_start_delimiter):
                if in_output_block:
                    message = 'Extra opening tag at line {}'.format(i + 1)
                    raise ValueError(message)
                in_output_block = True
                starting_line_number = i
            elif line.startswith(output_stop_delimiter):
                if not in_output_block:
                    message = 'Extra closing tag at line {}'.format(i + 1)
                    raise ValueError(message)
                in_output_block = False
                stopping_line_number = i
                source_line_range = (
                    starting_line_number,
                    stopping_line_number,
                    )
                output_blocks.append(source_line_range)
        return output_blocks

    @staticmethod
    def extract_code_block_options(source_line):
        r'''Extracts code block options.

        ::

            >>> source_line = '<abjad>'
            >>> document_handler.extract_code_block_options(source_line)
            {}

        ::

            >>> source_line = '<abjad>[hide=True]'
            >>> document_handler.extract_code_block_options(source_line)
            {'hide': True}

        ::

            >>> source_line = '<abjad>[strip_prompt=true, hide=false]'
            >>> options = document_handler.extract_code_block_options(
            ...     source_line)
            >>> for key, value in sorted(options.items()):
            ...     key, value
            ...
            ('hide', False)
            ('strip_prompt', True)

        ::

            >>> source_line = '<abjad>[allow_exceptions]'
            >>> options = document_handler.extract_code_block_options(
            ...     source_line)
            >>> for key, value in sorted(options.items()):
            ...     key, value
            ...
            ('allow_exceptions', True)

        '''
        options = {}
        line = source_line.strip()
        if '[' in line and line.endswith(']'):
            option_string = line.partition('[')[2][:-1]
            for part in option_string.split(','):
                part = part.strip()
                if '=' in part:
                    key, sep, value = part.partition('=')
                    key = key.lower().strip()
                    value = value.lower().strip()
                    if value == 'true':
                        options[key] = True
                    elif value == 'false':
                        options[key] = False
                    else:
                        options[key] = value
                else:
                    options[part] = True
        return options

    @classmethod
    def from_path(
        cls,
        input_file_path=None,
        assets_directory=None,
        latex_root_directory=None,
        ):
        assert os.path.exists(input_file_path)
        input_file_path = os.path.abspath(input_file_path)
        input_directory, _ = os.path.split(input_file_path)
        if not assets_directory:
            assets_directory = os.path.join(input_directory, 'assets')
        if not latex_root_directory:
            latex_root_directory = input_directory
        with open(input_file_path, 'r') as file_pointer:
            input_file_contents = file_pointer.read()
        document_handler = cls(
            input_file_contents=input_file_contents,
            input_file_path=input_file_path,
            assets_directory=assets_directory,
            latex_root_directory=latex_root_directory,
            )
        return document_handler

    def get_default_stylesheet(self):
        return None

    def interpret_input_blocks(self, input_blocks, console, verbose=True):
        code_blocks = tuple(input_blocks.values())
        if not code_blocks:
            return
        progress_indicator = systemtools.ProgressIndicator(
            message='    Interpreting code blocks',
            total=len(code_blocks),
            verbose=verbose,
            )
        with progress_indicator:
            for code_block in code_blocks:
                code_block.interpret(console)
                progress_indicator.advance()

    def rebuild_source(
        self,
        input_blocks,
        output_blocks,
        input_file_contents,
        configuration=None,
        ):
        input_file_contents = list(input_file_contents)
        blocks = list(input_blocks.items())
        output_blocks = ((_, None) for _ in output_blocks)
        blocks.extend(output_blocks)
        blocks.sort()
        for source_line_range, block in reversed(blocks):
            start, stop = source_line_range
            if block is None:
                input_file_contents[start:stop + 1] = []
                if start < len(input_file_contents) and \
                    not input_file_contents[start].strip():
                    input_file_contents[start:start + 1] = []
                continue
            output_lines = block.as_latex(
                configuration=configuration,
                output_directory=self.assets_directory,
                relative_output_directory=self.latex_assets_prefix,
                )
            if output_lines:
                output_lines.insert(0, '')
                stop += 1
                if stop < len(input_file_contents):
                    if '\\end{comment}' in input_file_contents[stop]:
                        stop += 1
                input_file_contents[stop:stop] = output_lines
        input_file_contents = '\n'.join(input_file_contents)
        input_file_contents = input_file_contents.splitlines()
        input_file_contents = (_.rstrip() for _ in input_file_contents)
        input_file_contents = '\n'.join(input_file_contents)
        return input_file_contents

    def register_error(self):
        self._errored = True

    def render_asset_output_proxies(
        self,
        input_blocks,
        ):
        asset_output_proxies = self.collect_asset_output_proxies(input_blocks)
        if not asset_output_proxies:
            return
        if not os.path.exists(self.assets_directory):
            os.makedirs(self.assets_directory)

        progress_indicator = systemtools.ProgressIndicator(
            message='    Writing assets',
            total=len(asset_output_proxies),
            )
        with progress_indicator:
            for asset_output_proxy in asset_output_proxies:
                asset_output_proxy.render_for_latex(
                    self.assets_directory,
                    )
                progress_indicator.advance()

    def report(
        self,
        output_file_path=None,
        stylesheet=None,
        verbose=None,
        ):
        if verbose:
            print('Processing {}:'.format(self.input_file_path))
            print('    output file:     {}'.format(output_file_path))
            print('    asset directory: {}'.format(self.assets_directory))
            print('    asset prefix:    {}'.format(self.latex_assets_prefix))
            print('    latex root:      {}'.format(self.latex_root_directory))
            if stylesheet is not None:
                print('    stylesheet:      {} ({})'.format(
                    stylesheet,
                    os.path.abspath(os.path.join(
                        self.assets_directory,
                        stylesheet,),)
                    ))
            else:
                print('    stylesheet:      None')
        else:
            print('Processing {}'.format(self.input_file_path))

    def unregister_error(self):
        self._errored = False

    def write_rebuilt_source(
        self,
        rebuilt_source,
        output_file_path=None,
        ):
        if os.path.exists(output_file_path):
            with open(output_file_path, 'r') as file_pointer:
                old_source = file_pointer.read()
            if old_source == rebuilt_source:
                return
        with open(output_file_path, 'w') as file_pointer:
            file_pointer.write(rebuilt_source)

    ### PUBLIC PROPERTIES ###

    @property
    def assets_directory(self):
        return self._assets_directory

    @property
    def console(self):
        return self._console

    @property
    def errored(self):
        return self._errored

    @property
    def input_directory(self):
        if self.input_file_path is None:
            return '.'
        return os.path.dirname(self.input_file_path)

    @property
    def input_file_contents(self):
        return self._input_file_contents

    @property
    def input_file_path(self):
        return self._input_file_path

    @property
    def latex_assets_prefix(self):
        assets_directory = self.assets_directory
        if not assets_directory:
            assets_directory = 'assets'
        if self.latex_root_directory:
            return os.path.relpath(
                assets_directory,
                self.latex_root_directory,
                )
        return os.path.relpath(
            assets_directory,
            self.input_directory,
            )
    @property
    def latex_root_directory(self):
        return self._latex_root_directory

