from abjad.core.abjadcore import _Abjad


class _HistoryInterface(_Abjad):

   def __init__(self, client):
      self._client = client

   ## OVERLOADS ##

   def __len__(self):
      return len(self.getAttributeNames( ))

   ## PUBLIC METHODS ##

   def clear(self):
      for item in self.__dict__.items( ):
         self.__dict__.pop(item)

   def getAttributeNames(self):
      result = [ ]
      for key in self.__dict__.keys( ):
         if not key.startswith('_'):
            result.append(key)
      return result
