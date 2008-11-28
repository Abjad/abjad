from abjad.core.formatcarrier import _FormatCarrier
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

   def _collectLocation(self, location):
      result = [ ]
      for carrier in self._getFormatCarriers( ):
         try:
            exec('result.extend(carrier.%s)' % location)
         except AttributeError:
            pass
      try:
         exec('result.extend(self._client.spanners.%s)' % location)
      except AttributeError:
         pass
      # add self._client._before, if self._client is a Rest:
      try:
         exec('result.extend(self._client.%s)' % location)
      except:
         pass
      return result

   def _getFormatCarriers(self):
      result = [ ]
      for value in self._client.__dict__.values( ):
         if isinstance(value, _FormatCarrier):
            result.append(value)
      result.sort(lambda x, y: cmp(x.__class__.__name__, y.__class__.__name__))
      return result
