import abc
import functools
import numbers
from abjad import mathtools
from abjad.system.AbjadValueObject import AbjadValueObject
from . import constants


@functools.total_ordering
class PitchClass(AbjadValueObject):
    """
    Abstract pitch-class.
    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, argument):
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
            dpc_name = group_dict['diatonic_pc_name'].lower()
            dpc_number = constants._diatonic_pc_name_to_diatonic_pc_number[dpc_name]
            alteration = abjad.Accidental(group_dict['comprehensive_accidental']).semitones
            self._from_named_parts(dpc_number, alteration)
        elif isinstance(argument, numbers.Number):
            self._from_number(argument)
        elif isinstance(argument, (abjad.Pitch, abjad.PitchClass)):
            self._from_pitch_or_pitch_class(argument)
        else:
            try:
                pitch = abjad.NamedPitch(argument)
                self._from_pitch_or_pitch_class(pitch)
            except Exception:
                message = 'can not instantiate {} from {!r}.'
                message = message.format(type(self).__name__, argument)
                raise ValueError(message)

    ### SPECIAL METHODS ###

    def __float__(self):
        """
        Coerce to float.

        Returns float.
        """
        return float(self.number)

    def __format__(self, format_specification=''):
        """
        Formats pitch-class.

        Set `format_specification` to `''`, `'lilypond'` or `'storage'`.

        Returns string.
        """
        if format_specification == 'lilypond':
            return self._get_lilypond_format()
        return super().__format__(format_specification=format_specification)

    @abc.abstractmethod
    def __lt__(self, argument):
        """
        Is true when pitch-class is less than `argument`.

        Returns true or false.
        """
        raise NotImplementedError

    ### PRIVATE METHODS ###

    @abc.abstractmethod
    def _from_named_parts(self, dpc_number, alteration):
        raise NotImplementedError

    @abc.abstractmethod
    def _from_number(self, number):
        raise NotImplementedError

    @abc.abstractmethod
    def _from_pitch_or_pitch_class(self, pitch_or_pitch_class):
        raise NotImplementedError

    @abc.abstractmethod
    def _get_alteration(self):
        raise NotImplementedError

    @abc.abstractmethod
    def _get_diatonic_pc_number(self):
        raise NotImplementedError

    @abc.abstractmethod
    def _get_lilypond_format(self):
        raise NotImplementedError

    @staticmethod
    def _to_nearest_quarter_tone(number):
        number = round((float(number) % 12) * 4) / 4
        div, mod = divmod(number, 1)
        if mod == 0.75:
            div += 1
        elif mod == 0.5:
            div += 0.5
        div %= 12
        return mathtools.integer_equivalent_number_to_integer(div)

    ### PUBLIC PROPERTIES ###

    @abc.abstractproperty
    def accidental(self):
        """
        Gets accidental of pitch-class.
        """
        raise NotImplementedError

    @abc.abstractproperty
    def pitch_class_label(self):
        """
        Gets pitch-class label of pitch-class.
        """
        raise NotImplementedError

    ### PUBLIC METHODS ###

    @abc.abstractmethod
    def invert(self, axis=None):
        """
        Inverts pitch-class about `axis`.

        Returns new pitch-class.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def multiply(self, n=1):
        """
        Multiplies pitch-class by `n`.

        Returns new pitch-class.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def transpose(self, n=0):
        """
        Transposes pitch-class by index `n`.

        Returns new pitch-class.
        """
        raise NotImplementedError
