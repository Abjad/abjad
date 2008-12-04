def _wrap_format(format):
   lines = format.split('\n')
   if '{' not in lines[0] and '<<' not in lines[0]:
      return '{\n%s\n}' % ''.join(['\t' + line for line in lines])
   else:
      return format
