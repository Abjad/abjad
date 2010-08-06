def _filter_directories(dirs_list):
   '''Remove nondocumenting directories from dirs_list.'''

   ## add newly created nondocumenting directories to this list
   dirs_remove = ['.svn', 'book', 'cfg', 'checks', 'debug', 'demos',
      'docs', 'exceptions', 'navigator', 'scm', 'scr', 'test',
      'update',
      ]

   for dir in dirs_remove:
      try:
         dirs_list.remove(dir)
      except ValueError:
         pass
