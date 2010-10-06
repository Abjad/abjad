from abjad.core import _UnaryComparator
from abjad.tools.pitchtools._Pitch import _Pitch


class _NumericPitch(_Pitch, _UnaryComparator):
   '''.. versionadded:: 1.1.2

   Numeric pitch base class from which concrete classes inherit.
   '''

   __slots__ = ( )
