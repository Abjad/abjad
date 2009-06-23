
def _filter_files(files):
   '''Remove all *.py and _* files.'''
   for f in files[:]:
      if not f.endswith('.py') or f.startswith('_'):
         files.remove(f)

