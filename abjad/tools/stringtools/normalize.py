# -*- encoding: utf-8 -*-
import textwrap


def normalize(string):
    r"""Normalizes `string`.

    ::

        >>> string = r'''
        ...     foo
        ...         bar
        ... '''
        >>> print(string)
        <BLANKLINE>
            foo
                bar
        <BLANKLINE>

    ::

        >>> print(stringtools.normalize(string))
        foo
            bar

    Returns string.
    """
    string = string.replace('\t', '    ')
    lines = string.split('\n')
    while lines and (not lines[0] or lines[0].isspace()):
        lines.pop(0)
    while lines and (not lines[-1] or lines[-1].isspace()):
        lines.pop()
    for i, line in enumerate(lines):
        lines[i] = line.rstrip()
    string = '\n'.join(lines)
    string = textwrap.dedent(string)
    return string
