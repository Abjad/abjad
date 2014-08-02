# -*- encoding: utf-8 -*-


def format_input_lines_as_regression_test(input_lines, tab_width=3):
    r"""Formats `input_lines` as regression test.

    ..  container:: example

        ::

            >>> input_lines = '''
            ... staff = Staff("c'8 d'8 e'8 f'8")
            ... beam = spannertools.Beam()
            ... attach(beam, staff.select_leaves())
            ... f(staff)
            ...
            ... scoretools.FixedDurationTuplet(Duration(2, 8), staff[:3])
            ... f(staff)
            ... '''

        ::

            >>> stringtools.format_input_lines_as_regression_test(input_lines) # doctest: +SKIP

                staff = Staff("c'8 d'8 e'8 f'8")
                beam = spannertools.Beam()
                attach(beam, staff.select_leaves())

                r'''
                \new Staff {
                    c'8 [
                    d'8
                    e'8
                    f'8 ]
                }
                '''

                scoretools.FixedDurationTuplet(Duration(2, 8), staff[:3])

                r'''
                \new Staff {
                    \times 2/3 {
                        c'8 [
                        d'8
                        e'8
                    }
                    f'8 ]
                }

                assert select(staff).is_well_formed()
                assert format(staff) == "\\new Staff {
                    \n\t\\times 2/3 {\n\t\tc'8 [\n\t\td'8\n\t\te'8\n\t}\n\tf'8 ]\n}"
                '''

    Formats expressions intelligently.

    Treats blank lines intelligently.

    Removes line-final hash characters.

    Use when writing tests.

    Returns string.
    """

    tab = ' ' * tab_width
    start = tab
    lines = input_lines.split('\n')
    most = ''
    for i, line in enumerate(lines):
        if line == '':
            print('')
        elif line.startswith('f('):
            last_format_line = line
            print('')
            print(tab + "r'''")
            print(_replace_line_with_tabbed_format(tab, most, line))
            print(tab + "'''")
        elif line.endswith('#'):
            line = line.replace('#', '')
            most += line + '\n'
            print(start + line)
        else:
            most += line + '\n'
            print(start + line)
    last_variable = last_format_line[2:-1]
    print(tab + 'assert select(%s).is_well_formed()' % last_variable)
    format_string = _replace_line_with_format(most, last_format_line)
    format_string = repr(format_string)
    print(tab + 'assert format(%s) == %s' % (last_variable, format_string))


def _replace_line_with_format(most_lines, last_line):
    header = 'from abjad import *\n'
    most_lines = header + most_lines
    exec(most_lines)
    last_variable = last_line[2:-1]
    exec(most_lines)
    exec('__x = %s.format' % last_variable)
    return __x


def _replace_line_with_tabbed_format(tab, most_lines, last_line):
    __x = _replace_line_with_format(most_lines, last_line)
    format_lines = __x.split('\n')
    format_lines = [tab + format_line for format_line in format_lines]
    format_str = '\n'.join(format_lines)
    return format_str