from abjad.leaf.leaf import _Leaf


def has_duplicate_pitch_class(leaf):
   '''.. versionadded:: 1.1.2

   Return ``True`` when `leaf` contains duplicate pitch class.
   Otherwise ``False``.

   '''

   if not isinstance(leaf, _Leaf):
      raise TypeError('%s must be note, rest or chord.' % leaf)

   pass
