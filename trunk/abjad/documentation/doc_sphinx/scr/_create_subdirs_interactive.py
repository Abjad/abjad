import os

def _create_subdirs_interactive(root_dir, dirs):
   '''Create directories `dirs` in directory `root_dir` interactively.
   i.e. the user is prompted before the creation of each new directory.'''
   for dir in dirs:
      new_dir = os.path.join(root_dir, dir)
      if not os.path.exists(new_dir):
         msg = 'Will create new directory "%s". Proceed? [Y/n]: ' % new_dir
         input = raw_input(msg)
         if input.lower( ) in ('y', ''):
            os.mkdir(new_dir)
