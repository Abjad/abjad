from .. core.formatter import _Formatter
from .. core.interface import _Interface

class _LeafFormatter(_Formatter):

   def __init__(self, client):
      _Formatter.__init__(self, client)

   def _getInterfaces(self):
      result = [ ]
      for value in self._client.__dict__.values( ):
         if isinstance(value, _Interface):
            result.append(value)
      result.sort(lambda x, y: cmp(x.__class__.__name__, y.__class__.__name__))
      return result

   def _collectLocation(self, location):
      result = [ ]
      for interface in self._getInterfaces( ):
         try:
            exec('result.extend(interface.%s)' % location)
         except AttributeError:
            pass
      exec('result.extend(self._client.spanners.%s)' % location)
      return result

   @property
   def _number(self):
      result = [ ]
      if self.number or self._client._parentage._number:
         result.append(r'^ \markup { %s }' % self._client.number)
      return result

   @property
   def _grace(self):
      result = [ ]
      grace = self._client.grace.before
      if grace:
         result.append(grace.format)
      return result

   @property
   def _agrace_opening(self):
      if self._client.grace.after:
         return [r'\afterGrace']
      else:
         return [ ] 

   @property
   def _agrace(self):
      result = [ ]
      agrace = self._client.grace.after
      if agrace:
         result.append(agrace.format)
      return result

   @property
   def _body(self):
      result = [ ]
      result.extend(self.left)
      result.extend(self._collectLocation('_left'))
      if hasattr(self._client, 'notehead') and \
         self._client.notehead is not None:
         result.extend(self._client.notehead._formatter.left)
      result.append(self._client._body)
      result.extend(self._client.tremolo.body)
      result.extend(self._collectLocation('_right'))
      result.extend(self.right)
      result.extend(self._number)
      result.extend(self._client.comments._right)
      return [' '.join(result)]

   @property
   def _clef(self):
      result = [ ]
      if hasattr(self._client, '_clef'):
         result.append(self._client._clef.format)
      return result

   ### NOTE - clef *must* come lexically before set-octavation ###

   @property
   def lily(self):
      result = [ ]
      result.extend(self._client.comments._before)
      result.extend(self.before)
      result.extend(self._grace)
      result.extend(self._clef)
      result.extend(self._collectLocation('_before'))
      result.extend(self._agrace_opening)
      result.extend(self._body)
      result.extend(self._agrace)
      result.extend(self._collectLocation('_after'))
      result.extend(self._after)
      result.extend(self.after)
      result.extend(self._client.comments._after)
      return '\n'.join(result)

   def _clone(self, client):
      result = _LeafFormatter(client)  
      for key, value in self.__dict__.items( ):
         if key is not '_client':
            setattr(result, key, deepcopy(value))
      return result
