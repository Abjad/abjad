# -*- encoding: utf-8 -*-
import abc
from abjad.tools import mathtools
from abjad.tools.pitchtools.Interval import Interval


class NamedInterval(Interval):
    '''Abjad model of a named interval:

    ::

        >>> pitchtools.NamedInterval('+M9')
        NamedInterval('+M9')

    Return named interval
    '''

    ### CLASS VARIABLES ##

    __slots__ = (
        '_number',
        '_quality_string',
        )

    ### INITIALIZER ###

    def __init__(self, *args):
        from abjad.tools import pitchtools
        if len(args) == 1 and isinstance(args[0], type(self)):
            quality_string = args[0].quality_string
            number = args[0].number
        elif len(args) == 1 and isinstance(args[0], str):
            match = pitchtools.Interval._interval_name_abbreviation_regex.match(args[0])
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
        self._quality_string = quality_string
        self._number = number

    ### SPECIAL METHODS ###

    def __abs__(self):
        return type(self)(self.quality_string, abs(self.number))

    def __add__(self, arg):
        from abjad.tools import pitchtools
        if not isinstance(arg, type(self)):
            raise TypeError('%s must be melodic diatonic interval.' % arg)
        dummy_pitch = pitchtools.NamedPitch(0)
        new_pitch = dummy_pitch + self + arg
        return pitchtools.NamedInterval.from_pitch_carriers(
            dummy_pitch, new_pitch)

    def __copy__(self, *args):
        return type(self)(self.quality_string, self.number)

    __deepcopy__ = __copy__

    def __eq__(self, arg):
        if isinstance(arg, type(self)):
            if self.quality_string == arg.quality_string:
                if self.number == arg.number:
                    return True
        return False

    def __float__(self):
        return float(self._number)

    def __ge__(self, arg):
        if not isinstance(arg, type(self)):
            raise TypeError
        if self.number == arg.number:
            return self.semitones >= arg.semitones
        return self.number >= arg.number

    def __gt__(self, arg):
        if not isinstance(arg, type(self)):
            raise TypeError
        if self.number == arg.number:
            return self.semitones > arg.semitones
        return self.number > arg.number

    def __int__(self):
        return self._number

    def __le__(self, arg):
        if not isinstance(arg, type(self)):
            raise TypeError
        if self.number == arg.number:
            return self.semitones <= arg.semitones
        return self.number <= arg.number

    def __lt__(self, arg):
        if not isinstance(arg, type(self)):
            raise TypeError
        if self.number == arg.number:
            return self.semitones < arg.semitones
        return self.number < arg.number

    def __mul__(self, arg):
        from abjad.tools import pitchtools
        if not isinstance(arg, (int, long)):
            raise TypeError('%s must be int.' % arg)
        dummy_pitch = pitchtools.NamedPitch(0)
        for i in range(abs(arg)):
            dummy_pitch += self
        result = pitchtools.NamedInterval.from_pitch_carriers(
            pitchtools.NamedPitch(0), dummy_pitch)
        if arg < 0:
            return -result
        return result

    def __ne__(self, arg):
        return not self == arg

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
        dummy_pitch = pitchtools.NamedPitch(0)
        new_pitch = dummy_pitch + self - arg
        return pitchtools.NamedInterval.from_pitch_carriers(
            dummy_pitch, new_pitch)

    ### PRIVATE PROPERTIES ###

    _acceptable_quality_strings = (
        'perfect',
        'major',
        'minor',
        'diminished',
        'augmented',
        )

    _quality_abbreviation_to_quality_string = {
        'M': 'major',
        'm': 'minor',
        'P': 'perfect',
        'aug': 'augmented',
        'dim': 'diminished',
        }

    @property
    def _format_string(self):
        return '%s%s' % (self._quality_abbreviation, self.number)

    @property
    def _interval_string(self):
        interval_to_string = {
            1: 'unison',
            2: 'second',
            3: 'third',
            4: 'fourth',
            5: 'fifth',
            6: 'sixth',
            7: 'seventh',
            8: 'octave',
            9: 'ninth',
            10: 'tenth',
            11: 'eleventh',
            12: 'twelth',
            13: 'thirteenth',
            14: 'fourteenth',
            15: 'fifteenth',
            }
        try:
            interval_string = interval_to_string[abs(self.number)]
        except KeyError:
            abs_number = abs(self.number)
            residue = abs_number % 10
            if residue == 1:
                suffix = 'st'
            elif residue == 2:
                suffix = 'nd'
            elif residue == 3:
                suffix = 'rd'
            else:
                suffix = 'th'
            interval_string = '%s%s' % (abs_number, suffix)
        return interval_string

    @property
    def _quality_abbreviation(self):
        _quality_string_to_quality_abbreviation = {
            'major': 'M', 'minor': 'm', 'perfect': 'P',
            'augmented': 'aug', 'diminished': 'dim'}
        return _quality_string_to_quality_abbreviation[self.quality_string]

    ### PUBLIC METHODS ###

    @classmethod
    def from_pitch_carriers(cls, pitch_carrier_1, pitch_carrier_2):
        '''Calculate melodic diatonic interval from `pitch_carrier_1` to
        `pitch_carrier_2`:

        ::

            >>> pitchtools.NamedInterval.from_pitch_carriers(
            ...     pitchtools.NamedPitch(-2),
            ...     pitchtools.NamedPitch(12),
            ...     )
            NamedInterval('+M9')

        Return melodic diatonic interval.
        '''
        from abjad.tools import pitchtools
        pitch_1 = pitchtools.get_named_pitch_from_pitch_carrier(pitch_carrier_1)
        pitch_2 = pitchtools.get_named_pitch_from_pitch_carrier(pitch_carrier_2)
        degree_1 = pitch_1._diatonic_pitch_number
        degree_2 = pitch_2._diatonic_pitch_number
        #degree_1 = abs(pitch_1.numbered_diatonic_pitch)
        #degree_2 = abs(pitch_2.numbered_diatonic_pitch)
        diatonic_interval_number = abs(degree_1 - degree_2) + 1
        chromatic_interval_number = abs(abs(pitch_1.numbered_pitch) -
            abs(pitch_2.numbered_pitch))
        absolute_diatonic_interval = \
            pitchtools.spell_chromatic_interval_number(
            diatonic_interval_number, chromatic_interval_number)
        if pitch_2 < pitch_1:
            diatonic_interval = -absolute_diatonic_interval
        else:
            diatonic_interval = absolute_diatonic_interval
        return cls(diatonic_interval)

    ### PUBLIC PROPERTIES ###

    @property
    def diatonic_interval_class(self):
        from abjad.tools import pitchtools
        quality_string, number = self._quality_string, self.number
        return pitchtools.NamedInversionEquivalentIntervalClass(
            quality_string, number)

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
    def interval_class(self):
        return ((abs(self.number) - 1) % 7) + 1

    @property
    def interval_string(self):
        return self._interval_string

    @property
    def number(self):
        return self._number

    @property
    def quality_string(self):
        return self._quality_string

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
            pitchtools.NamedIntervalClass(self).number)
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
