from abjad.leaf import _Leaf
from abjad.notehead import NoteHead
from abjad.note.initializer import _NoteInitializer
from abjad.pitch import Pitch


class Note(_Leaf):
   '''The `Abjad` model of a single note.'''
   
   def __init__(self, *args):
      self._initializer = _NoteInitializer(self, _Leaf, *args)

   ## OVERLOADS ##

   def __repr__(self):
      return 'Note(%s, %s)' % (self.pitch, self.duration._product)

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
      result += str(self.duration._product)
      return [result] 

   @apply
   def note_head( ):
      def fget(self):
         '''Read / write reference to `Abjad` note_head instance.'''
         return self._note_head
      def fset(self, arg):
         if isinstance(arg, type(None)):
            self._note_head = None
         elif isinstance(arg, (int, float, long)):
            self._note_head = NoteHead(self, pitch = arg)
         elif isinstance(arg, tuple) and len(arg) == 2:
            pitch = Pitch(*arg)
            self._note_head = NoteHead(self, pitch = pitch)
         elif isinstance(arg, Pitch):
            self._note_head = NoteHead(self, pitch = arg)
         elif isinstance(arg, NoteHead):
            self._note_head = arg
         else:
            print 'Can not bind %s to Note.note_head.' % arg
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
         if arg is None:
            if self.note_head is not None:
               self.note_head.pitch = None
         else:
            if self.note_head is None:
               self.note_head = NoteHead(self, pitch = None)
            if isinstance(arg, (int, float, long)):
               self.note_head.pitch = Pitch(arg)
            elif isinstance(arg, tuple):
               self.note_head.pitch = Pitch(*arg)
            elif isinstance(arg, Pitch):
               self.note_head.pitch = arg
            else:
               raise ValueError('Can not set Note.pitch from %s' % str(arg))
      return property(**locals( ))

   @property
   def pitches(self):
      '''Read-only one-tuple of pitch of note.'''
      if self.pitch:
         return (self.pitch, )
      else:
         return ( )
