# -*- encoding: utf-8 -*-
from abjad.tools import mathtools
from abjad.tools.pitchtools.NamedInterval import NamedInterval


class NamedMelodicInterval(NamedInterval):
    '''Abjad model of melodic diatonic interval:

    ::

        >>> pitchtools.NamedMelodicInterval('+M9')
        NamedMelodicInterval('+M9')

    Melodic diatonic intervals are immutable.
    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### PUBLIC METHODS ###

    @classmethod
    def from_pitch_carriers(cls, pitch_carrier_1, pitch_carrier_2):
        '''Calculate melodic diatonic interval from `pitch_carrier_1` to
        `pitch_carrier_2`:

        ::

            >>> pitchtools.NamedMelodicInterval.from_pitch_carriers(
            ...     pitchtools.NamedPitch(-2), 
            ...     pitchtools.NamedPitch(12),
            ...     )
            NamedMelodicInterval('+M9')

        Return melodic diatonic interval.
        '''
        from abjad.tools import pitchtools
        pitch_1 = pitchtools.get_named_chromatic_pitch_from_pitch_carrier(pitch_carrier_1)
        pitch_2 = pitchtools.get_named_chromatic_pitch_from_pitch_carrier(pitch_carrier_2)
        degree_1 = pitch_1._diatonic_pitch_number
        degree_2 = pitch_2._diatonic_pitch_number
        #degree_1 = abs(pitch_1.numbered_diatonic_pitch)
        #degree_2 = abs(pitch_2.numbered_diatonic_pitch)
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
    def semitones(self):
        from abjad.tools import pitchtools
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
            pitchtools.NamedMelodicIntervalClass(self).number)
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
