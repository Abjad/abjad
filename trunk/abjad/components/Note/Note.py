from abjad.components._Leaf import _Leaf
from abjad.components.NoteHead import NoteHead
from abjad.components.Note._NoteInitializer import _NoteInitializer


class Note(_Leaf):
   '''The Abjad model of a single note.'''
   
   def __init__(self, *args):
      self._initializer = _NoteInitializer(self, _Leaf, *args)

   ## OVERLOADS ##

   def __len__(self):
      if self.pitch is None:
         return 0
      else:
         return 1

   def __repr__(self):
      return 'Note(%s, %s)' % (self.pitch, self.duration)

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
         if isinstance(arg, type(None)):
            self._note_head = None
#         elif isinstance(arg, (int, float, long)):
#            self._note_head = NoteHead(self, pitch = arg)
#         elif isinstance(arg, tuple) and len(arg) == 2:
#            pitch = pitchtools.NamedPitch(*arg)
#            self._note_head = NoteHead(self, pitch = pitch)
#         elif isinstance(arg, NamedPitch):
#            self._note_head = NoteHead(self, pitch = arg)
         elif isinstance(arg, NoteHead):
            self._note_head = arg
#         else:
#            print 'Can not bind %s to Note.note_head.' % arg
         else:
            note_head = NoteHead(self, pitch = arg)
            self._note_head = note_head
      return property(**locals( ))

   @property
   def numbers(self):
      '''Read-only sorted tuple of pitch number of note, if any.'''
      if self.pitch:
         return (self.pitch.number, )
      else:
         return ( )

   @property
   def pairs(self):
      '''Read-only pair of pitch of note.'''
      if self.pitch:
         return (self.pitch.pair, )
      else:
         return ( )

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

   @property
   def pitches(self):
      '''Read-only one-tuple of pitch of note.'''
      if self.pitch:
         return (self.pitch, )
      else:
         return ( )
