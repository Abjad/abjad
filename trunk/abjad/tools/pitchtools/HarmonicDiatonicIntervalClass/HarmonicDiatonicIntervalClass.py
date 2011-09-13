from abjad.tools.pitchtools._DiatonicIntervalClass import _DiatonicIntervalClass
from abjad.tools.pitchtools._HarmonicIntervalClass import _HarmonicIntervalClass


class HarmonicDiatonicIntervalClass(_DiatonicIntervalClass, _HarmonicIntervalClass):
    '''.. versionadded:: 2.0

    Abjad model harmonic diatonic interval-class::

        abjad> pitchtools.HarmonicDiatonicIntervalClass('-M9')
        HarmonicDiatonicIntervalClass('M2')

    Harmonic diatonic interval-classes are immutable.
    '''

    def __new__(klass, *args):
        from abjad.tools.pitchtools.is_melodic_diatonic_interval_abbreviation import melodic_diatonic_interval_abbreviation_regex
        from abjad.tools import pitchtools
        self = object.__new__(klass)
        if len(args) == 1:
            if isinstance(args[0], pitchtools.HarmonicDiatonicInterval):
                quality_string = args[0]._quality_string
                number = args[0].number
            elif isinstance(args[0], str):
                match = melodic_diatonic_interval_abbreviation_regex.match(args[0])
                if match is None:
                    raise ValueError('"%s" does not have the form of an hdic abbreviation.' % args[0])
                direction_string, quality_abbreviation, number_string = match.groups()
                quality_string = _DiatonicIntervalClass._quality_abbreviation_to_quality_string[quality_abbreviation]
                number = int(number_string)
            elif isinstance(args[0], tuple) and len(args[0]) == 2:
                quality_string, number = args[0]
            else:
                raise TypeError
        else:
            quality_string, number = args
        if quality_string not in _DiatonicIntervalClass._acceptable_quality_strings:
            raise ValueError('not acceptable quality string.')
        object.__setattr__(self, '_quality_string', quality_string)
        if not isinstance(number, int):
            raise TypeError('must be integer.')
        if number == 0:
            raise ValueError('must be nonzero.')
        abs_number = abs(number)
        if abs_number % 7 == 1 and 8 <= abs_number:
            number = 8
        else:
            number = abs_number % 7
            if number == 0:
                number = 7
        object.__setattr__(self, '_number', number)
        return self

    ### OVERLOADS ###

    def __eq__(self, arg):
        if isinstance(arg, type(self)):
            if self._quality_string == arg._quality_string:
                if self.number == arg.number:
                    return True
        return False

    def __ne__(self, arg):
        return not self == arg

    def __str__(self):
        return '%s%s' % (self._quality_abbreviation, self.number)

    ### PRIVATE ATTRIBUTES ###

    @property
    def _full_name(self):
        return '%s %s' % (self._quality_string, self._interval_string)

    ### PUBLIC METHODS ###

    def invert(self):
        '''Read-only inversion of harmonic diatonic interval-class::

            abjad> hdic = pitchtools.HarmonicDiatonicIntervalClass('major', -9)
            abjad> hdic.invert()
            HarmonicDiatonicIntervalClass('m7')

        Return harmonic diatonic interval-class.
        '''
        from abjad.tools import pitchtools
        low = pitchtools.NamedChromaticPitch('c', 4)
        quality_string, number = self._quality_string, self.number
        mdi = pitchtools.MelodicDiatonicInterval(quality_string, number)
        middle = low + mdi
        octave = pitchtools.MelodicDiatonicInterval('perfect', 8)
        high = low + octave
        hdi = pitchtools.calculate_harmonic_diatonic_interval_class_from_named_chromatic_pitch_to_named_chromatic_pitch(
            middle, high)
        return hdi
