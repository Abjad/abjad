from abjad.core.interface import _Interface
from abjad.core.formatcarrier import _FormatCarrier


class _VoiceInterface(_Interface, _FormatCarrier):

   def __init__(self, client):
      _Interface.__init__(self, client)
      _FormatCarrier.__init__(self)
      self.number = None

   ## PUBLIC ATTRIBUTES ##

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
   def opening(self):
      '''String content, if any, this voice will write to the 
         'before' slot of its first leaf at format-time.'''
      result = [ ]
      voices = {
         1:r'\voiceOne', 2:r'\voiceTwo', 3:r'\voiceThree', 4:r'\voiceFour'}
      if self.number:
         result.append(voices[self.number])
      return result

