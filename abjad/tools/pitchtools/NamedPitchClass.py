# -*- encoding: utf-8 -*-
import numbers
from abjad.tools.pitchtools.PitchClass import PitchClass


class NamedPitchClass(PitchClass):
    '''A named pitch-class.

    ::

        >>> pitchtools.NamedPitchClass('cs')
        NamedPitchClass('cs')

    ::

        >>> pitchtools.NamedPitchClass(14)
        NamedPitchClass('d')

    ::

        >>> pitchtools.NamedPitchClass(NamedPitch('g,'))
        NamedPitchClass('g')

    ::

        >>> pitchtools.NamedPitchClass(pitchtools.NumberedPitch(15))
        NamedPitchClass('ef')

    ::

        >>> pitchtools.NamedPitchClass(pitchtools.NumberedPitchClass(4))
        NamedPitchClass('e')

    ::

        >>> pitchtools.NamedPitchClass('C#5')
        NamedPitchClass('cs')

    ::

        >>> pitchtools.NamedPitchClass(Note("a'8."))
        NamedPitchClass('a')

    Returns named pitch-class.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_alteration_in_semitones',
        '_diatonic_pitch_class_number',
        )

    ### INITIALIZER ###

    def __init__(self, expr):
        from abjad.tools import pitchtools
        if isinstance(expr, type(self)):
            self._init_by_named_pitch_class(expr)
        elif isinstance(expr, pitchtools.NamedPitch):
            self._init_by_named_pitch(expr)
        elif pitchtools.Pitch.is_pitch_class_octave_number_string(expr):
            self._init_by_pitch_class_octave_number_string(expr)
        elif pitchtools.Pitch.is_pitch_name(expr):
            self._init_by_pitch_name(expr)
        elif isinstance(expr, (
            numbers.Number,
            pitchtools.NumberedPitch,
            pitchtools.NumberedPitchClass,
            )):
            self._init_by_number(float(expr))
        elif pitchtools.Pitch.is_pitch_carrier(expr):
            self._init_by_pitch_carrier(expr)
        else:
            raise TypeError('Cannot instantiate {} from '
                '{!r}.'.format(type(self).__name__, expr))

    ### SPECIAL METHODS ###

    def __abs__(self):
        return abs(self.numbered_pitch_class)

    def __add__(self, named_interval):
        from abjad.tools import pitchtools
        dummy = pitchtools.NamedPitch(
            self.pitch_class_name, 4)
        mdi = named_interval
        new = pitchtools.transpose_pitch_carrier_by_interval(
            dummy, mdi)
        return type(self)(new)

    def __copy__(self, *args):
        return type(self)(self)

    def __eq__(self, expr):
        if isinstance(expr, type(self)):
            return self.pitch_class_name == \
                expr.pitch_class_name
        return self.pitch_class_name == expr

    def __float__(self):
        return float(self.numbered_pitch_class)

    def __int__(self):
        return int(self.numbered_pitch_class)

    def __repr__(self):
        return '{}({!r})'.format(
            type(self).__name__,
            self.pitch_class_name,
            )

    def __str__(self):
        return self.pitch_class_name

    def __sub__(self, arg):
        if not isinstance(arg, type(self)):
            raise TypeError('%s must be named pitch-class.' % arg)
        from abjad.tools import pitchtools
        pitch_1 = pitchtools.NamedPitch(self, 4)
        pitch_2 = pitchtools.NamedPitch(arg, 4)
        mdi = pitchtools.NamedInterval.from_pitch_carriers(
            pitch_1, pitch_2)
        dic = pitchtools.NamedInversionEquivalentIntervalClass(
            mdi.quality_string, mdi.number)
        return dic

    ### PRIVATE METHODS ###

    def _init_by_named_pitch(self, expr):
        self._alteration_in_semitones = expr.alteration_in_semitones
        self._diatonic_pitch_class_number = expr.diatonic_pitch_class_number

    def _init_by_named_pitch_class(self, expr):
        self._alteration_in_semitones = expr.alteration_in_semitones
        self._diatonic_pitch_class_number = expr.diatonic_pitch_class_number

    def _init_by_number(self, expr):
        from abjad.tools import pitchtools
        pitch_class_number = float(expr) % 12
        numbered_pitch_class = pitchtools.NumberedPitchClass(
            pitch_class_number)
        pitch_class_name = numbered_pitch_class.pitch_class_name
        self._init_by_pitch_name(pitch_class_name)

    def _init_by_pitch_carrier(self, expr):
        from abjad.tools import pitchtools
        named_pitch = pitchtools.get_named_pitch_from_pitch_carrier(
            expr)
        self._init_by_named_pitch(named_pitch)

    def _init_by_pitch_class_octave_number_string(self, expr):
        from abjad.tools import pitchtools
        groups = pitchtools.Pitch._pitch_class_octave_number_regex.match(
            expr).groups()
        diatonic_pitch_class_name = groups[0].lower()
        symbolic_string = groups[1]
        self._alteration_in_semitones = \
            pitchtools.Accidental._symbolic_string_to_semitones[
                symbolic_string]
        self._diatonic_pitch_class_number = \
            self._diatonic_pitch_class_name_to_diatonic_pitch_class_number[
                diatonic_pitch_class_name]

    def _init_by_pitch_name(self, expr):
        from abjad.tools import pitchtools
        match = pitchtools.Pitch._pitch_name_regex.match(expr.lower())
        if match is None:
            raise ValueError
        groups = match.groups()
        diatonic_pitch_class_name = groups[0]
        abbreviation = groups[1]
        self._alteration_in_semitones = \
            pitchtools.Accidental._abbreviation_to_semitones[abbreviation]
        self._diatonic_pitch_class_number = \
            self._diatonic_pitch_class_name_to_diatonic_pitch_class_number[
                diatonic_pitch_class_name]

    ### PUBLIC METHODS ###

    def apply_accidental(self, accidental):
        r'''Applies `accidental`.

        ::

            >>> pitchtools.NamedPitchClass('cs').apply_accidental('qs')
            NamedPitchClass('ctqs')

        Emits new named pitch-class.
        '''
        from abjad.tools import pitchtools
        accidental = pitchtools.Accidental(accidental)
        new_accidental = self.accidental + accidental
        new_name = self.diatonic_pitch_class_name + new_accidental.abbreviation
        return type(self)(new_name)

    def invert(self):
        r'''Invert pitch-class.

        Not yet implemented.
        '''
        raise NotImplementedError

    def multiply(self, n=1):
        r'''Multiply pitch-class number by `n`:

        ::

            >>> pitchtools.NamedPitchClass('cs').multiply(3)
            NamedPitchClass('ef')

        Emit new named pitch-class.
        '''
        return type(self)(self.pitch_class_number * n)

    def transpose(self, n):
        r'''Transpose named pitch-class by
        `named_interval`:

        ::

            >>> pitchtools.NamedPitchClass('cs').transpose(
            ...     pitchtools.NamedInterval('major', 2))
            NamedPitchClass('ds')

        Emit new named pitch-class.
        '''
        from abjad.tools import pitchtools
        named_interval = pitchtools.NamedInterval(n)
        pitch = pitchtools.NamedPitch(self, 4)
        transposed_pitch = \
            pitchtools.transpose_pitch_carrier_by_interval(
                pitch, named_interval)
        return type(self)(transposed_pitch)

    ### PUBLIC PROPERTIES ###

    @property
    def accidental(self):
        r'''Accidental.

        ::

            >>> pitchtools.NamedPitchClass('cs').accidental
            Accidental('s')

        Returns accidental.
        '''
        from abjad.tools import pitchtools
        return pitchtools.Accidental(self._alteration_in_semitones)

    @property
    def alteration_in_semitones(self):
        r'''Alteration in semitones.

        ::

            >>> pitchtools.NamedPitchClass('cs').alteration_in_semitones
            1

        Returns integer or float.
        '''
        return self._alteration_in_semitones

    @property
    def diatonic_pitch_class_name(self):
        r'''Diatonic pitch-class name.

        ::

            >>> pitchtools.NamedPitchClass('cs').diatonic_pitch_class_name
            'c'

        Returns string.
        '''
        return self._diatonic_pitch_class_number_to_diatonic_pitch_class_name[
            self._diatonic_pitch_class_number]

    @property
    def diatonic_pitch_class_number(self):
        r'''Diatonic pitch-class number.

        ::

            >>> pitchtools.NamedPitchClass('cs').diatonic_pitch_class_number
            0

        Returns integer.
        '''
        return self._diatonic_pitch_class_number

    @property
    def named_pitch_class(self):
        r'''Named pitch-class.

        ::

            >>> pitchtools.NamedPitchClass('cs').named_pitch_class
            NamedPitchClass('cs')

        Returns named pitch-class.
        '''
        return type(self)(self)

    @property
    def numbered_pitch_class(self):
        r'''Numbered pitch-class.

        ::

            >>> pitchtools.NamedPitchClass('cs').numbered_pitch_class
            NumberedPitchClass(1)

        Returns numbered pitch-class.
        '''
        from abjad.tools import pitchtools
        return pitchtools.NumberedPitchClass(self)

    @property
    def pitch_class_label(self):
        r'''Pitch-class label.

        ::

            >>> pitchtools.NamedPitchClass('cs').pitch_class_label
            'C#'

        Returns string.
        '''
        return '{}{}'.format(
            self.diatonic_pitch_class_name.upper(),
            self.accidental.symbolic_string,
            )

    @property
    def pitch_class_name(self):
        r'''Pitch-class name.

        ::

            >>> pitchtools.NamedPitchClass('cs').pitch_class_name
            'cs'

        Returns string.
        '''
        from abjad.tools import pitchtools
        return '{}{}'.format(
            self.diatonic_pitch_class_name,
            pitchtools.Accidental._semitones_to_abbreviation[
                self._alteration_in_semitones],
            )

    @property
    def pitch_class_number(self):
        r'''Pitch-class number.

        ::

            >>> pitchtools.NamedPitchClass('cs').pitch_class_number
            1

        Returns integer or float.
        '''
        return (self._diatonic_pitch_class_number_to_pitch_class_number[
            self._diatonic_pitch_class_number] +
            self._alteration_in_semitones) % 12
