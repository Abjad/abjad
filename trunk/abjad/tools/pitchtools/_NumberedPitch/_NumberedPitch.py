from abc import ABCMeta
from abjad.tools.pitchtools._Numbered import _Numbered
from abjad.tools.pitchtools.PitchObject import PitchObject


class _NumberedPitch(PitchObject, _Numbered):
    '''.. versionadded:: 2.0

    Numbered pitch base class from which concrete classes inherit.
    '''

    __metaclass__ = ABCMeta
    __slots__ = ()
