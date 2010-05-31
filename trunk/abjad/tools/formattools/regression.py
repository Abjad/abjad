def regression(code, tab_width = 3):
   r""".. versionadded:: 1.1.2

   Format `code` for regression test::

      abjad> code = '''
      ... staff = Staff(construct.scale(4))
      ... Beam(staff.leaves)
      ... f(staff)
      ... 
      ... FixedDurationTuplet((2, 8), staff[:3])
      ... f(staff)
      ... '''
      abjad> formattools.regression(code)

         staff = Staff(construct.scale(4))
         Beam(staff.leaves)

         r'''
         \new Staff {
              c'8 [
              d'8
              e'8
              f'8 ]
         }
         '''

         FixedDurationTuplet((2, 8), staff[:3])

         r'''
         \new Staff {
              \times 2/3 {
                      c'8 [
                      d'8
                      e'8
              }
              f'8 ]
         }
         '''

   Format expressions intelligently.

   Treat blank lines intelligently.

   Use when writing tests.
   """

   tab = ' ' * tab_width
   start = tab
   lines = code.split('\n')
   last_line_index = len(lines) - 1
   most = ''
   for i, line in enumerate(lines):
      if line == '':
         print ''
      elif line.startswith('f('):
         print ''
         print tab + "r'''"
         print _replace_line_with_format(tab, most, line)
         print tab + "'''"
      else:
         most += line + '\n'
         print start + line


def _replace_line_with_format(tab, most_lines, last_line):
   header = 'from abjad import *\n'
   most_lines = header + most_lines
   exec(most_lines)
   last_variable = last_line[2:-1]
   exec(most_lines)
   exec('__x = %s.format' % last_variable)
   format_lines = __x.split('\n')
   format_lines = [tab + format_line for format_line in format_lines]
   format_str = '\n'.join(format_lines)
   return format_str
