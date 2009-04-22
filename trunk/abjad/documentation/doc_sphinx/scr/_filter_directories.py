
def _filter_directories(dirs_list, dirs_remove=['.svn', 'test']):
   '''Remove all directories in `dirs_remove` from `dirs_list`.'''
   for dir in dirs_remove:
      try:
         dirs_list.remove(dir)
      except ValueError:
         pass

