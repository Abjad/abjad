from abjad.core.formatcontributor import _FormatContributor
from abjad.interfaces.interface.interface import _Interface


class VoiceInterface(_Interface, _FormatContributor):
   '''Manage *LilyPond* and *Abjad* voice settings.
   
      ::

         abjad> t = Voice(macros.scale(4))
         abjad> t[0].voice      
         <VoiceInterface>'''

   def __init__(self, _client):
      '''Bind to ``_client``, register as ``_FormatContributor`` 
         and set ``number`` to ``None``.'''

      _Interface.__init__(self, _client)
      _FormatContributor.__init__(self)
      self.number = None

   ## PUBLIC ATTRIBUTES ##

   @property
   def explicit(self):
      '''Read-only reference to first \
         *Abjad* :class:`Voice <abjad.voice.voice.Voice>` \
         in parentage of client.

         * If no explicit *Abjad* \
            :class:`Voice <abjad.voice.voice.Voice>` \
            in parentage of client, return ``None``.

         ::

            abjad> t.voice.explicit
            Voice{4}'''

      from abjad.voice import Voice
      for parent in self._client.parentage.parentage:
         if isinstance(parent, Voice):
            return parent

   @apply
   def number( ):
      def fget(self):
         r'''Read / write *LilyPond* number of this voice.

            * Default value: ``None``.
            * Allowed values: ``1``, ``2``, ``3``, ``4``, ``None``.

            ::

               abjad> t.voice.number = 1
               abjad> t.voice.number
               1
               abjad> print t.format
               \new Voice {
                       \voiceOne
                       c'8
                       d'8
                       e'8
                       f'8
               }'''

         return self._number
      def fset(self, arg):
         if not arg in (1, 2, 3, 4, None):
            raise ValueError('Voice number must be 1, 2, 3, 4 or None.')
         self._number = arg
      return property(**locals( ))

   @property
   def _opening(self):
      '''Read-only format contribution at container opening or before leaf.

         * Derived from ``VoiceInterface.number``.

         ::

            abjad> t.voice.number = 1
            abjad> t.voice.opening
            ['\\voiceOne']'''

      result = [ ]
      voices = {
         1:r'\voiceOne', 2:r'\voiceTwo', 3:r'\voiceThree', 4:r'\voiceFour'}
      if self.number:
         result.append(voices[self.number])
      return result
