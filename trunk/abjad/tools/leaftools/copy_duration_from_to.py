from abjad.leaf import _Leaf
from abjad.rational import Rational


def copy_duration_from_to(source, target):
   r'''.. versionadded:: 1.1.2

   Copy duration from leaf `source` to leaf `target`::

      abjad> note = Note(0, (1, 4))
      abjad> note.duration.multiplier = Rational(1, 2)
      abjad> rest = Rest((1, 64))
      abjad> leaftools.copy_duration_from_to(note, rest)
      Rest(4 * 1/2)

   Return leaf `target`.
   '''

   if not isinstance(source, _Leaf):
      raise TypeError('must be leaf.')
   
   if not isinstance(target, _Leaf):
      raise TypeError('must be leaf.')

   written = Rational(source.duration.written)
   multiplier = Rational(source.duration.multiplier)

   target.duration.written = written
   target.duration.multiplier = multiplier

   return target
