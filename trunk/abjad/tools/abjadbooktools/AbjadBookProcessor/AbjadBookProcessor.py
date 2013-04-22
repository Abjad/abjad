import importlib
import inspect
import os
import shutil
import subprocess
import tempfile
from abjad.tools import abctools
from abjad.tools import sequencetools
from abjad.tools import documentationtools
from abjad.tools.abjadbooktools.CodeBlock import CodeBlock
from abjad.tools.abjadbooktools.OutputFormat import OutputFormat


class AbjadBookProcessor(abctools.AbjadObject):

    ### INITIALIZER ###

    def __init__(self, directory, lines, output_format, skip_rendering=False,
        image_prefix='image', verbose=False):
        assert isinstance(output_format, OutputFormat)
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

        # Verify input, and extract code blocks
        code_blocks = self._extract_code_blocks(self.lines)
        for code_block in code_blocks:
            self._total_code_lines += len(code_block.lines)

        # Create a temporary directory, and step into it.
        tmp_directory = self._setup_tmp_directory(self.directory)
        os.chdir(tmp_directory)

        # Process code blocks, and render images inside the temporary directory
        pipe = self._setup_pipe()
        image_count = self._process_code_blocks(pipe, code_blocks, tmp_directory,
            self.image_prefix)
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
        self._cleanup_image_files(self.directory, tmp_directory, image_count, self.image_prefix,
            self.output_format.image_format)
        self._cleanup_tmp_directory(tmp_directory)

        return result

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def directory(self):
        return self._directory

    @property
    def image_prefix(self):
        return self._image_prefix

    @property
    def lines(self):
        return self._lines

    @property
    def output_format(self):
        return self._output_format

    @property
    def skip_rendering(self):
        return self._skip_rendering

    @property
    def verbose(self):
        return self._verbose

    ### PRIVATE METHODS ###

    def _cleanup_image_files(self, directory, tmp_directory,
        image_count, image_prefix, image_format):
        #print 'CLEANUP IMAGE FILES'
        image_directory = os.path.join(directory, 'images')
        if not os.path.isdir(image_directory):
            os.mkdir(image_directory)
        # remove old images
        #for x in os.listdir(image_directory):
        #    if x.startswith('{}-'.format(image_prefix)) and x.endswith(image_format):
        #        # this should handle both 'index-1.png' and 'index-1-page3.png'
        #        name = os.path.splitext(x)[0]
        #        number = int(name.split('-')[1])
        #        if image_count < number:
        #            os.remove(os.path.join(image_directory, x))
        for x in os.listdir(tmp_directory):
            if x.endswith('.png'):
                source = os.path.join(tmp_directory, x)
                target = os.path.join(image_directory, x)
                if not os.path.exists(target) or \
                    not documentationtools.compare_images(source, target):
                    os.rename(source, target)
                    if self.verbose:
                        print '\tMoving {}.'.format(x)
                else:
                    if self.verbose:
                        print '\tKeeping old {}.'.format(x)
            elif x.endswith('.pdf'):
                source = os.path.join(tmp_directory, x)
                target = os.path.join(image_directory, x)
                os.rename(source, target)
                if self.verbose:
                    print '\tMoving {}.'.format(x)

    def _cleanup_pipe(self, pipe):
        #print 'CLEANUP PIPE'
        pipe.write('quit()\n')
        pipe.close()

    def _cleanup_tmp_directory(self, tmp_directory):
        #print 'CLEANUP TMP DIRECTORY'
        shutil.rmtree(tmp_directory)

    def _extract_code_blocks(self, lines):
        #print 'EXTRACT CODE BLOCKS'
        blocks = []
        block = []
        starting_line_number = 0
        in_block = False
        for i, line in enumerate(lines):
            if line.startswith('<abjad>'):
                if in_block:
                    raise Exception('Extra opening tag at line {}.'.format(i))
                else:
                    in_block = True
                    block = [line]
                    starting_line_number = i

            elif line.startswith('</abjad>'):
                if in_block:
                    in_block = False
                    hide = 'hide=true' in block[0]
                    strip_prompt = 'strip_prompt=true' in block[0]
                    stopping_line_number = i
                    code_block = CodeBlock(
                        block[1:],
                        starting_line_number,
                        stopping_line_number,
                        hide=hide,
                        strip_prompt=strip_prompt
                        )
                    blocks.append(code_block)
                else:
                    raise Exception('Extra closing tag at line {}'.format(i))

            elif in_block:
                block.append(line)

            elif line.startswith('<abjadextract '):
                block = []
                starting_line_number = stopping_line_number = i
                hide = 'hide=true' in line
                strip_prompt = 'strip_prompt=true' in line
                code_address = line.partition('<abjadextract ')[-1].partition(' \>')[0]
                module_name, dot, attr_name = code_address.rpartition('.')
                module = importlib.import_module(module_name)
                attr = getattr(module, attr_name)
                code_lines = inspect.getsource(attr).splitlines()
                code_block = CodeBlock(
                    code_lines,
                    starting_line_number,
                    stopping_line_number,
                    hide=hide,
                    strip_prompt=strip_prompt
                    )
                blocks.append(code_block)

        if in_block:
            raise Exception('Unterminated tag at EOF.')

        return tuple(blocks)

    def _extract_ly_file_names(self, code_blocks):
        #print 'EXTRACT LY FILENAMES'
        file_names = []
        for code_block in code_blocks:
            for result in code_block.processed_results:
                if isinstance(result, dict):
                    file_names.append(result['file_name'])
        return file_names

    def _interleave_source_with_code_blocks(self, tmp_directory, lines, code_blocks, output_format):

        #print 'INTERLEAVE SOURCE WITH CODE BLOCKS'
        image_file_names = [x for x in os.listdir(tmp_directory)
            if (x.endswith(output_format.image_format) and
               x.startswith(self.image_prefix))]

        image_dict = {}
        for image_filename in image_file_names:
            suffix = os.path.splitext(image_filename.partition('-')[2])[0]
            index, part, page = suffix.partition('-')
            index = int(index)
            if page:
                page = int(page.strip('page'))
            else:
                page = 0
            if index not in image_dict:
                image_dict[index] = {}
            image_dict[index][page] = image_filename

        interleaved = []
        interleaved.append('\n'.join(lines[:code_blocks[0].starting_line_number]))
        for pair in sequencetools.iterate_sequence_pairwise_strict(code_blocks):
            first_block, second_block = pair
            interleaved.extend(output_format(first_block, image_dict))
            interleaved.append('\n'.join(lines[
                first_block.ending_line_number + 1:second_block.starting_line_number]))

        interleaved.extend(output_format(code_blocks[-1], image_dict))
        interleaved.append('\n'.join(lines[code_blocks[-1].ending_line_number + 1:]))
        return '\n'.join(interleaved)

    def _process_code_blocks(self, pipe, code_blocks, directory, image_prefix):
        #print 'PROCESS CODE BLOCKS'
        image_count = 0
        for i, code_block in enumerate(code_blocks):
            #print '\tCODE BLOCK', i
            image_count = code_block(self, pipe, image_count, directory, image_prefix, verbose=self.verbose)
        return image_count

    def _render_ly_files(self, file_names, output_format, verbose):
        #print 'RENDER LY FILES'
        for file_name in file_names:
            if self.verbose:
                print '\tRendering {}.ly...'.format(file_name)
            try:
                if output_format.image_format == 'pdf':
                    command = 'lilypond {}.ly'.format(file_name)
                    if self.verbose:
                        print '\t\t{}'.format(command)
                    self._run_command(command, verbose)
                    command = 'pdfcrop {}.pdf {}.pdf'.format(file_name, file_name)
                    if self.verbose:
                        print '\t\t{}'.format(command)
                    self._run_command(command, verbose)
                elif output_format.image_format == 'png':
                    command = 'lilypond --png -dresolution=300 {}.ly'.format(file_name)
                    if self.verbose:
                        print '\t\t{}'.format(command)
                    assert os.path.exists('{}.ly'.format(file_name))
                    self._run_command(command, verbose)
                    for file in os.listdir('.'):
                        if file.startswith(file_name) and file.endswith('.png'):
                            command = 'convert {} -trim -resample 40%% {}'.format(file, file)
                            if self.verbose:
                                print '\t\t{}'.format(command)
                            self._run_command(command, verbose)
            except AssertionError, e:
                print e

    def _run_command(self, command, verbose):
        if verbose:
            subprocess.call(command, shell=True)
        else:
            subprocess.call(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def _setup_pipe(self):
        #print 'SETUP PIPE'
        pipe = documentationtools.Pipe()
        pipe.read_wait()
        pipe.write('from abjad import *\n')
        pipe.read_wait()
        return pipe

    def _setup_tmp_directory(self, directory):
        #print 'SETUP TMP DIRECTORY'
        tmp_directory = os.path.abspath(tempfile.mkdtemp(dir=directory))
        return tmp_directory

    ### PUBLIC METHODS ###

    def update_status(self, line):
        self._current_code_line += 1
        percentage = float(self._current_code_line) / self._total_code_lines
        message = '[{:4.0%}] {}'.format(percentage, line)
        if self.verbose:
            print message
