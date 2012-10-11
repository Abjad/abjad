from abjad.tools import abctools
from abjad.tools import sequencetools
from abjad.tools import documentationtools
from abjad.tools.abjadbooktools.CodeBlock import CodeBlock
from abjad.tools.abjadbooktools.OutputFormat import OutputFormat
import os
import shutil
import subprocess
import tempfile


class AbjadBookProcessor(abctools.AbjadObject):

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_directory', '_image_prefix', '_lines', '_output_format', '_skip_rendering')

    ### INITIALIZER ###

    def __init__(self, directory, lines, output_format, skip_rendering=False, image_prefix='image'):
        assert isinstance(output_format, OutputFormat)
        self._directory = os.path.abspath(directory)
        self._image_prefix = image_prefix
        self._lines = tuple(lines)
        self._output_format = output_format
        self._skip_rendering = bool(skip_rendering)

    ### SPECIAL METHOD ###

    def __call__(self, verbose=True):

        # Verify input, and extract code blocks
        code_blocks = self._extract_code_blocks(self.lines)        

        # Create a temporary directory, and step into it.
        tmp_directory = self._setup_tmp_directory(self.directory)
        os.chdir(tmp_directory)

        # Process code blocks, and render images inside the temporary directory
        pipe = self._setup_pipe()
        image_count = self._process_code_blocks(pipe, code_blocks, tmp_directory,
            self.image_prefix)
        ly_filenames = self._extract_ly_filenames(code_blocks)
        self._cleanup_pipe(pipe)
        if not self.skip_rendering:
            self._render_ly_files(ly_filenames, self.output_format, verbose)

        # Step out of the tmp directory, back to the original, and cleanup.
        os.chdir(self.directory)
        self._cleanup_image_files(self.directory, tmp_directory, image_count, self.image_prefix,
            self.output_format.image_format)
        self._cleanup_tmp_directory(tmp_directory)

        # Interleave newly reformatted code with the old, and return.
        if code_blocks:
            result = self._interleave_source_with_code_blocks(self.lines, code_blocks, self.output_format)
        else:
            result = '\n'.join(self.lines)
        return result

    ### PUBLIC READ-ONLY PROPERTIES ###

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

    ### PRIVATE METHODS ###

    def _cleanup_image_files(self, directory, tmp_directory,
            image_count, image_prefix, image_format):
        image_directory = os.path.join(directory, 'images')
        if not os.path.isdir(image_directory):
            os.mkdir(image_directory)
        for x in os.listdir(image_directory):
            if x.startswith('{}-'.format(image_prefix)) and x.endswith(image_format):
                # this should handle both 'index-1.png' and 'index-1-page3.png'
                name = os.path.splitext(x)[0]
                number = int(name.split('-')[1])
                if image_count < number:
                    os.remove(os.path.join(image_directory, x))
        for x in os.listdir(tmp_directory):
            if x.endswith(('.pdf', '.png')):
                old = os.path.join(tmp_directory, x)
                new = os.path.join(image_directory, x)
                os.rename(old, new)

    def _cleanup_pipe(self, pipe):
        pipe.write('quit()\n')
        pipe.close()

    def _cleanup_tmp_directory(self, tmp_directory):
        shutil.rmtree(tmp_directory)

    def _extract_code_blocks(self, lines):
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
                    code_block = CodeBlock(block[1:],
                        starting_line_number,
                        i,
                        hide=hide,
                        strip_prompt=strip_prompt)
                    blocks.append(code_block)
                else:
                    raise Exception('Extra closing tag at line {}'.format(i))
            elif in_block:
                block.append(line)
        if in_block:
            raise Exception('Unterminated tag at EOF.')
        return tuple(blocks)

    def _extract_ly_filenames(self, code_blocks):
        filenames = []
        for code_block in code_blocks:
            for result in code_block.processed_results:
                if isinstance(result, str):
                    filenames.append(result)
        return filenames

    def _interleave_source_with_code_blocks(self, lines, code_blocks, output_format):
        interleaved = []
        interleaved.append('\n'.join(lines[:code_blocks[0].starting_line_number]))
        for pair in sequencetools.iterate_sequence_pairwise_strict(code_blocks):
            first_block, second_block = pair
            interleaved.extend(output_format(first_block))
            interleaved.append('\n'.join(lines[first_block.ending_line_number + 1:second_block.starting_line_number]))
        interleaved.extend(output_format(code_blocks[-1]))
        interleaved.append('\n'.join(lines[code_blocks[-1].ending_line_number + 1:]))
        return '\n'.join(interleaved)

    def _process_code_blocks(self, pipe, code_blocks, directory, image_prefix):
        image_count = 0
        for code_block in code_blocks:
            image_count = code_block(pipe, image_count, directory, image_prefix)
        return image_count

    def _setup_pipe(self):
        pipe = documentationtools.Pipe()
        pipe.read_wait()
        pipe.write('from abjad import *\n')
        pipe.read_wait()
        return pipe

    def _setup_tmp_directory(self, directory):
        tmp_directory = os.path.abspath(tempfile.mkdtemp(dir=directory))
        return tmp_directory

    def _render_ly_files(self, filenames, output_format, verbose):
        if output_format.image_format == 'pdf':
            commands = [ 
                'lilypond {}.ly',
                'pdfcrop {}.pdf {}.pdf'
            ]
        elif output_format.image_format == 'png':
            commands = [
                'lilypond --png -dresolution=300 {}.ly',
                'convert {}.png -trim -resample 40%% {}.png'
            ]
        for filename in filenames:
            print '\tRendering {}.ly...'.format(filename)
            for command in commands:
                command = command.format(*([filename] * command.count('{}')))
                if verbose:
                    subprocess.call(command, shell=True)
                else:
                    subprocess.call(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
