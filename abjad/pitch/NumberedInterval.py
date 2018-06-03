import copy
import numbers
from abjad import mathtools
from abjad.pitch.Interval import Interval
from . import constants


class NumberedInterval(Interval):
    '''Numbered interval.

    ..  container:: example

        Initializes from number of semitones:

        >>> abjad.NumberedInterval(-14)
        NumberedInterval(-14)

    ..  container:: example

        Initializes from other numbered interval

        >>> abjad.NumberedInterval(abjad.NumberedInterval(-14))
        NumberedInterval(-14)

    ..  container:: example

        Initializes from named interval:

        >>> abjad.NumberedInterval(abjad.NamedInterval('-P4'))
        NumberedInterval(-5)

    ..  container:: example

        Initializes from interval string:

        >>> abjad.NumberedInterval('-P4')
        NumberedInterval(-5)

    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self, number=0):
        super().__init__(number or 0)

    ### SPECIAL METHODS ###

    def __abs__(self):
        r'''Absolute value of numbered interval.

        ..  container:: example

            >>> abs(abjad.NumberedInterval(-14))
            NumberedInterval(14)

        Returns new numbered interval.
        '''
        return type(self)(abs(self.number))

    def __add__(self, argument):
        r'''Adds `argument` to numbered interval.

        ..  container:: example

            >>> abjad.NumberedInterval(3) + abjad.NumberedInterval(14)
            NumberedInterval(17)

            >>> abjad.NumberedInterval(3) + abjad.NumberedInterval(-14)
            NumberedInterval(-11)

        Returns new numbered interval.
        '''
        if isinstance(argument, type(self)):
            number = self.number + argument.number
            return type(self)(number)
        message = 'must be {}: {!r}.'
        message = message.format(type(self), argument)
        raise TypeError(message)

    def __copy__(self):
        r'''Copies numbered interval.

        >>> import copy

        ..  container:: example

            >>> copy.copy(abjad.NumberedInterval(-14))
            NumberedInterval(-14)

        Returns new numbered interval.
        '''
        return type(self)(self.number)

    def __eq__(self, argument):
        r'''Is true when `argument` is a numbered interval with number equal to that of
        this numbered interval.

        ..  container:: example

            >>> interval_1 = abjad.NumberedInterval(12)
            >>> interval_2 = abjad.NumberedInterval(12)
            >>> interval_3 = abjad.NumberedInterval(13)

            >>> interval_1 == interval_1
            True
            >>> interval_1 == interval_2
            True
            >>> interval_1 == interval_3
            False

            >>> interval_2 == interval_1
            True
            >>> interval_2 == interval_2
            True
            >>> interval_2 == interval_3
            False

            >>> interval_3 == interval_1
            False
            >>> interval_3 == interval_2
            False
            >>> interval_3 == interval_3
            True

        Returns true or false.
        '''
        return super(NumberedInterval, self).__eq__(argument)

    def __float__(self):
        r'''Coerce to float.

        Returns float.
        '''
        return float(self.number)

    def __hash__(self):
        r'''Hashes numbered interval.

        Returns integer.
        '''
        return super(NumberedInterval, self).__hash__()

    def __lt__(self, argument):
        r'''Is true when `argument` is a numbered interval with same direction
        number as this numbered interval and with number greater than that of
        this numbered interval.

        ..  container:: example

            >>> interval_1 = abjad.NumberedInterval(12)
            >>> interval_2 = abjad.NumberedInterval(12)
            >>> interval_3 = abjad.NumberedInterval(13)

            >>> interval_1 < interval_1
            False

            >>> interval_1 < interval_2
            False

            >>> interval_1 < interval_3
            True

            >>> interval_2 < interval_1
            False

            >>> interval_2 < interval_2
            False

            >>> interval_2 < interval_3
            True

            >>> interval_3 < interval_1
            False

            >>> interval_3 < interval_2
            False

            >>> interval_3 < interval_3
            False

        Returns true or false.
        '''
        if not isinstance(argument, type(self)):
            message = 'must be numbered interval: {!r}.'
            message = message.format(argument)
            raise TypeError(message)
        if not self.direction_number == argument.direction_number:
            message = 'can only compare intervals of same direction.'
            raise ValueError(message)
        return abs(self.number) < abs(argument.number)

    def __neg__(self):
        r'''Negates numbered interval.

        ..  container:: example

            >>> -abjad.NumberedInterval(-14)
            NumberedInterval(14)

        Returns new numbered interval.
        '''
        return type(self)(-self.number)

    def __radd__(self, argument):
        r'''Adds numbered interval to `argument`.

        ..  container:: example

            >>> interval = abjad.NumberedInterval(14)
            >>> abjad.NumberedInterval(3).__radd__(interval)
            NumberedInterval(17)

            >>> interval = abjad.NumberedInterval(-14)
            >>> abjad.NumberedInterval(3).__radd__(interval)
            NumberedInterval(-11)

        Returns new numbered interval.
        '''
        if not isinstance(argument, type(self)):
            message = '{!r} must be {}.'
            message = message.format(argument, type(self))
            raise TypeError(message)
        return argument.__add__(self)

    def __str__(self):
        r'''String representation of numbered interval.

        Returns string.
        '''
        direction_symbol = constants._direction_number_to_direction_symbol[
            mathtools.sign(self.number)]
        return '{}{}'.format(direction_symbol, abs(self.number))

    def __sub__(self, argument):
        r'''Subtracts `argument` from numbered interval.

        Returns new numbered interval.
        '''
        if isinstance(argument, type(self)):
            number = self.number - argument.number
            return type(self)(number)
        message = 'must be {}: {!r}.'
        message = message.format(type(self), argument)
        raise TypeError(message)

    ### PRIVATE METHODS ###

    def _from_named_parts(self, direction, quality, diatonic_number):
        self._from_number(self._named_to_numbered(
            direction,
            quality,
            diatonic_number,
            ))

    def _from_number(self, argument):
        import abjad
        number = self._to_nearest_quarter_tone(argument)
        direction = mathtools.sign(number)
        octaves = 0
        pc_number = abs(number)
        while pc_number > 12:
            pc_number -= 12
            octaves += 1
        self._octaves = octaves
        self._interval_class = abjad.NumberedIntervalClass(
            pc_number * direction)

    def _from_interval_or_interval_class(self, argument):
        self._from_number(float(argument))

    def _get_format_specification(self):
        import abjad
        values = [self.number]
        return abjad.FormatSpecification(
            client=self,
            coerce_for_equality=True,
            repr_is_indented=False,
            storage_format_is_indented=False,
            storage_format_args_values=values,
            )

    ### PUBLIC PROPERTIES ###

    @property
    def direction_number(self):
        r'''Gets direction number of numbered interval.

        ..  container:: example

            >>> abjad.NumberedInterval(-14).direction_number
            -1

            >>> abjad.NumberedInterval(0).direction_number
            0

            >>> abjad.NumberedInterval(6).direction_number
            1

        Returns integer.
        '''
        return mathtools.sign(self.number)

    @property
    def interval_class(self):
        r'''Gets interval class of numbered interval.

        Returns numbered interval-class.
        '''
        return self._interval_class

    @property
    def number(self):
        r'''Gets number of numbered interval.

        ..  container:: example

            >>> abjad.NumberedInterval(-14).number
            -14

            >>> abjad.NumberedInterval(-2).number
            -2

            >>> abjad.NumberedInterval(0).number
            0

        Returns number.
        '''
        number = self._interval_class._number
        direction = mathtools.sign(number)
        number = abs(number) + (12 * self.octaves)
        return number * direction

    @property
    def octaves(self):
        r'''Gets octaves of interval.

        Returns nonnegative number.
        '''
        return self._octaves

    @property
    def semitones(self):
        r'''Gets semitones corresponding to numbered interval.

        ..  container:: example

            >>> abjad.NumberedInterval(-14).semitones
            -14

        Returns nonnegative number.
        '''
        return self.number

    ### PUBLIC METHODS ###

    @classmethod
    def from_pitch_carriers(class_, pitch_carrier_1, pitch_carrier_2):
        '''Makes numbered interval from `pitch_carrier_1` and
        `pitch_carrier_2`.

        ..  container:: example

            >>> abjad.NumberedInterval.from_pitch_carriers(
            ...     abjad.NamedPitch(-2),
            ...     abjad.NamedPitch(12),
            ...     )
            NumberedInterval(14)

            >>> abjad.NumberedInterval.from_pitch_carriers(
            ...     abjad.NamedPitch(12),
            ...     abjad.NamedPitch(12),
            ...     )
            NumberedInterval(0)

            >>> abjad.NumberedInterval.from_pitch_carriers(
            ...     abjad.NamedPitch(9),
            ...     abjad.NamedPitch(12),
            ...     )
            NumberedInterval(3)

            >>> abjad.NumberedInterval.from_pitch_carriers(
            ...     abjad.NamedPitch(12),
            ...     abjad.NamedPitch(9),
            ...     )
            NumberedInterval(-3)

            >>> abjad.NumberedInterval.from_pitch_carriers(
            ...     abjad.NamedPitch(12),
            ...     abjad.NamedPitch(-2),
            ...     )
            NumberedInterval(-14)

        Returns numbered interval.
        '''
        import abjad.pitch
        pitch_1 = abjad.pitch.NamedPitch(pitch_carrier_1)
        pitch_2 = abjad.pitch.NamedPitch(pitch_carrier_2)
        number = abjad.pitch.NumberedPitch(pitch_2).number - \
            abjad.pitch.NumberedPitch(pitch_1).number
        number = mathtools.integer_equivalent_number_to_integer(number)
        return class_(number)

    def to_named_interval(self, staff_positions):
        r'''Changes numbered interval to named interval that encompasses
        `staff_positions`.

        ..  container:: example

            >>> abjad.NumberedInterval(0).to_named_interval(1)
            NamedInterval('P1')

            >>> abjad.NumberedInterval(0).to_named_interval(2)
            NamedInterval('+d2')

        ..  container:: example

            >>> abjad.NumberedInterval(1).to_named_interval(1)
            NamedInterval('+A1')

            >>> abjad.NumberedInterval(1).to_named_interval(2)
            NamedInterval('+m2')

        ..  container:: example

            >>> abjad.NumberedInterval(-1).to_named_interval(1)
            NamedInterval('-A1')

            >>> abjad.NumberedInterval(-1).to_named_interval(2)
            NamedInterval('-m2')

        ..  container:: example

            >>> abjad.NumberedInterval(2).to_named_interval(2)
            NamedInterval('+M2')

        Returns named interval.
        '''
        import abjad
        direction_number = mathtools.sign(self.number)
        quality_string = None
        if staff_positions == 1:
            if self.number % 12 == 11:
                quality_string = 'augmented'
            elif self.number % 12 == 0:
                quality_string = 'perfect'
            elif self.number % 12 == 1:
                quality_string = 'augmented'
            if not direction_number == 0:
                staff_positions *= direction_number
            if quality_string is None:
                # TODO: handle double-augmented named intervals
                return abjad.NamedInterval(self.number)
            named_interval = abjad.NamedInterval((
                quality_string,
                staff_positions,
                ))
            return named_interval
        named_interval_class_number = staff_positions % 7
        numbered_interval_class_number = abs(self.number) % 12
        if named_interval_class_number == 0:
            if numbered_interval_class_number == 9:
                quality_string = 'diminished'
            elif numbered_interval_class_number == 10:
                quality_string = 'minor'
            elif numbered_interval_class_number == 11:
                quality_string = 'major'
            elif numbered_interval_class_number == 0:
                quality_string = 'augmented'
        elif named_interval_class_number == 1:
            if numbered_interval_class_number == 11:
                quality_string = 'diminished'
            elif numbered_interval_class_number == 0:
                quality_string = 'perfect'
            elif numbered_interval_class_number == 1:
                quality_string = 'augmented'
        elif named_interval_class_number == 2:
            if numbered_interval_class_number == 0:
                quality_string = 'diminished'
            elif numbered_interval_class_number == 1:
                quality_string = 'minor'
            elif numbered_interval_class_number == 2:
                quality_string = 'major'
            elif numbered_interval_class_number == 3:
                quality_string = 'augmented'
        elif named_interval_class_number == 3:
            if numbered_interval_class_number == 2:
                quality_string = 'diminished'
            elif numbered_interval_class_number == 3:
                quality_string = 'minor'
            elif numbered_interval_class_number == 4:
                quality_string = 'major'
            elif numbered_interval_class_number == 5:
                quality_string = 'augmented'
        elif named_interval_class_number == 4:
            if numbered_interval_class_number == 4:
                quality_string = 'diminished'
            elif numbered_interval_class_number == 5:
                quality_string = 'perfect'
            elif numbered_interval_class_number == 6:
                quality_string = 'augmented'
        elif named_interval_class_number == 5:
            if numbered_interval_class_number == 6:
                quality_string = 'diminished'
            elif numbered_interval_class_number == 7:
                quality_string = 'perfect'
            elif numbered_interval_class_number == 8:
                quality_string = 'augmented'
        elif named_interval_class_number == 6:
            if numbered_interval_class_number == 7:
                quality_string = 'diminished'
            elif numbered_interval_class_number == 8:
                quality_string = 'minor'
            elif numbered_interval_class_number == 9:
                quality_string = 'major'
            elif numbered_interval_class_number == 10:
                quality_string = 'augmented'
        elif named_interval_class_number == 7:
            if numbered_interval_class_number == 9:
                quality_string = 'diminished'
            elif numbered_interval_class_number == 10:
                quality_string = 'minor'
            elif numbered_interval_class_number == 11:
                quality_string = 'major'
            elif numbered_interval_class_number == 0:
                quality_string = 'augmented'
        elif named_interval_class_number == 8:
            if numbered_interval_class_number == 11:
                quality_string = 'diminished'
            elif numbered_interval_class_number == 0:
                quality_string = 'perfect'
            elif numbered_interval_class_number == 1:
                quality_string = 'augmented'
        if not direction_number == 0:
            staff_positions *= direction_number
        if quality_string is None:
            # TODO: It is possible to for quality string to *never* get set to
            #       anything, generally during inversion with double-sharps or
            #       double-flats. This suite provides a sane result.
            #       Don't remove it - fix whatever's allowing quality string to
            #       remain unset.
            return abjad.NamedInterval(self.number)
        named_interval = abjad.NamedInterval((
            quality_string,
            staff_positions,
            ))
        return named_interval

    def transpose(self, pitch_carrier):
        r'''Transposes `pitch_carrier`.

        ..  container:: example

            Transposes chord:

            >>> chord = abjad.Chord("<c' e' g'>4")

            >>> interval = abjad.NumberedInterval(1)
            >>> interval.transpose(chord)
            Chord("<cs' f' af'>4")

        Returns newly constructed object of `pitch_carrier` type.
        '''
        import abjad
        if isinstance(pitch_carrier, abjad.Pitch):
            number = pitch_carrier.number + self.semitones
            return type(pitch_carrier)(number)
        elif isinstance(pitch_carrier, numbers.Number):
            pitch_carrier = abjad.NumberedPitch(pitch_carrier)
            result = self.transpose(pitch_carrier)
            return result.number
        elif isinstance(pitch_carrier, abjad.Note):
            new_note = copy.copy(pitch_carrier)
            number = abjad.NumberedPitch(pitch_carrier.written_pitch)
            number = number.number
            number += self.number
            new_pitch = abjad.NamedPitch(number)
            new_note.written_pitch = new_pitch
            return new_note
        elif isinstance(pitch_carrier, abjad.Chord):
            new_chord = copy.copy(pitch_carrier)
            pairs = zip(new_chord.note_heads, pitch_carrier.note_heads)
            for new_nh, old_nh in pairs:
                number = \
                    abjad.NumberedPitch(old_nh.written_pitch).number
                number += self.number
                new_pitch = abjad.NamedPitch(number)
                new_nh.written_pitch = new_pitch
            return new_chord
        else:
            return pitch_carrier
