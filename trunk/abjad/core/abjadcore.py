class _Abjad(object):
   '''
   Abjad root class. All Abjad classes inherit from _Abjad.
   '''
   
   def __eq__(self, arg):
      return id(self) == id(arg)

   def __ge__(self, arg):
      return Exception(NoteImplemented)

   def __gt__(self, arg):
      return Exception(NoteImplemented)

   def __le__(self, arg):
      return Exception(NoteImplemented)

   def __lt__(self, arg):
      return Exception(NoteImplemented)

   def __ne__(self, arg):
      return id(self) != id(arg)

   def __nonzero__(self):
      return True

   def __repr__(self):
      return '<%s>' % self.__class__.__name__
