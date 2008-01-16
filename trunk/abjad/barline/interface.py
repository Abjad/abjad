from .. core.interface import _Interface

class BarLineInterface(_Interface):
   
   def __init__(self, client):
      _Interface.__init__(self, client, 'BarLine')
      self.type = None
      
   ### REPR ###

   def __repr__(self):
      if self.isSet( ):
         return 'BarLineInterface(%s)' % len(self)
      else:
         return 'BarLineInterface( )' 

   ### FORMATTING ###

   _barlineNameToLilyPondSymbol = {
      'final'  : '|.',
      'double' : '||',
      'single' : '|',
   }

   def _barlineNameToLilyPondString(self, barlineName):
      LPSymbol = self._barlineNameToLilyPondSymbol[barlineName]
      return r'\bar "%s"' % LPSymbol

   @property
   def _after(self):
      result = [ ]
      if self._client.kind('Leaf'):
         if self.type:
            result.append(self._barlineNameToLilyPondString(self.type))
      return result

   @property
   def _closing(self):
      result = [ ]
      if self._client.kind('Container'):
         if self.type:
            result.append(self._barlineNameToLilyPondString(self.type))
      result = ['\t' + x for x in result]
      return result
