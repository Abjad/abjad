from abjad.core.formatcontributor import _FormatContributor
from abjad.core.interface import _Interface


class _VoiceInterface(_Interface, _FormatContributor):
   '''Publish LilyPond voice-number settings.
      Handle no LilyPond grob.'''

   def __init__(self, _client):
      '''Bind to client and set voice number to None.'''
      _Interface.__init__(self, _client)
      _FormatContributor.__init__(self)
      self.number = None

   ## PUBLIC ATTRIBUTES ##

   @property
   def explicit(self):
      '''First explicit *Abjad* ``Voice`` in parenage of client.
         If no explicit *Abjad* ``Voice``, return ``None``.'''
      from abjad.voice.voice import Voice
      for parent in self._client.parentage.parentage:
         if isinstance(parent, Voice):
            return parent

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
      '''Format contribution at container opening or before leaf.'''
      result = [ ]
      voices = {
         1:r'\voiceOne', 2:r'\voiceTwo', 3:r'\voiceThree', 4:r'\voiceFour'}
      if self.number:
         result.append(voices[self.number])
      return result
