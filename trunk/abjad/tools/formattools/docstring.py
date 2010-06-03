def docstring(code, tab_width = 3):
   r""".. versionadded:: 1.1.2

   Format `code` for docstring::

      abjad> code = '''
      ... staff = Staff(construct.scale(4))
      ... Beam(staff.leaves)
      ... f(staff)
      ... 
      ... FixedDurationTuplet((2, 8), staff[:3]) ##

      ... f(staff)
      ... '''
      abjad> formattools.docstring(code)

            abjad> staff = Staff(construct.scale(4))
            abjad> Beam(staff.leaves)
            abjad> f(staff)
            \new Staff {
               c'8 [
               d'8
               e'8
               f'8 ]
            }
            
         ::
            
            abjad> FixedDurationTuplet((2, 8), staff[:3])
            FixedDurationTuplet(1/4, [c'8, d'8, e'8])

         ::

            abjad> f(staff)
            \new Staff {
               \times 2/3 {
                  c'8 [
                  d'8
                  e'8
               }
               f'8 ]
            }

   Format expressions intelligently.

   Treat blank lines intelligently.

   Capture hash-suffixed line output.

   Use when writing docstrings.
   """

   tab = '   '
   start = tab + tab + 'abjad> '
   lines = code.split('\n')
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
      elif line.endswith('##'):
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
