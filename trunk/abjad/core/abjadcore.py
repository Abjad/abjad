
class _Abjad(object):
   '''
   Abjad root class. All (or just public?) Abjad classes inherit from it.
   '''
   
   def __cmp__(self, arg):
      raise Exception(NotImplemented)

   def __eq__(self, arg):
      return id(self) == id(arg)

   def __ne__(self, arg):
      return id(self) != id(arg)

   def __nonzero__(self):
      return True
