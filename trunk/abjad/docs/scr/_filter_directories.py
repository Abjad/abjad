#def _filter_directories(dirs_list):
#   '''Remove nondocumenting directories from dirs_list.'''
#
#   ## add newly created nondocumenting directories to this list
#   dirs_remove = ['.svn', 'book', 'cfg', 'checks', 'core', 'debug', 'demos',
#      'docs', 'exceptions', 'navigator', 'optimization', 'scm', 'scr', 'test',
#      'update',
#      ]
#
#   result = [ ]
#
##   for dir in dirs_remove:
##      try:
##         dirs_list.remove(dir)
##      except ValueError:
##         pass
#
#   for directory in dirs_list:
#      if directory not in dirs_remove:
#         result.append(directory)
#
#   return result
