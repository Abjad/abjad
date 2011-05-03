from abjad.tools import contexttools
from abjad.tools import leaftools
from abjad.tools.instrumenttools.get_effective_instrument import get_effective_instrument


def leaves_in_expr_are_on_expected_clefs(expr):
   '''.. versionadded:: 1.1.2

   True when leaves in `expr` are on expected clefs::

      abjad> staff = Staff("c'8 d'8 e'8 f'8")
      abjad> contexttools.ClefMark('treble')(staff)
      ClefMark('treble')(Staff{4})
      abjad> instrumenttools.Violin( )(staff)
      Violin('Violin', 'Vn.')

   ::

      abjad> instrumenttools.leaves_in_expr_are_on_expected_clefs(staff)
      True

   False otherwise::

      abjad> staff = Staff("c'8 d'8 e'8 f'8")
      abjad> contexttools.ClefMark('alto')(staff)
      ClefMark('alto')(Staff{4})
      abjad> instrumenttools.Violin( )(staff)
      Violin('Violin', 'Vn.')

   ::

      abjad> instrumenttools.leaves_in_expr_are_on_expected_clefs(staff)
      False

   Return boolean.
   '''

   for leaf in leaftools.iterate_leaves_forward_in_expr(expr):
      instrument = get_effective_instrument(leaf)
      if not instrument:
         return False
      clef = contexttools.get_effective_clef(leaf)
      if not clef:
         return False
      if clef not in instrument.all_clefs:
         return False
   else:
      return True
