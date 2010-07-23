from abjad.leaf import _Leaf
from abjad.rational import Rational
from abjad.rest import Rest
from abjad.skip import Skip
from abjad.tools import iterate
import types


def _insert_measure_padding(expr, front, back, klass, splice = False):
   r'''.. versionadded:: 1.1.2

   Generalizes measuretools.pad_measures_in_expr_with_rests( ) and
   measuretools.pad_measures_in_expr_with_skips( ).
   '''

   if not isinstance(front, (Rational, types.NoneType)):
      raise ValueError

   if not isinstance(back, (Rational, types.NoneType)):
      raise ValueError

   if not isinstance(klass, (Rest, Skip)):
      raise TypeError

   root = expr[0].parentage.root

   ## forbid updates because _Component.splice_left( ) and ##
   ## _Component.splice( ) call self.offset.prolated.stop  ##
   root._update._forbidUpdate( )

   for measure in iterate.measures_forward_in_expr(expr):
      if front is not None:
         start_components = measure._navigator._contemporaneousStartContents
         start_leaves = [x for x in start_components if isinstance(x, _Leaf)]
         for start_leaf in start_leaves:
            if splice:
               start_leaf.splice_left([klass.__class__(front)])
            else:
               start_leaf.extend_left_in_parent([klass.__class__(front)])
      if back is not None:
         stop_components = measure._navigator._contemporaneousStopContents
         stop_leaves = [x for x in stop_components if isinstance(x, _Leaf)]
         for stop_leaf in stop_leaves:
            if splice:
               stop_leaf.splice([klass.__class__(back)])
            else:
               stop_leaf.extend_in_parent([klass.__class__(back)])

   ## allow updates after all calls to splice( ) are done. ##
   root._update._allowUpdate( )
