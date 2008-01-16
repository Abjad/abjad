from .. leaf.leaf import Leaf
from caster import NoteCaster
from .. notehead.notehead import NoteHead
from .. pitch.pitch import Pitch

class Note(Leaf):
   
   def __init__(self, pitch = None, 
      duration = None, multiplier = None, notehead = None):
      Leaf.__init__(self, duration = duration, multiplier = multiplier)
      self.caster = NoteCaster(self)
      self.notehead = notehead
      self.pitch = pitch

   ### REPR ###

   def __repr__(self):
      if self.pitch and self._product:
         return 'Note(%s, %s)' % (self.pitch, self._product)
      elif self.pitch:
         return 'Note(%s)' % self.pitch
      elif self._product:
         return 'Note(%s)' % self._product
      else:
         return 'Note( )'

   def __str__(self):
      return self._body

   ### PROPERTIES ###

   @apply
   def pitch( ):
      def fget(self):
         if self.notehead:
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
      if self.pitch and self._product:
         return '%s%s' % (self.pitch, self._product)
      elif self.pitch:
         return str(self.pitch)
      elif self._product:
         return str(self._product)
      else:
         return ''
