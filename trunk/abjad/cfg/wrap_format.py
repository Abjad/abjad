def _wrap_format(format):
   lines = format.split('\n')
   if r'\markup' in lines[0] or \
      ('{' not in lines[0] and '<<' not in lines[0]):
      return '{\n%s\n}' % ''.join(['\t' + line for line in lines])
   else:
      return format

   ### TODO: wrap everything inside \score{ } block?
   ### return '\\score{\n%s\n}' % '\n'.join(['\t' + line for line in lines])
