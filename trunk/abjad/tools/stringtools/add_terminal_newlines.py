# -*- encoding: utf-8 -*-
def add_terminal_newlines(lines):
    r'''Add terminal newlines to `lines`:

        >>> lines = ['first line', 'second line']
        >>> stringtools.add_terminal_newlines(lines)
        ['first line\n', 'second line\n']

    Do nothing when line in `lines` already ends in newline:

    ::

        >>> lines = ['first line\n', 'second line\n']
        >>> stringtools.add_terminal_newlines(lines)
        ['first line\n', 'second line\n']

    Return newly constructed object of `lines` type.
    '''

    terminated_lines = []
    for line in lines:
        if not line.endswith('\n'):
            line = line + '\n'
        terminated_lines.append(line)
    terminated_lines = type(lines)(terminated_lines)
    return terminated_lines
