from abjad.components._Component._Component import _Component
from abjad.components._Leaf._LeafDurationInterface import _LeafDurationInterface
import operator


class _Leaf(_Component):

   def __init__(self, duration):
      _Component.__init__(self)
      self._duration = _LeafDurationInterface(self, duration)

   ## OVERLOADS ##

   def __and__(self, arg):
      return self._operate(arg, operator.__and__)
   
   def __eq__(self, arg):
      if isinstance(arg, type(self)):
         if self.duration.written == arg.duration.written:
            if self.duration.multiplier == arg.duration.multiplier:
               return True
      return False

   def __or__(self, arg):
      return self._operate(arg, operator.__or__)

   def __ne__(self, arg):
      return not self == arg

   def __str__(self):
      return self._compact_representation

   def __sub__(self, arg):
      return self._operate(arg, operator.__sub__)

   def __xor__(self, arg):
      return self._operate(arg, operator.__xor__)

   ## PRIVATE METHODS ##

   def _operate(self, arg, operator):
      assert isinstance(arg, _Leaf)
      from abjad.tools.leaftools._engender import _engender
      from abjad.tools import pitchtools
      self_pairs = set([
         (x.name, x.octave) for x in pitchtools.list_named_pitches_in_expr(self) if x is not None])
      arg_pairs = set([
         (x.name, x.octave) for x in pitchtools.list_named_pitches_in_expr(arg) if x is not None])
      pairs = operator(self_pairs, arg_pairs)
      return _engender(pairs, self.duration.written)

   ## PUBLIC ATTRIBUTES ##

   @property
   def format(self):
      from abjad.tools.leaftools._format_leaf import _format_leaf
      return _format_leaf(self)
