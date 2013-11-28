# -*- encoding: utf-8 -*-
import abc
import functools
from abjad.tools import mathtools
from abjad.tools.pitchtools.Interval import Interval


@functools.total_ordering
class NamedInterval(Interval):
    '''A named interval.

    ::

        >>> interval = pitchtools.NamedInterval('+M9')
        >>> interval
        NamedInterval('+M9')

    '''

    ### CLASS VARIABLES ##

    __slots__ = (
        '_number',
        '_quality_string',
        )

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

    ### INITIALIZER ###

    def __init__(self, *args):
        from abjad.tools import pitchtools
        if len(args) == 1 and isinstance(args[0], type(self)):
            quality_string = args[0].quality_string
            number = args[0].number
        elif len(args) == 1 and isinstance(args[0], str):
            match = \
                pitchtools.Interval._interval_name_abbreviation_regex.match(
                args[0])
            if match is None:
                message = '{!r} does not have the form of a mdi abbreviation.'
                message = message.format(args[0])
                raise ValueError(message)
            direction_string, quality_abbreviation, number_string = \
                match.groups()
            quality_string = self._quality_abbreviation_to_quality_string[
                quality_abbreviation]
            number = int(direction_string + number_string)
        elif len(args) == 2:
            quality_string, number = args
        elif len(args) == 0:
            quality_string = 'perfect'
            number = 1
        else:
            message = 'can not initialize {}: {!r}'
            message = message.format(type(self).__init__, args)
            raise ValueError(message)
        self._quality_string = quality_string
        self._number = number

    ### SPECIAL METHODS ###

    def __abs__(self):
        r'''Absolute value of named interval.

        ::

            >>> abs(interval)
            NamedInterval('+M9')

        Returns named interval.
        '''
        return type(self)(self.quality_string, abs(self.number))

    def __add__(self, arg):
        r'''Adds `arg` to named interval.

        ::

            >>> interval + pitchtools.NamedInterval('M2')
            NamedInterval('+M10')

        Returns new named interval.
        '''
        from abjad.tools import pitchtools
        if not isinstance(arg, type(self)):
            message = 'must be named interval: {!r}.'.format(arg)
            raise TypeError(message)
        dummy_pitch = pitchtools.NamedPitch(0)
        new_pitch = dummy_pitch + self + arg
        return pitchtools.NamedInterval.from_pitch_carriers(
            dummy_pitch, new_pitch)

    def __copy__(self, *args):
        r'''Copies named interval.

        ::

            >>> import copy
            >>> copy.copy(interval)
            NamedInterval('+M9')

        Returns new named interval.
        '''
        return type(self)(self.quality_string, self.number)

    def __eq__(self, arg):
        r'''True when `arg` is a named interval with a quality string and
        number equal to this named interval.

        ::

            >>> interval == pitchtools.NamedInterval('+M9')
            True

        Otherwise false:

        ::

            >>> interval == pitchtools.NamedInterval('-M9')
            False

        Returns boolean.
        '''
        if isinstance(arg, type(self)):
            if self.quality_string == arg.quality_string:
                if self.number == arg.number:
                    return True
        return False

    def __float__(self):
        r'''Changes number of named interval to a float.

        ::

            >>> float(interval)
            9.0

        Returns float.
        '''
        return float(self._number)

    def __int__(self):
        r'''Returns number of named interval.

        ::

            >>> int(interval)
            9

        Returns integer.
        '''
        return self._number

    def __lt__(self, arg):
        r'''True when `arg` is a named interval with a number greater than that
        of this named interval.
        
        ::

            >>> interval < pitchtools.NamedInterval('+M10')
            True

        Also true when `arg` is a named interval with a
        number equal to this named interval and with semitones greater than
        this named interval:

        ::

            >>> pitchtools.NamedInterval('+m9') < interval
            True

        Otherwise false:

        ::

            >>> interval < pitchtools.NamedInterval('+M2')
            False

        Returns boolean.
        '''
        if isinstance(arg, type(self)):
            if self.number == arg.number:
                return self.semitones < arg.semitones
            return self.number < arg.number
        return False

    def __mul__(self, arg):
        r'''Multiplies named interval by `arg`.

        ::

            >>> 3 * interval
            NamedInterval('+aug25')

        Returns new named interval.
        '''
        from abjad.tools import pitchtools
        if not isinstance(arg, (int, long)):
            message = 'must be integer: {!r}.'.format(arg)
            raise TypeError(message)
        dummy_pitch = pitchtools.NamedPitch(0)
        for i in range(abs(arg)):
            dummy_pitch += self
        result = pitchtools.NamedInterval.from_pitch_carriers(
            pitchtools.NamedPitch(0), dummy_pitch)
        if arg < 0:
            return -result
        return result

    def __ne__(self, arg):
        r'''True when `arg` does not equal this named interval. Otherwise
        false.

        Returns boolean.
        '''
        return not self == arg

    def __neg__(self):
        r'''Negates named interval.

        ::

            >>> -interval
            NamedInterval('-M9')

        Returns new named interval.
        '''
        return type(self)(self.quality_string, -self.number)

    def __rmul__(self, arg):
        r'''Multiplies `arg` by named interval.

        ::

            >>> interval * 3
            NamedInterval('+aug25')

        Returns new named interval.
        '''
        return self * arg

    def __str__(self):
        r'''String representation of named interval.

        ::

            >>> str(interval)
            '+M9'

        Returns string.
        '''
        return '{}{}{}'.format(
            self._direction_symbol,
            self._quality_abbreviation,
            abs(self.number),
            )

    def __sub__(self, arg):
        r'''Subtracts `arg` from named interval.

        ::

            >>> interval - pitchtools.NamedInterval('+M2')
            NamedInterval('+P8')

        Returns new named interval.
        '''
        from abjad.tools import pitchtools
        if not isinstance(arg, type(self)):
            message = 'must be named interval: {!r}.'.format(arg)
            raise TypeError(message)
        dummy_pitch = pitchtools.NamedPitch(0)
        new_pitch = dummy_pitch + self - arg
        return pitchtools.NamedInterval.from_pitch_carriers(
            dummy_pitch, new_pitch)

    ### PRIVATE PROPERTIES ###

    @property
    def _format_string(self):
        return '{}{}'.format(self._quality_abbreviation, self.number)

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

    @property
    def _storage_format_specification(self):
        from abjad.tools import systemtools
        positional_argument_values = (
            str(self),
            )
        return systemtools.StorageFormatSpecification(
            self,
            positional_argument_values=positional_argument_values,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def from_pitch_carriers(cls, pitch_carrier_1, pitch_carrier_2):
        '''Calculate named interval from `pitch_carrier_1` to
        `pitch_carrier_2`:

        ::

            >>> pitchtools.NamedInterval.from_pitch_carriers(
            ...     NamedPitch(-2),
            ...     NamedPitch(12),
            ...     )
            NamedInterval('+M9')

        Returns named interval.
        '''
        from abjad.tools import pitchtools
        pitch_1 = pitchtools.get_named_pitch_from_pitch_carrier(pitch_carrier_1)
        pitch_2 = pitchtools.get_named_pitch_from_pitch_carrier(pitch_carrier_2)
        degree_1 = pitch_1.diatonic_pitch_number
        degree_2 = pitch_2.diatonic_pitch_number
        named_interval_number = abs(degree_1 - degree_2) + 1
        numbered_interval_number = abs(abs(pitchtools.NumberedPitch(pitch_1))
            - abs(pitchtools.NumberedPitch(pitch_2)))
        absolute_named_interval = \
            pitchtools.spell_numbered_interval_number(
            named_interval_number, numbered_interval_number)
        if pitch_2 < pitch_1:
            named_interval = -absolute_named_interval
        else:
            named_interval = absolute_named_interval
        return cls(named_interval)

    ### PUBLIC PROPERTIES ###

    @property
    def direction_number(self):
        r'''Direction number of named interval.

        ::

            >>> interval.direction_number
            1

        Returns ``-1``, ``0`` or ``1``.
        '''
        if self.quality_string == 'perfect' and abs(self.number) == 1:
            return 0
        else:
            return mathtools.sign(self.number)

    @property
    def direction_string(self):
        r'''Direction string of named interval.

        ::

            >>> interval.direction_string
            'ascending'

        Returns ``'ascending'``, ``'descending'`` or none.
        '''
        if self.direction_number == -1:
            return 'descending'
        elif self.direction_number == 0:
            return None
        elif self.direction_number == 1:
            return 'ascending'

    @property
    def interval_class(self):
        r'''Interval class of named interval.

        ::

            >>> interval.interval_class
            2

        Returns nonnegative integer.
        '''
        return ((abs(self.number) - 1) % 7) + 1

    @property
    def interval_string(self):
        r'''Interval string of named interval.

        ::

            >>> interval.interval_string
            'ninth'

        Returns string.
        '''
        return self._interval_string

    @property
    def named_interval_class(self):
        r'''Named interval class of named interval.

        ::

            >>> interval.named_interval_class
            NamedInversionEquivalentIntervalClass('+M2')

        Returns named inversion-equivalent interval-class.
        '''
        from abjad.tools import pitchtools
        quality_string, number = self._quality_string, self.number
        return pitchtools.NamedInversionEquivalentIntervalClass(
            quality_string, number)

    @property
    def number(self):
        r'''Number of named interval.

        ::

            >>> interval.number
            9

        Returns nonnegative number.
        '''
        return self._number

    @property
    def quality_string(self):
        r'''Quality string of named interval.

        ::

            >>> interval.quality_string
            'major'

        Returns string.
        '''
        return self._quality_string

    @property
    def semitones(self):
        r'''Semitones of named interval.

        ::

            >>> interval.semitones
            14

        Returns number.
        '''
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
        perfect_interval_classes = (
            1,
            4,
            5,
            8,
            )
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
        if interval_class_number not in perfect_interval_classes and \
            self.quality_string == "augmented":
            result += 1
        if self.number < 0:
            result *= -1
        return result

    @property
    def staff_spaces(self):
        r'''Staff spaces of named interval.

        ::

            >>> interval.staff_spaces
            8

        Returns nonnegative integer.
        '''
        if self.direction_string == 'descending':
            return self.number + 1
        elif self.direction_string is None:
            return 0
        elif self.direction_string == 'ascending':
            return self.number - 1
