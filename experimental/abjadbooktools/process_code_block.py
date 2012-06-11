from abjad.tools import *
from experimental import *


def process_code_block(pipe, code_block, image_count=0):
    '''Process a single code block, `code_block` over `pipe`,
    generating .ly files along the way with each instance of show().

    The .ly files will be numbered starting at `image_count` + 1.

    Return a tuple of a list, and an updated `image_count`.

    The list consists of lines which have been passed over `pipe`,
    and filenames for each .ly file generated after a call to show().

    TODO: Clean up this explanation!
    '''

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
