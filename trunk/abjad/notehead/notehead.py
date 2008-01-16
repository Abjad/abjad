from formatter import NoteHeadFormatter
from .. pitch.pitch import Pitch

class NoteHead(object):

   def __init__(self, client, pitch = None, style = None, 
      transparent = None):
      self._client = client
      self.formatter = NoteHeadFormatter(self)
      self.pitch = pitch
      self.style = style
      self.transparent = transparent

   ### REPR ###

   def __repr__(self):
      if self.pitch:
         return 'NoteHead(%s)' % self.pitch
      else:
         return 'NoteHead( )'

   def __str__(self):
      if self.pitch:
         return str(self.pitch)
      else:
         return ''

   ### PROPERTIES ###

   @apply
   def pitch( ):
      def fget(self):
         return self._pitch
      def fset(self, arg):
         if arg is None:
            self._pitch = None
         elif isinstance(arg, Pitch):
            self._pitch = arg
         elif isinstance(arg, (int, float, long)):
            self._pitch = Pitch(arg)
         else:
            raise ValueError('Can not set NoteHead.pitch = %s' % arg)
      def fdel(self):
         self._pitch = None
      return property(**locals( ))

   @property
   def format(self):
      return self.formatter.lily
