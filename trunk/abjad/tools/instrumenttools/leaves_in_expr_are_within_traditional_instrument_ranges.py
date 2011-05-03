from abjad.tools import leaftools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.get_effective_instrument import get_effective_instrument


def leaves_in_expr_are_within_traditional_instrument_ranges(expr):
   '''.. versionadded:: 1.1.2

   True when leaves in `expr` are within traditional instrument ranges::

      abjad> staff = Staff("c'8 r8 <d' fs'>8 r8")
      abjad> instrumenttools.Violin( )(staff)
   
   ::

      abjad> instrumenttools.leaves_in_expr_are_within_traditional_instrument_ranges(staff)
      True

   False otherwise::

      abjad> staff = Staff("c'8 r8 <d fs>8 r8")
      abjad> instrumenttools.Violin( )(staff)
   
   ::

      abjad> instrumenttools.leaves_in_expr_are_within_traditional_instrument_ranges(staff)
      False

   Return boolean.
   '''

   for leaf in leaftools.iterate_leaves_forward_in_expr(expr):
      instrument = get_effective_instrument(leaf)
      if not instrument:
         return False
      if pitchtools.is_pitch_carrier(leaf) and not leaf in instrument.traditional_range:
         return False
   else:
      return True
