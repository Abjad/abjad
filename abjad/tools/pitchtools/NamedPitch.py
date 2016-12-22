# -*- coding: utf-8 -*-
import collections
import math
import numbers
from abjad.tools import mathtools
from abjad.tools import stringtools
from abjad.tools.pitchtools.Pitch import Pitch


class NamedPitch(Pitch):
    '''Named pitch.

    ..  container:: example

        Initializes from pitch name:

        ::

            >>> pitch = NamedPitch("cs''")
            >>> show(pitch) # doctest: +SKIP

    ..  container:: example

        Initializes from pitch-class / octave string:

        ::

            >>> pitch = NamedPitch('C#5')
            >>> show(pitch) # doctest: +SKIP

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_alteration_in_semitones',
        '_diatonic_pitch_class_number',
        '_octave_number',
        )

    ### INITIALIZER ###

    def __init__(self, *arguments):
        from abjad.tools import pitchtools
        if (
            arguments and
            isinstance(arguments[0], collections.Iterable) and
            not stringtools.is_string(arguments[0]) and
            len(arguments) == 1
            ):
            arguments = arguments[0]
        if len(arguments) == 1:
            if isinstance(arguments[0], (int, float)):
                argument = mathtools.integer_equivalent_number_to_integer(
                    float(arguments[0]))
                self._initialize_by_pitch_number(argument)
            elif isinstance(arguments[0], type(self)):
                self._initialize_by_named_pitch(*arguments)
            elif isinstance(arguments[0], pitchtools.NumberedPitch):
                self._initialize_by_pitch_number(
                    arguments[0].pitch_number)
            elif isinstance(arguments[0], pitchtools.PitchClass):
                self._initialize_by_named_pitch_class_and_octave_number(
                    pitchtools.NamedPitchClass(arguments[0]), 4)
            elif hasattr(arguments[0], 'named_pitch'):
                self._initialize_by_named_pitch(arguments[0].named_pitch)
            elif self.is_pitch_class_octave_number_string(arguments[0]):
                self._initialize_by_pitch_class_octave_number_string(*arguments)
            elif isinstance(arguments[0], str):
                self._initialize_by_pitch_name(*arguments)
            else:
                message = 'can not initialize {} from {!r}.'
                message = message.format(type(self).__name__, arguments)
                raise ValueError(message)
        elif len(arguments) == 2:
            if isinstance(arguments[0], str):
                self._initialize_by_pitch_class_name_and_octave_number(
                    *arguments)
            elif isinstance(arguments[0], pitchtools.NamedPitchClass):
                self._initialize_by_named_pitch_class_and_octave_number(
                    *arguments)
            elif isinstance(arguments[0], (int, float)):
                if isinstance(arguments[1], str):
                    self._initialize_by_pitch_number_and_diatonic_pitch_class_name(
                        *arguments)
                elif isinstance(arguments[1], (int, float)):
                    self._initialize_by_pitch_number_and_octave_number(
                        *arguments)
                elif isinstance(arguments[1], pitchtools.NamedPitchClass):
                    self._initialize_by_pitch_number_and_named_pitch_class(
                        *arguments)
                else:
                    message = 'can not initialize {}: {!r}.'
                    message = message.format(type(self).__name__, arguments)
                    raise TypeError(message)
            else:
                message = 'can not initialize {}: {!r}.'
                message = message.format(type(self).__name__, arguments)
                raise ValueError(message)
        elif len(arguments) == 0:
            self._initialize_by_pitch_class_name_and_octave_number('c', 4)
        else:
            message = 'can not initialize {}: {!r}.'
            message = message.format(type(self).__name__, arguments)
            raise ValueError(message)

    ### SPECIAL METHODS ###

    def __add__(self, interval):
        r'''Adds named pitch to `interval`.

        ..  container:: example

            Adds an ascending major second to C#5:

            ::

                >>> NamedPitch("cs''") + NamedInterval('+M2')
                NamedPitch("ds''")

        ..  container:: example

            Adds a descending major second to C#5:

            ::

                >>> NamedPitch("cs''") + NamedInterval('-M2')
                NamedPitch("b'")

        Returns new named pitch.
        '''
        from abjad.tools import pitchtools
        interval = pitchtools.NamedInterval(interval)
        pitch = interval.transpose(self)
        return pitch

    def __copy__(self, *arguments):
        r'''Copies named pitch.

        ..  container:: example

            Copies C#5:

            ::

                >>> import copy
                >>> copy.copy(NamedPitch("cs''"))
                NamedPitch("cs''")

        ..  container:: example

            Copies Db5:

            ::

                >>> copy.copy(NamedPitch("df''"))
                NamedPitch("df''")

        Returns new named pitch.
        '''
        return type(self)(self)

    def __eq__(self, argument):
        r'''Is true when `argument` is a named pitch equal to this named pitch.
        Otherwise false.

        ..  container:: example

            C#5 equals C#5:

            ::

                >>> NamedPitch('C#5') == NamedPitch("cs''")
                True

        ..  container:: example

            C#5 does not equal Db5:

            ::

                >>> NamedPitch('C#5') == NamedPitch('Db5')
                False

        Returns true or false.
        '''
        try:
            argument = type(self)(argument)
            if str(self) == str(argument):
                return True
            return False
        except (TypeError, ValueError):
            return False

    def __float__(self):
        r'''Changes named pitch to float.

        ..  container:: example

            Changes C#5 to float:

            ::

                >>> float(NamedPitch('C#5'))
                13.0

        ..  container:: example

            Changes Ctqs5 to float:

            ::

                >>> float(NamedPitch('C#+5'))
                13.5

        Returns float.
        '''
        return float(self.pitch_number)

    def __ge__(self, argument):
        r'''Is true when named pitch is greater than or equal to `argument`.
        Otherwise false.

        Returns true or false.
        '''
        from abjad.tools import pitchtools
        if isinstance(argument, type(self)):
            return self.diatonic_pitch_number > argument.diatonic_pitch_number or \
                (self.diatonic_pitch_number == argument.diatonic_pitch_number and
                self.alteration_in_semitones >= argument.alteration_in_semitones)
        elif isinstance(argument, pitchtools.PitchRange):
            return self >= argument.stop_pitch
        else:
            try:
                argument = type(self)(argument)
                return self.__ge__(argument)
            except (TypeError, ValueError):
                pass
        return False

    def __getnewargs__(self):
        r'''Gets new arguments.

        Returns tuple.
        '''
        return (self.pitch_name,)

    def __gt__(self, argument):
        r'''Is true when named pitch is greater than `argument`. Otherwise false.

        Returns true or false.
        '''
        from abjad.tools import pitchtools
        if isinstance(argument, type(self)):
            return (self.diatonic_pitch_number > argument.diatonic_pitch_number or
                (self.diatonic_pitch_number == argument.diatonic_pitch_number and
                self.alteration_in_semitones > argument.alteration_in_semitones))
        elif isinstance(argument, pitchtools.PitchRange):
            return self > argument.stop_pitch
        else:
            try:
                argument = type(self)(argument)
                return self.__gt__(argument)
            except (TypeError, ValueError):
                pass
        return False

    def __hash__(self):
        r'''Required to be explicitly redefined on Python 3 if
        __eq__ changes.

        Returns integer.
        '''
        return super(NamedPitch, self).__hash__()

    def __int__(self):
        r'''Changes named pitch to integer.

        ..  container:: example

            Changes C#5 to integer:

            ::

                >>> int(NamedPitch('C#5'))
                13

        ..  container:: example

            Changes Db5 to integer:

            ::

                >>> int(NamedPitch('Db5'))
                13

        Returns integer.
        '''
        if not mathtools.is_integer_equivalent_number(self.pitch_number):
            raise TypeError
        return int(self.pitch_number)

    def __le__(self, argument):
        r'''Is true when named pitch is less than or equal to `argument`. Otherwise
        false.

        Returns true or false.
        '''
        from abjad.tools import pitchtools
        if isinstance(argument, type(self)):
            if not self.diatonic_pitch_number == argument.diatonic_pitch_number:
                return self.diatonic_pitch_number <= argument.diatonic_pitch_number
            if not self.alteration_in_semitones == argument.alteration_in_semitones:
                return self.alteration_in_semitones <= \
                    argument.alteration_in_semitones
            return True
        elif isinstance(argument, pitchtools.PitchRange):
            return self <= argument.start_pitch
        else:
            try:
                argument = type(self)(argument)
                return self.__le__(argument)
            except (TypeError, ValueError):
                pass
        return False

    def __lt__(self, argument):
        r'''Is true when named pitch is less than `argument`. Otherwise false.

        Returns true or false.
        '''
        from abjad.tools import pitchtools
        if isinstance(argument, type(self)):
            return (self.diatonic_pitch_number < argument.diatonic_pitch_number or
                (self.diatonic_pitch_number == argument.diatonic_pitch_number and
                self.alteration_in_semitones < argument.alteration_in_semitones))
        elif isinstance(argument, pitchtools.PitchRange):
            return self < argument.start_pitch
        elif argument is None:
            return True
        else:
            try:
                argument = type(self)(argument)
                return self.__lt__(argument)
            except (TypeError, ValueError):
                pass
        return False

    def __ne__(self, argument):
        r'''Is true when named pitch does not equal `argument`. Otherwise false.

        ..  container:: example

            C#5 is not equal to D#5:

            ::

                >>> NamedPitch("cs''") != NamedPitch("ds''")
                True

        ..  container:: example

            C#5 is equal to C#5:

            ::

                >>> NamedPitch("cs''") != NamedPitch("cs''")
                False

        Returns true or false.
        '''
        return not self == argument

    def __str__(self):
        r'''Gets string representation of named pitch.

        ..  container:: example

            Gets string representation of C#5:

            ::

                >>> str(NamedPitch("cs''"))
                "cs''"

        ..  container:: example

            Gets string representation of Db5:

            ::

                >>> str(NamedPitch("df''"))
                "df''"

        Returns string.
        '''
        return self.pitch_name

    def __sub__(self, argument):
        r'''Subtracts `argument` from named pitch.

        ..  container:: example

            Subtracts B4 from C#5:

            ::

                >>> NamedPitch("cs''") - NamedPitch("b'")
                NamedInterval('-M2')

        ..  container:: example

            Subtracts F#5 from C#5:

            ::

                >>> NamedPitch("cs''") - NamedPitch("fs''")
                NamedInterval('+P4')

        Returns named interval.
        '''
        from abjad.tools import pitchtools
        if isinstance(argument, type(self)):
            return pitchtools.NamedInterval.from_pitch_carriers(self, argument)
        interval = pitchtools.NamedInterval(argument)
        interval = -interval
        pitch = interval.transpose(self)
        return pitch

    ### PRIVATE METHODS ###

    def _get_lilypond_format(self):
        return str(self)

    def _initialize_by_named_pitch(self, named_pitch):
        self._alteration_in_semitones = named_pitch._alteration_in_semitones
        self._diatonic_pitch_class_number = \
            named_pitch.diatonic_pitch_class_number
        self._octave_number = named_pitch.octave.number

    def _initialize_by_named_pitch_class_and_octave_number(
        self, named_pitch_class, octave_number):
        self._alteration_in_semitones = \
            named_pitch_class._alteration_in_semitones
        self._diatonic_pitch_class_number = \
            named_pitch_class._diatonic_pitch_class_number
        self._octave_number = int(octave_number)

    def _initialize_by_pitch_class_name_and_octave_number(
        self, pitch_class_name, octave_number):
        from abjad.tools import pitchtools
        named_pitch_class = pitchtools.NamedPitchClass(pitch_class_name)
        self._initialize_by_named_pitch_class_and_octave_number(
            named_pitch_class, octave_number)

    def _initialize_by_pitch_class_name_octave_number_pair(self, pair):
        pitch_class_name, octave_number = pair
        self._initialize_by_pitch_class_name_and_octave_number(
            pitch_class_name, octave_number)

    def _initialize_by_pitch_class_octave_number_string(
        self, pitch_class_octave_number_string):
        from abjad.tools import pitchtools
        group_dict = self._pitch_class_octave_number_regex.match(
            pitch_class_octave_number_string).groupdict()
        named_pitch_class = pitchtools.NamedPitchClass(
            pitch_class_octave_number_string)
        octave_number = int(group_dict['octave_number'])
        self._initialize_by_named_pitch_class_and_octave_number(
            named_pitch_class, octave_number)

    def _initialize_by_pitch_name(self, pitch_string):
        from abjad.tools import pitchtools
        named_pitch_class = pitchtools.NamedPitchClass(pitch_string)
        octave = pitchtools.Octave.from_pitch_name(pitch_string)
        self._initialize_by_named_pitch_class_and_octave_number(
            named_pitch_class, octave.number)

    def _initialize_by_pitch_number(self, pitch_number):
        from abjad.tools import pitchtools
        named_pitch_class = pitchtools.NamedPitchClass(pitch_number)
        octave_number = pitch_number // 12 + 4
        self._initialize_by_named_pitch_class_and_octave_number(
            named_pitch_class, octave_number)

    def _initialize_by_pitch_number_and_diatonic_pitch_class_name(
        self, pitch_number, diatonic_pitch_class_name):
        from abjad.tools import pitchtools
        accidental, octave_number = self._spell_pitch_number(
            pitch_number,
            diatonic_pitch_class_name,
            )
        pitch_class_name = diatonic_pitch_class_name + \
            accidental.abbreviation
        named_pitch_class = pitchtools.NamedPitchClass(pitch_class_name)
        self._initialize_by_named_pitch_class_and_octave_number(
            named_pitch_class, octave_number)

    def _initialize_by_pitch_number_and_named_pitch_class(
        self, pitch_number, named_pitch_class):
        diatonic_pitch_class_name = named_pitch_class.diatonic_pitch_class_name
        self._initialize_by_pitch_number_and_diatonic_pitch_class_name(
            pitch_number, diatonic_pitch_class_name)

    def _initialize_by_pitch_number_and_octave_number(
        self, pitch_number, octave_number):
        pitch_class_name = type(self)(pitch_number).pitch_class_name
        octave_number = int(octave_number)
        self._initialize_by_pitch_class_name_and_octave_number(
            pitch_class_name, octave_number)

    @staticmethod
    def _spell_pitch_number(pitch_number, diatonic_pitch_class_name):
        from abjad.tools import pitchtools
        # check input
        if not isinstance(pitch_number, (int, float)):
            raise TypeError
        if not isinstance(diatonic_pitch_class_name, str):
            raise TypeError
        if diatonic_pitch_class_name not in ['c', 'd', 'e', 'f', 'g', 'a', 'b']:
            raise ValueError
        # find accidental semitones
        pc = pitchtools.PitchClass._diatonic_pitch_class_name_to_pitch_class_number[
            diatonic_pitch_class_name]
        nearest_neighbor = NamedPitch._to_nearest_octave(pitch_number, pc)
        semitones = pitch_number - nearest_neighbor
        # find accidental alphabetic string
        abbreviation = pitchtools.Accidental._semitones_to_abbreviation[
            semitones]
        accidental = pitchtools.Accidental(abbreviation)
        # find octave
        octave_number = int(math.floor((pitch_number - semitones) / 12)) + 4
        # return accidental and octave
        return accidental, octave_number

    @staticmethod
    def _to_nearest_octave(pitch_number, pitch_class_number):
        target_pc = pitch_number % 12
        down = (target_pc - pitch_class_number) % 12
        up = (pitch_class_number - target_pc) % 12
        if up < down:
            return pitch_number + up
        else:
            return pitch_number - down

    ### PUBLIC PROPERTIES ###

    @property
    def accidental(self):
        r'''Gets accidental of named pitch.

        ..  container:: example

            Gets accidental of C#5:

            ::

                >>> NamedPitch("cs''").accidental
                Accidental('s')

        ..  container:: example

            Gets accidental of C5:

            ::

                >>> NamedPitch("c''").accidental
                Accidental('')

        Returns accidental.
        '''
        from abjad.tools import pitchtools
        return pitchtools.Accidental(self._alteration_in_semitones)

    @property
    def alteration_in_semitones(self):
        r'''Gets alteration of named pitch in semitones.

        ..  container:: example

            Gets alteration of C#5 in semitones:

            ::

                >>> NamedPitch("cs''").alteration_in_semitones
                1

        ..  container:: example

            Gets alteration of Ctqs5 in semitones:

            ::

                >>> NamedPitch("ctqs''").alteration_in_semitones
                1.5

        Returns integer or float.
        '''
        return self._alteration_in_semitones

    @property
    def diatonic_pitch_class_name(self):
        r'''Gets diatonic pitch-class name of named pitch.

        ..  note:: Deprecated.

        ..  container:: example

            Gets diatonic pitch-class name of C#5:

            ::

                >>> NamedPitch("cs''").diatonic_pitch_class_name
                'c'

        ..  container:: example

            Gets diatonic pitch-class names of many pitches:

            ::

                >>> staff = Staff("g16 a b c' d' e' f' g' a' b' c'' d'' e'' f'' g'' a''")
                >>> for note in staff:
                ...     name = note.written_pitch.diatonic_pitch_class_name
                ...     markup = Markup(name)
                ...     attach(markup, note)
                ...
                >>> override(staff).text_script.staff_padding = 5
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff \with {
                    \override TextScript.staff-padding = #5
                } {
                    g16 - \markup { g }
                    a16 - \markup { a }
                    b16 - \markup { b }
                    c'16 - \markup { c }
                    d'16 - \markup { d }
                    e'16 - \markup { e }
                    f'16 - \markup { f }
                    g'16 - \markup { g }
                    a'16 - \markup { a }
                    b'16 - \markup { b }
                    c''16 - \markup { c }
                    d''16 - \markup { d }
                    e''16 - \markup { e }
                    f''16 - \markup { f }
                    g''16 - \markup { g }
                    a''16 - \markup { a }
                }

        Returns string.
        '''
        from abjad.tools import pitchtools
        class_ = pitchtools.PitchClass
        return class_._diatonic_pitch_class_number_to_diatonic_pitch_class_name[
            self._diatonic_pitch_class_number]

    @property
    def diatonic_pitch_class_number(self):
        r'''Gets diatonic pitch-class number of named pitch.

        ..  note:: Deprecated.

        ..  container:: example

            Gets diatonic pitch-class number of C#5:

            ::

                >>> NamedPitch("cs''").diatonic_pitch_class_number
                0

        ..  container:: example

            Gets diatonic pitch-class numbers of many pitches:

            ::

                >>> staff = Staff("g16 a b c' d' e' f' g' a' b' c'' d'' e'' f'' g'' a''")
                >>> for note in staff:
                ...     number = note.written_pitch.diatonic_pitch_class_number
                ...     markup = Markup(number)
                ...     attach(markup, note)
                ...
                >>> override(staff).text_script.staff_padding = 5
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff \with {
                    \override TextScript.staff-padding = #5
                } {
                    g16 - \markup { 4 }
                    a16 - \markup { 5 }
                    b16 - \markup { 6 }
                    c'16 - \markup { 0 }
                    d'16 - \markup { 1 }
                    e'16 - \markup { 2 }
                    f'16 - \markup { 3 }
                    g'16 - \markup { 4 }
                    a'16 - \markup { 5 }
                    b'16 - \markup { 6 }
                    c''16 - \markup { 0 }
                    d''16 - \markup { 1 }
                    e''16 - \markup { 2 }
                    f''16 - \markup { 3 }
                    g''16 - \markup { 4 }
                    a''16 - \markup { 5 }
                }

        Returns integer.
        '''
        return self._diatonic_pitch_class_number

    @property
    def diatonic_pitch_name(self):
        r'''Gets diatonic pitch name of named pitch.

        ..  note:: Deprecated.

        ..  container:: example

            Gets diatonic pitch name of C#5:

            ::

                >>> NamedPitch("cs''").diatonic_pitch_name
                "c''"

        ..  container:: example

            Gets diatonic pitch names of many pitches:

            ::

                >>> staff = Staff("g16 a b c' d' e' f' g' a' b' c'' d'' e'' f'' g'' a''")
                >>> for note in staff:
                ...     name = note.written_pitch.diatonic_pitch_name
                ...     markup = Markup(name)
                ...     attach(markup, note)
                ...
                >>> override(staff).text_script.staff_padding = 5
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff \with {
                    \override TextScript.staff-padding = #5
                } {
                    g16 - \markup { g }
                    a16 - \markup { a }
                    b16 - \markup { b }
                    c'16 - \markup { c' }
                    d'16 - \markup { d' }
                    e'16 - \markup { e' }
                    f'16 - \markup { f' }
                    g'16 - \markup { g' }
                    a'16 - \markup { a' }
                    b'16 - \markup { b' }
                    c''16 - \markup { c'' }
                    d''16 - \markup { d'' }
                    e''16 - \markup { e'' }
                    f''16 - \markup { f'' }
                    g''16 - \markup { g'' }
                    a''16 - \markup { a'' }
                }

        Returns string.
        '''
        return '{}{}'.format(
            self.diatonic_pitch_class_name,
            self.octave.tick_string,
            )

    @property
    def diatonic_pitch_number(self):
        r'''Gets diatonic pitch number of named pitch.

        ..  note:: Deprecated.

        ..  container:: example

            Gets diatonic pitch number of C#5:

            ::

                >>> NamedPitch("cs''").diatonic_pitch_number
                7

        ..  container:: example

            Gets diatonic pitch numbers of many pitches:

            ::

                >>> staff = Staff("g16 a b c' d' e' f' g' a' b' c'' d'' e'' f'' g'' a''")
                >>> for note in staff:
                ...     number = note.written_pitch.diatonic_pitch_number
                ...     markup = Markup(number)
                ...     attach(markup, note)
                ...
                >>> override(staff).text_script.staff_padding = 5
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff \with {
                    \override TextScript.staff-padding = #5
                } {
                    g16 - \markup { -3 }
                    a16 - \markup { -2 }
                    b16 - \markup { -1 }
                    c'16 - \markup { 0 }
                    d'16 - \markup { 1 }
                    e'16 - \markup { 2 }
                    f'16 - \markup { 3 }
                    g'16 - \markup { 4 }
                    a'16 - \markup { 5 }
                    b'16 - \markup { 6 }
                    c''16 - \markup { 7 }
                    d''16 - \markup { 8 }
                    e''16 - \markup { 9 }
                    f''16 - \markup { 10 }
                    g''16 - \markup { 11 }
                    a''16 - \markup { 12 }
                }

        Returns integer.
        '''
        diatonic_pitch_number = 7 * (self.octave.number - 4)
        diatonic_pitch_number += self.diatonic_pitch_class_number
        return diatonic_pitch_number

    @property
    def name(self):
        r'''Gets pitch name.

        ..  container:: example

            ::

                >>> NamedPitch("cs''").name
                "cs''"

        Returns string.
        '''
        return self.pitch_name

    @property
    def named_pitch(self):
        r'''Gets new named pitch.

        ..  note:: Deprecated.

        ..  container:: example

            Gets new named pitch from C#5:

            ::

                >>> NamedPitch("cs''").named_pitch
                NamedPitch("cs''")

        ..  container:: example

            Gets new named pitch from Db5:

            ::

                >>> NamedPitch("df''").named_pitch
                NamedPitch("df''")

        Returns new named pitch.
        '''
        return type(self)(self)

    @property
    def named_pitch_class(self):
        r'''Gets named pitch-class of named pitch.

        ..  note:: Deprecated.

        ..  container:: example

            Gets named pitch-class of C#5:

            ::

                >>> NamedPitch("cs''").named_pitch_class
                NamedPitchClass('cs')

        ..  container:: example

            Gets named pitch-class of Db5:

            ::

                >>> NamedPitch("df''").named_pitch_class
                NamedPitchClass('df')

        Returns named pitch-class.
        '''
        from abjad.tools import pitchtools
        return pitchtools.NamedPitchClass(self)

    @property
    def number(self):
        r'''Gets pitch number.

        ..  container:: ex

            Gets pitch number of C#5:

            ::

                >>> NamedPitch("cs''").number
                13


        Returns number.
        '''
        return self.numbered_pitch.number

    @property
    def numbered_pitch(self):
        r'''Gets numbered pitch corresponding to named pitch.

        ..  note:: Deprecated.

        ..  container:: example

            Gets numbered pitch corresponding to C#5:

            ::

                >>> NamedPitch("cs''").numbered_pitch
                NumberedPitch(13)

        ..  container:: example

            Gets numbered pitch corresponding to Db5:

            ::

                >>> NamedPitch("df''").numbered_pitch
                NumberedPitch(13)

        Returns numbered pitch.
        '''
        from abjad.tools import pitchtools
        return pitchtools.NumberedPitch(self)

    @property
    def numbered_pitch_class(self):
        r'''Gets numbered pitch-class corresponding to named pitch.

        ..  note:: Deprecated.

        ..  container:: example

            Gets numbered pitch-class corresponding to C#5:

            ::

                >>> NamedPitch("cs''").numbered_pitch_class
                NumberedPitchClass(1)

        ..  container:: example

            Gets numbered pitch-class corresponding to Db5:

            ::

                >>> NamedPitch("df''").numbered_pitch_class
                NumberedPitchClass(1)

        Returns numbered pitch-class.
        '''
        from abjad.tools import pitchtools
        return pitchtools.NumberedPitchClass(self)

    @property
    def octave(self):
        r'''Gets octave of named pitch.

        ..  container:: example

            Gets octave of C#5:

            ::

                >>> NamedPitch("cs''").octave
                Octave(5)

        ..  container:: example

            Gets octave of Db5:

            ::

                >>> NamedPitch("df''").octave
                Octave(5)

        Returns octave.
        '''
        from abjad.tools import pitchtools
        return pitchtools.Octave(self._octave_number)

    @property
    def pitch_class(self):
        r'''Gets pitch-class.

        ..  container:: example

            ::

                >>> NamedPitch("cs''").pitch_class
                NamedPitchClass('cs')

        Returns named pitch-class.
        '''
        from abjad.tools import pitchtools
        return pitchtools.NamedPitchClass(self)

    @property
    def pitch_class_name(self):
        r'''Gets pitch-class name of named pitch.

        ..  note:: Deprecated.

        ..  container:: example

            Gets pitch-class name of C#5:

            ::

                >>> NamedPitch("cs''").pitch_class_name
                'cs'

        ..  container:: example

            Gets pitch-class name of Db5:

            ::

                >>> NamedPitch("df''").pitch_class_name
                'df'

        Returns string.
        '''
        from abjad.tools import pitchtools
        return '{}{}'.format(
            self.diatonic_pitch_class_name,
            pitchtools.Accidental(self._alteration_in_semitones).abbreviation
            )

    @property
    def pitch_class_number(self):
        r'''Gets pitch-class number of named pitch.

        ..  note:: Deprecated.

        ..  container:: example

            Gets pitch-class number of C#5:

            ::

                >>> NamedPitch("cs''").pitch_class_number
                1

        ..  container:: example

            Gets pitch-class number of Ctqs5:

            ::

                >>> NamedPitch("ctqs''").pitch_class_number
                1.5

        Returns integer or float.
        '''
        from abjad.tools import pitchtools
        class_ = pitchtools.PitchClass
        return (class_._diatonic_pitch_class_number_to_pitch_class_number[
            self._diatonic_pitch_class_number] +
            self._alteration_in_semitones) % 12

    @property
    def pitch_class_octave_label(self):
        r'''Gets pitch-class / octave label of named pitch.

        ..  note:: Deprecated.

        ..  container:: example

            Gets pitch-class / octave label of C#5:

            ::

                >>> NamedPitch("cs''").pitch_class_octave_label
                'C#5'

        ..  container:: example

            Gets pitch-class / octave label of Ctqs5:

            ::

                >>> NamedPitch("ctqs''").pitch_class_octave_label
                'C#+5'

        Returns string.
        '''
        return '{}{}{}'.format(
            self.diatonic_pitch_class_name.upper(),
            self.accidental.symbolic_string,
            self.octave.number,
            )

    @property
    def pitch_name(self):
        r'''Gets pitch name of named pitch.

        ..  note:: Deprecated.

        ..  container:: example

            Gets pitch name of C#5:

            ::

                >>> NamedPitch("cs''").pitch_name
                "cs''"

        ..  container:: example

            Gets pitch name of Ctqs5:

            ::

                >>> NamedPitch("ctqs''").pitch_name
                "ctqs''"

        Returns string.
        '''
        return '{}{}'.format(
            self.pitch_class_name,
            self.octave.tick_string,
            )

    @property
    def pitch_number(self):
        r'''Gets pitch number of named pitch.

        ..  note:: Deprecated.

        ..  container:: example

            Gets pitch number of C#5:

            ::

                >>> NamedPitch("cs''").pitch_number
                13

        ..  container:: example

            Gets pitch number of Cbb5:

            ::

                >>> NamedPitch("cff''").pitch_number
                10

        Returns integer or float.
        '''
        from abjad.tools import pitchtools
        pitch_class_number = pitchtools.PitchClass._diatonic_pitch_class_number_to_pitch_class_number[
            self.diatonic_pitch_class_number]
        pitch_number = pitch_class_number + 12 * (self.octave.number - 4)
        pitch_number += self.alteration_in_semitones
        return pitch_number

    ### PUBLIC METHODS ###

    def apply_accidental(self, accidental=None):
        '''Applies `accidental` to named pitch.

        ..  container:: example

            Applies sharp to C#5:

            ::

                >>> NamedPitch("cs''").apply_accidental('s')
                NamedPitch("css''")

        ..  container:: example

            Applies sharp to Db5:

            ::

                >>> NamedPitch("df''").apply_accidental('s')
                NamedPitch("d''")

        Returns new named pitch.
        '''
        from abjad.tools import pitchtools
        accidental = pitchtools.Accidental(accidental)
        new_accidental = self.accidental + accidental
        new_name = self.diatonic_pitch_class_name
        new_name += new_accidental.abbreviation
        return type(self)(new_name, self.octave.number)

    @staticmethod
    def from_pitch_carrier(pitch_carrier):
        r'''Initializes named pitch from `pitch_carrier`.

        ..  container:: example

            Initializes named pitch from named pitch:

            ::

                >>> pitch = NamedPitch('df', 5)
                >>> NamedPitch.from_pitch_carrier(pitch)
                NamedPitch("df''")

        ..  container:: example

            Initializes named pitch from note:

            ::

                >>> note = Note("df''4")
                >>> NamedPitch.from_pitch_carrier(note)
                NamedPitch("df''")

        ..  container:: example

            Initializes named pitch from note-head:

            ::

                >>> note = Note("df''4")
                >>> NamedPitch.from_pitch_carrier(note.note_head)
                NamedPitch("df''")

        ..  container:: example

            Initializes named pitch from chord:

            ::

                >>> chord = Chord("<df''>4")
                >>> NamedPitch.from_pitch_carrier(chord)
                NamedPitch("df''")

        ..  container:: example

            Initializes named pitch from integer:

            ::

                >>> NamedPitch.from_pitch_carrier(13)
                NamedPitch("cs''")

        ..  container:: example

            Initializes named pitch from numbered pitch-class:

            ::

                >>> pitch_class = NumberedPitchClass(7)
                >>> NamedPitch.from_pitch_carrier(pitch_class)
                NamedPitch("g'")

        Raises value error when `pitch_carrier` carries no pitch.

        Raises value error when `pitch_carrier` carries more than one pitch.

        Returns new named pitch.
        '''
        from abjad.tools import pitchtools
        from abjad.tools import scoretools
        if isinstance(pitch_carrier, pitchtools.NamedPitch):
            return pitch_carrier
        elif isinstance(pitch_carrier, pitchtools.NumberedPitch):
            return pitchtools.NamedPitch(pitch_carrier)
        elif isinstance(pitch_carrier, numbers.Number):
            return pitchtools.NamedPitch(pitch_carrier)
        elif isinstance(pitch_carrier, scoretools.Note):
            pitch = pitch_carrier.written_pitch
            if pitch is not None:
                return NamedPitch.from_pitch_carrier(pitch)
            else:
                message = 'no pitch found on {!r}.'
                message = message.format(pitch_carrier)
                raise ValueError(message)
        elif isinstance(pitch_carrier, scoretools.NoteHead):
            pitch = pitch_carrier.written_pitch
            if pitch is not None:
                return NamedPitch.from_pitch_carrier(pitch)
            else:
                message = 'no pitch found on {!r}.'
                message = message.format(pitch_carrier)
                raise ValueError(message)
        elif isinstance(pitch_carrier, scoretools.Chord):
            pitches = pitch_carrier.written_pitches
            if len(pitches) == 0:
                message = 'no pitch found on {!r}.'
                message = message.format(pitch_carrier)
                raise ValueError(message)
            elif len(pitches) == 1:
                return NamedPitch.from_pitch_carrier(pitches[0])
            else:
                message = 'multiple pitches found on {!r}.'
                message = message.format(pitch_carrier)
                raise ValueError(message)
        elif isinstance(pitch_carrier, pitchtools.NumberedPitchClass):
            named_pitch_class = pitch_carrier.named_pitch_class
            named_pitch = pitchtools.NamedPitch(named_pitch_class)
            return named_pitch
        else:
            message = 'pitch carrier {!r} must be'
            message += ' pitch, note, note-head or chord.'
            message = message.format(pitch_carrier)
            raise TypeError(message)

    @staticmethod
    def from_staff_position(staff_position, clef=None):
        r'''Initializes named pitch from `staff_position` and optional `clef`.

        ..  container:: example

            Initializes notes from absolute staff positions:

            ::

                >>> for n in range(-6, 6):
                ...     staff_position = pitchtools.StaffPosition(n)
                ...     pitch = NamedPitch.from_staff_position(staff_position)
                ...     message = '{!s}\t{}'.format(staff_position, pitch)
                ...     print(message)
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

            Initializes notes inside treble staff from staff positions:

            ::

                >>> clef = Clef('treble')
                >>> for n in range(-6, 6):
                ...     staff_position = pitchtools.StaffPosition(n)
                ...     pitch = NamedPitch.from_staff_position(
                ...         staff_position,
                ...         clef=clef,
                ...         )
                ...     message = '{!s}\t{}'.format(staff_position, pitch)
                ...     print(message)
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

            Initializes notes inside bass staff from staff positions:

            ::

                >>> clef = Clef('bass')
                >>> for n in range(-6, 6):
                ...     staff_position = pitchtools.StaffPosition(n)
                ...     pitch = NamedPitch.from_staff_position(
                ...         staff_position,
                ...         clef=clef,
                ...         )
                ...     message = '{!s}\t{}'.format(staff_position, pitch)
                ...     print(message)
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

            Initializes notes inside alto staff from staff positions:

            ::

                >>> clef = Clef('alto')
                >>> for n in range(-6, 6):
                ...     staff_position = pitchtools.StaffPosition(n)
                ...     pitch = NamedPitch.from_staff_position(
                ...         staff_position,
                ...         clef=clef,
                ...         )
                ...     message = '{!s}\t{}'.format(staff_position, pitch)
                ...     print(message)
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
        '''
        from abjad.tools import pitchtools
        if not isinstance(staff_position, pitchtools.StaffPosition):
            staff_position = pitchtools.StaffPosition(staff_position)
        if clef is not None:
            offset_staff_position_number = staff_position.number
            offset_staff_position_number -= clef.middle_c_position.number
            offset_staff_position = pitchtools.StaffPosition(
                offset_staff_position_number)
        else:
            offset_staff_position = staff_position
        octave_number = offset_staff_position.number // 7 + 4
        diatonic_pitch_class_number = offset_staff_position.number % 7
        pitch_class_number = pitchtools.PitchClass._diatonic_pitch_class_number_to_pitch_class_number[
            diatonic_pitch_class_number]
        pitch_number = 12 * (octave_number - 4)
        pitch_number += pitch_class_number
        named_pitch = NamedPitch(pitch_number)
        return named_pitch

    def invert(self, axis=None):
        r'''Inverts named pitch around `axis`.

        ..  container:: example

            Inverts pitch around middle C explicitly:

            ::

                >>> NamedPitch("d'").invert("c'")
                NamedPitch('bf')

            ::

                >>> NamedPitch('bf').invert("c'")
                NamedPitch("d'")

        ..  container:: example

            Inverts pitch around middle C implicitly:

            ::

                >>> NamedPitch("d'").invert()
                NamedPitch('bf')

            ::

                >>> NamedPitch('bf').invert()
                NamedPitch("d'")

        ..  container:: example

            Inverts pitch around A3:

            ::

                >>> NamedPitch("d'").invert('a')
                NamedPitch('e')

        Interprets none-valued `axis` equal to middle C.

        Returns new named pitch.
        '''
        try:
            return Pitch.invert(self, axis=axis)
        except:
            return Pitch.invert(type(self)(float(self)), axis=axis)

    def multiply(self, n=1):
        r'''Multiplies pitch-class of named pitch by `n` while maintaining
        octave of named pitch.

        ..  note:: This is wrong. Should not preserve octave.

        ..  container:: example

            Multiplies D2 by 3:

            ::

                >>> NamedPitch('d,').multiply(3)
                NamedPitch('fs,')

        ..  container:: example

            Multiplies D2 by 4:

            ::

                >>> NamedPitch('d,').multiply(4)
                NamedPitch('af,')

        Returns new named pitch.
        '''
        pitch_class_number = (self.pitch_class_number * n) % 12
        octave_floor = (self.octave.number - 4) * 12
        return type(self)(pitch_class_number + octave_floor)

    def respell_with_flats(self):
        r'''Respells named pitch with flats.

        ..  container:: example

            Respells C#5 with flats:

            ::

                >>> NamedPitch("cs''").respell_with_flats()
                NamedPitch("df''")

        ..  container:: example

            Respells Db5 with flats:

            ::

                >>> NamedPitch("df''").respell_with_flats()
                NamedPitch("df''")

        Returns new named pitch.
        '''
        from abjad.tools import pitchtools
        class_ = pitchtools.PitchClass
        octave = pitchtools.Octave.from_pitch_number(
            self.numbered_pitch.pitch_number)
        name = class_._pitch_class_number_to_pitch_class_name_with_flats[
            self.pitch_class_number]
        pitch = type(self)(name, octave.number)
        return pitch

    def respell_with_sharps(self):
        r'''Respells named pitch with sharps.

        ..  container:: example

            Respells Db5 with sharps:

            ::

                >>> NamedPitch("df''").respell_with_sharps()
                NamedPitch("cs''")

        ..  container:: example

            Respells C#5 with sharps:

            ::

                >>> NamedPitch("cs''").respell_with_sharps()
                NamedPitch("cs''")

        Returns new named pitch.
        '''
        from abjad.tools import pitchtools
        class_ = pitchtools.PitchClass
        octave = pitchtools.Octave.from_pitch_number(
            self.numbered_pitch.pitch_number)
        name = class_._pitch_class_number_to_pitch_class_name_with_sharps[
            self.pitch_class_number]
        pitch = type(self)(name, octave.number)
        return pitch

    def to_staff_position(self, clef=None):
        r'''Changes named pitch to staff position with optional `clef`.

        ..  container:: example

            Changes C#5 to absolute staff position:

            ::

                >>> NamedPitch('C#5').to_staff_position()
                StaffPosition(number=7)

        ..  container:: example

            Changes C#5 to treble staff position:

            ::


                >>> NamedPitch('C#5').to_staff_position(clef=Clef('treble'))
                StaffPosition(number=1)

        ..  container:: example

            Changes C#5 to bass staff position:

            ::


                >>> NamedPitch('C#5').to_staff_position(clef=Clef('bass'))
                StaffPosition(number=13)

        ..  container:: example

            Marks up absolute staff position of many pitches:

            ::

                >>> staff = Staff("g16 a b c' d' e' f' g' a' b' c'' d'' e'' f'' g'' a''")
                >>> for note in staff:
                ...     staff_position = note.written_pitch.to_staff_position()
                ...     markup = Markup(staff_position.number)
                ...     attach(markup, note)
                ...
                >>> override(staff).text_script.staff_padding = 5
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff \with {
                    \override TextScript.staff-padding = #5
                } {
                    g16 - \markup { -3 }
                    a16 - \markup { -2 }
                    b16 - \markup { -1 }
                    c'16 - \markup { 0 }
                    d'16 - \markup { 1 }
                    e'16 - \markup { 2 }
                    f'16 - \markup { 3 }
                    g'16 - \markup { 4 }
                    a'16 - \markup { 5 }
                    b'16 - \markup { 6 }
                    c''16 - \markup { 7 }
                    d''16 - \markup { 8 }
                    e''16 - \markup { 9 }
                    f''16 - \markup { 10 }
                    g''16 - \markup { 11 }
                    a''16 - \markup { 12 }
                }

        ..  container:: example

            Marks up treble staff position of many pitches:

            ::

                >>> staff = Staff("g16 a b c' d' e' f' g' a' b' c'' d'' e'' f'' g'' a''")
                >>> clef = Clef('treble')
                >>> for note in staff:
                ...     staff_position = note.written_pitch.to_staff_position(
                ...         clef=clef
                ...         )
                ...     markup = Markup(staff_position.number)
                ...     attach(markup, note)
                ...
                >>> override(staff).text_script.staff_padding = 5
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff \with {
                    \override TextScript.staff-padding = #5
                } {
                    g16 - \markup { -9 }
                    a16 - \markup { -8 }
                    b16 - \markup { -7 }
                    c'16 - \markup { -6 }
                    d'16 - \markup { -5 }
                    e'16 - \markup { -4 }
                    f'16 - \markup { -3 }
                    g'16 - \markup { -2 }
                    a'16 - \markup { -1 }
                    b'16 - \markup { 0 }
                    c''16 - \markup { 1 }
                    d''16 - \markup { 2 }
                    e''16 - \markup { 3 }
                    f''16 - \markup { 4 }
                    g''16 - \markup { 5 }
                    a''16 - \markup { 6 }
                }

        ..  container:: example

            Marks up bass staff position of many pitches:

            ::

                >>> staff = Staff("g,16 a, b, c d e f g a b c' d' e' f' g' a'")
                >>> clef = Clef('bass')
                >>> attach(clef, staff)
                >>> for note in staff:
                ...     staff_position = note.written_pitch.to_staff_position(
                ...         clef=clef
                ...         )
                ...     markup = Markup(staff_position.number)
                ...     attach(markup, note)
                ...
                >>> override(staff).text_script.staff_padding = 5
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff \with {
                    \override TextScript.staff-padding = #5
                } {
                    \clef "bass"
                    g,16 - \markup { -4 }
                    a,16 - \markup { -3 }
                    b,16 - \markup { -2 }
                    c16 - \markup { -1 }
                    d16 - \markup { 0 }
                    e16 - \markup { 1 }
                    f16 - \markup { 2 }
                    g16 - \markup { 3 }
                    a16 - \markup { 4 }
                    b16 - \markup { 5 }
                    c'16 - \markup { 6 }
                    d'16 - \markup { 7 }
                    e'16 - \markup { 8 }
                    f'16 - \markup { 9 }
                    g'16 - \markup { 10 }
                    a'16 - \markup { 11 }
                }

        Returns staff position.
        '''
        from abjad.tools import pitchtools
        staff_position_number = self.diatonic_pitch_number
        if clef is not None:
            staff_position_number += clef.middle_c_position.number
        staff_position = pitchtools.StaffPosition(staff_position_number)
        return staff_position

    def transpose(self, n=0):
        r'''Transposes named pitch by index `n`.

        ..  container:: example

            Transposes C4 up a minor second:

            ::

                >>> NamedPitch("c'").transpose(n='m2')
                NamedPitch("df'")

        ..  container:: example

            Transposes C4 down a major second:

            ::

                >>> NamedPitch("c'").transpose(n='-M2')
                NamedPitch('bf')

        Returns new named pitch.
        '''
        from abjad.tools import pitchtools
        interval = pitchtools.NamedInterval(n)
        pitch = interval.transpose(self)
        return type(self)(pitch)

    def transpose_staff_position(self, staff_positions, interval):
        '''Transposes named pitch by `staff_positions` and `interval`.

        ..  container:: example

            Transposes middle C but leaves at same staff position:

            ::

                >>> pitch = NamedPitch(0)

            ::

                >>> pitch.transpose_staff_position(0, -2)
                NamedPitch("cff'")
                >>> pitch.transpose_staff_position(0, -1.5)
                NamedPitch("ctqf'")
                >>> pitch.transpose_staff_position(0, -1)
                NamedPitch("cf'")
                >>> pitch.transpose_staff_position(0, -0.5)
                NamedPitch("cqf'")
                >>> pitch.transpose_staff_position(0, 0)
                NamedPitch("c'")
                >>> pitch.transpose_staff_position(0, 0.5)
                NamedPitch("cqs'")
                >>> pitch.transpose_staff_position(0, 1)
                NamedPitch("cs'")
                >>> pitch.transpose_staff_position(0, 1.5)
                NamedPitch("ctqs'")

        ..  container:: example

            Transposes middle C and then respells up 1 staff position:

                >>> pitch.transpose_staff_position(1, 0)
                NamedPitch("dff'")
                >>> pitch.transpose_staff_position(1, 0.5)
                NamedPitch("dtqf'")
                >>> pitch.transpose_staff_position(1, 1)
                NamedPitch("df'")
                >>> pitch.transpose_staff_position(1, 1.5)
                NamedPitch("dqf'")
                >>> pitch.transpose_staff_position(1, 2)
                NamedPitch("d'")
                >>> pitch.transpose_staff_position(1, 2.5)
                NamedPitch("dqs'")
                >>> pitch.transpose_staff_position(1, 3)
                NamedPitch("ds'")
                >>> pitch.transpose_staff_position(1, 3.5)
                NamedPitch("dtqs'")
                >>> pitch.transpose_staff_position(1, 4)
                NamedPitch("dss'")

        Returns new named pitch.
        '''
        from abjad.tools import pitchtools
        pitch_number = self.pitch_number + interval
        diatonic_pitch_class_number = self.diatonic_pitch_class_number
        diatonic_pitch_class_number += staff_positions
        diatonic_pitch_class_number %= 7
        class_ = pitchtools.PitchClass
        dictionary = \
            class_._diatonic_pitch_class_number_to_diatonic_pitch_class_name
        diatonic_pitch_class_name = dictionary[diatonic_pitch_class_number]
        return type(self)(pitch_number, diatonic_pitch_class_name)
