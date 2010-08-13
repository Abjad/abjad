class _ImmutableList(list):

   def append(self, *args):
      raise AttributeError('%s objects are immutable.' % self.__class__.__name__)

   def extend(self, *args):
      raise AttributeError('%s objects are immutable.' % self.__class__.__name__)

   def insert(self, *args):
      raise AttributeError('%s objects are immutable.' % self.__class__.__name__)
