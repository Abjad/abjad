class _Interface(object):

   def __init__(self, client):
      self._client = client

   ### OVERLOADS ###

   def __cmp__(self, arg):
      raise Exception(NotImplemented)

   def __repr__(self):
      return '<%s>' % self.__class__.__name__

   def _copy(self):
      from copy import copy
      client = self._client
      self._client = None
      result = copy(self)
      self._client = client
      return result
