from abjad.components._Leaf import _Leaf
from abjad.tools.pitchtools.NamedPitch.NamedPitch import NamedPitch
from abjad.components.Rest.initializer import _RestInitializer


class Rest(_Leaf):
   '''The `Abjad` model of a single rest.'''

   def __init__(self, *args):
      self._initializer = _RestInitializer(self, _Leaf, *args)
   
   ## OVERLOADS ##

   def __len__(self):
      return 0

   def __repr__(self):
      return 'Rest(%s)' % self.duration

   ## PRIVATE ATTRIBUTES ##

   @property
   def _compact_representation(self):
      return 'r%s' % self.duration

   ## PUBLIC ATTRIBUTES ##

   @property
   def _body(self):
      '''Read-only list of string representation of body of rest.
      Picked up as format contribution at format-time.'''
      result = ''
      if self.pitch:
         result += str(self.pitch)
      else:
         result += 'r'
      result += str(self.duration)
      if self.pitch:
         result += r' \rest'
      return [result]

   @property
   def numbers(self):
      '''Read-only empty tuple because rests have no pitch.'''
      return ( )
  
   @property
   def pairs(self):
      '''Read-only empty tuple because rests have no pitch.'''
      return ( )

   @apply
   def pitch( ):
      def fget(self):
         '''Read / write value for so-called pitched rest.'''
         return self._pitch
      def fset(self, arg):
         if isinstance(arg, type(None)):
            self._pitch = None
         elif isinstance(arg, (int, float, long)):
            self._pitch = NamedPitch(arg)
         elif isinstance(arg, tuple):
            self._pitch = NamedPitch(*arg)
         elif isinstance(arg, NamedPitch):
            self._pitch = arg
         else:
            raise ValueError('Can not set Rest.pitch from %s' % str(arg))
      return property(**locals( ))

   @property
   def pitches(self):
      '''Read-only empty tuple because rests have no pitch.'''
      return ( )
