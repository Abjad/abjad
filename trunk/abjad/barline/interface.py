from .. core.interface import _Interface

class BarLineInterface(_Interface):
   
   def __init__(self, client):
      _Interface.__init__(self, client, 'BarLine', ['BarLine'])
      self._type = None
      
   ### MANAGED ###

   @apply
   def type( ):
      def fget(self):
         return self._type
      def fset(self, expr):
         self._type = expr
      return property(**locals())

   ### FORMATTING ###

   ### TODO - accept either 'double' or '||' equivalently, etc. ###

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
