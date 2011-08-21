def _get_module_members(module_path, klass='class'):
   '''Get members in module.'''

   f = open(module_path, 'r')
   lines = f.readlines()
   f.close()
   result = [ ]
   for line in lines:
      if line.startswith(klass):
         attr_name = line.split(' ')[1].split('(')[0]
         result.append(attr_name)
   return result
