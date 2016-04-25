# -*- coding: utf-8 -*-
import six
import textwrap


def normalize(string, indent=None):
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

    ::

        >>> print(stringtools.normalize(string, indent=4))
            foo
                bar

    ::

        >>> print(stringtools.normalize(string, indent='* '))
        * foo
        *     bar

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
    if indent:
        if not isinstance(indent, six.string_types):
            indent = ' ' * abs(int(indent))
        lines = string.split('\n')
        for i, line in enumerate(lines):
            if line:
                lines[i] = '{}{}'.format(indent, line)
        string = '\n'.join(lines)
    return string
