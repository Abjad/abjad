from abjad.tools.pitchtools._CounterpointInterval import _CounterpointInterval
from abjad.tools.pitchtools._HarmonicInterval import _HarmonicInterval


class HarmonicCounterpointInterval(_CounterpointInterval, _HarmonicInterval):
    '''.. versionadded:: 2.0

    Abjad model of harmonic counterpoint interval::

        abjad> pitchtools.HarmonicCounterpointInterval(-9)
        HarmonicCounterpointInterval(9)

    Harmonic counterpoint intervals are immutable.
    '''

    def __new__(klass, token):
        from abjad.tools import pitchtools
        self = object.__new__(klass)
        if isinstance(token, int):
            _number = abs(token)
        elif isinstance(token, pitchtools._DiatonicInterval._DiatonicInterval):
            _number = abs(token.number)
        else:
            raise TypeError('must be number or diatonic interval.')
        object.__setattr__(self, '_number', _number)
        return self

    ### OVERLOADS ###

    def __eq__(self, arg):
        if isinstance(arg, type(self)):
            if self.number == arg.number:
                return True
        return False

    def __ne__(self, arg):
        return not self == arg

    ### PUBLIC ATTRIBUTES ###

    @property
    #def interval_class(self):
    def harmonic_counterpoint_interval_class(self):
        from abjad.tools import pitchtools
        return pitchtools.HarmonicCounterpointIntervalClass(self)
