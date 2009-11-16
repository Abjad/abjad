from abjad.leaf import _Leaf
from abjad.rational import Rational


def get_duration_from(source, target):
   r'''.. versionadded:: 1.1.2

   Get duration from `source` leaf and set on `target` leaf. ::

      abjad> note = Note(0, (1, 4))
      abjad> note.duration.multiplier = Rational(1, 2)
      abjad> rest = Rest((1, 64))
      abjad> leaftools.get_duration_from(note, rest)
      Rest(4 * 1/2)

   Return `target` leaf.
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
