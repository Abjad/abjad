#from abjad.core.grobhandler import _GrobHandler
from abjad.leaf.leaf import _Leaf
from abjad.pitch.pitch import Pitch
from abjad.rest.initializer import _RestInitializer


#class Rest(_Leaf, _GrobHandler):
class Rest(_Leaf):

   def __init__(self, *args):
      #_GrobHandler.__init__(self, 'Rest')
      self._initializer = _RestInitializer(self, _Leaf, *args)
   
   ### REPR ###

   def __repr__(self):
      return 'Rest(%s)' % self.duration._product

   def __str__(self):
      return 'r%s' % self.duration._product

   ### PRIVATE ATTRIBUTES ###
  
   @property
   def _body(self):
      result = ''
      if self.pitch:
         result += str(self.pitch)
      else:
         result += 'r'
      result += str(self.duration._product)
      if self.pitch:
         result += r' \rest'
      if self.stem.tremolo:
         result += ' :%s' % self.stem.tremolo
      return result

   ### PUBLIC ATTRIBUTES ###
  
   @property
   def pairs(self):
      return ( )

   @apply
   def pitch( ):
      def fget(self):
          return self._pitch
      def fset(self, arg):
         if isinstance(arg, type(None)):
            self._pitch = None
         elif isinstance(arg, (int, float, long)):
            self._pitch = Pitch(arg)
         elif isinstance(arg, tuple):
            self._pitch = Pitch(*arg)
         elif isinstance(arg, Pitch):
            self._pitch = arg
         else:
            raise ValueError('Can not set Rest.pitch from %s' % str(arg))
      return property(**locals( ))

   @property
   def pitches(self):
      return ( )
