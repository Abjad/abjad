import os


def _create_subdirectories(root_dir, dirs, interactive):
   '''Create dirs in root_dir.
   If user specifies interactive mode, prompt before each.
   '''

   for dir in dirs:
      new_dir = os.path.join(root_dir, dir)
      if not os.path.exists(new_dir):
         if interactive.lower() in ('y', ''):
            msg = 'Will create new directory "%s". Proceed? [Y/n]: ' % new_dir
            input = raw_input(msg)
         else:
            input = 'Y'
         if input.lower() in ('y', ''):
            print 'Creating directory %s ...' % new_dir
            os.mkdir(new_dir)
