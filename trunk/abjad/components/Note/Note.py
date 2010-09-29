from abjad.components._Leaf import _Leaf


class Note(_Leaf):
   '''The Abjad model of a note.
   '''
   
   def __init__(self, *args, **kwargs):
      from abjad.tools.notetools._initialize_note import _initialize_note
      _initialize_note(self, _Leaf, *args)
      self._initialize_keyword_values(**kwargs)

   ## OVERLOADS ##

   def __eq__(self, arg):
      if isinstance(arg, type(self)):
         if self.duration.written == arg.duration.written:
            if self.duration.multiplier == arg.duration.multiplier:
               if self.pitch == arg.pitch:
                  return True
      return False

   def __len__(self):
      if self.pitch is None:
         return 0
      else:
         return 1

   def __repr__(self):
      return '%s(%s, %s)' % (self.__class__.__name__, self.pitch, self.duration)

   ## PRIVATE ATTRIBUTES ##

   @property
   def _compact_representation(self):
      return self._body[0]

   ## PUBLIC ATTRIBUTES ##

   @property
   def _body(self):
      '''Read-only list of string representation of body of note.
      Picked up as format contribution at format-time.'''
      result = ''
      if self.pitch:
         result += str(self.pitch)
      result += str(self.duration)
      return [result] 

   @apply
   def note_head( ):
      def fget(self):
         '''Read / write reference to Abjad note_head instance.'''
         return self._note_head
      def fset(self, arg):
         from abjad.tools.notetools.NoteHead import NoteHead
         if isinstance(arg, type(None)):
            self._note_head = None
         elif isinstance(arg, NoteHead):
            self._note_head = arg
         else:
            note_head = NoteHead(self, pitch = arg)
            self._note_head = note_head
      return property(**locals( ))

#   @property
#   def numbers(self):
#      '''Read-only sorted tuple of pitch number of note, if any.'''
#      if self.pitch:
#         return (self.pitch.number, )
#      else:
#         return ( )

   @apply
   def pitch( ):
      def fget(self):
         '''Read / write pitch of note.'''
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
               pitch = pitchtools.NamedPitch(arg)
               self.note_head.pitch = pitch
      return property(**locals( ))
