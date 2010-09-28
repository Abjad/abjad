from abjad.components._Leaf import _Leaf
from abjad.components.Rest.Rest import Rest


class MultiMeasureRest(Rest):
   '''The Abjad model of a multi-measure rest.'''
   
   def __init__(self, *args, **kwargs):
      from abjad.tools.resttools._initialize_multi_measure_rest import \
         _initialize_multi_measure_rest
      _initialize_multi_measure_rest(self, _Leaf, *args)
      self._initialize_keyword_values(**kwargs)

   ## OVERLOADS ##

   def __repr__(self):
      return '%s(%s)' % (self.__class__.__name__, self.duration)

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

   @property
   def pitch(self):
      '''Read-only empty tuple.
      Multi-measure rests do not support so-called pitched rest.
      To change a multi-measure rest's staff position,
      override the grob's staff-position property instead.'''
      return ( )
