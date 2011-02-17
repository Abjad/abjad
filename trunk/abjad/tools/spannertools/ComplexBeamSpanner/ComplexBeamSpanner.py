from abjad.tools.spannertools.ComplexBeamSpanner._ComplexBeamSpannerFormatInterface import _ComplexBeamSpannerFormatInterface
from abjad.tools.spannertools.BeamSpanner.BeamSpanner import BeamSpanner
from fractions import Fraction
import types


class ComplexBeamSpanner(BeamSpanner):
   r'''Abjad complex beam spanner::

      abjad> staff = Staff("c'16 e'16 r16 f'16 g'2")

   ::

      abjad> f(staff)
      \new Staff {
         c'16
         e'16
         r16
         f'16
         g'2
      }

   ::

      abjad> spannertools.ComplexBeamSpanner(staff[:4])
      ComplexBeamSpanner(c'16, e'16, r16, f'16)

   ::

      abjad> f(staff)
      \new Staff {
         \set stemLeftBeamCount = #0
         \set stemRightBeamCount = #2
         c'16 [
         \set stemLeftBeamCount = #2
         \set stemRightBeamCount = #2
         e'16 ]
         r16
         \set stemLeftBeamCount = #2
         \set stemRightBeamCount = #0
         f'16 [ ]
         g'2
      }
   '''

   def __init__(self, leaves, lone = False, nibs = 'neither'):
      BeamSpanner.__init__(self, leaves)
      self._format = _ComplexBeamSpannerFormatInterface(self)
      self.lone = lone
      self.nibs = nibs
   
   ## PUBLIC ATTRIBUTES ##

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
