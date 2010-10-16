from abjad.components._Leaf import _Leaf
from abjad.components import Rest


class MultiMeasureRest(Rest):
   '''The Abjad model of a multi-measure rest.
   '''
   
   __slots__ = ( )

   ## PRIVATE ATTRIBUTES ##

   @property
   def _compact_representation(self):
      return 'R%s' % self.duration

   ## PUBLIC ATTRIBUTES ##

   @property
   def _body(self):
      '''Read-only list of string representation of body of rest.  
      Picked up as format contribution at format-time.'''
      result = 'R' + str(self.duration)
      return [result]
