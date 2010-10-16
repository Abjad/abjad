from abjad.components._Component._Component import _Component
from abjad.components._Leaf._LeafDurationInterface import _LeafDurationInterface
import copy
import operator


class _Leaf(_Component):

   ## TODO: encapsuate grace and tremolo attributes ##
   __slots__ = ('_after_grace', '_duration', '_grace', 'after_grace', 'grace', 
      'tremolo_subdivision', )

   def __init__(self, written_duration, lilypond_multiplier = None):
      _Component.__init__(self)
      self._duration = _LeafDurationInterface(self, written_duration)
      self._duration.multiplier = lilypond_multiplier

   ## OVERLOADS ##

   def __and__(self, arg):
      return self._operate(arg, operator.__and__)

   def __copy__(self, *args):
      new = type(self)(*self.__getnewargs__( ))
      if getattr(self, '_override', None) is not None:
         new._override = copy.copy(self.override)
      if getattr(self, '_set', None) is not None:
         new._set = copy.copy(self.set)
      return new

   def __eq__(self, arg):
      if isinstance(arg, type(self)):
         if self.duration.written == arg.duration.written:
            if self.duration.multiplier == arg.duration.multiplier:
               return True
      return False

   def __getnewargs__(self):
      result = [ ]
      result.append(self.duration.written)
      if self.duration.multiplier is not None:
         result.append(self.duration.multiplier)
      return tuple(result)

   def __or__(self, arg):
      return self._operate(arg, operator.__or__)

   def __ne__(self, arg):
      return not self == arg

   def __repr__(self):
      return '%s(%s)' % (self.__class__.__name__, repr(self._compact_representation))

   def __str__(self):
      return self._compact_representation

   def __sub__(self, arg):
      return self._operate(arg, operator.__sub__)

   def __xor__(self, arg):
      return self._operate(arg, operator.__xor__)

   ## PRIVATE METHODS ##

   def _copy_override_and_set_from_leaf(self, leaf):
      if getattr(leaf, '_override', None) is not None:
         self._override = copy.copy(leaf.override)
      if getattr(leaf, '_set', None) is not None:
         self._set = copy.copy(leaf.set)

   def _operate(self, arg, operator):
      assert isinstance(arg, _Leaf)
      from abjad.tools.leaftools._engender import _engender
      from abjad.tools import pitchtools
      self_pairs = set([(str(x.named_chromatic_pitch_class), x.octave_number) 
         for x in pitchtools.list_named_chromatic_pitches_in_expr(self) if x is not None])
      arg_pairs = set([(str(x.named_chromatic_pitch_class), x.octave_number) 
         for x in pitchtools.list_named_chromatic_pitches_in_expr(arg) if x is not None])
      pairs = operator(self_pairs, arg_pairs)
      return _engender(pairs, self.duration.written)

   ## PUBLIC ATTRIBUTES ##

   @property
   def format(self):
      from abjad.tools.leaftools._format_leaf import _format_leaf
      return _format_leaf(self)
