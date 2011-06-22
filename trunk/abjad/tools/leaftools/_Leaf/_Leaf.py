from abjad.tools.componenttools._Component import _Component
from abjad.tools.leaftools._Leaf._LeafDurationInterface import _LeafDurationInterface
from abjad.core._StrictComparator import _StrictComparator
import copy
import operator


class _Leaf(_Component, _StrictComparator):

   ## TODO: encapsuate grace and tremolo attributes ##
   __slots__ = ('_after_grace', '_duration', '_grace', 
      '_written_pitch_indication_is_nonsemantic',
      '_written_pitch_indication_is_at_sounding_pitch',
      'after_grace', 'grace', )

   def __init__(self, written_duration, lilypond_multiplier = None):
      _Component.__init__(self)
      self._duration = _LeafDurationInterface(self, written_duration)
      self._duration.multiplier = lilypond_multiplier
      self.written_pitch_indication_is_nonsemantic = False
      self.written_pitch_indication_is_at_sounding_pitch = True

   ## OVERLOADS ##

   def __and__(self, arg):
      return self._operate(arg, operator.__and__)

   #__deepcopy__ = __copy__

   def __getnewargs__(self):
      result = [ ]
      result.append(self.duration.written)
      if self.duration.multiplier is not None:
        result.append(self.duration.multiplier)
      return tuple(result)

   def __or__(self, arg):
      return self._operate(arg, operator.__or__)

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
      from abjad.tools import leaftools
      from abjad.tools import pitchtools
      self_pairs = set(pitchtools.list_named_chromatic_pitches_in_expr(self))
      arg_pairs = set(pitchtools.list_named_chromatic_pitches_in_expr(arg))
      pairs = operator(self_pairs, arg_pairs)
      if len(pairs) == 0:
         pairs = [None]
      elif len(pairs) == 1:
         pairs = list(pairs)
      else:
         pairs = [tuple(pairs)]
      leaves = leaftools.make_leaves(pairs, self.duration.written)
      leaf = leaves[0]
      return leaf

   ## PRIVATE ATTRIBUTES ##

   @property
   def _format_pieces(self):
      return self.format.split('\n')

   ## PUBLIC ATTRIBUTES ##

   @property
   def format(self):
      from abjad.tools.leaftools._format_leaf import _format_leaf
      return _format_leaf(self)

   @apply
   def written_pitch_indication_is_nonsemantic( ):
      def fset(self, arg):
         '''Read / write flag to be set when using leaves only graphically.

         setting this value to true sets sounding pitch indicator to false.
         '''
         if not isinstance(arg, type(True)):
            raise TypeError
         self._written_pitch_indication_is_nonsemantic = arg
         if arg == True:
            self.written_pitch_indication_is_at_sounding_pitch = False
      def fget(self):
         return self._written_pitch_indication_is_nonsemantic
      return property(**locals( ))

   @apply
   def written_pitch_indication_is_at_sounding_pitch( ):
      def fset(self, arg):
         '''Read / write flag to be set to false when pitch indication is transposed.
         '''
         if not isinstance(arg, type(True)):
            raise TypeError
         self._written_pitch_indication_is_at_sounding_pitch = arg
      def fget(self):
         return self._written_pitch_indication_is_at_sounding_pitch
      return property(**locals( ))
