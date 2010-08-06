def _filter_files(files):
   '''Retain all *.py files.
      Remove all _*   files.'''
   for f in files[:]:
      if not f.endswith('.py') or f.startswith('_'):
         files.remove(f)
