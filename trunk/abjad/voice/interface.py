from abjad.core.interface import _Interface
from abjad.core.formatcarrier import _FormatCarrier

'''
   Every Abjad component aggregates a _VoiceInterface.
   The primary purpose of the _VoiceInterface is to resolve
   and publish the 'voice signature' of any Abjad component,
   usually as t.voice.signature for any component t.

   The idea of the 'voice signature' derives from a related
   idea of a 'governing voice' which, in turn, derives
   from the idea of 'governing' in general.

   We say that some voice v governs component t if
   v is the first voice in the parentage of t,
   as we read the parentage of t from t towards score root.

   There's another idea of the 'signator', too, which will
   need further explanation later.

   TODO: It might be nice to use the _MarkupInterface to
         allow for the labelling of voice id in the PDF
         output of the score.
'''

class _VoiceInterface(_Interface, _FormatCarrier):

   def __init__(self, client):
      _Interface.__init__(self, client)
      _FormatCarrier.__init__(self)
      ## TODO: Is _VoiceInterface._defaultSignature dead code?
      self._defaultSignature = (0, )
      self.number = None

   ## PRIVATE ATTRIBUTES ##

   ## TODO: Combine _opening and _before in many interfaces
   @property
   def _before(self):
      '''String content, if any, this voice will write to the 
         'before' slot of its first leaf at format-time.'''
      result = [ ]
      voices = {
         1:r'\voiceOne', 2:r'\voiceTwo', 3:r'\voiceThree', 4:r'\voiceFour'}
      if self.number:
         result.append(voices[self.number])
      return result

   @property
   def _naiveSignature(self):
      '''Naive signature of this voice used to distinguish
         this voice from all other runtime objects.'''
      client = self._client
      if hasattr(client, 'invocation'):
         name = client.invocation.name
         if name is not None:
            return (name, )
      return (id(client), )

   ## TODO: Combine _opening and _before in many interfaces
   @property
   def _opening(self):
      '''String content, if any, this voice will write to its own
         'opening' slot at format-time.'''
      return self._before

   ## PUBLIC ATTRIBUTES ##

   @property
   def anonymous(self):
      '''True when this voice is not named, otherwise False.'''
      return not self.named

   @property
   def default(self):
      '''TODO: Is _VoiceInterface.default dead code?'''
      return self.signature == self._defaultSignature
   
   @property
   def name(self):
      '''String name of context from which client voice signature derives,
         otherwise None.'''
      if self.named:
         return self.signature[0]
      else:
         return None

   @apply
   def number( ):
      '''LilyPond voice number 1 - 4 of this voice, or None.'''
      def fget(self):
         return self._number
      def fset(self, arg):
         if not arg in (1, 2, 3, 4, None):
            raise ValueError('Voice number must be 1, 2, 3, 4 or None.')
         self._number = arg
      return property(**locals( ))

   @property
   def named(self):
      '''True when voice signature first is string,
         otherwise False.'''
      return isinstance(self.signature[0], str)
   
   @property
   def numeric(self):
      '''True when voice signature fist element is numeric, 
         otherwise False.'''
      first = self.signature[0]
      return isinstance(first, (int, long)) 

   @property
   def signature(self):
      '''Return unique (id, ) 1-tuple of voice that governs client.
         TODO: Can't the implementation here be greatly simplified?
         TODO: Shouldn't this implement in _Parentage instead?

         Notes:

            * orphan leaves carry no voice signature
            * incorporated but noncontext leaves carry default voice'''
      from abjad.leaf.leaf import _Leaf
      from abjad.context.context import _Context
      parentage = self._client.parentage.parentage
      found_lilypond_expression = False
      signator = None
      for i, p in enumerate(parentage):
         if isinstance(p, _Leaf):
            signator = p
         elif isinstance(p, _Context) and not getattr(p, 'parallel', False):
            found_lilypond_expression = True
            return p.voice._naiveSignature 
         elif isinstance(p, _Context) and getattr(p, 'parallel', False):
            found_lilypond_expression = True
            if parentage.index(p) == 0:
               return p.voice._naiveSignature
            else:
               return parentage[i - 1].voice._naiveSignature
         elif not isinstance(p, _Context) and not getattr(p, 'parallel', False):
            found_lilypond_expression = True
            signator = p
         elif not isinstance(p, _Context) and getattr(p, 'parallel', False):
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
