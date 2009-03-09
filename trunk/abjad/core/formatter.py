from abjad.core.formatcarrier import _FormatCarrier
from abjad.core.interface import _Interface


class _Formatter(_Interface):

   ## The 'number' attribute causes only leaf numbering but attaches
   ## to the core _Formatter so that containers can number leaves.
   def __init__(self, client):
      _Interface.__init__(self, client)
      self.after = [ ]
      self.before = [ ]
      self.number = False

   ## PRIVATE ATTRIBUTES ##
   
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

   @property
   def _knownFormatLocations(self):
      '''Output-ordered list of known format locations.'''
      result = ['_before', '_opening', '_closing', '_after']
      return result

   ## PRIVATE METHODS ##

   def _collectLocation(self, location):
      '''Collect all format contributions in a single Python list.'''
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
      return result

   def _collectLocationVerbose(self, location):
      '''Collect all format contributions as (interface, strings) pairs.'''
      result = [ ]
      for carrier in self._getFormatCarriers( ):
         try:
            exec('result.append((carrier, carrier.%s))' % location)
         except AttributeError:
            pass
      try:
         exec(
            'result.append((self._client.spanners, self._client.spanners.%s))' 
            % location)
      except AttributeError:
         pass
      return result

   def _getFormatCarriers(self):
      '''Get all format carriers attaching to client.'''
      result = [ ]
      client = self._client
      for value in client.__dict__.values( ):
         if isinstance(value, _FormatCarrier):
            result.append(value)
      result.sort(
         lambda x, y: cmp(x.__class__.__name__, y.__class__.__name__))
      return result

   def _revealFormatContributions(self):
      '''Return string comprising indented list of all format contributions.
         Contributions order first by location and then by interface.
         Debugging tool to find sources of different format contributions.'''
      result = ''
      formatLocations = self._knownFormatLocations
      for location in formatLocations:
         contributions = self._collectLocationVerbose(location)
         contributions = [x for x in contributions if x[1]]
         if contributions:
            result += location + '\n'
            for contribution in contributions:
               interface, strings = contribution
               result += '\t%s\n' % interface 
               for string in strings:
                  result += '\t\t%s\n' % string
      return result
