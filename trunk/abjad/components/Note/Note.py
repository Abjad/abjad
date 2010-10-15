from abjad.components._Leaf import _Leaf


class Note(_Leaf):
   '''The Abjad model of a note:

   ::

      abjad> Note(13, (3, 16))
      Note("cs''8.")
   '''

   ## TODO: remove _note_heads attribute after removing casting code ##
   #__slots__ = ('_note_head', '_note_heads', '_pitch', )
   
   def __init__(self, *args, **kwargs):
      from abjad.tools.notetools._initialize_note import _initialize_note
      #written_duration, pitch = (1, 4), 0
      #if isinstance(args[0], Note):
      if False:
         note = args[0]
         written_duration, pitch = note.duration.written, note.pitch
      else:
         _initialize_note(self, _Leaf, *args)
      self._initialize_keyword_values(**kwargs)

   ## OVERLOADS ##

   def __eq__(self, arg):
      if _Leaf.__eq__(self, arg):
         if self.pitch == arg.pitch:
            return True
      return False

   #def __repr__(self):
   #   return '%s(%s)' % (self.__class__.__name__, repr(self._compact_representation))

   ## PRIVATE ATTRIBUTES ##

   @property
   def _body(self):
      result = ''
      if self.pitch:
         result += str(self.pitch)
      result += str(self.duration)
      return [result] 

   @property
   def _compact_representation(self):
      return self._body[0]

   ## PUBLIC ATTRIBUTES ##

   @apply
   def note_head( ):
      def fget(self):
         '''Get note head of note::

            abjad> note = Note(13, (3, 16))
            abjad> note.note_head
            NoteHead("cs''")

         Set note head of note::

            abjad> note = Note(13, (3, 16))
            abjad> note.note_head = 14
            abjad> note
            Note("d''8.")
         '''
         return self._note_head
      def fset(self, arg):
         from abjad.tools.notetools.NoteHead import NoteHead
         if isinstance(arg, type(None)):
            self._note_head = None
         elif isinstance(arg, NoteHead):
            self._note_head = arg
         else:
            note_head = NoteHead(self, arg)
            self._note_head = note_head
      return property(**locals( ))

   @apply
   def pitch( ):
      def fget(self):
         '''Get named pitch of note::

            abjad> note = Note(13, (3, 16))
            abjad> note.pitch
            NamedChromaticPitch("cs''")

         Set named pitch of note::

            abjad> note = Note(13, (3, 16))
            abjad> note.pitch = 14
            abjad> note
            Note("d''8.")
         '''
         if self.note_head is not None and hasattr(self.note_head, 'pitch'):
            return self._note_head.pitch
         else:
            return None
      def fset(self, arg):
         from abjad.tools import pitchtools
         from abjad.tools.notetools.NoteHead import NoteHead
         if arg is None:
            if self.note_head is not None:
               self.note_head.pitch = None
         else:
            if self.note_head is None:
               self.note_head = NoteHead(self, pitch = None)
            else:
               pitch = pitchtools.NamedChromaticPitch(arg)
               self.note_head.pitch = pitch
      return property(**locals( ))
