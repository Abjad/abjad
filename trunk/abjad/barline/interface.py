from abjad.core.attributeformatter import _AttributeFormatter
from abjad.core.interface import _Interface

class _BarLineInterface(_Interface, _AttributeFormatter):
   
   def __init__(self, client):
      _Interface.__init__(self, client)
      _AttributeFormatter.__init__(self, 'BarLine')
      self._type = None
      
   ### MANAGED ###
   # TODO: should we check validity of input and reject invalid barline types?

   @apply
   def type( ):
      def fget(self):
         return self._type
      def fset(self, expr):
         self._type = expr
      return property(**locals())

   ### FORMATTING ###

   _barlineNameToLilyPondSymbol = {
      '|' : '|'   , 'single' : '|',
      '||' : '||' , 'double' : '||',
      '.|' :'.|'  , 'thickthin' : '.|',
      '.|.':'.|.' , 'doublethick' : '.|.',
      '|.' : '|.' , 'final'  : '|.',
      ':' : ':'   , 'dotted' : ':',
      'dashed':'dashed',
      '|:' : '|:' , 'repeatopen' : '|:',
      ':|:':':|:' , 'repeatopenclose' : ':|:',
      ':|' : ':|' , 'repeatclose' : ':|',
      '' : ''     , 'invisible' : '',
   }

   def _barlineNameToLilyPondString(self, barlineName):
      LPSymbol = self._barlineNameToLilyPondSymbol[barlineName]
      return r'\bar "%s"' % LPSymbol

   @property
   def _after(self):
      result = [ ]
      if self._client.kind('_Leaf'):
         if self.type is not None:
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
