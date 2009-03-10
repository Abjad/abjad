from abjad.leaf.leaf import _Leaf
from abjad.notehead.notehead import NoteHead
from abjad.note.initializer import _NoteInitializer
from abjad.pitch.pitch import Pitch


class Note(_Leaf):
   
   def __init__(self, *args):
      self._initializer = _NoteInitializer(self, _Leaf, *args)

   ## OVERLOADS ##

   def __repr__(self):
      return 'Note(%s, %s)' % (self.pitch, self.duration._product)

   def __str__(self):
      return self._body

   ## PRIVATE ATTRIBUTES ##

   @property
   def _body(self):
      result = ''
      if self.pitch:
         result += str(self.pitch)
      result += str(self.duration._product)
      if self.stem.tremolo:
         result += ' :%s' % self.stem.tremolo
      return result 

   ## PUBLIC ATTRIBUTES ##

   @apply
   def notehead( ):
      def fget(self):
         return self._notehead
      def fset(self, arg):
         if isinstance(arg, type(None)):
            self._notehead = None
         elif isinstance(arg, (int, float, long)):
            self._notehead = NoteHead(pitch = arg)
            self._notehead._client = self
         elif isinstance(arg, Pitch):
            self._notehead = NoteHead(pitch = arg)
            self._notehead._client = self
         elif isinstance(arg, NoteHead):
            self._notehead = arg
            self._notehead._client = self
         else:
            print 'Can not bind %s to Note.notehead.' % arg
      return property(**locals( ))

   @property
   def pairs(self):
      if self.pitch:
         return (self.pitch.pair, )
      else:
         return ( )

   @apply
   def pitch( ):
      def fget(self):
         if self.notehead is not None:
            return self._notehead.pitch
         else:
            return None
      def fset(self, arg):
         if arg is None:
            if self.notehead is not None:
               self.notehead.pitch = None
         else:
            if self.notehead is None:
               self.notehead = NoteHead(pitch = None)
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
      if self.pitch:
         return (self.pitch, )
      else:
         return ( )
