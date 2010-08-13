class _ImmutableDictionary(dict):

   def __delitem__(self, *args):
      raise AttributeError('%s objects are immutable.' % self.__class__.__name__)

   def __setitem__(self, *args):
      raise AttributeError('%s objects are immutable.' % self.__class__.__name__)
