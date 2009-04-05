from abjad.beam.complexformat import _ComplexBeamSpannerFormatInterface
from abjad.beam.spanner import Beam
from abjad.rational.rational import Rational
import types


class ComplexBeam(Beam):

   def __init__(self, leaves, 
      durations = None, span = 1, lone = False, nibs = 'neither'):
      Beam.__init__(self, leaves)
      self._format = _ComplexBeamSpannerFormatInterface(self)
      self.durations = durations
      self.lone = lone
      self.nibs = nibs
      self.span = span

   ## PRIVATE ATTRIBUTES ##

   @property
   def _spanPoints(self):
      result = [ ]
      if self.durations is not None:
         result.append(self.durations[0])
         for d in self.durations[1:]:
            result.append(result[-1] + d)   
      return result

   ## PUBLIC ATTRIBUTES ##
      
   @apply
   def durations( ):
      def fget(self):
         return self._durations
      def fset(self, arg):
         if arg is None:
            self._durations = None
         elif isinstance(arg, list):
            for i, d in enumerate(arg):
               if isinstance(d, tuple):
                  arg[i] = Rational(*d)
               else:
                  arg[i] = Rational(d)
            self._durations = arg
         else:
            raise ValueError('durations must be list of Rationals, or None.')
      return property(**locals( ))

   @apply
   def lone( ):
      def fget(self):
         return self._lone
      def fset(self, arg):
         assert isinstance(arg, bool) or arg in ('left', 'right', 'both')
         self._lone = arg 
      return property(**locals( ))

   @apply
   def nibs( ):
      def fget(self):
         return self._nibs
      def fset(self, arg):
         assert arg in ('left', 'rigth', 'both', 'neither')
         self._nibs = arg 
      return property(**locals( ))

   @apply
   def span( ):
      def fget(self):
         return self._span
      def fset(self, arg):
         assert isinstance(arg, (int, types.NoneType))
         self._span = arg 
      return property(**locals( ))

#   ## PUBLIC METHODS ##
#
#   def before(self, leaf):
#      result = [ ]
#      if leaf.beam.beamable:
#         left, right = None, None
#         # lone
#         if self._isMyOnlyLeaf(leaf):
#            #elif self.lone == 'left':
#            if self.nibs == 'left':
#               left = leaf.beam._flags
#               right = 0
#            #elif self.lone == 'right':
#            elif self.nibs == 'right':
#               left = 0
#               right = leaf.beam._flags
#            #elif self.lone == 'both':
#            elif self.nibs == 'both':
#               left = leaf.beam._flags
#               right = leaf.beam._flags
#            #if self.lone in (True, False):
#            elif self.nibs == 'neither':
#               left = None
#               right = None
#            else:
#               #raise ValueError('lone must be left, right or both.')
#               raise ValueError('nibs must be left, right, both or neither.')
#         # first
#         elif self._isMyFirstLeaf(leaf) or not leaf.prev:
#            left = 0
#            right = leaf.beam._flags
#         # last
#         elif self._isMyLastLeaf(leaf) or not leaf.next:
#            left = leaf.beam._flags
#            right = 0
#         # just right of span gap
#         elif self._durationOffsetInMe(leaf) in self._spanPoints and not \
#            (self._durationOffsetInMe(leaf) + leaf.duration.prolated in \
#            self._spanPoints):
#            assert isinstance(self.span, int)
#            left = self.span
#            right = leaf.beam._flags
#         # just left of span gap
#         elif self._durationOffsetInMe(leaf) + leaf.duration.prolated in \
#            self._spanPoints and not self._durationOffsetInMe(leaf) in \
#            self._spanPoints:
#            assert isinstance(self.span, int)
#            left = leaf.beam._flags
#            right = self.span
#         # [unbeamable leaf beamable]
#         elif not leaf.prev.beam.beamable and leaf.next.beam.beamable:
#            left = leaf.beam._flags
#            right = min(leaf.beam._flags, leaf.next.beam._flags)
#         # [beamable leaf unbeamable]
#         elif leaf.prev.beam.beamable and not leaf.next.beam.beamable:
#            left = min(leaf.beam._flags, leaf.prev.beam._flags)
#            right = leaf.beam._flags
#         # [unbeamable leaf unbeamable]
#         elif not leaf.prev.beam.beamable and not leaf.next.beam.beamable:
#            left = leaf.beam._flags
#            right = leaf.beam._flags
#         # [beamable leaf beamable]
#         else:
#            left = min(leaf.beam._flags, leaf.prev.beam._flags)
#            right = min(leaf.beam._flags, leaf.next.beam._flags)
#            if left != leaf.beam._flags and right != leaf.beam._flags:
#               left = leaf.beam._flags
#         if left is not None:
#            result.append(r'\set stemLeftBeamCount = #%s' % left)
#         if right is not None:
#            result.append(r'\set stemRightBeamCount = #%s' % right)
#      return result
#
#   def right(self, leaf):
#      result = [ ]
#      if leaf.beam.beamable:
#         #if self._isMyFirstLeaf(leaf) or not leaf.prev or \
#         #   not leaf.prev.beam.beamable or (self._isMyOnlyLeaf(leaf) and
#         #   self.lone):
#         # lone
#         if self._isMyOnlyLeaf(leaf):
#               if self.lone:
#                  result.append('[')
#         # otherwise
#         elif self._isMyFirstLeaf(leaf) or not leaf.prev or \
#            not leaf.prev.beam.beamable:
#            result.append('[')
#         #if self._isMyLastLeaf(leaf) or not leaf.next or \
#         #   not leaf.next.beam.beamable or (self._isMyOnlyLeaf(leaf) and
#         #   self.lone):
#         # lone
#         if self._isMyOnlyLeaf(leaf):
#            if self.lone:
#               result.append(']')
#         # otherwise
#         elif self._isMyLastLeaf(leaf) or not leaf.next or \
#            not leaf.next.beam.beamable:
#            result.append(']')
#      return result
