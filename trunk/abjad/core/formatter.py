from abjad.core.interface import _Interface


#class _Formatter(object):
class _Formatter(_Interface):

   def __init__(self, client):
      #self._client = client
      _Interface.__init__(self, client)
      self.number = False
      self.before = [ ]
      self.after = [ ]
#      self.opening = [ ]
#      self.closing = [ ]
#      self.left = [ ]
#      self.right = [ ]
   
#   def __repr__(self):
#      return '<%s>' % self.__class__.__name__

#   @property
#   def _before(self):
#      result = [ ]
#      return result
#
#   @property
#   def _after(self):
#      result = [ ]
#      return result

#   @property
#   def _opening(self):
#      result = [ ]
#      return result
#
#   @property
#   def _closing(self):
#      result = [ ]
#      return result
