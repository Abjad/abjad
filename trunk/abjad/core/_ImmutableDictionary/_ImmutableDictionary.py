class _ImmutableDictionary(dict):
   '''.. versionadded:: 1.1.2
   '''

   def __delitem__(self, *args):
      raise AttributeError('objects are immutable: "%s".' % self.__class__.__name__)

   def __setitem__(self, *args):
      raise AttributeError('objects are immutable: "%s".' % self.__class__.__name__)
