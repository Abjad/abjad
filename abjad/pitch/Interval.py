import abc
import copy
import functools
import numbers
from abjad import mathtools
from abjad.system.AbjadValueObject import AbjadValueObject
from . import constants


@functools.total_ordering
class Interval(AbjadValueObject):
    """
    Abstract interval.
    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_interval_class',
        '_octaves',
        )

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, argument):
        import abjad
        if isinstance(argument, str):
            match = constants._interval_name_abbreviation_regex.match(argument)
            if match is None:
                try:
                    argument = float(argument)
                    self._from_number(argument)
                    return
                except ValueError:
                    message = 'can not initialize {} from {!r}.'
                    message = message.format(type(self).__name__, argument)
                    raise ValueError(message)
                message = 'can not initialize {} from {!r}.'
                message = message.format(type(self).__name__, argument)
                raise ValueError(message)
            group_dict = match.groupdict()
            direction = group_dict['direction']
            if direction == '-':
                direction = -1
            else:
                direction = 1
            quality = group_dict['quality']
            diatonic_number = int(group_dict['number'])
            quality = self._validate_quality_and_diatonic_number(
                quality, diatonic_number,
            )
            quartertone = group_dict['quartertone']
            quality += quartertone
            self._from_named_parts(direction, quality, diatonic_number)
        elif isinstance(argument, tuple) and len(argument) == 2:
            quality, number = argument
            direction = mathtools.sign(number)
            diatonic_number = abs(number)
            quality = self._validate_quality_and_diatonic_number(
                quality, diatonic_number,
            )
            self._from_named_parts(direction, quality, diatonic_number)
        elif isinstance(argument, numbers.Number):
            self._from_number(argument)
        elif isinstance(argument, (Interval, abjad.IntervalClass)):
            self._from_interval_or_interval_class(argument)
        else:
            message = 'can not initialize {} from {!r}.'
            message = message.format(type(self).__name__, argument)
            raise ValueError(message)

    ### SPECIAL METHODS ###

    @abc.abstractmethod
    def __abs__(self):
        """
        Gets absolute value of interval.

        Returns new interval.
        """
        raise NotImplementedError

    def __float__(self):
        """
        Coerce to semitones as float.

        Returns float.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def __lt__(self, argument):
        """
        Is true when interval is less than `argument`.

        Returns true or false.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def __neg__(self):
        """
        Negates interval.

        Returns interval.
        """
        raise NotImplementedError

    def __str__(self):
        """
        Gets string representation of interval.

        Returns string.
        """
        return str(self.number)

    ### PRIVATE METHODS ###

    @abc.abstractmethod
    def _from_named_parts(self, direction, quality, diatonic_number):
        raise NotImplementedError

    @abc.abstractmethod
    def _from_number(self, argument):
        raise NotImplementedError

    @abc.abstractmethod
    def _from_interval_or_interval_class(self, argument):
        raise NotImplementedError

    @classmethod
    def _named_to_numbered(cls, direction, quality, diatonic_number):
        octave_number = 0
        diatonic_pc_number = abs(diatonic_number)
        while diatonic_pc_number >= 8:
            diatonic_pc_number -= 7
            octave_number += 1

        quartertone = ''
        if quality.endswith(('+', '~')):
            quality, quartertone = quality[:-1], quality[-1]

        base_quality = quality
        if len(quality) > 1:
            base_quality = quality[0]

        semitones = constants._diatonic_number_and_quality_to_semitones[
            diatonic_pc_number][base_quality]
        if base_quality == 'd':
            semitones -= (len(quality) - 1)
        elif base_quality == 'A':
            semitones += (len(quality) - 1)

        if quartertone == '+':
            semitones += 0.5
        elif quartertone == '~':
            semitones -= 0.5

        if abs(diatonic_number) == 1:
            semitones = abs(semitones)
        else:
            semitones += octave_number * 12
        semitones *= direction
        return mathtools.integer_equivalent_number_to_integer(semitones)

    @classmethod
    def _numbered_to_named(cls, number):
        number = cls._to_nearest_quarter_tone(float(number))
        direction = mathtools.sign(number)
        octaves, semitones = divmod(abs(number), 12)
        quartertone = ''
        if semitones % 1:
            semitones -= 0.5
            quartertone = '+'
        quality, diatonic_number = constants._semitones_to_quality_and_diatonic_number[semitones]
        quality += quartertone
        diatonic_number += octaves * 7
        diatonic_number = cls._to_nearest_quarter_tone(diatonic_number)
        return direction, quality, diatonic_number

    @staticmethod
    def _to_nearest_quarter_tone(number):
        number = round(float(number) * 4) / 4
        div, mod = divmod(number, 1)
        if mod == 0.75:
            div += 1
        elif mod == 0.5:
            div += 0.5
        return mathtools.integer_equivalent_number_to_integer(div)

    @classmethod
    def _validate_quality_and_diatonic_number(cls, quality, diatonic_number):
        if quality in constants._quality_string_to_quality_abbreviation:
            quality = constants._quality_string_to_quality_abbreviation[quality]
        if quality == 'aug':
            quality = 'A'
        if quality == 'dim':
            quality = 'd'
        octaves = 0
        diatonic_pc_number = diatonic_number
        while diatonic_pc_number > 7:
            diatonic_pc_number -= 7
            octaves += 1
        if constants._diatonic_number_and_quality_to_semitones.get(
            diatonic_pc_number, {}).get(quality[0]) is None:
            message = 'can not initialize {} from {!r} and {!r}.'
            message = message.format(cls.__name__, quality, diatonic_number)
            raise ValueError(message)
        return quality

    ### PUBLIC PROPERTIES ###

    @property
    def cents(self):
        """
        Gets cents of interval.

        Returns nonnegative number.
        """
        return 100 * self.semitones

    @abc.abstractproperty
    def direction_number(self):
        """
        Gets direction number of interval

        Returns integer.
        """
        raise NotImplementedError

    @abc.abstractproperty
    def interval_class(self):
        """
        Gets interval-class of interval.

        Returns interval-class.
        """
        raise NotImplementedError

    @abc.abstractproperty
    def number(self):
        """
        Gets number of interval.

        Returns integer.
        """
        raise NotImplementedError

    @abc.abstractproperty
    def octaves(self):
        """
        Gets octaves of interval.

        Returns nonnegative number.
        """
        raise NotImplementedError

    @abc.abstractproperty
    def semitones(self):
        """
        Gets semitones of interval.

        Returns integer or float.
        """
        raise NotImplementedError

    ### PUBLIC METHODS ###

    def transpose(self, pitch_carrier):
        """
        Transposes `pitch_carrier` by interval.

        Returns new pitch carrier.
        """
        import abjad
        if isinstance(pitch_carrier, (abjad.Pitch, abjad.PitchClass)):
            return pitch_carrier.transpose(self)
        elif isinstance(pitch_carrier, abjad.Note):
            new_note = copy.copy(pitch_carrier)
            new_pitch = pitch_carrier.written_pitch.transpose(self)
            new_note.written_pitch = new_pitch
            return new_note
        elif isinstance(pitch_carrier, abjad.Chord):
            new_chord = copy.copy(pitch_carrier)
            pairs = zip(new_chord.note_heads, pitch_carrier.note_heads)
            for new_nh, old_nh in pairs:
                new_pitch = old_nh.written_pitch.transpose(self)
                new_nh.written_pitch = new_pitch
            return new_chord
        return pitch_carrier
