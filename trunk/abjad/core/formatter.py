from abjad.core.formatcarrier import _FormatCarrier
from abjad.core.interface import _Interface


class _Formatter(_Interface):

   def __init__(self, client):
      _Interface.__init__(self, client)
      self.number = False
      self.before = [ ]
      self.after = [ ]

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
         # these two lines are a hack:
         # _Accidental is a _GrobHandler ... 
         # so how do we best make this loop find _Accidental?
         if hasattr(value, 'pitch'):
            result.append(value.pitch.accidental)
      result.sort(lambda x, y: cmp(x.__class__.__name__, y.__class__.__name__))
      return result

   @property
   def _grobOverrides(self):
      result = [ ]
      for carrier in self._getFormatCarriers( ):
         try:
            result.extend(carrier._grobOverrides)
         except AttributeError:
            pass
      try:
         result.extend(self._client.spanners._grobOverrides)
      except AttributeError:
         pass
      return result

   @property
   def _grobReverts(self):
      result = [ ]
      for carrier in self._getFormatCarriers( ):
         try:
            result.extend(carrier._grobReverts)
         except AttributeError:
            pass
      try:
         result.extend(self._client.spanners._grobReverts)
      except AttributeError:
         pass
      return result
