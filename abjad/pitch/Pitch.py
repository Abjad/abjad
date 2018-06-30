import abc
import functools
import math
import numbers
from abjad import mathtools
from abjad.system.AbjadValueObject import AbjadValueObject
from abjad.system.StorageFormatManager import StorageFormatManager
from . import constants


@functools.total_ordering
class Pitch(AbjadValueObject):
    """
    Abstract pitch.
    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_pitch_class',
        '_octave',
        )

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, argument, accidental=None, arrow=None, octave=None):
        import abjad
        if isinstance(argument, str):
            match = constants._comprehensive_pitch_name_regex.match(argument)
            if not match:
                match = constants._comprehensive_pitch_class_name_regex.match(argument)
            if not match:
                message = 'can not instantiate {} from {!r}.'
                message = message.format(type(self).__name__, argument)
                raise ValueError(message)
            group_dict = match.groupdict()
            _dpc_name = group_dict['diatonic_pc_name'].lower()
            _dpc_number = constants._diatonic_pc_name_to_diatonic_pc_number[_dpc_name]
            _alteration = abjad.Accidental(group_dict['comprehensive_accidental']).semitones
            _octave = abjad.Octave(group_dict.get('comprehensive_octave', '')).number
            self._from_named_parts(_dpc_number, _alteration, _octave)
        elif isinstance(argument, numbers.Number):
            self._from_number(argument)
        elif isinstance(argument, (abjad.Pitch, abjad.PitchClass)):
            self._from_pitch_or_pitch_class(argument)
        elif isinstance(argument, tuple) and len(argument) == 2:
            _pitch_class = abjad.NamedPitchClass(argument[0])
            _octave = abjad.Octave(argument[1])
            self._from_named_parts(
                _pitch_class._get_diatonic_pc_number(),
                _pitch_class._get_alteration(),
                _octave.number,
            )
        elif hasattr(argument, 'written_pitch'):
            self._from_pitch_or_pitch_class(argument.written_pitch)
        elif isinstance(argument, abjad.Chord) and len(argument.note_heads):
            self._from_pitch_or_pitch_class(argument.note_heads[0])
        else:
            message = 'can not instantiate {} from {!r}.'
            message = message.format(type(self).__name__, argument)
            raise ValueError(message)
        if accidental is not None:
            accidental = abjad.Accidental(accidental)
            self._pitch_class = type(self._pitch_class)(
                self._pitch_class,
                accidental=accidental,
                )
        if arrow is not None:
            self._pitch_class = type(self._pitch_class)(
                self._pitch_class,
                arrow=arrow,
                )
        if octave is not None:
            octave = abjad.Octave(octave)
            self._octave = octave

    ### SPECIAL METHODS ###

    def __float__(self):
        """
        Coerce to float.

        Returns float.
        """
        return float(self.number)

    def __format__(self, format_specification=''):
        """
        Formats pitch.

        Set `format_specification` to `''`, `'lilypond'` or `'storage'`.

        Returns string.
        """
        if format_specification in ('', 'lilypond'):
            return self._get_lilypond_format()
        elif format_specification == 'storage':
            return StorageFormatManager(self).get_storage_format()
        return str(self)

    def __illustrate__(self):
        """
        Illustrates pitch.

        Returns LilyPond file.
        """
        import abjad
        pitch = abjad.NamedPitch(self)
        note = abjad.Note(pitch, 1)
        abjad.attach(abjad.Multiplier(1, 4), note)
        clef = abjad.Clef.from_selection([pitch])
        abjad.attach(clef, note)
        staff = abjad.Staff()
        staff.append(note)
        abjad.override(staff).time_signature.stencil = False
        lilypond_file = abjad.LilyPondFile.new(staff)
        return lilypond_file

    @abc.abstractmethod
    def __lt__(self, argument):
        """
        Is true when pitch is less than `argument`.

        Returns true or false.
        """
        raise NotImplementedError

    ### PRIVATE PROPERTIES ###

    @abc.abstractmethod
    def _get_lilypond_format(self):
        raise NotImplementedError

    @staticmethod
    def _to_nearest_octave(pitch_number, pitch_class_number):
        target_pc = pitch_number % 12
        down = (target_pc - pitch_class_number) % 12
        up = (pitch_class_number - target_pc) % 12
        if up < down:
            return pitch_number + up
        else:
            return pitch_number - down

    @staticmethod
    def _to_nearest_quarter_tone(number):
        number = round(float(number) * 4) / 4
        div, mod = divmod(number, 1)
        if mod == 0.75:
            div += 1
        elif mod == 0.5:
            div += 0.5
        return mathtools.integer_equivalent_number_to_integer(div)

    @staticmethod
    def _to_pitch_class_item_class(item_class):
        import abjad
        item_class = item_class or abjad.NumberedPitch
        if item_class in (abjad.NamedPitchClass, abjad.NumberedPitchClass):
            return item_class
        elif item_class is abjad.NamedPitch:
            return abjad.NamedPitchClass
        elif item_class is abjad.NumberedPitch:
            return abjad.NumberedPitchClass
        else:
            raise TypeError(item_class)

    @staticmethod
    def _to_pitch_item_class(item_class):
        import abjad
        item_class = item_class or abjad.NumberedPitch
        if item_class in (abjad.NamedPitch, abjad.NumberedPitch):
            return item_class
        elif item_class is abjad.NamedPitchClass:
            return abjad.NamedPitch
        elif item_class is abjad.NumberedPitchClass:
            return abjad.NumberedPitch
        else:
            raise TypeError(item_class)

    ### PUBLIC PROPERTIES ###

    @abc.abstractproperty
    def arrow(self):
        """
        Gets arrow of pitch.
        """
        raise NotImplementedError

    @abc.abstractproperty
    def hertz(self):
        """
        Gets frequency of pitch in Hertz.

        Returns float.
        """
        hertz = pow(2., (float(self.number) - 9.) / 12.) * 440.
        return hertz

    @abc.abstractproperty
    def name(self):
        """
        Gets name of pitch.

        Returns string.
        """
        raise NotImplementedError

    @abc.abstractproperty
    def number(self):
        """
        Gets number of pitch.

        Returns number.
        """
        raise NotImplementedError

    @abc.abstractproperty
    def octave(self):
        """
        Gets octave of pitch.

        Returns octave.
        """
        raise NotImplementedError

    @abc.abstractproperty
    def pitch_class(self):
        """
        Gets pitch-class of pitch.

        Returns pitch-class.
        """
        raise NotImplementedError

    ### PUBLIC METHODS ###

    @classmethod
    @abc.abstractmethod
    def from_hertz(class_, hertz):
        """
        Creates pitch from `hertz`.

        Returns new pitch.
        """
        midi = 9. + (12. * math.log(float(hertz) / 440., 2))
        pitch = class_(midi)
        return pitch

    @abc.abstractmethod
    def get_name(self, locale=None):
        """
        Gets name of pitch according to `locale`.

        Returns string.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def invert(self, axis=None):
        """
        Inverts pitch about `axis`.

        Interprets `axis` of none equal to middle C.

        Returns new pitch.
        """
        import abjad
        axis = axis or abjad.NamedPitch("c'")
        axis = type(self)(axis)
        interval = self - axis
        result = axis.transpose(interval)
        return result

    @abc.abstractmethod
    def multiply(self, n=1):
        """
        Multiplies pitch by `n`.

        Returns new pitch.
        """
        return type(self)(n * self.number)

    @abc.abstractmethod
    def transpose(self, n):
        """
        Transposes pitch by index `n`.

        Returns new pitch.
        """
        raise NotImplementedError
