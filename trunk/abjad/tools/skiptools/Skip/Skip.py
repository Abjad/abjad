from abjad.components._Leaf import _Leaf
import copy


class Skip(_Leaf):
   '''The Abjad model of a LilyPond skip:

   ::

      abjad> skiptools.Skip((3, 16))
      Skip('s8.')
   '''

   __slots__ = ( )

   def __init__(self, *args, **kwargs):
      from abjad.tools.skiptools._initialize_skip import _initialize_skip
      _initialize_skip(self, _Leaf, *args)
      self._initialize_keyword_values(**kwargs)

   ## OVERRIDES ##

   def __copy__(self, *args):
      new = type(self)(*self.__getnewargs__( ))
      if getattr(self, '_override', None) is not None:
         new._override = copy.copy(self.override)
      if getattr(self, '_set', None) is not None:
         new._set = copy.copy(self.set)
      return new

   #__deepcopy__ = __copy__
      
   def __getnewargs__(self):
      result = [ ]
      result.append(self.duration.written)
      if self.duration.multiplier is not None:
         result.append(self.duration.multiplier)
      return tuple(result)

   ## PRIVATE ATTRIBUTES ##

   @property
   def _body(self):
      result = [ ]
      result.append('s%s' % self.duration)
      return result

   @property
   def _compact_representation(self):
      return 's%s' % self.duration
