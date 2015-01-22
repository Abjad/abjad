# -*- encoding: utf-8 -*-
import importlib
import inspect
import os
import re
import shutil
import subprocess
from abjad.tools import sequencetools
from abjad.tools import documentationtools
from abjad.tools.abctools.AbjadObject import AbjadObject


class AbjadBookProcessor(AbjadObject):
    r'''Abjad book processor.
    '''

    ### CLASS VARIABLES ###

    _wrap_width_pattern = re.compile('wrap_width=(\d+)')

    ### INITIALIZER ###

    def __init__(
        self,
        directory=None,
        lines=None,
        output_format=None,
        skip_rendering=False,
        image_prefix='image',
        verbose=False,
        ):
        from abjad.tools import abjadbooktools
        directory = directory = '.'
        lines = lines or []
        output_format = output_format or abjadbooktools.HTMLOutputFormat()
        assert isinstance(output_format, abjadbooktools.OutputFormat)
        self._current_code_line = 0
        self._total_code_lines = 0
        self._directory = os.path.abspath(directory)
        self._image_prefix = image_prefix
        self._lines = tuple(lines)
        self._output_format = output_format
        self._skip_rendering = bool(skip_rendering)
        self._verbose = bool(verbose)

    ### SPECIAL METHOD ###

    def __call__(self, verbose=True):
        r'''Calls Abjad book processor.
        '''

        # Verify input, and extract code blocks
        code_blocks = self._extract_code_blocks(self.lines)
        for code_block in code_blocks:
            self._total_code_lines += len(code_block.lines)

        # Create a temporary directory, and step into it.
        tmp_directory = self._setup_tmp_directory(self.directory)
        os.chdir(tmp_directory)

        # Process code blocks and render images inside the temporary directory
        pipe = self._setup_pipe()
        image_count = self._process_code_blocks(
            pipe, code_blocks, tmp_directory, self.image_prefix)
        ly_file_names = self._extract_ly_file_names(code_blocks)
        self._cleanup_pipe(pipe)
        if not self.skip_rendering:
            self._render_ly_files(ly_file_names, self.output_format, verbose)

        # Interleave newly reformatted code with the old, and return.
        if code_blocks:
            result = self._interleave_source_with_code_blocks(
                tmp_directory, self.lines, code_blocks, self.output_format)
        else:
            result = '\n'.join(self.lines)

        # Step out of the tmp directory, back to the original, and cleanup.
        os.chdir(self.directory)
        self._cleanup_image_files(
            self.directory,
            tmp_directory,
            image_count,
            self.image_prefix,
            self.output_format.image_format,
            )
        self._cleanup_tmp_directory(tmp_directory)

        return result

    ### PUBLIC PROPERTIES ###

    @property
    def directory(self):
        r'''Directory.
        '''
        return self._directory

    @property
    def image_prefix(self):
        r'''Image prefix.
        '''
        return self._image_prefix

    @property
    def lines(self):
        r'''Lines.
        '''
        return self._lines

    @property
    def output_format(self):
        r'''Output format.
        '''
        return self._output_format

    @property
    def skip_rendering(self):
        r'''Skip rendering.
        '''
        return self._skip_rendering

    @property
    def verbose(self):
        r'''Verbose.
        '''
        return self._verbose

    ### PRIVATE METHODS ###

    def _cleanup_image_files(
        self,
        directory,
        tmp_directory,
        image_count,
        image_prefix,
        image_format,
        ):
        from abjad.tools import systemtools
        image_directory = os.path.join(directory, 'images')
        if not os.path.isdir(image_directory):
            os.mkdir(image_directory)
        for x in os.listdir(tmp_directory):
            if x.endswith('.png'):
                source = os.path.join(tmp_directory, x)
                target = os.path.join(image_directory, x)
                if not os.path.exists(target) or \
                    not documentationtools.compare_images(source, target):
                    os.rename(source, target)
                    if self.verbose:
                        print('\tMoving {}.'.format(x))
                else:
                    if self.verbose:
                        print('\tKeeping old {}.'.format(x))
            elif x.endswith('.pdf'):
                source = os.path.join(tmp_directory, x)
                target = os.path.join(image_directory, x)
                if systemtools.TestManager.compare_files(source, target):
                    if self.verbose:
                        print('\tKeeping old {}.'.format(x))
                    continue
                os.rename(source, target)
                if self.verbose:
                    print('\tMoving {}.'.format(x))

    def _cleanup_pipe(self, pipe):
        #print 'CLEANUP PIPE'
        pipe.write('quit()\n')
        pipe.close()

    def _cleanup_tmp_directory(self, tmp_directory):
        #print 'CLEANUP TMP DIRECTORY'
        shutil.rmtree(tmp_directory)

    def _extract_code_blocks(self, lines):
        from abjad.tools import abjadbooktools
        #print 'EXTRACT CODE BLOCKS'
        blocks = []
        block = []
        starting_line_number = 0
        in_block = False
        for i, line in enumerate(lines):
            if line.startswith('<abjad>'):
                if in_block:
                    message = 'extra opening tag at line {}.'
                    message = message.format(i)
                    raise Exception(message)
                else:
                    in_block = True
                    block = [line]
                    starting_line_number = i

            elif line.startswith('</abjad>'):
                if in_block:
                    in_block = False
                    hide = 'hide=true' in block[0]
                    scale = None
                    if 'scale=' in block[0]:
                        pattern = re.compile('scale=([0-9]*\.[0-9]+|[0-9]+)')
                        match = pattern.search(block[0])
                        if match is not None:
                            group = match.groups()[0]
                            scale = float(group)
                    strip_prompt = 'strip_prompt=true' in block[0]
                    wrap_width = None
                    wrap_width_match = self._wrap_width_pattern.search(
                        block[0])
                    if wrap_width_match is not None:
                        wrap_width = int(wrap_width_match.groups()[0])
                    stopping_line_number = i
                    code_block = abjadbooktools.CodeBlock(
                        hide=hide,
                        lines=block[1:],
                        scale=scale,
                        starting_line_number=starting_line_number,
                        stopping_line_number=stopping_line_number,
                        strip_prompt=strip_prompt,
                        wrap_width=wrap_width,
                        )
                    blocks.append(code_block)
                else:
                    message = 'extra closing tag at line {}.'
                    message = message.format(i)
                    raise Exception(message)

            elif in_block:
                block.append(line)

            elif line.startswith('<abjadextract '):
                block = []
                starting_line_number = stopping_line_number = i
                hide = 'hide=true' in line
                scale = None
                if 'scale=' in line:
                    pattern = re.compile('scale=([0-9]*\.[0-9]+|[0-9]+)')
                    match = pattern.search(block[0])
                    if match is not None:
                        group = match.groups()[0]
                        scale = float(group)
                strip_prompt = 'strip_prompt=true' in line
                code_address = line.partition(
                    '<abjadextract ')[-1].partition(' \>')[0]
                module_name, dot, attr_name = code_address.rpartition('.')
                module = importlib.import_module(module_name)
                attr = getattr(module, attr_name)
                code_lines = inspect.getsource(attr).splitlines()
                code_block = abjadbooktools.CodeBlock(
                    hide=hide,
                    lines=code_lines,
                    scale=scale,
                    starting_line_number=starting_line_number,
                    stopping_line_number=stopping_line_number,
                    strip_prompt=strip_prompt
                    )
                blocks.append(code_block)

        if in_block:
            message = 'unterminated tag at EOF.'
            raise Exception(message)

        return tuple(blocks)

    def _extract_ly_file_names(self, code_blocks):
        #print 'EXTRACT LY file_nameS'
        file_names = []
        for code_block in code_blocks:
            for result in code_block.processed_results:
                if isinstance(result, dict):
                    file_names.append(result['file_name'])
        return file_names

    def _interleave_source_with_code_blocks(
        self,
        tmp_directory,
        lines,
        code_blocks,
        output_format,
        ):

        #print 'INTERLEAVE SOURCE WITH CODE BLOCKS'
        image_file_names = [x for x in os.listdir(tmp_directory)
            if (x.endswith(output_format.image_format) and
               x.startswith(self.image_prefix))]

        image_dict = {}
        for image_file_name in image_file_names:
            suffix = os.path.splitext(image_file_name.partition('-')[2])[0]
            index, part, page = suffix.partition('-')
            index = int(index)
            if page:
                page = int(page.strip('page'))
            else:
                page = 0
            if index not in image_dict:
                image_dict[index] = {}
            image_dict[index][page] = image_file_name

        interleaved = []
        interleaved.append(
            '\n'.join(lines[:code_blocks[0].starting_line_number]))
        for pair in sequencetools.iterate_sequence_nwise(code_blocks):
            first_block, second_block = pair
            interleaved.extend(output_format(first_block, image_dict))
            interleaved.append('\n'.join(lines[
                first_block.stopping_line_number+1:
                second_block.starting_line_number]))

        interleaved.extend(output_format(code_blocks[-1], image_dict))
        interleaved.append('\n'.join(
            lines[code_blocks[-1].stopping_line_number+1:]))
        return '\n'.join(interleaved)

    def _process_code_blocks(
        self,
        pipe,
        code_blocks,
        directory,
        image_prefix,
        ):
        #print 'PROCESS CODE BLOCKS'
        image_count = 0
        for i, code_block in enumerate(code_blocks):
            #print '\tCODE BLOCK', i
            image_count = code_block(
                self,
                pipe,
                image_count,
                directory,
                image_prefix,
                verbose=self.verbose,
                )
        return image_count

    def _render_ly_files(self, file_names, output_format, verbose):
        #print 'RENDER LY FILES'
        for file_name in file_names:
            if self.verbose:
                print('\tRendering {}.ly ...'.format(file_name))
            try:
                if output_format.image_format == 'pdf':
                    command = 'lilypond {}.ly'.format(file_name)
                    if self.verbose:
                        print('\t\t{}'.format(command))
                    self._run_command(command, verbose)
                    command = 'pdfcrop {}.pdf {}.pdf'.format(
                        file_name, file_name)
                    if self.verbose:
                        print('\t\t{}'.format(command))
                    self._run_command(command, verbose)
                elif output_format.image_format == 'png':
                    command = 'lilypond --png -dresolution=300 {}.ly'.format(
                        file_name)
                    if self.verbose:
                        print('\t\t{}'.format(command))
                    assert os.path.exists('{}.ly'.format(file_name))
                    self._run_command(command, verbose)
                    for file in os.listdir('.'):
                        if file.startswith(file_name) and file.endswith('.png'):
                            command = '\
                                convert {} -trim -resample 40%% {}'.format(
                                    file, file)
                            if self.verbose:
                                print('\t\t{}'.format(command))
                            self._run_command(command, verbose)
            except AssertionError as e:
                print(e)

    def _run_command(self, command, verbose):
        if verbose:
            subprocess.call(command, shell=True)
        else:
            subprocess.call(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                )

    def _setup_pipe(self):
        #print 'SETUP PIPE'
        pipe = documentationtools.Pipe()
        pipe.read_wait()
        pipe.write('from abjad import *\n')
        pipe.read_wait()
        pipe.write('from __future__ import print_function\n')
        pipe.read_wait()
        return pipe

    def _setup_tmp_directory(self, directory):
        #print 'SETUP TMP DIRECTORY'
        import tempfile
        tmp_directory = os.path.abspath(tempfile.mkdtemp(dir=directory))
        return tmp_directory

    ### PUBLIC METHODS ###

    def update_status(self, line):
        r'''Updates status.

        Returns none.
        '''
        self._current_code_line += 1
        percentage = float(self._current_code_line) / self._total_code_lines
        message = '[{:4.0%}] {}'
        message = message.format(percentage, line)
        if self.verbose:
            print(message)