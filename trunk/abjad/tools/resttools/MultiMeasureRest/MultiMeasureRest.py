from abjad.components import Rest
from abjad.components._Leaf import _Leaf


class MultiMeasureRest(Rest):
   '''.. versionadded:: 1.1.2

   Abjad model of a multi-measure rest::

      abjad> resttools.MultiMeasureRest((1, 4))
      MultiMeasureRest('R4')

   Multi-measure rests are immutable.
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
