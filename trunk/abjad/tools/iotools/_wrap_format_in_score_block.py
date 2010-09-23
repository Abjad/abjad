def _wrap_format_in_score_block(format, midi = False, layout = False):
   lines = format.split('\n')
   if layout:
      lines.append('\\layout{ }')
   if midi:
      lines.append('\\midi{ }')
   return '\\score{\n%s\n}' % '\n'.join(['\t' + line for line in lines])

