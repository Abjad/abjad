from abjad.tools.pitchtools._Numbered import _Numbered
from abjad.tools.pitchtools._Pitch import _Pitch


class _NumberedPitch(_Pitch, _Numbered):
    '''.. versionadded:: 2.0

    Numbered pitch base class from which concrete classes inherit.
    '''

    __slots__ = ()
