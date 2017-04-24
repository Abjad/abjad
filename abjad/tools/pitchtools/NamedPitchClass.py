# -*- coding: utf-8 -*-
import numbers
from abjad.tools.pitchtools.PitchClass import PitchClass


class NamedPitchClass(PitchClass):
    '''Named pitch-class.

    ..  container:: example

        Initializes from pitch-class name:

        ::

            >>> NamedPitchClass('cs')
            NamedPitchClass('cs')

    ..  container:: example

        Initializes from number of semitones:

        ::

            >>> NamedPitchClass(14)
            NamedPitchClass('d')

    ..  container:: example

        Initializes from named pitch:

        ::

            >>> NamedPitchClass(NamedPitch('g,'))
            NamedPitchClass('g')

    ..  container:: example

        Initializes from numbered pitch:

        ::

            >>> NamedPitchClass(NumberedPitch(15))
            NamedPitchClass('ef')

    ..  container:: example

        Initializes from numbered pitch-class:

        ::

            >>> NamedPitchClass(NumberedPitchClass(4))
            NamedPitchClass('e')

    ..  container:: example

        Initializes from named pitch-class:


        ::

            >>> NamedPitchClass('C#5')
            NamedPitchClass('cs')


    ..  container:: example

        Initializes from named pitch-class:

        ::

            >>> NamedPitchClass(Note("a'8."))
            NamedPitchClass('a')

    ..  container:: example

        Initializes from pitch-class name:

            >>> pitch_class = NamedPitchClass('cs')
            >>> pitch_class
            NamedPitchClass('cs')

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_alteration_in_semitones',
        '_diatonic_pitch_class_number',
        )

    ### INITIALIZER ###

    def __init__(self, argument=None):
        from abjad.tools import pitchtools
        if isinstance(argument, type(self)):
            self._initialize_by_named_pitch_class(argument)
        elif isinstance(argument, pitchtools.NamedPitch):
            self._initialize_by_named_pitch(argument)
        elif pitchtools.Pitch.is_pitch_class_octave_number_string(argument):
            self._initialize_by_pitch_class_octave_number_string(argument)
        elif pitchtools.Pitch.is_pitch_name(argument):
            self._initialize_by_pitch_name(argument)
        elif isinstance(argument, (
            numbers.Number,
            pitchtools.NumberedPitch,
            pitchtools.NumberedPitchClass,
            )):
            self._initialize_by_number(float(argument))
        elif pitchtools.Pitch.is_pitch_carrier(argument):
            self._initialize_by_pitch_carrier(argument)
        elif argument is None:
            self._initialize_by_number(0)
        else:
            message = 'can not instantiate {} from {!r}.'
            message = message.format(type(self).__name__, argument)
            raise TypeError(message)

    ### SPECIAL METHODS ###

    def __add__(self, named_interval):
        r'''Adds `named_interval` to named pitch-class.

        ::

            >>> pitch_class + NamedInterval('+M9')
            NamedPitchClass('ds')

        Return new named pitch-class.
        '''
        from abjad.tools import pitchtools
        dummy_pitch = pitchtools.NamedPitch(self.pitch_class_name, 4)
        pitch = named_interval.transpose(dummy_pitch)
        return type(self)(pitch)

    def __copy__(self, *arguments):
        r'''Copies named pitch-class.

        ::

            >>> import copy
            >>> copy.copy(pitch_class)
            NamedPitchClass('cs')

        Returns new named pitch-class.
        '''
        return type(self)(self)

    def __eq__(self, argument):
        r'''Is true when `argument` can be coerced to a named pitch-class with
        pitch-class name equal to that of this named pitch-class.

        ::

            >>> pitch_class == 'cs'
            True

        Otherwise false:

            >>> pitch_class == 'ds'
            False

        Returns true or false.
        '''
        if isinstance(argument, type(self)):
            return self.pitch_class_name == argument.pitch_class_name
        return self.pitch_class_name == argument

    def __float__(self):
        r'''Changes named pitch-class to a float.

        ::

            >>> float(pitch_class)
            1.0

        Returns float.
        '''
        return float(self.numbered_pitch_class)

    def __format__(self, format_specification=''):
        r'''Formats named pitch-class.

        ..  container:: example

            ::

                >>> format(NamedPitchClass('cs'))
                "pitchtools.NamedPitchClass('cs')"

        Set `format_specification` to `''`, `'lilypond'` or `'storage'`.

        Returns string.
        '''
        superclass = super(NamedPitchClass, self)
        return superclass.__format__(format_specification=format_specification)

    def __hash__(self):
        r'''Hashes named pitch-class.

        Required to be explicitly redefined on Python 3 if __eq__ changes.

        Returns integer.
        '''
        return super(NamedPitchClass, self).__hash__()

    def __int__(self):
        r'''Changes named pitch-class to an integer.

        ::

            >>> int(pitch_class)
            1

        Returns nonnegative integer.
        '''
        return int(self.numbered_pitch_class)

    def __lt__(self, argument):
        r'''Is true when `argument` is a named pitch-class with a pitch
        number greater than that of this named pitch-class.

        ..  container:: example

            Compares less than:

            ::

                >>> NamedPitchClass('cs') < NamedPitchClass('d')
                True

        ..  container:: example

            Does not compare less than:

            ::

                >>> NamedPitchClass('d') < NamedPitchClass('cs')
                False

        Raises type error when `argument` is not a named pitch-class.
        '''
        if not isinstance(argument, type(self)):
            message = 'can not compare named pitch-class to {!r}.'
            message = message.format(argument)
            raise TypeError(message)
        return self.number < argument.number

    def __str__(self):
        r'''Gets string representation of named pitch-class.

        ..  container:: example

            ::

                >>> str(pitch_class)
                'cs'

        Returns string.
        '''
        return self.pitch_class_name

    def __sub__(self, argument):
        r'''Subtracts `argument` from named pitch-class.

        ..  container:: example

            ::

                >>> pitch_class - NamedPitchClass('g')
                NamedInversionEquivalentIntervalClass('+aug4')

        Returns named inversion-equivalent interval-class.
        '''
        from abjad.tools import pitchtools
        if not isinstance(argument, type(self)):
            message = 'must be named pitch-class: {!r}.'
            message = message.format(argument)
            raise TypeError(message)
        pitch_1 = pitchtools.NamedPitch(self, 4)
        pitch_2 = pitchtools.NamedPitch(argument, 4)
        mdi = pitchtools.NamedInterval.from_pitch_carriers(
            pitch_1, pitch_2)
        dic = pitchtools.NamedInversionEquivalentIntervalClass(
            mdi.quality_string, mdi.number)
        return dic

    ### PRIVATE METHODS ###

    def _initialize_by_named_pitch(self, argument):
        self._alteration_in_semitones = argument.alteration_in_semitones
        self._diatonic_pitch_class_number = argument.diatonic_pitch_class_number

    def _initialize_by_named_pitch_class(self, argument):
        self._alteration_in_semitones = argument.alteration_in_semitones
        self._diatonic_pitch_class_number = argument.diatonic_pitch_class_number

    def _initialize_by_number(self, argument):
        from abjad.tools import pitchtools
        pitch_class_number = float(argument) % 12
        numbered_pitch_class = pitchtools.NumberedPitchClass(
            pitch_class_number)
        pitch_class_name = numbered_pitch_class.pitch_class_name
        self._initialize_by_pitch_name(pitch_class_name)

    def _initialize_by_pitch_carrier(self, argument):
        from abjad.tools import pitchtools
        named_pitch = pitchtools.NamedPitch.from_pitch_carrier(argument)
        self._initialize_by_named_pitch(named_pitch)

    def _initialize_by_pitch_class_octave_number_string(self, argument):
        from abjad.tools import pitchtools
        group_dict = pitchtools.Pitch._pitch_class_octave_number_regex.match(
            argument).groupdict()
        diatonic_pitch_class_name = group_dict['diatonic_pitch_class_name'].lower()
        symbolic_string = group_dict['symbolic_string']
        self._alteration_in_semitones = \
            pitchtools.Accidental._symbolic_string_to_semitones[
                symbolic_string]
        self._diatonic_pitch_class_number = \
            self._diatonic_pitch_class_name_to_diatonic_pitch_class_number[
                diatonic_pitch_class_name]

    def _initialize_by_pitch_name(self, argument):
        from abjad.tools import pitchtools
        match = pitchtools.Pitch._pitch_name_regex.match(argument.lower())
        if match is None:
            raise ValueError
        groups = match.groups()
        diatonic_pitch_class_name = groups[0]
        abbreviation = groups[1]
        accidental = pitchtools.Accidental(abbreviation)
        self._alteration_in_semitones = accidental.semitones
        self._diatonic_pitch_class_number = \
            self._diatonic_pitch_class_name_to_diatonic_pitch_class_number[
                diatonic_pitch_class_name]

    ### PUBLIC PROPERTIES ###

    @property
    def accidental(self):
        r'''Gets accidental.

        ..  container:: example

            ::

                >>> NamedPitchClass('cs').accidental
                Accidental('s')

        Returns accidental.
        '''
        from abjad.tools import pitchtools
        return pitchtools.Accidental(self._alteration_in_semitones)

    @property
    def alteration_in_semitones(self):
        r'''Gets alteration in semitones.

        ..  container:: example

            ::

                >>> NamedPitchClass('cs').alteration_in_semitones
                1

        Returns nonnegative integer or float.
        '''
        return self._alteration_in_semitones

    # TODO: rename as diatonic_name
    @property
    def diatonic_pitch_class_name(self):
        r'''Gets diatonic pitch-class name.

        ..  container:: example

            ::

                >>> NamedPitchClass('cs').diatonic_pitch_class_name
                'c'

        Returns string.
        '''
        return self._diatonic_pitch_class_number_to_diatonic_pitch_class_name[
            self._diatonic_pitch_class_number]

    @property
    def diatonic_pitch_class_number(self):
        r'''Gets diatonic pitch-class number.

        ::

            >>> NamedPitchClass('cs').diatonic_pitch_class_number
            0

        Returns nonnegative integer.
        '''
        return self._diatonic_pitch_class_number

    # TODO: remove
    @property
    def named_pitch_class(self):
        r'''Gets named pitch-class.

        ..  container:: example

            ::

                >>> NamedPitchClass('cs').named_pitch_class
                NamedPitchClass('cs')

        Returns new named pitch-class.
        '''
        return type(self)(self)

    @property
    def number(self):
        r'''Gets number.

        ..  container:: example

            ::

                >>> NamedPitchClass('cs').number
                1

        Returns nonnegative integer or float.
        '''
        from abjad.tools import pitchtools
        return pitchtools.NumberedPitchClass(self).number

    # TODO: remove
    @property
    def numbered_pitch_class(self):
        r'''Gets numbered pitch-class.

        ..  container:: example

            ::

                >>> NamedPitchClass('cs').numbered_pitch_class
                NumberedPitchClass(1)

        Returns numbered pitch-class.
        '''
        from abjad.tools import pitchtools
        return pitchtools.NumberedPitchClass(self)

    @property
    def pitch_class_label(self):
        r'''Gets pitch-class label.

        ..  container:: example

            ::

                >>> NamedPitchClass('cs').pitch_class_label
                'C#'

        Returns string.
        '''
        return '{}{}'.format(
            self.diatonic_pitch_class_name.upper(),
            self.accidental.symbolic_string,
            )

    # TODO: rename as 'name'
    @property
    def pitch_class_name(self):
        r'''Gets pitch-class name.

        ..  container:: example

            ::

                >>> NamedPitchClass('cs').pitch_class_name
                'cs'

        Returns string.
        '''
        from abjad.tools import pitchtools
        return '{}{}'.format(
            self.diatonic_pitch_class_name,
            pitchtools.Accidental._semitones_to_abbreviation[
                self._alteration_in_semitones],
            )

    # TODO: remove
    @property
    def pitch_class_number(self):
        r'''Gets pitch-class number.

        ..  container:: example

            ::

                >>> NamedPitchClass('cs').pitch_class_number
                1

        Returns integer or float.
        '''
        return (
            self._diatonic_pitch_class_number_to_pitch_class_number[
                self._diatonic_pitch_class_number] +
                self._alteration_in_semitones) % 12

    ### PUBLIC METHODS ###

    def apply_accidental(self, accidental):
        r'''Applies `accidental` to named pitch-class.

        ..  container:: example

            ::

                >>> NamedPitchClass('cs').apply_accidental('qs')
                NamedPitchClass('ctqs')

        Returns new named pitch-class.
        '''
        from abjad.tools import pitchtools
        accidental = pitchtools.Accidental(accidental)
        new_accidental = self.accidental + accidental
        new_name = self.diatonic_pitch_class_name + new_accidental.abbreviation
        return type(self)(new_name)

    def invert(self, axis=None):
        r'''Inverts named pitch-class.

        Not yet implemented.
        '''
        from abjad.tools import pitchtools
        axis = axis or pitchtools.NamedPitch('c')
        axis = pitchtools.NamedPitch(axis)
        this = pitchtools.NamedPitch(self)
        interval = this - axis
        result = axis.transpose(interval)
        result = type(self)(result)
        return result

    def multiply(self, n=1):
        r'''Multiplies named pitch-class by `n`.

        ..  container:: example

            ::

                >>> NamedPitchClass('cs').multiply(3)
                NamedPitchClass('ef')

        Returns new named pitch-class.
        '''
        return type(self)(self.pitch_class_number * n)

    def transpose(self, n=0):
        r'''Transposes named pitch-class by index `n`.

        ..  container:: example

            ::

                >>> named_interval = NamedInterval('major', 2)
                >>> NamedPitchClass('cs').transpose(named_interval)
                NamedPitchClass('ds')

        Returns new named pitch-class.
        '''
        from abjad.tools import pitchtools
        interval = pitchtools.NamedInterval(n)
        pitch = pitchtools.NamedPitch(self, 4)
        pitch = interval.transpose(pitch)
        return type(self)(pitch)
