from .. leaf.leaf import Leaf
from .. notehead.notehead import NoteHead
from initializer import NoteInitializer
from .. pitch.pitch import Pitch

class Note(Leaf):
   
   def __init__(self, *args):
      self.initializer = NoteInitializer(self, Leaf, *args)

   ### REPR ###

   def __repr__(self):
      return 'Note(%s, %s)' % (self.pitch, self.duration._product)

   def __str__(self):
      return self._body

   ### PROPERTIES ###

   @apply
   def pitch( ):
      def fget(self):
         if self.notehead != None:
            return self._notehead.pitch
         else:
            return None
      def fset(self, arg):
         if arg is None:
            if  self.notehead is not None:
               self.notehead.pitch = None
         else:
            if self.notehead is None:
               self.notehead = NoteHead(self)
            if isinstance(arg, (int, float, long)):
               self.notehead.pitch = Pitch(arg)
            elif isinstance(arg, tuple):
               self.notehead.pitch = Pitch(*arg)
            elif isinstance(arg, Pitch):
               self.notehead.pitch = arg
            else:
               raise ValueError('Can not set Note.pitch from %s' % str(arg))
      return property(**locals( ))

   @apply
   def notehead( ):
      def fget(self):
         return self._notehead
      def fset(self, arg):
         if isinstance(arg, type(None)):
            self._notehead = None
         elif isinstance(arg, (int, float, long)):
            self._notehead = NoteHead(self, pitch = arg)
         elif isinstance(arg, Pitch):
            self._notehead = NoteHead(self, pitch = arg)
         elif isinstance(arg, NoteHead):
            self._notehead = arg
            self._notehead._client = self
         else:
            print 'Can not bind %s to Note.notehead.' % arg
      return property(**locals( ))

   ### FORMATTING ###

   @property
   def _body(self):
      result = ''
      if self.pitch:
         result += str(self.pitch)
      result += str(self.duration._product)
      if self.stem.tremolo:
         result += ' :%s' % self.stem.tremolo
      return result 
