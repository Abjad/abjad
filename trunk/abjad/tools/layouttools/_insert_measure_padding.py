from abjad.core import Fraction
from abjad.components._Leaf import _Leaf
from abjad.components.Rest import Rest
from abjad.components.Skip import Skip


def _insert_measure_padding(expr, front, back, klass, splice = False):
   r'''.. versionadded:: 1.1.2

   Generalizes measuretools.pad_measures_in_expr_with_rests( ) and
   measuretools.pad_measures_in_expr_with_skips( ).
   '''
   from abjad.tools import measuretools

   if not isinstance(front, (Fraction, type(None))):
      raise ValueError

   if not isinstance(back, (Fraction, type(None))):
      raise ValueError

   if not isinstance(klass, (Rest, Skip)):
      raise TypeError

   root = expr[0].parentage.root

   ## forbid updates because _Component.splice_left( ) and ##
   ## _Component.splice( ) call self.offset.stop  ##
   root._update._forbid_component_update( )

   for measure in measuretools.iterate_measures_forward_in_expr(expr):
      if front is not None:
         start_components = measure._navigator._contemporaneous_start_contents
         start_leaves = [x for x in start_components if isinstance(x, _Leaf)]
         for start_leaf in start_leaves:
            if splice:
               start_leaf.splice_left([klass.__class__(front)])
            else:
               start_leaf.extend_left_in_parent([klass.__class__(front)])
      if back is not None:
         stop_components = measure._navigator._contemporaneous_stop_contents
         stop_leaves = [x for x in stop_components if isinstance(x, _Leaf)]
         for stop_leaf in stop_leaves:
            if splice:
               stop_leaf.splice([klass.__class__(back)])
            else:
               stop_leaf.extend_in_parent([klass.__class__(back)])

   ## allow updates after all calls to splice( ) are done. ##
   root._update._allow_component_update( )
