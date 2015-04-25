# -*- encoding: utf-8 -*-
import os
import textwrap
from abjad.tools import documentationtools
from abjad.tools.abctools.AbjadObject import AbjadObject


class CodeBlock(AbjadObject):
    r'''A code block.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_hide',
        '_lines',
        '_processed_results',
        '_scale',
        '_starting_line_number',
        '_stopping_line_number',
        '_strip_prompt',
        '_wrap_width',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        hide=False,
        lines=None,
        scale=None,
        starting_line_number=0,
        stopping_line_number=1,
        strip_prompt=False,
        wrap_width=None
        ):
        lines = lines or []
        assert starting_line_number <= stopping_line_number
        self._hide = bool(hide)
        self._lines = tuple(lines)
        self._processed_results = None
        self._scale = scale
        self._starting_line_number = starting_line_number
        self._stopping_line_number = stopping_line_number
        self._strip_prompt = bool(strip_prompt)
        self._wrap_width = wrap_width

    ### SPECIAL METHODS ###

    def __call__(
        self,
        processor,
        pipe,
        image_count=0,
        directory=None,
        image_prefix='image',
        verbose=False,
        ):
        r'''Calls code block.

        Returns image count.
        '''

        assert isinstance(pipe, documentationtools.Pipe)

        if verbose:
            print('\nCODEBLOCK: {}:{}'.format(
                self.starting_line_number,
                self.stopping_line_number
                ))

        grouped_results = []
        result = []

        pipe.write('\n')

        previous_line_was_empty = False

        for line in self.lines:

            processor.update_status(line)


            if not self.strip_prompt or not previous_line_was_empty:
                current = self.read(pipe)

            hide = self.hide
            if '<hide' in line:
                hide = True
                line = line.replace('<hide', '')
                line = line.rstrip()

            no_doc_template = False
            if '<no-doc-template' in line:
                no_doc_template = True
                line = line.replace('<no-doc-template', '')
                line = line.rstrip()

            page_range = None
            if '<page' in line:
                parts = line.rpartition('<page')
                line = parts[0]
                page_range = parts[-1].strip()
                if '-' in page_range:
                    parts = page_range.partition('-')
                    page_range = range(int(parts[0]), int(parts[-1]) + 1)
                else:
                    page_range = [int(page_range)]

            if not hide:
                current[-1] += line
                result.extend(current)

            if verbose:
                for x in current:
                    print(x)

            if line.startswith('show('):
                image_count += 1
                file_name = '{}-{}'.format(image_prefix, image_count)

                line = line.rpartition(')')[0]
                line = line[5:]

                object_name = line
                keywords = ''
                if ',' in line:
                    object_name, _, keywords = line.partition(',')
                file_path = file_name + '.ly'
                if directory:
                    file_path = os.path.join(directory, file_path)
                if keywords and no_doc_template:
                    command = '__result__ = persist({}).as_ly({!r}, {})'.format(
                        object_name, file_path, keywords)
                elif keywords:
                    object_name = 'documentationtools.make_reference_manual_lilypond_file({}, {})'.format(
                        object_name, keywords)
                    command = '__result__ = persist({}).as_ly({!r})'.format(
                        object_name, file_path)
                elif no_doc_template:
                    command = '__result__ = persist({}).as_ly({!r})'.format(
                        object_name, file_path)
                else:
                    object_name = 'documentationtools.make_reference_manual_lilypond_file({})'.format(
                        object_name)
                    command = '__result__ = persist({}).as_ly({!r})'.format(
                        object_name, file_path)
                print('COMMAND', command)

                pipe.write(command)
                grouped_results.append(result)
                image_dict = {
                    'file_name': file_name,
                    'image_count': image_count,
                    'image_prefix': image_prefix,
                    'page_range': page_range,
                    'scale': self.scale,
                    }
                grouped_results.append(image_dict)
                result = []
                pipe.write('\n')
                previous_line_was_empty = False

            else:
                if not self.strip_prompt or len(line.strip()):
                    pipe.write(line)
                    pipe.write('\n')
                    previous_line_was_empty = False
                else:
                    previous_line_was_empty = True
                #print '  LINE?', line
                #if len(line.strip()):
                #    #print '  PIPE:', line
                #    pipe.write(line)
                #    pipe.write('\n')
                #    previous_line_was_empty = False
                #else:
                #    previous_line_was_empty = True

        result.extend(self.read(pipe))
        if result[-1] == '>>> ':
            result.pop()

        pipe.write('\n')
        result.extend(self.read(pipe))
        if result[-1] == '>>> ':
            result.pop()

        grouped_results.append(result)

        if self.strip_prompt:
            for result in [group for group in grouped_results
                if isinstance(group, list)]:
                for i, line in enumerate(result):
                    if line.startswith(('>>> ', '... ')):
                        result[i] = line[4:]
                while not result[-1]:
                    result.pop()

        for i, result in enumerate(grouped_results):
            if isinstance(result, list):
                grouped_results[i] = tuple(result)

        self._processed_results = tuple([x for x in grouped_results if x])

        return image_count

    def __eq__(self, expr):
        r'''Is true when `expr` is a code block with lines, starting line
        number, ending line number, hide and strip prompt boolean equal to
        those of this code block. Otherwise false.

        Returns boolean.
        '''
        if type(self) == type(expr) and \
            self.lines == expr.lines and \
            self.starting_line_number == expr.starting_line_number and \
            self.stopping_line_number == expr.stopping_line_number and \
            self.hide == expr.hide and \
            self.strip_prompt == expr.strip_prompt:
            return True
        return False

    def __hash__(self):
        r'''Hashes code block.

        Required to be explicitly re-defined on Python 3 if __eq__ changes.

        Returns integer.
        '''
        return super(CodeBlock, self).__hash__()

    ### PUBLIC PROPERTIES ###

    @property
    def hide(self):
        r'''Is true when code block should hide.
        '''
        return self._hide

    @property
    def lines(self):
        r'''Lines of code block.
        '''
        return self._lines

    @property
    def processed_results(self):
        r'''Processed results of code block.
        '''
        return self._processed_results

    @property
    def scale(self):
        r'''Image scaling factor.
        '''
        return self._scale

    @property
    def starting_line_number(self):
        r'''Starting line number of code block.
        '''
        return self._starting_line_number

    @property
    def stopping_line_number(self):
        r'''Ending line number of code block.
        '''
        return self._stopping_line_number

    @property
    def strip_prompt(self):
        r'''Is true when code block should strip prompt.
        '''
        return self._strip_prompt

    @property
    def wrap_width(self):
        r'''Wrap width.
        '''
        return self._wrap_width

    ### PUBLIC METHODS ###

    def read(self, pipe):
        r'''Reads `pipe`.
        '''
        # Guarantee we make it to the next prompt.
        # Exceptions sometimes take longer than expected.
        result = pipe.read_wait().replace('\t', '    ').split('\n')
        if result[-1] == '':
            result.pop()
        while result[-1] not in ('>>> ', '... '):
            new = pipe.read_wait().replace('\t', '    ').split('\n')
            if new[-1] == '':
                new.pop()
            result.extend(new)
        if self.wrap_width is not None:
            new_result = []
            for line in result:
                if self.wrap_width < len(line):
                    new_result.extend(textwrap.wrap(line, self.wrap_width))
                else:
                    new_result.append(line)
            return new_result
        return result