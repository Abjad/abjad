#from abjad.core import _Abjad


#class _Interface(_Abjad):
class _Interface(object):

   def __init__(self, client):
      self._client = client

   ## OVERLOADS ##

   def __repr__(self):
      return '<%s>' % self.__class__.__name__
