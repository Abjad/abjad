from abjad.core import LilyPondTweakReservoir
from abjad.core import _UnaryComparator


class NoteHead(_UnaryComparator):
   r'''Abjad model of a note head:

   ::

      abjad> notetools.NoteHead(13)
      NoteHead("cs''")

   Note heads are immutable.
   '''

   __slots__ = ('_client', '_pitch', '_tweak')

   def __init__(self, *args):
      primary_args = [ ]
      tweak_pairs = [ ]
      for x in args:
         if isinstance(x, tuple) and len(x) == 2 and \
            isinstance(x[0], str) and isinstance(x[1], str):
            tweak_pairs.append(x)
         else:
            primary_args.append(x) 
      args = primary_args
      if len(args) == 1:
         _client = None
         pitch = args[0]
      elif len(args) == 2:
         _client, pitch = args
      else:
         raise ValueError('\n\tCan not initialize note head from args "%s".' % str(args))
      self._client = _client
      self.pitch = pitch
      ## must assign comparison attribute after pitch initialization ##
      self._comparison_attribute = self.pitch
      for tweak_pair in tweak_pairs:
         key, value = tweak_pair
         setattr(self.tweak, key, value)

   ## OVERLOADS ##

   def __copy__(self, *args):
      return type(self)(*self.__getnewargs__( ))

   __deepcopy__ = __copy__
      
   def __getnewargs__(self):
      args = [self.pitch]
      args.extend(self.tweak._get_attribute_pairs( ))
      return args

   def __repr__(self):
      args = [repr(self._format_string)]
      args.extend(self.tweak._get_attribute_pairs( ))
      args = ', '.join([str(x) for x in args])
      return '%s(%s)' % (self.__class__.__name__, args)

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
      
         abjad> note_head = notetools.NoteHead("cs''")
         abjad> note_head.format
         "cs'"
      '''
      from abjad.tools.notetools._format_note_head import _format_note_head
      return _format_note_head(self)

   @property
   def named_chromatic_pitch(self):
      '''Read-only named chromatic pitch equal to note head:

      ::

         abjad> note_head = notetools.NoteHead("cs''")
         abjad> note_head.named_chromatic_pitch
         NamedChromaticPitch("cs''")
      '''
      return self.pitch

   ## TODO: rename pitch as named pitch ##
   @apply
   def pitch( ):
      def fget(self):
         '''Get named pitch of note head::

            abjad> note_head = notetools.NoteHead("cs''")
            abjad> note_head.pitch
            NamedChromaticPitch("cs''")

         Set named pitch of note head::

            abjad> note_head = notetools.NoteHead("cs''")
            abjad> note_head.pitch = "d''"
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
      '''Read-only LilyPond tweak reservoir:

      ::

         abjad> note_head = notetools.NoteHead("cs''")
         abjad> note_head.tweak
         LilyPondTweakReservoir( )
      '''
      if not hasattr(self, '_tweak'):
         self._tweak = LilyPondTweakReservoir( )
      return self._tweak
