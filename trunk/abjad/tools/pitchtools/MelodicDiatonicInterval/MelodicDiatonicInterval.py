# -*- encoding: utf-8 -*-
from abjad.tools import mathtools
from abjad.tools.pitchtools.NamedInterval import NamedInterval
from abjad.tools.pitchtools.MelodicInterval import MelodicInterval


class MelodicDiatonicInterval(NamedInterval, MelodicInterval):
    '''Abjad model of melodic diatonic interval:

    ::

        >>> pitchtools.MelodicDiatonicInterval('+M9')
        MelodicDiatonicInterval('+M9')

    Melodic diatonic intervals are immutable.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_quality_string', 
        '_number',
        )

    ### INITIALIZER ###

    def __init__(self, *args):
        from abjad.tools.pitchtools.is_melodic_diatonic_interval_abbreviation \
            import melodic_diatonic_interval_abbreviation_regex
        if len(args) == 1 and isinstance(args[0], type(self)):
            quality_string = args[0].quality_string
            number = args[0].number
        elif len(args) == 1 and isinstance(args[0], str):
            match = melodic_diatonic_interval_abbreviation_regex.match(args[0])
            if match is None:
                raise ValueError(
                    '"%s" does not have the form of a mdi abbreviation.' % 
                    args[0])
            direction_string, quality_abbreviation, number_string = \
                match.groups()
            quality_string = self._quality_abbreviation_to_quality_string[
                quality_abbreviation]
            number = int(direction_string + number_string)
        elif len(args) == 2:
            quality_string, number = args
        object.__setattr__(self, '_quality_string', quality_string)
        object.__setattr__(self, '_number', number)

    ### SPECIAL METHODS ###

    def __abs__(self):
        from abjad.tools import pitchtools
        return pitchtools.HarmonicDiatonicInterval(
            self.quality_string, abs(self.number))

    def __add__(self, arg):
        from abjad.tools import pitchtools
        if not isinstance(arg, type(self)):
            raise TypeError('%s must be melodic diatonic interval.' % arg)
        dummy_pitch = pitchtools.NamedChromaticPitch(0)
        new_pitch = dummy_pitch + self + arg
        return pitchtools.MelodicDiatonicInterval.from_pitch_carriers(
            dummy_pitch, new_pitch)

    def __copy__(self, *args):
        return type(self)(self.quality_string, self.number)

    __deepcopy__ = __copy__

    def __mul__(self, arg):
        from abjad.tools import pitchtools
        if not isinstance(arg, (int, long)):
            raise TypeError('%s must be int.' % arg)
        dummy_pitch = pitchtools.NamedChromaticPitch(0)
        for i in range(abs(arg)):
            dummy_pitch += self
        result = pitchtools.MelodicDiatonicInterval.from_pitch_carriers(
            pitchtools.NamedChromaticPitch(0), dummy_pitch)
        if arg < 0:
            return -result
        return result

    def __neg__(self):
        return type(self)(self.quality_string, -self.number)

    def __repr__(self):
        return "%s('%s')" % (self._class_name, str(self))

    def __rmul__(self, arg):
        return self * arg

    def __str__(self):
        return '%s%s%s' % (
            self._direction_symbol, 
            self._quality_abbreviation, 
            abs(self.number),
            )

    def __sub__(self, arg):
        from abjad.tools import pitchtools
        if not isinstance(arg, type(self)):
            raise TypeError('%s must be melodic diatonic interval.' % arg)
        dummy_pitch = pitchtools.NamedChromaticPitch(0)
        new_pitch = dummy_pitch + self - arg
        return pitchtools.MelodicDiatonicInterval.from_pitch_carriers(
            dummy_pitch, new_pitch)

    ### PUBLIC METHODS ###

    @classmethod
    def from_pitch_carriers(cls, pitch_carrier_1, pitch_carrier_2):
        '''Calculate melodic diatonic interval from `pitch_carrier_1` to
        `pitch_carrier_2`:

        ::

            >>> pitchtools.MelodicDiatonicInterval.from_pitch_carriers(
            ...     pitchtools.NamedChromaticPitch(-2), 
            ...     pitchtools.NamedChromaticPitch(12),
            ...     )
            MelodicDiatonicInterval('+M9')

        Return melodic diatonic interval.
        '''
        from abjad.tools import pitchtools
        pitch_1 = pitchtools.get_named_chromatic_pitch_from_pitch_carrier(pitch_carrier_1)
        pitch_2 = pitchtools.get_named_chromatic_pitch_from_pitch_carrier(pitch_carrier_2)
        degree_1 = abs(pitch_1.numbered_diatonic_pitch)
        degree_2 = abs(pitch_2.numbered_diatonic_pitch)
        diatonic_interval_number = abs(degree_1 - degree_2) + 1
        chromatic_interval_number = abs(abs(pitch_1.numbered_chromatic_pitch) -
            abs(pitch_2.numbered_chromatic_pitch))
        absolute_diatonic_interval = \
            pitchtools.spell_chromatic_interval_number(
            diatonic_interval_number, chromatic_interval_number)
        if pitch_2 < pitch_1:
            diatonic_interval = -absolute_diatonic_interval
        else:
            diatonic_interval = absolute_diatonic_interval
        return diatonic_interval

    ### PUBLIC PROPERTIES ###

    @property
    def direction_number(self):
        if self.quality_string == 'perfect' and abs(self.number) == 1:
            return 0
        else:
            return mathtools.sign(self.number)

    @property
    def direction_string(self):
        if self.direction_number == -1:
            return 'descending'
        elif self.direction_number == 0:
            return None
        elif self.direction_number == 1:
            return 'ascending'

    @property
    def harmonic_chromatic_interval(self):
        from abjad.tools import pitchtools
        return pitchtools.HarmonicChromaticInterval(self)

    @property
    def harmonic_diatonic_interval(self):
        from abjad.tools import pitchtools
        return pitchtools.HarmonicDiatonicInterval(self)

    @property
    def inversion_equivalent_chromatic_interval_class(self):
        from abjad.tools import pitchtools
        n = self.semitones
        n %= 12
        if 6 < n:
            n = 12 - n
        return pitchtools.InversionEquivalentChromaticIntervalClass(n)

    @property
    def melodic_chromatic_interval(self):
        from abjad.tools import pitchtools
        return pitchtools.MelodicChromaticInterval(self)

    @property
    def melodic_diatonic_interval_class(self):
        from abjad.tools import pitchtools
        return pitchtools.MelodicDiatonicIntervalClass(self)

    @property
    def semitones(self):
        result = 0
        interval_class_number_to_semitones = {
            1: 0,  
            2: 1,  
            3: 3, 
            4: 5, 
            5: 7, 
            6: 8, 
            7: 10, 
            8: 0,
            }
        interval_class_number = abs(
            self.melodic_diatonic_interval_class.number)
        result += interval_class_number_to_semitones[interval_class_number]
        result += (abs(self.number) - 1) / 7 * 12
        quality_string_to_semitones = {
            'perfect': 0, 
            'major': 1, 
            'minor': 0, 
            'augmented': 1, 
            'diminished': -1,
            }
        result += quality_string_to_semitones[self.quality_string]
        if self.number < 0:
            result *= -1
        return result

    @property
    def staff_spaces(self):
        if self.direction_string == 'descending':
            return self.number + 1
        elif self.direction_string is None:
            return 0
        elif self.direction_string == 'ascending':
            return self.number - 1
