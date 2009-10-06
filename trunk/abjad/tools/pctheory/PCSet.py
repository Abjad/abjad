from PC import PC


class PCSet(set):
   '''12-ET pitch-class set from American pitch-class theory.'''

   def __init__(self, pcs):
      self.update(pcs)

   ## OVERLOADS ##

   def __contains__(self, arg):
      if isinstance(arg, PC):
         for pc in self:
            if pc == arg:
               return True
      return False

   def __eq__(self, arg):
      if isinstance(arg, PCSet):
         for element in arg:
            if element not in self:
               return False
         else:
            return True
      return False

   def __ne__(self, arg):
      return not self == arg

   def __repr__(self):
      contents = list(self)
      contents.sort( )
      return '%s(%s)' % (self.__class__.__name__, contents)

   ## PUBLIC ATTRIBUTES ##

   @property
   def prime_form(self):
      '''To be implemented.'''
      return None

   ## PUBLIC METHODS ##
   
   def add(self, arg):
      '''Built-in add( ) extended with type- and value-checking.'''
      if isinstance(arg, PC):
         candidate_pc = arg
      elif isinstance(arg, (int, float, long)):
         if 0 <= arg < 12:
            candidate_pc = PC(arg)
         else:
            raise ValueError
      else:
         raise TypeError
      if candidate_pc not in self:
         set.add(self, candidate_pc)

   def update(self, arg):
      '''Build-in update( ) extended with type- and value-checking.'''
      for element in arg:
         self.add(element)
