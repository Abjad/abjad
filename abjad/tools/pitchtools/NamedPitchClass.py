import numbers
from abjad.tools.pitchtools.PitchClass import PitchClass


class NamedPitchClass(PitchClass):
    '''Named pitch-class.

    ..  container:: example

        Initializes from pitch-class name:

        >>> abjad.NamedPitchClass('cs')
        NamedPitchClass('cs')

        >>> abjad.NamedPitchClass('cqs')
        NamedPitchClass('cqs')

    ..  container:: example

        Initializes from number of semitones:

        >>> abjad.NamedPitchClass(14)
        NamedPitchClass('d')

        >>> abjad.NamedPitchClass(14.5)
        NamedPitchClass('dqs')

    ..  container:: example

        Initializes from named pitch:

        >>> abjad.NamedPitchClass(abjad.NamedPitch('d'))
        NamedPitchClass('d')

        >>> abjad.NamedPitchClass(abjad.NamedPitch('dqs'))
        NamedPitchClass('dqs')

    ..  container:: example

        Initializes from numbered pitch:

        >>> abjad.NamedPitchClass(abjad.NumberedPitch(14))
        NamedPitchClass('d')

        >>> abjad.NamedPitchClass(abjad.NumberedPitch(14.5))
        NamedPitchClass('dqs')

    ..  container:: example

        Initializes from numbered pitch-class:

        >>> abjad.NamedPitchClass(abjad.NumberedPitchClass(2))
        NamedPitchClass('d')

        >>> abjad.NamedPitchClass(abjad.NumberedPitchClass(2.5))
        NamedPitchClass('dqs')

    ..  container:: example

        Initializes from pitch-class / octave-number string:

        >>> abjad.NamedPitchClass('C#5')
        NamedPitchClass('cs')

        >>> abjad.NamedPitchClass('Cs5')
        NamedPitchClass('cs')

        Initializes quartertone from pitch-class / octave-number string:

        >>> abjad.NamedPitchClass('C+5')
        NamedPitchClass('cqs')

        >>> abjad.NamedPitchClass('Cqs5')
        NamedPitchClass('cqs')

    ..  container:: example

        Initializes from pitch-class string:

        >>> abjad.NamedPitchClass('C#')
        NamedPitchClass('cs')

        >>> abjad.NamedPitchClass('Cs')
        NamedPitchClass('cs')

        >>> abjad.NamedPitchClass('cs')
        NamedPitchClass('cs')

        Initializes quartertone from pitch-class string

        >>> abjad.NamedPitchClass('C+')
        NamedPitchClass('cqs')

        >>> abjad.NamedPitchClass('Cqs')
        NamedPitchClass('cqs')

        >>> abjad.NamedPitchClass('cqs')
        NamedPitchClass('cqs')

    ..  container:: example

        Initializes from note:

        >>> abjad.NamedPitchClass(abjad.Note("d''8."))
        NamedPitchClass('d')

        >>> abjad.NamedPitchClass(abjad.Note("dqs''8."))
        NamedPitchClass('dqs')

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_alteration',
        '_diatonic_pitch_class_number',
        )

    ### INITIALIZER ###

    # TODO: clean up
    def __init__(self, name='c'):
        import abjad
        numbered_prototype = (
            abjad.NumberedPitch,
            abjad.NumberedPitchClass,
            )
        if isinstance(name, type(self)):
            self._initialize_by_named_pitch_class(name)
        elif isinstance(name, abjad.NamedPitch):
            self._initialize_by_named_pitch(name)
        elif abjad.Pitch._is_pitch_class_octave_number_string(name):
            self._initialize_by_pitch_class_octave_number_string(name)
        elif abjad.Pitch._is_pitch_name(name):
            self._initialize_by_pitch_name(name)
        elif isinstance(name, numbers.Number):
            self._initialize_by_number(name)
        elif isinstance(name, numbered_prototype):
            self._initialize_by_number(name.number)
        elif abjad.Pitch._is_pitch_carrier(name):
            self._initialize_by_pitch_carrier(name)
        else:
            message = 'can not instantiate {} from {!r}.'
            message = message.format(type(self).__name__, name)
            raise TypeError(message)

    ### SPECIAL METHODS ###

    def __add__(self, named_interval):
        r'''Adds `named_interval` to named pitch-class.

        ..  container:: example

            >>> abjad.NamedPitchClass('cs') + abjad.NamedInterval('+M9')
            NamedPitchClass('ds')

            >>> abjad.NamedPitchClass('cs') + abjad.NamedInterval('-M9')
            NamedPitchClass('b')

        Returns new named pitch-class.
        '''
        import abjad
        dummy_pitch = abjad.NamedPitch((self.name, 4))
        pitch = named_interval.transpose(dummy_pitch)
        return type(self)(pitch)

    def __copy__(self, *arguments):
        r'''Copies named pitch-class.

        ..  container:: example

            >>> import copy
            >>> copy.copy(abjad.NamedPitchClass('cs'))
            NamedPitchClass('cs')

        Returns new named pitch-class.
        '''
        return super(NamedPitchClass, self).__copy__(*arguments)

    def __eq__(self, argument):
        r'''Is true when `argument` can be coerced to a named pitch-class with
        pitch-class name equal to that of this named pitch-class.

        ..  container:: example

            >>> pitch_class_1 = abjad.NamedPitchClass('cs')
            >>> pitch_class_2 = abjad.NamedPitchClass('cs')
            >>> pitch_class_3 = abjad.NamedPitchClass('df')

            >>> pitch_class_1 == pitch_class_1
            True
            >>> pitch_class_1 == pitch_class_2
            True
            >>> pitch_class_1 == pitch_class_3
            False

            >>> pitch_class_2 == pitch_class_1
            True
            >>> pitch_class_2 == pitch_class_2
            True
            >>> pitch_class_2 == pitch_class_3
            False

            >>> pitch_class_3 == pitch_class_1
            False
            >>> pitch_class_3 == pitch_class_2
            False
            >>> pitch_class_3 == pitch_class_3
            True

        Returns true or false.
        '''
        return super(NamedPitchClass, self).__eq__(argument)

    def __format__(self, format_specification=''):
        r'''Formats named pitch-class.

        ..  container:: example

            >>> format(abjad.NamedPitchClass('cs'))
            "abjad.NamedPitchClass('cs')"

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

    def __lt__(self, argument):
        r'''Is true when `argument` is a named pitch-class with a pitch
        number greater than that of this named pitch-class.

        ..  container:: example

            Compares less than:

            >>> abjad.NamedPitchClass('cs') < abjad.NamedPitchClass('d')
            True

        ..  container:: example

            Does not compare less than:

            >>> abjad.NamedPitchClass('d') < abjad.NamedPitchClass('cs')
            False

        Raises type error when `argument` is not a named pitch-class.
        '''
        if not isinstance(argument, type(self)):
            message = 'can not compare named pitch-class to {!r}.'
            message = message.format(argument)
            raise TypeError(message)
        return self.number < argument.number

    def __radd__(self, interval):
        r'''Right-addition not defined on named pitch-classes.

        ..  container:: example

            >>> abjad.NamedPitchClass("cs").__radd__(1)
            Traceback (most recent call last):
            ...
            NotImplementedError: right-addition not defined on NamedPitchClass.

        '''
        message = 'right-addition not defined on {}.'
        message = message.format(type(self).__name__)
        raise NotImplementedError(message)

    def __str__(self):
        r'''Gets string representation of named pitch-class.

        ..  container:: example

            >>> str(abjad.NamedPitchClass('cs'))
            'cs'

        Returns string.
        '''
        return self.name

    def __sub__(self, argument):
        r'''Subtracts `argument` from named pitch-class.

        ..  container:: example

            >>> abjad.NamedPitchClass('cs') - abjad.NamedPitchClass('g')
            NamedInversionEquivalentIntervalClass('+aug4')

            >>> abjad.NamedPitchClass('c') - abjad.NamedPitchClass('cf')
            NamedInversionEquivalentIntervalClass('aug1')

            >>> abjad.NamedPitchClass('cf') - abjad.NamedPitchClass('c')
            NamedInversionEquivalentIntervalClass('aug1')

        Returns named inversion-equivalent interval-class.
        '''
        import abjad
        if not isinstance(argument, type(self)):
            message = 'must be named pitch-class: {!r}.'
            message = message.format(argument)
            raise TypeError(message)
        pitch_1 = abjad.NamedPitch((self.name, 4))
        pitch_2 = abjad.NamedPitch((argument.name, 4))
        mdi = abjad.NamedInterval.from_pitch_carriers(pitch_1, pitch_2)
        pair = (mdi.quality_string, mdi.number)
        dic = abjad.NamedInversionEquivalentIntervalClass(pair)
        return dic

    ### PRIVATE METHODS ###

    def _apply_accidental(self, accidental=None):
        from abjad.tools import pitchtools
        accidental = pitchtools.Accidental(accidental)
        new_accidental = self.accidental + accidental
        new_name = self._get_diatonic_pitch_class_name() + str(new_accidental)
        return type(self)(new_name)

    def _get_diatonic_pitch_class_name(self):
        return self._diatonic_pitch_class_number_to_diatonic_pitch_class_name[
            self._diatonic_pitch_class_number]

    def _get_format_specification(self):
        import abjad
        values = [self.name]
        return abjad.FormatSpecification(
            client=self,
            coerce_for_equality=True,
            storage_format_is_indented=False,
            storage_format_args_values=values,
            )

    def _initialize_by_named_pitch(self, argument):
        self._alteration = argument._get_alteration()
        number = argument._get_diatonic_pitch_class_number()
        self._diatonic_pitch_class_number = number

    def _initialize_by_named_pitch_class(self, argument):
        self._alteration = argument._alteration
        self._diatonic_pitch_class_number = argument._diatonic_pitch_class_number

    def _initialize_by_number(self, argument):
        import abjad
        pitch_class_number = float(argument) % 12
        numbered_pitch_class = abjad.NumberedPitchClass(pitch_class_number)
        pitch_class_name = numbered_pitch_class.name
        self._initialize_by_pitch_name(pitch_class_name)

    def _initialize_by_pitch_carrier(self, argument):
        import abjad
        named_pitch = abjad.NamedPitch.from_pitch_carrier(argument)
        self._initialize_by_named_pitch(named_pitch)

    def _initialize_by_pitch_class_octave_number_string(self, argument):
        import abjad
        group_dict = abjad.Pitch._pitch_class_octave_number_regex.match(
            argument).groupdict()
        diatonic_pitch_class_name = group_dict['diatonic_pitch_class_name'].lower()
        #symbol = group_dict['symbol']
        symbol = group_dict['comprehensive_accidental']
        self._alteration = abjad.Accidental._symbol_to_semitones[symbol]
        self._diatonic_pitch_class_number = \
            self._diatonic_pitch_class_name_to_diatonic_pitch_class_number[
                diatonic_pitch_class_name]

    def _initialize_by_pitch_name(self, argument):
        import abjad
        match = abjad.Pitch._pitch_name_regex.match(argument.lower())
        assert match is not None, repr(match)
        groups = match.groups()
        diatonic_pitch_class_name = groups[0]
        abbreviation = groups[1]
        accidental = abjad.Accidental(abbreviation)
        self._alteration = accidental.semitones
        self._diatonic_pitch_class_number = \
            self._diatonic_pitch_class_name_to_diatonic_pitch_class_number[
                diatonic_pitch_class_name]

    ### PUBLIC PROPERTIES ###

    @property
    def accidental(self):
        r'''Gets accidental.

        ..  container:: example

            >>> abjad.NamedPitchClass('cs').accidental
            Accidental('sharp')

        Returns accidental.
        '''
        from abjad.tools import pitchtools
        return pitchtools.Accidental(self._alteration)

    @property
    def name(self):
        r'''Gets name of named pitch-class.

        ..  container:: example

            >>> abjad.NamedPitchClass('cs').name
            'cs'

        Returns string.
        '''
        import abjad
        diatonic_pitch_class_name = self._diatonic_pitch_class_number_to_diatonic_pitch_class_name[
            self._diatonic_pitch_class_number
            ]
        accidental_abbreviation = abjad.Accidental._semitones_to_abbreviation[
            self._alteration
            ]
        return '{}{}'.format(
            diatonic_pitch_class_name,
            accidental_abbreviation,
            )

    @property
    def number(self):
        r'''Gets number.

        ..  container:: example

            >>> abjad.NamedPitchClass('cs').number
            1

        Returns nonnegative integer or float.
        '''
        dictionary = self._diatonic_pitch_class_number_to_pitch_class_number
        result = dictionary[self._diatonic_pitch_class_number]
        result += self._alteration
        result %= 12
        return result

    @property
    def pitch_class_label(self):
        r'''Gets pitch-class label.

        ..  container:: example

            >>> abjad.NamedPitchClass('cs').pitch_class_label
            'C#'

        Returns string.
        '''
        return '{}{}'.format(
            self._get_diatonic_pitch_class_name().upper(),
            self.accidental.symbol,
            )

    ### PUBLIC METHODS ###

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

            >>> abjad.NamedPitchClass('cs').multiply(3)
            NamedPitchClass('ef')

        Returns new named pitch-class.
        '''
        return type(self)(n * self.number)

    def transpose(self, n=0):
        r'''Transposes named pitch-class by index named interval `n`.

        ..  container:: example

            >>> interval = abjad.NamedInterval('-M2')
            >>> abjad.NamedPitchClass('cs').transpose(interval)
            NamedPitchClass('b')

            >>> interval = abjad.NamedInterval('P1')
            >>> abjad.NamedPitchClass('cs').transpose(interval)
            NamedPitchClass('cs')

            >>> interval = abjad.NamedInterval('+M2')
            >>> abjad.NamedPitchClass('cs').transpose(interval)
            NamedPitchClass('ds')

        Returns new named pitch-class.
        '''
        from abjad.tools import pitchtools
        interval = pitchtools.NamedInterval(n)
        pitch = pitchtools.NamedPitch((self.name, 4))
        pitch = interval.transpose(pitch)
        return type(self)(pitch)
