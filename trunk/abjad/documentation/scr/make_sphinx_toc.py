from _get_public_abjad_names import _get_public_abjad_names
from _module_path_to_doc_path import _module_path_to_doc_path
import os


def make_sphinx_toc( ):
   '''Make table of contents for Abjad API.
   Divide TOC into classes, interfaces and tools.'''

   names = _get_public_abjad_names( )
   klasses, interfaces, functions, tools = [ ], [ ], [ ], [ ]
   for name in names:
      if name['kind'] == 'class':
         if 'exceptions' not in name['module']:
            if 'Interface' in name['name']:
               interfaces.append(name)
            else:
               klasses.append(name)
      elif name['kind'] == 'function':
         if 'tools' in name['module']:
            tools.append(name)
         else:
            functions.append(name)
      else:
         raise ValueError('name must be class or function.')

   result = 'Abjad API\n'
   result += '=' * (len(result) - 1)
   result += '\n\n'
   result += '.. toctree::'
   result += '\n\n'

   result += 'Classes\n'
   result += '-' * (len('Classes'))
   result += '\n\n'
   result += '.. toctree::\n'
   result += '   :maxdepth: 1\n'
   result += '\n'
   for name in klasses:
      if not name['name'].startswith('_'):
         doc_path = _module_path_to_doc_path(name['module'])
         result += '   %s\n' % doc_path
   result += '\n\n'
  
   result += 'Facade classes'
   result += '\n\n'
   result += '.. toctree::\n'
   result += '   :maxdepth: 1\n'
   result += '\n'
   for name in functions:
      if not name['name'].startswith('_'):
         doc_path = _module_path_to_doc_path(name['module'])
         result += '   %s\n' % doc_path
   result += '\n\n'

   result += 'Interfaces\n'
   result += '-' * (len('Interfaces'))
   result += '\n\n'
   result += '.. toctree::\n'
   result += '   :maxdepth: 1\n'
   result += '\n'
   for name in interfaces:
      if not name['name'].startswith('_'):
         doc_path = _module_path_to_doc_path(name['module'])
         result += '   %s\n' % doc_path
   result += '\n\n'
  
   tools.sort(lambda x, y: cmp(x['module'], y['module']))

   result += 'Tools\n'
   result += '-' * (len('Tools'))
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


#def make_sphinx_toc(content):
##def make_sphinx_toc(klasses, interfaces, tools):
#   result = 'Abjad API\n'
#   result += '=' * (len(result) - 1)
#   result += '\n\n'
#   result += '.. toctree::'
#   result += '\n\n'
#   for line in content:
#      result += '   %s' % line
#      result += '\n'
#   return result
