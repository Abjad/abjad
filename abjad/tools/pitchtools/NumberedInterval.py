# -*- coding: utf-8 -*-
import copy
import functools
import numbers
from abjad.tools import mathtools
from abjad.tools.pitchtools.Interval import Interval


@functools.total_ordering
class NumberedInterval(Interval):
    '''Numbered interval.

    ..  container:: example

        Initializes from number of semitones:

        ::

            >>> numbered_interval = NumberedInterval(-14)
            >>> numbered_interval
            NumberedInterval(-14)

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_number',
        )

    ### INITIALIZER ###

    def __init__(self, argument=None):
        from abjad.tools import pitchtools
        if isinstance(argument, (int, float, int)):
            number = argument
        elif isinstance(argument, pitchtools.Interval):
            number = argument.semitones
        elif isinstance(argument, pitchtools.IntervalClass):
            interval_class = pitchtools.NumberedIntervalClass(argument)
            number = interval_class.number
        elif argument is None:
            number = 0
        else:
            message = 'can not initialize {}: {!r}.'
            message = message.format(type(self).__name__, argument)
            raise TypeError(message)
        self._number = mathtools.integer_equivalent_number_to_integer(number)

    ### SPECIAL METHODS ###

    def __abs__(self):
        r'''Absolute value of numbered interval.

        Returns new numbered interval.
        '''
        return type(self)(abs(self._number))

    def __add__(self, argument):
        r'''Adds `argument` to numbered interval.

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

        Returns new numbered interval.
        '''
        return type(self)(self.number)

    def __eq__(self, argument):
        r'''Is true when `argument` is a numbered interval with number equal to that of
        this numbered interval. Otherwise false.

        Returns true or false.
        '''
        if isinstance(argument, type(self)):
            if self.number == argument.number:
                return True
        return False

    def __float__(self):
        r'''Changes numbered interval to float.

        Returns float.
        '''
        return float(self._number)

    def __hash__(self):
        r'''Hashes numbered interval.

        Returns integer.
        '''
        return hash(repr(self))

    def __int__(self):
        r'''Changes numbered interval to integer.

        Returns integer.
        '''
        return int(self._number)

    def __lt__(self, argument):
        r'''Is true when `argument` is a numbered interval with same direction number
        as this numbered interval and with number greater than that of this
        numbered interval. Otherwise false.

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

        Returns new numbered interval.
        '''
        return type(self)(-self._number)

    def __str__(self):
        r'''String representation of numbered interval.

        Returns string.
        '''
        return self._format_string

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

    ### PRIVATE PROPERTIES ###

    @property
    def _format_string(self):
        return '{}{}'.format(self._direction_symbol, abs(self.number))

    ### PUBLIC PROPERTIES ###

    @property
    def direction_number(self):
        r'''Direction sign of numbered interval.

        ::

            >>> NumberedInterval(-14).direction_number
            -1

        Returns integer.
        '''
        return mathtools.sign(self.number)

    @property
    def direction_string(self):
        r'''Direction string of named interval.

        ::

            >>> NumberedInterval(-14).direction_string
            'descending'

        Returns ``'ascending'``, ``'descending'`` or none.
        '''
        if self.direction_number == -1:
            return 'descending'
        elif self.direction_number == 0:
            return None
        elif self.direction_number == 1:
            return 'ascending'

    @property
    def number(self):
        r'''Number of numbered interval.

        Returns number.
        '''
        return self._number

    @property
    def numbered_interval_number(self):
        r'''Number of numbered interval.

        ::

            >>> NumberedInterval(-14).numbered_interval_number
            -14

        Returns integer or float.
        '''
        return self._number

    @property
    def semitones(self):
        r'''Semitones corresponding to numbered interval.

        Returns nonnegative number.
        '''
        return self.number

    ### PUBLIC METHODS ###

    @classmethod
    def from_pitch_carriers(class_, pitch_carrier_1, pitch_carrier_2):
        '''Makes numbered interval from `pitch_carrier_1` and
        `pitch_carrier_2`.

        ::

            >>> NumberedInterval.from_pitch_carriers(
            ...     NamedPitch(-2),
            ...     NamedPitch(12),
            ...     )
            NumberedInterval(14)

        Returns numbered interval.
        '''
        from abjad.tools import pitchtools
        # get pitches
        pitch_1 = pitchtools.NamedPitch.from_pitch_carrier(pitch_carrier_1)
        pitch_2 = pitchtools.NamedPitch.from_pitch_carrier(pitch_carrier_2)
        # get difference in semitones
        number = pitchtools.NumberedPitch(pitch_2).pitch_number - \
            pitchtools.NumberedPitch(pitch_1).pitch_number
        # change 1.0, 2.0, ... into 1, 2, ...
        number = mathtools.integer_equivalent_number_to_integer(number)
        # return numbered interval
        return class_(number)

    def to_named_interval(self, staff_positions):
        r'''Changes numbered interval to named interval that encompasses
        `staff_positions`.

        ..  container:: example

            ::

                >>> numbered_interval = NumberedInterval(1)
                >>> numbered_interval.to_named_interval(2)
                NamedInterval('+m2')

        Returns named interval.
        '''
        from abjad.tools import pitchtools
        direction_number = mathtools.sign(self.number)
        if staff_positions == 1:
            quality_string = None
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
                return pitchtools.NamedInterval(self.number)
            named_interval = pitchtools.NamedInterval(
                quality_string, staff_positions)
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
        named_interval = pitchtools.NamedInterval(
            quality_string,
            staff_positions,
            )
        return named_interval

    def transpose(self, pitch_carrier):
        r'''Transposes `pitch_carrier`.

        ..  container:: example

            Transposes chord:

            ::

                >>> chord = Chord("<c' e' g'>4")

            ::

                >>> interval = NumberedInterval(1)
                >>> interval.transpose(chord)
                Chord("<cs' f' af'>4")

        Returns new (copied) object of `pitch_carrier` type.
        '''
        from abjad.tools import pitchtools
        from abjad.tools import scoretools
        if isinstance(pitch_carrier, pitchtools.Pitch):
            number = pitch_carrier.pitch_number + self.semitones
            return type(pitch_carrier)(number)
        elif isinstance(pitch_carrier, numbers.Number):
            pitch_carrier = pitchtools.NumberedPitch(pitch_carrier)
            result = self.transpose(pitch_carrier)
            return result.pitch_number
        elif isinstance(pitch_carrier, scoretools.Note):
            new_note = copy.copy(pitch_carrier)
            number = pitchtools.NumberedPitch(pitch_carrier.written_pitch).pitch_number
            number += self.number
            new_pitch = pitchtools.NamedPitch(number)
            new_note.written_pitch = new_pitch
            return new_note
        elif isinstance(pitch_carrier, scoretools.Chord):
            new_chord = copy.copy(pitch_carrier)
            pairs = zip(new_chord.note_heads, pitch_carrier.note_heads)
            for new_nh, old_nh in pairs:
                number = \
                    pitchtools.NumberedPitch(old_nh.written_pitch).pitch_number
                number += self.number
                new_pitch = pitchtools.NamedPitch(number)
                new_nh.written_pitch = new_pitch
            return new_chord
        else:
            return pitch_carrier
