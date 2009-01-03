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

   ### TODO - reimplement _getFormatCarriers( ) in terms of a 
   ###        special type of 'attribute traversal'. Ie, not
   ###        a traversal of the score hierarchy (which _Navigator
   ###        currently implements just fine) but instead a 
   ###        traversal of all the attributes of client.
   ###        The loop in _getFormatCarriers( ) which iterates over
   ###        the attribute dictionary of client is a naive
   ###        attempt at this type of traversal; we will need
   ###        to recursively iterate over the attribute dictionary
   ###        of each attribute in the attribute dictionary.

   def _getFormatCarriers(self):
      result = [ ]
      client = self._client
      if isinstance(client, _FormatCarrier):
         result.append(client)
      for value in client.__dict__.values( ):
         if isinstance(value, _FormatCarrier):
            result.append(value)
         # these two lines are a hack:
         # _Accidental is a _GrobHandler ... 
         # so how do we best make this loop find _Accidental?
         if hasattr(value, 'pitch'):
            result.append(value.pitch.accidental)
#         if client.kind('_Leaf'):
#            for spanner in client.spanners._spannersInParentage:
#               if isinstance(spanner, _FormatCarrier):
#                  result.append(value)
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
