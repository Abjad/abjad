class _Abjad(object):
   '''Mix-in base class designed to regularize comparison behavior.
   '''

   __slots__ = ( )

   ## OVERLOADS ##
   
   def __eq__(self, arg):
      return id(self) == id(arg)

   def __ge__(self, arg):
      raise TypeError

   def __gt__(self, arg):
      raise TypeError

   def __le__(self, arg):
      raise TypeError

   def __lt__(self, arg):
      raise TypeError

   def __ne__(self, arg):
      return id(self) != id(arg)

   def __nonzero__(self):
      return True

   def __repr__(self):
      return '<%s>' % self.__class__.__name__
