from abjad.tools import leaftools
from abjad.tools import pitchtools
from abjad.tools import voicetools
from abjad.tools.instrumenttools.get_effective_instrument import get_effective_instrument


def iterate_leaves_in_expr_outside_traditional_instrument_ranges(expr):
   '''.. versionadded:: 1.1.2

   Iterate leaves in `expr` outside traditional instrument ranges::

      abjad> staff = Staff("c'8 r8 <d fs>8 r8")
      abjad> instrumenttools.Violin( )(staff)
   
   ::

      abjad> for leaf in instrumenttools.iterate_leaves_in_expr_outside_traditional_instrument_ranges(staff):
      ...   leaf
      Chord('<d fs>8')

   Return generator.
   '''

   for leaf in leaftools.iterate_leaves_forward_in_expr(expr):
      instrument = get_effective_instrument(leaf)
      if leaf not in instrument.traditional_range:
         yield leaf
