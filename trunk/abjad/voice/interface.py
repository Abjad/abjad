from abjad.core.interface import _Interface
from abjad.core.formatcarrier import _FormatCarrier


class _VoiceInterface(_Interface, _FormatCarrier):

   def __init__(self, client):
      _Interface.__init__(self, client)
      _FormatCarrier.__init__(self)
      self._defaultSignature = (0, )
      self.number = None

   ## PRIVATE ATTRIBUTES ##

   @property
   def _before(self):
      result = [ ]
      voices = {
         1:r'\voiceOne', 2:r'\voiceTwo', 3:r'\voiceThree', 4:r'\voiceFour'}
      if self.number:
         result.append(voices[self.number])
      return result

   @property
   def _naiveSignature(self):
      if hasattr(self._client, 'invocation'):
         if self._client.invocation.name is not None:
            return (self._client.invocation.name, )
      return (id(self._client), )

   ## this aliasing follows the method found in the TempoInterface 
   ## and the ClefInterface.
   @property
   def _opening(self):
      return self._before

   ## PUBLIC ATTRIBUTES ##

   @property
   def anonymous(self):
      return not self.named

   @property
   def default(self):
      return self.signature == self._defaultSignature
   
   @property
   def name(self):
      if self.named:
         return self.signature[0]
      else:
         return None

   @apply
   def number( ):
      def fget(self):
         return self._number
      def fset(self, arg):
         if not arg in (1, 2, 3, 4, None):
            raise ValueError('Voice number must be 1, 2, 3, 4 or None.')
         self._number = arg
      return property(**locals( ))

   @property
   def named(self):
      return isinstance(self.signature[0], str)
   
   @property
   def numeric(self):
      first = self.signature[0]
      return isinstance(first, (int, long)) 

   @property
   def signature(self):
      parentage = self._client.parentage.parentage
      found_lilypond_expression = False
      signator = None
      for i, p in enumerate(parentage):
         if p.kind('_Leaf'):
            signator = p
         elif p.kind('_Context') and not getattr(p, 'parallel', False):
            found_lilypond_expression = True
            return p.voice._naiveSignature 
         elif p.kind('_Context') and getattr(p, 'parallel', False):
            found_lilypond_expression = True
            if parentage.index(p) == 0:
               return p.voice._naiveSignature
            else:
               return parentage[i - 1].voice._naiveSignature
         elif not p.kind('_Conext') and not getattr(p, 'parallel', False):
            found_lilypond_expression = True
            signator = p
         elif not p.kind('_Context') and getattr(p, 'parallel', False):
            found_lilypond_expression = True
            if p.parentage.orphan:
               if parentage.index(p) == 0:
                  return self._defaultSignature
               else:
                  return parentage[i - 1].voice._naiveSignature
            else:
               signator = p
         else:
            found_lilypond_expression = True
            raise ValueError('%s is unknown container.' % p)
      if found_lilypond_expression:
         return self._defaultSignature
      else:
         return None
