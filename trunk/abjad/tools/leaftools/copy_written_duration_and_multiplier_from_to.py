from abjad._Leaf import _Leaf
from abjad.Rational import Rational


def copy_written_duration_and_multiplier_from_to(source_leaf, target_leaf):
   r'''.. versionadded:: 1.1.2

   Copy written duration and multiplier from `source_leaf` to `target_leaf`::

      abjad> note = Note(0, (1, 4))
      abjad> note.duration.multiplier = Rational(1, 2)
      abjad> rest = Rest((1, 64))
      abjad> leaftools.copy_written_duration_and_multiplier_from_to(note, rest)
      Rest(4 * 1/2)

   Return `target_leaf`.
   '''

   ## check source leaf type
   if not isinstance(source_leaf, _Leaf):
      raise TypeError('must be leaf.')
   
   ## check target leaf type
   if not isinstance(target_leaf, _Leaf):
      raise TypeError('must be leaf.')

   ## copy source leaf written duration and multiplier
   written = Rational(source_leaf.duration.written)
   multiplier = Rational(source_leaf.duration.multiplier)

   ## set target leaf written duration and multiplier
   target_leaf.duration.written = written
   target_leaf.duration.multiplier = multiplier

   ## return target leaf
   return target_leaf
