import functools
import numbers
from . import constants
from abjad.system.AbjadValueObject import AbjadValueObject
from abjad.system.FormatSpecification import FormatSpecification


@functools.total_ordering
class StaffPosition(AbjadValueObject):
    """
    Staff position.

    ..  container:: example

        Initializes staff position at middle line of staff:

        >>> abjad.StaffPosition(0)
        StaffPosition(0)

    ..  container:: example

        Initializes staff position one space below middle line of staff:

        >>> abjad.StaffPosition(-1)
        StaffPosition(-1)

    ..  container:: example

        Initializes staff position one line below middle line of staff:

        >>> abjad.StaffPosition(-2)
        StaffPosition(-2)

    ..  container:: example

        Initializes from other staff position:

        >>> staff_position = abjad.StaffPosition(-2)
        >>> abjad.StaffPosition(staff_position)
        StaffPosition(-2)

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_number',
        )

    ### INITIALIZER ###

    def __init__(self, number=0):
        if isinstance(number, type(self)):
            number = number.number
        assert isinstance(number, numbers.Number), repr(number)
        self._number = number

    ### SPECIAL METHODS ###

    def __eq__(self, argument):
        """
        Is true when `argument` is a staff position with the same number as
        this staff position.

        ..  container:: example

            >>> staff_position_1 = abjad.StaffPosition(-2)
            >>> staff_position_2 = abjad.StaffPosition(-2)
            >>> staff_position_3 = abjad.StaffPosition(0)

            >>> staff_position_1 == staff_position_1
            True
            >>> staff_position_1 == staff_position_2
            True
            >>> staff_position_1 == staff_position_3
            False

            >>> staff_position_2 == staff_position_1
            True
            >>> staff_position_2 == staff_position_2
            True
            >>> staff_position_2 == staff_position_3
            False

            >>> staff_position_3 == staff_position_1
            False
            >>> staff_position_3 == staff_position_2
            False
            >>> staff_position_3 == staff_position_3
            True

        Returns true or false.
        """
        return super().__eq__(argument)

    def __hash__(self):
        """
        Hashes staff position.

        Returns integer.
        """
        return super().__hash__()

    def __lt__(self, argument):
        """
        Is true when staff position is less than `argument`.

        ..  container:: example

            >>> staff_position_1 = abjad.StaffPosition(-2)
            >>> staff_position_2 = abjad.StaffPosition(-2)
            >>> staff_position_3 = abjad.StaffPosition(0)

            >>> staff_position_1 < staff_position_1
            False
            >>> staff_position_1 < staff_position_2
            False
            >>> staff_position_1 < staff_position_3
            True

            >>> staff_position_2 < staff_position_1
            False
            >>> staff_position_2 < staff_position_2
            False
            >>> staff_position_2 < staff_position_3
            True

            >>> staff_position_3 < staff_position_1
            False
            >>> staff_position_3 < staff_position_2
            False
            >>> staff_position_3 < staff_position_3
            False

        Returns true or false.
        """
        try:
            argument = type(self)(argument)
        except Exception:
            return False
        return self.number < argument.number

    def __str__(self):
        """
        Gets string representation of staff position.

        ..  container:: example

            >>> str(abjad.StaffPosition(-2))
            'StaffPosition(-2)'

        Returns string.
        """
        return '{}({})'.format(type(self).__name__, self.number)

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        return FormatSpecification(
            client=self,
            repr_is_indented=False,
            storage_format_is_indented=False,
            storage_format_args_values=[self.number],
            storage_format_kwargs_names=[],
            )

    ### PUBLIC PROPERTIES ###

    @property
    def number(self):
        """
        Gets staff position number.

        ..  container:: example

            >>> abjad.StaffPosition(-2).number
            -2

        Returns number.
        """
        return self._number

    ### PUBLIC METHODS ###

    def to_pitch(self, clef='treble'):
        """
        Makes named pitch from staff position and `clef`.

        ..  container:: example

            Treble clef:

            >>> clef = abjad.Clef('treble')
            >>> for n in range(-6, 6):
            ...     staff_position = abjad.StaffPosition(n)
            ...     pitch = staff_position.to_pitch(clef=clef)
            ...     message = '{!s}\t{}'.format(staff_position, pitch)
            ...     print(message)
            ...
            StaffPosition(-6)	c'
            StaffPosition(-5)	d'
            StaffPosition(-4)	e'
            StaffPosition(-3)	f'
            StaffPosition(-2)	g'
            StaffPosition(-1)	a'
            StaffPosition(0)	b'
            StaffPosition(1)	c''
            StaffPosition(2)	d''
            StaffPosition(3)	e''
            StaffPosition(4)	f''
            StaffPosition(5)	g''

        ..  container:: example

            Bass clef:

            >>> clef = abjad.Clef('bass')
            >>> for n in range(-6, 6):
            ...     staff_position = abjad.StaffPosition(n)
            ...     pitch = staff_position.to_pitch(clef=clef)
            ...     message = '{!s}\t{}'.format(staff_position, pitch)
            ...     print(message)
            ...
            StaffPosition(-6)	e,
            StaffPosition(-5)	f,
            StaffPosition(-4)	g,
            StaffPosition(-3)	a,
            StaffPosition(-2)	b,
            StaffPosition(-1)	c
            StaffPosition(0)	d
            StaffPosition(1)	e
            StaffPosition(2)	f
            StaffPosition(3)	g
            StaffPosition(4)	a
            StaffPosition(5)	b

        ..  container:: example

            Alto clef:

            >>> clef = abjad.Clef('alto')
            >>> for n in range(-6, 6):
            ...     staff_position = abjad.StaffPosition(n)
            ...     pitch = staff_position.to_pitch(clef=clef)
            ...     message = '{!s}\t{}'.format(staff_position, pitch)
            ...     print(message)
            ...
            StaffPosition(-6)	d
            StaffPosition(-5)	e
            StaffPosition(-4)	f
            StaffPosition(-3)	g
            StaffPosition(-2)	a
            StaffPosition(-1)	b
            StaffPosition(0)	c'
            StaffPosition(1)	d'
            StaffPosition(2)	e'
            StaffPosition(3)	f'
            StaffPosition(4)	g'
            StaffPosition(5)	a'

        ..  container:: example

            Percussion clef:

            >>> clef = abjad.Clef('percussion')
            >>> for n in range(-6, 6):
            ...     staff_position = abjad.StaffPosition(n)
            ...     pitch = staff_position.to_pitch(clef=clef)
            ...     message = '{!s}\t{}'.format(staff_position, pitch)
            ...     print(message)
            ...
            StaffPosition(-6)	d
            StaffPosition(-5)	e
            StaffPosition(-4)	f
            StaffPosition(-3)	g
            StaffPosition(-2)	a
            StaffPosition(-1)	b
            StaffPosition(0)	c'
            StaffPosition(1)	d'
            StaffPosition(2)	e'
            StaffPosition(3)	f'
            StaffPosition(4)	g'
            StaffPosition(5)	a'

        Returns new named pitch.
        """
        import abjad
        clef = abjad.Clef(clef)
        offset_staff_position_number = self.number
        offset_staff_position_number -= clef.middle_c_position.number
        offset_staff_position = type(self)(offset_staff_position_number)
        octave_number = offset_staff_position.number // 7 + 4
        diatonic_pc_number = offset_staff_position.number % 7
        pitch_class_number = constants._diatonic_pc_number_to_pitch_class_number[
            diatonic_pc_number]
        pitch_number = 12 * (octave_number - 4)
        pitch_number += pitch_class_number
        named_pitch = abjad.NamedPitch(pitch_number)
        return named_pitch
