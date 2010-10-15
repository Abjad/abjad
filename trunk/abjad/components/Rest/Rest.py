from abjad.components._Leaf import _Leaf
import copy


class Rest(_Leaf):
   '''The Abjad model of a rest:

   ::

      abjad> Rest((3, 16))
      Rest('r8.')
   '''

   def __init__(self, *args, **kwargs):
      from abjad.tools.resttools._initialize_rest import _initialize_rest
      _initialize_rest(self, _Leaf, *args)
      self._initialize_keyword_values(**kwargs)

   ## OVERRIDES ##

   def __copy__(self, *args):
      new = type(self)(*self.__getnewargs__( ))
      if getattr(self, '_override', None) is not None:
         new._override = copy.copy(self.override)
      if getattr(self, '_set', None) is not None:
         new._set = copy.copy(self.set)
      return new

   def __getnewargs__(self):
      result = [ ]
      result.append(self.duration.written)
      if self.duration.multiplier is not None:
         result.append(self.duration.multiplier)
      return tuple(result)
   
   ## PRIVATE ATTRIBUTES ##

   @property
   def _body(self):
      '''Read-only body of rest.
      '''
      result = ''
      vertical_positioning_pitch = getattr(self, '_vertical_positioning_pitch', None)
      if vertical_positioning_pitch:
         result += str(vertical_positioning_pitch)
      else:
         result += 'r'
      result += str(self.duration)
      if vertical_positioning_pitch:
         result += r' \rest'
      return [result]

   @property
   def _compact_representation(self):
      return 'r%s' % self.duration
