def format_input_lines_as_doc_string(input_lines):
    r""".. versionadded:: 2.0

    Format `input_lines` as doc string.

    Format expressions intelligently.

    Treat blank lines intelligently.

    Capture hash-suffixed line output.

    Use when writing docstrings.

    Example skipped because docstring goes crazy on example input.
    """

    tab = '    '
    start = tab + tab + 'abjad> '
    lines = input_lines.split('\n')
    last_line_index = len(lines) - 1
    most = ''
    for i, line in enumerate(lines):
        if line == '':
            if i not in (0, last_line_index):
                print tab + tab
                print tab + '::'
                print tab + tab
        elif line.startswith('f('):
            print _replace_line_with_format(tab, most, line)
        elif line.endswith('###'):
            _handle_repr_line(tab, most, line)
            most += line + '\n'
        else:
            most += line + '\n'
            print start + line


def _handle_repr_line(tab, most_lines, line):
    header = 'from abjad import *\n'
    most_lines = header + most_lines
    exec(most_lines)
    line = line.replace('#', '')
    print tab + tab + 'abjad> ' + line
    exec('__x = %s' % line)
    if __x is not None:
        print tab + tab + repr(__x)


def _replace_line_with_format(tab, most_lines, last_line):
    header = 'from abjad import *\n'
    most_lines = header + most_lines
    exec(most_lines)
    last_variable = last_line[2:-1]
    print tab + tab + 'abjad> ' + 'f(%s)' % last_variable
    exec(most_lines)
    exec('__x = %s.format' % last_variable)
    format_lines = __x.split('\n')
    format_lines = [x.replace('\t', tab) for x in format_lines]
    format_lines = [tab + tab + format_line for format_line in format_lines]
    format_str = '\n'.join(format_lines)
    return format_str
