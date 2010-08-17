from abjad.components.NoteHead._NoteHeadFormatInterface import _NoteHeadFormatInterface
from abjad.core import LilyPondTweakReservoir


class NoteHead(object):
   r'''Note or chord note head:

   ::

      abjad> note = Note(1, (1, 4))
      abjad> note.note_head
      NoteHead(cs')
   '''

   __slots__ = ('_client', '_formatter', '_pitch', 'tweak')

   def __init__(self, client, pitch = None):
      self._client = client
      self.tweak = LilyPondTweakReservoir( )
      self._formatter = _NoteHeadFormatInterface(self)
      self.pitch = pitch

   ## OVERLOADS ##

   def __eq__(self, expr):
      if isinstance(expr, NoteHead):
         if self.pitch == expr.pitch:
            return True
      return False

   def __ne__(self, expr):
      return not self == expr

   def __repr__(self):
      return '%s(%s)' % (self.__class__.__name__, self._format_string)

   def __str__(self):
      if self.pitch:
         return str(self.pitch)
      else:
         return ''

   ## PRIVATE ATTRIBUTES ##

   @property
   def _format_string(self):
      if self.pitch:
         return str(self.pitch)
      return ' '

   ## PUBLIC ATTRIBUTES ##

   @property
   def format(self):
      '''Read-only format string of note_head.

      .. todo:: appears to not currently be working, or necessary.

      ::
      
         abjad> note = Note(1, (1, 4))
         abjad> note.nothead.format
         "cs'"
      '''
      return self._formatter.format

   @apply
   def pitch( ):
      def fget(self):
         '''Read / write pitch of note_head.

         ::

            abjad> note = Note(1, (1, 4))
            abjad> note.note_head.pitch = 2
            abjad> print note.format
            d'4
         '''
         return self._pitch
      def fset(self, arg):
         from abjad.tools import pitchtools
         if arg is None:
            self._pitch = None
         elif isinstance(arg, NoteHead):
            self._pitch = arg.pitch
         else:
            pitch = pitchtools.NamedPitch(arg)
            self._pitch = pitch
      return property(**locals( ))
