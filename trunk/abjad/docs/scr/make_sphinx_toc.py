from _get_documenting_names import _get_documenting_names
from _module_path_to_doc_path import _module_path_to_doc_path
import os


def make_sphinx_toc( ):
   '''Make table of contents for Abjad API.
   Divide TOC into classes, interfaces, spanners and tools.
   Divide tools into classes and functions.
   '''

   print 'Now making Sphinx TOC ...'
   names = _get_documenting_names( )
   klasses, interfaces, spanners, exceptions, tools = [ ], [ ], [ ], [ ], [ ]
   for name in names:
      if name['kind'] == 'class':
         if 'exceptions' not in name['module']:
            if 'tools' in name['module']:
               tools.append(name)
            elif 'Interface' in name['name'] and not 'Parentage' in name['name']:
               interfaces.append(name)
            elif 'spanner' in name['module']:
               spanners.append(name)
            else:
               klasses.append(name)
         else:
            exceptions.append(name)
      elif name['kind'] == 'function':
         if 'tools' in name['module']:
            tools.append(name)
         else:
            raise ValueError('all public functions must be tools.')
      else:
         raise ValueError('name must be class or function.')
   #print len(klasses)
   #print len(interfaces)
   #print len(spanners)
   #print len(tools)
   #print ''

   result = 'Abjad API\n'
   result += '=' * (len(result) - 1)
   result += '\n\n'
   result += '.. toctree::'
   result += '\n\n'

   section_title = 'Abjad score components'
   result += '%s\n' % section_title
   result += '-' * (len(section_title))
   result += '\n\n'
   result += '.. toctree::\n'
   result += '   :maxdepth: 1\n'
   result += '\n'
   for name in klasses:
      if not name['name'].startswith('_'):
         doc_path = _module_path_to_doc_path(name['module'])
         result += '   %s\n' % doc_path
   result += '\n\n'
  
#   section_title = 'Score component interfaces'
#   result += '%s\n' % section_title
#   result += '-' * (len(section_title))
#   result += '\n\n'
#   result += '.. toctree::\n'
#   result += '   :maxdepth: 1\n'
#   result += '\n'
#   for name in interfaces:
#      if not name['name'].startswith('_'):
#         doc_path = _module_path_to_doc_path(name['module'])
#         result += '   %s\n' % doc_path
#   result += '\n\n'
  
#   result += 'Spanners\n'
#   result += '-' * (len('Spanners'))
#   result += '\n\n'
#   result += '.. toctree::\n'
#   result += '   :maxdepth: 1\n'
#   result += '\n'
#   for name in spanners:
#      if not name['name'].startswith('_'):
#         doc_path = _module_path_to_doc_path(name['module'])
#         result += '   %s\n' % doc_path
#   result += '\n\n'
  
   tools.sort(lambda x, y: cmp(x['module'], y['module']))

   section_title = 'Abjad composition packages'
   result += '%s\n' % section_title
   result += '-' * (len(section_title))
   result += '\n\n'
   result += '.. toctree::\n'
   result += '   :maxdepth: 1\n'
   result += '\n'

   last_tools_module = ''
   for name in tools:
      if not name['name'].startswith('_'):
         doc_path = _module_path_to_doc_path(name['module'])
         cur_tools_module = doc_path.split(os.sep)[1]
         if not cur_tools_module == last_tools_module:
            result += '\n\n'
            result += cur_tools_module
            result += '\n\n'
            result += '.. toctree::\n'
            result += '   :maxdepth: 1\n'
            result += '\n'
            last_tools_module = cur_tools_module
         result += '   %s\n' % doc_path
#   result += '\n\n'
#
#   result += 'Exceptions\n'
#   result += '-' * (len('Exceptions'))
#   result += '\n\n'
#   result += '.. toctree::\n'
#   result += '   :maxdepth: 1\n'
#   result += '\n'
#   result += '   exceptions/exceptions'

   return result
