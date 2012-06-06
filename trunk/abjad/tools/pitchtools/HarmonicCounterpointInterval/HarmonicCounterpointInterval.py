from abjad.tools.pitchtools.CounterpointIntervalObject import CounterpointIntervalObject
from abjad.tools.pitchtools.HarmonicIntervalObject import HarmonicIntervalObject


class HarmonicCounterpointInterval(CounterpointIntervalObject, HarmonicIntervalObject):
    '''.. versionadded:: 2.0

    Abjad model of harmonic counterpoint interval::

        >>> pitchtools.HarmonicCounterpointInterval(-9)
        HarmonicCounterpointInterval(9)

    Harmonic counterpoint intervals are immutable.
    '''

    def __init__(self, token):
        from abjad.tools import pitchtools
        if isinstance(token, int):
            _number = abs(token)
        elif isinstance(token, pitchtools.DiatonicIntervalObject):
            _number = abs(token.number)
        else:
            raise TypeError('must be number or diatonic interval.')
        object.__setattr__(self, '_number', _number)

    ### SPECIAL METHODS ###

    def __eq__(self, arg):
        if isinstance(arg, type(self)):
            if self.number == arg.number:
                return True
        return False

    def __ne__(self, arg):
        return not self == arg

    ### PUBLIC PROPERTIES ###

    @property
    #def interval_class(self):
    def harmonic_counterpoint_interval_class(self):
        from abjad.tools import pitchtools
        return pitchtools.HarmonicCounterpointIntervalClass(self)
