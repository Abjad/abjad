from abjad.tools import *
from experimental import *
import time


def process_code_block(pipe, lines, image_count=0, hide_prompt=False):

    grouped_results = []
    result = []

    pipe.write('\n')

    for line in lines:
        hide = False
        current = pipe.read_wait().split('\n')

        if line.endswith('<hide'):
            hide = True
            line = line.rpartition('<hide')[0]

        if not hide:
            current[-1] += line
            result.extend(current)

        if line.startswith('show(') and line.endswith(')'):
            image_count += 1
            file_name = 'image-{}'.format(image_count)
            object_name = line[5:-1]
            command = "iotools.write_expr_to_ly({}, {!r})".format(object_name, file_name)
            pipe.write(command)
            grouped_results.append(result)
            grouped_results.append(file_name)
            result = []
        else:
            pipe.write(line)

        pipe.write('\n')

    result.extend(pipe.read_wait().split('\n'))

    if result[-1] == '>>> ':
        result.pop()

    grouped_results.append(result)

    if hide_prompt:
        for result in [group for group in grouped_results if isinstance(group, list)]:
            for i, line in enumerate(result):
                if line.startswith(('>>> ', '... ')):
                    result[i] = line[4:]

    return grouped_results, image_count
