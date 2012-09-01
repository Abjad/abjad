from abjad.tools import abctools
from abjad.tools import documentationtools
import os


class CodeBlock(abctools.AbjadObject):

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_ending_line_number', '_hide', '_lines', '_processed_results',
        '_starting_line_number', '_strip_prompt')

    ### INITIALIZER ###

    def __init__(self, lines, starting_line_number, ending_line_number,
        hide=False, strip_prompt=False):
        assert starting_line_number < ending_line_number
        self._lines = tuple(lines)
        self._starting_line_number = starting_line_number
        self._ending_line_number = ending_line_number
        self._hide = bool(hide)
        self._strip_prompt = bool(strip_prompt)
        self._processed_results = None

    ### SPECIAL METHODS ###

    def __eq__(self, other):
        if type(self) == type(other) and \
            self.lines == other.lines and \
            self.starting_line_number == other.starting_line_number and \
            self.ending_line_number == other.ending_line_number and \
            self.hide == other.hide and \
            self.strip_prompt == other.strip_prompt:
            return True
        return False

    ### SPECIAL METHODS ###

    def __call__(self, pipe, image_count=0, directory=None, image_prefix='image'):

        assert isinstance(pipe, documentationtools.Pipe)

        grouped_results = []
        result = []

        pipe.write('\n')

        for line in self.lines:
            hide = self.hide

            current = self.read(pipe)

            if line.endswith('<hide'):
                hide = True
                line = line.rpartition('<hide')[0]

            if not hide:
                current[-1] += line
                result.extend(current)

            if line.startswith('show(') and line.endswith(')'):
                image_count += 1
                file_name = '{}-{}'.format(image_prefix, image_count)
                docs = False
                if ',' in line:
                    object_name = line.split(',')[0][5:].strip()
                    if 'docs=True' in line:
                        docs = True
                else:
                    object_name = line[5:-1]
                if directory:
                    command = "iotools.write_expr_to_ly({}, {!r}, docs={})".format(
                        object_name, os.path.join(directory, file_name), docs)
                else:
                    command = "iotools.write_expr_to_ly({}, {!r}, docs={})".format(
                        object_name, file_name, docs)
                pipe.write(command)
                grouped_results.append(result)
                grouped_results.append(file_name)
                result = []
            else:
                pipe.write(line)

            pipe.write('\n')

        result.extend(self.read(pipe))
        if result[-1] == '>>> ':
            result.pop()

        pipe.write('\n')
        result.extend(self.read(pipe))
        if result[-1] == '>>> ':
            result.pop()

        grouped_results.append(result)

        if self.strip_prompt:
            for result in [group for group in grouped_results if isinstance(group, list)]:
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

    ### PUBLIC READ-ONLY PROPERTIES ###

    @property
    def ending_line_number(self):
        return self._ending_line_number

    @property
    def hide(self):
        return self._hide

    @property
    def lines(self):
        return self._lines

    @property
    def processed_results(self):
        return self._processed_results

    @property
    def starting_line_number(self):
        return self._starting_line_number

    @property
    def strip_prompt(self):
        return self._strip_prompt
        
    ### PUBLIC METHODS ###

    def read(self, pipe):
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
        return result
