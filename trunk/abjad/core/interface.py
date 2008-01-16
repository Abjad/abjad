class _Interface(object):

   def __init__(self, client, interface):
      self._client = client
      self._interface = interface

   ### REPR ###

   def __repr__(self):
      return '%s( )' % self.__class__.__name__

   ### PROPERTIES ###

   def __len__(self):
      return len(self._getActiveAttributes( ))

   ### PREDICATES ###

   def isSet(self):
      return len(self._getActiveAttributes( )) > 0

   ### ACCESSORS ###

   def _getAttributes(self):
      result = [ ]
      for key in self.__dict__.iterkeys( ):
         if not key.startswith('_'):
            result.append(key)
      result.sort( )
      return result

   def _getActiveAttributes(self):
      result = [ ]
      for attr in self._getAttributes( ):
         value = self.__dict__[attr]
         if value:
            result.append(value)
      return result 

   @property
   def spanners(self):
      return self._client.spanners.get(self._interface)

   def clear(self):
      for attr in self._getActiveAttributes( ):
         attr = None

   def copy(self):
      from copy import copy
      client = self._client
      self._client = None
      result = copy(self)
      self._client = client
      return result
