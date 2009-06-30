from abjad.leaf.leaf import _Leaf
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

   def __str__(self):
      return self.body[0]

   ## PUBLIC ATTRIBUTES ##

   @property
   def body(self):
      '''Read-only list of string representation of body of note.
      Picked up as format contribution at format-time.'''
      result = ''
      if self.pitch:
         result += str(self.pitch)
      result += str(self.duration._product)
      return [result] 

   @apply
   def notehead( ):
      def fget(self):
         '''Read / write reference to `Abjad` notehead instance.'''
         return self._notehead
      def fset(self, arg):
         if isinstance(arg, type(None)):
            self._notehead = None
         elif isinstance(arg, (int, float, long)):
            self._notehead = NoteHead(self, pitch = arg)
         elif isinstance(arg, tuple) and len(arg) == 2:
            pitch = Pitch(*arg)
            self._notehead = NoteHead(self, pitch = pitch)
         elif isinstance(arg, Pitch):
            self._notehead = NoteHead(self, pitch = arg)
         elif isinstance(arg, NoteHead):
            self._notehead = arg
         else:
            print 'Can not bind %s to Note.notehead.' % arg
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
         if self.notehead is not None and hasattr(self.notehead, 'pitch'):
            return self._notehead.pitch
         else:
            return None
      def fset(self, arg):
         if arg is None:
            if self.notehead is not None:
               self.notehead.pitch = None
         else:
            if self.notehead is None:
               self.notehead = NoteHead(self, pitch = None)
            if isinstance(arg, (int, float, long)):
               self.notehead.pitch = Pitch(arg)
            elif isinstance(arg, tuple):
               self.notehead.pitch = Pitch(*arg)
            elif isinstance(arg, Pitch):
               self.notehead.pitch = arg
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
