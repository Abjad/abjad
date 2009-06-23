
def make_sphinx_toc(content):
   result = 'Abjad API\n'
   result += '=' * (len(result) - 1)
   result += '\n\n'
   result += '.. toctree::'
   result += '\n\n'
   for line in content:
      result += '   %s' % line
      result += '\n'
   return result
