from abjad.core import LilyPondTweakReservoir


class NoteHead(object):
   r'''The Abjad model of a note head:

   ::

      abjad> notetools.NoteHead(13)
      NoteHead("cs''")
   '''

   __slots__ = ('_client', '_pitch', '_tweak')

   def __init__(self, *args):
      if len(args) == 1:
         _client = None
         pitch = args[0]
      elif len(args) == 2:
         _client, pitch = args
      else:
         raise ValueError('\n\tCan not initialize note head from args: "%s".' % str(args))
      self._client = _client
      self.pitch = pitch

   ## OVERLOADS ##

   def __eq__(self, expr):
      if isinstance(expr, type(self)):
         if self.pitch == expr.pitch:
            return True
      return False

   def __ne__(self, expr):
      return not self == expr

   def __repr__(self):
      return '%s(%s)' % (self.__class__.__name__, repr(self._format_string))

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
      '''Read-only LilyPond input format of note head:

      ::
      
         abjad> note = Note(1, (1, 4))
         abjad> note.note_head.format
         "cs'"
      '''
      from abjad.tools.notetools._format_note_head import _format_note_head
      return _format_note_head(self)

   @property
   def named_chromatic_pitch(self):
      return self.pitch

   ## TODO: rename pitch as named pitch ##
   @apply
   def pitch( ):
      def fget(self):
         '''Get named pitch of note head::

            abjad> note_head = notetools.NoteHead(13)
            abjad> note_head.pitch
            NamedChromaticPitch("cs''")

         Set named pitch of note head::

            abjad> note_head = notetools.NoteHead(13)
            abjad> note_head.pitch = 14
            abjad> note_head.pitch
            NamedChromaticPitch("d''")
         '''
         return self._pitch
      def fset(self, arg):
         from abjad.tools import pitchtools
         pitch = pitchtools.NamedChromaticPitch(arg)
         self._pitch = pitch
      return property(**locals( ))

   @property
   def tweak(self):
      '''Read-only reference to LilyPond tweak reservoir.
      '''
      if not hasattr(self, '_tweak'):
         self._tweak = LilyPondTweakReservoir( )
      return self._tweak
