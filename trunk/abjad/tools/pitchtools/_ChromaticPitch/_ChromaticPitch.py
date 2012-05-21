from abc import ABCMeta
from abjad.tools.pitchtools._Chromatic import _Chromatic
from abjad.tools.pitchtools.PitchObject import PitchObject


class _ChromaticPitch(PitchObject, _Chromatic):
    '''.. versionadded:: 2.0

    Chromatic pitch base class.
    '''

    __metaclass__ = ABCMeta
    __slots__ = ()
