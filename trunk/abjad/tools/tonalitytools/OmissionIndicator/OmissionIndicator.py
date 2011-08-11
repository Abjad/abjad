from abjad.core import _Immutable


class OmissionIndicator(_Immutable):
    '''.. versionadded:: 2.0

    Indicator of missing chord tones.

    Value object that can not be chnaged after instantiation.
    '''

    def __init__(self):
        pass
