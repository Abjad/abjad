def make_sphinx_toc(content):
#def make_sphinx_toc(klasses, interfaces, tools):
   result = 'Abjad API\n'
   result += '=' * (len(result) - 1)
   result += '\n\n'
   result += '.. toctree::'
   result += '\n\n'
   for line in content:
      result += '   %s' % line
      result += '\n'

#   result += 'Classes'
#   result += '\n\n'
#   result += '.. toctree::'
#   result += '   :maxdepth: 1'
#   result += '\n'
#   for line in klasses:
#      result += '   %s\n' % line
#  
#   result += 'Interfaces'
#   result += '\n\n'
#   result += '.. toctree::'
#   result += '   :maxdepth: 1'
#   result += '\n'
#   for line in klasses:
#      result += '   %s\n' % line
#  
#   result += 'Tools'
#   result += '\n\n'
#   result += '.. toctree::'
#   result += '   :maxdepth: 1'
#   result += '\n'
#   for line in klasses:
#      result += '   %s\n' % line

   return result
