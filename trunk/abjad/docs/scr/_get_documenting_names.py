from _get_documenting_modules import _get_documenting_modules


def _get_documenting_names():
   '''Return a list of Abjad classes and functions to document in public API.
   Sort list alphabetically by name.
   Each list entry has the form of a dictionary with three items.
   The dictionary keys are 'name', 'kind' and 'module'.
   '''

   names = [ ]
   for module in _get_documenting_modules():
      f = open(module, 'r')
      lines = f.readlines()
      f.close()
      for line in lines:
         if line.startswith('def'):
            name = line.split(' ')[1].split('(')[0]
            names.append({'name': name, 'kind': 'function', 'module': module})
         elif line.startswith('class'):
            name = line.split(' ')[1].split('(')[0]
            names.append({'name': name, 'kind': 'class', 'module': module})
   names.sort(lambda x, y: cmp(x['name'], y['name']))
   for name in names[:]:
      if 'ParentageInterface' in name['name']:
         names.remove(name)
   return names

if __name__ == '__main__':
   names = _get_documenting_names()
   for name in names:
      print name
