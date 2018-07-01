import abc
import copy
import functools
import numbers
from abjad import mathtools
from abjad.system.AbjadValueObject import AbjadValueObject
from . import constants


@functools.total_ordering
class IntervalClass(AbjadValueObject):
    """
    Abstract interval-class.
    """

    ### CLASS VARIABLES ###

    __slots__ = ()

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
        elif isinstance(argument, (abjad.Interval, abjad.IntervalClass)):
            self._from_interval_or_interval_class(argument)
        else:
            message = 'can not initialize {} from {!r}.'
            message = message.format(type(self).__name__, argument)
            raise ValueError(message)

    ### SPECIAL METHODS ###

    def __abs__(self):
        """
        Gets absolute value of interval-class.

        Returns new interval-class.
        """
        return type(self)(abs(self._number))

    @abc.abstractmethod
    def __add__(self, argument):
        """
        Adds `argument` to interval-class.

        Returns new interval-class.
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
        Is true when interval-class is less than `argument`.

        Returns true or false.
        """
        raise NotImplementedError

    def __str__(self):
        """
        Gets string representation of interval-class.

        Returns string.
        """
        return str(self.number)

    @abc.abstractmethod
    def __sub__(self, argument):
        """
        Subtracts `argument` from interval-class.

        Returns new interval-class.
        """
        raise NotImplementedError

    ### PRIVATE METHODS ###

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
        if base_quality == 'P' and octave_number and diatonic_pc_number == 1:
            return 12 * direction
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
        while abs(semitones) > 12:
            semitones = (abs(semitones) - 12) * mathtools.sign(semitones)
        semitones *= direction
        return mathtools.integer_equivalent_number_to_integer(semitones)

    @classmethod
    def _numbered_to_named(cls, number):
        number = cls._to_nearest_quarter_tone(float(number))
        direction = mathtools.sign(number)
        octaves, semitones = divmod(abs(number), 12)
        if semitones == 0 and octaves:
            semitones = 12
        quartertone = ''
        if semitones % 1:
            semitones -= 0.5
            quartertone = '+'
        quality, diatonic_pc_number = constants._semitones_to_quality_and_diatonic_number[semitones]
        quality += quartertone
        diatonic_pc_number = cls._to_nearest_quarter_tone(diatonic_pc_number)
        return direction, quality, diatonic_pc_number

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
    def number(self):
        """
        Gets number of interval-class.

        Returns number.
        """
        return self._number

    ### PUBLIC METHODS ###

    def transpose(self, pitch_carrier):
        """
        Transposes `pitch_carrier` by interval-class.

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
