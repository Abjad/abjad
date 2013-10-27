# -*- encoding: utf-8 -*-
import collections
import re
from abjad.tools import mathtools
from abjad.tools.pitchtools.Pitch import Pitch


class NamedPitch(Pitch):
    '''A named pitch.

    ::

        >>> pitchtools.NamedPitch("cs''")
        NamedPitch("cs''")

    Returns named pitch.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_alteration_in_semitones',
        '_diatonic_pitch_class_number',
        '_octave_number',
        )

    ### INITIALIZER ###

    def __init__(self, *args):
        from abjad.tools import pitchtools
        if isinstance(args[0], collections.Iterable) and \
            not isinstance(args[0], basestring) and \
            len(args) == 1:
            args = args[0]
        if len(args) == 1:
            if isinstance(args[0], (int, long, float)):
                self._init_by_pitch_number(*args)
            elif isinstance(args[0], type(self)):
                self._init_by_named_pitch(*args)
            elif isinstance(args[0], pitchtools.NumberedPitch):
                self._init_by_pitch_number(
                    args[0].pitch_number)
            elif hasattr(args[0], 'named_pitch'):
                self._init_by_named_pitch(args[0].named_pitch)
            elif self.is_pitch_class_octave_number_string(args[0]):
                self._init_by_pitch_class_octave_number_string(*args)
            elif isinstance(args[0], str):
                self._init_by_pitch_name(*args)
            else:
                raise ValueError('Cannot instantiate {} from {!r}.'.format(
                    self._class_name, args))
        elif len(args) == 2:
            if isinstance(args[0], str):
                self._init_by_pitch_class_name_and_octave_number(*args)
            elif isinstance(args[0], pitchtools.NamedPitchClass):
                self._init_by_named_pitch_class_and_octave_number(*args)
            elif isinstance(args[0], (int, long, float)):
                if isinstance(args[1], str):
                    self._init_by_pitch_number_and_diatonic_pitch_class_name(
                        *args)
                elif isinstance(args[1], pitchtools.NamedPitchClass):
                    self._init_by_pitch_number_and_named_pitch_class(*args)
                else:
                    raise TypeError
            else:
                raise ValueError('Cannot instantiate {} from {!r}.'.format(
                    self._class_name, args))
        else:
            raise ValueError('Cannot instantiate {} from {!r}.'.format(
                self._class_name, args))

    ### SPECIAL METHODS ###

    def __abs__(self):
        return abs(self.pitch_number)

    def __add__(self, interval):
        from abjad.tools import pitchtools
        return pitchtools.transpose_pitch_carrier_by_interval(
            self, interval)

    def __copy__(self, *args):
        return type(self)(self)

    def __eq__(self, arg):
        try:
            arg = type(self)(arg)
            if str(self) == str(arg):
                return True
            return False
        except (TypeError, ValueError):
            return False

    def __float__(self):
        return float(self.pitch_number)

    def __ge__(self, arg):
        from abjad.tools import pitchtools
        try:
            arg = type(self)(arg)
            return self.diatonic_pitch_number > arg.diatonic_pitch_number or \
                (self.diatonic_pitch_number == arg.diatonic_pitch_number and
                self.alteration_in_semitones >= arg.alteration_in_semitones)
        except (TypeError, ValueError):
            if isinstance(arg, pitchtools.PitchRange):
                return self >= arg.stop_pitch
        return False

    def __getnewargs__(self):
        return (self.pitch_name,)

    def __gt__(self, arg):
        from abjad.tools import pitchtools
        if isinstance(arg, type(self)):
            return self.diatonic_pitch_number > arg.diatonic_pitch_number or \
                (self.diatonic_pitch_number == arg.diatonic_pitch_number and \
                self.alteration_in_semitones > arg.alteration_in_semitones)
        elif isinstance(arg, pitchtools.PitchRange):
            return self > arg.stop_pitch
        return False

    def __hash__(self):
        return hash(repr(self))

    def __int__(self):
        if not mathtools.is_integer_equivalent_number(self.pitch_number):
            raise TypeError
        return int(self.pitch_number)

    def __le__(self, arg):
        from abjad.tools import pitchtools
        if isinstance(arg, type(self)):
            if not self.diatonic_pitch_number == arg.diatonic_pitch_number:
                return self.diatonic_pitch_number <= arg.diatonic_pitch_number
            if not self.alteration_in_semitones == arg.alteration_in_semitones:
                return self.alteration_in_semitones <= arg.alteration_in_semitones
            return True
        elif isinstance(arg, pitchtools.PitchRange):
            return self <= arg.start_pitch
        return False

    def __lt__(self, arg):
        from abjad.tools import pitchtools
        if isinstance(arg, type(self)):
            return self.diatonic_pitch_number < arg.diatonic_pitch_number or \
                (self.diatonic_pitch_number == arg.diatonic_pitch_number and \
                self.alteration_in_semitones < arg.alteration_in_semitones)
        elif isinstance(arg, pitchtools.PitchRange):
            return self < arg.start_pitch
        return False

    def __ne__(self, arg):
        return not self == arg

    def __repr__(self):
        return '{}({!r})'.format(
            self._class_name,
            self.pitch_name,
            )

    def __str__(self):
        return self.pitch_name

    def __sub__(self, arg):
        from abjad.tools import pitchtools
        if isinstance(arg, type(self)):
            return pitchtools.NamedInterval.from_pitch_carriers(
                self, arg)
        else:
            interval = arg
            return pitchtools.transpose_pitch_carrier_by_interval(
                self, -interval)

    ### PRIVATE PROPERTIES ###

    @property
    def _positional_argument_values(self):
        return (
            self.pitch_name,
            )

    ### PRIVATE METHODS ###

    def _init_by_named_pitch(self, named_pitch):
        self._alteration_in_semitones = named_pitch._alteration_in_semitones
        self._diatonic_pitch_class_number = \
            named_pitch.diatonic_pitch_class_number
        self._octave_number = named_pitch.octave_number

    def _init_by_named_pitch_class_and_octave_number(
        self, named_pitch_class, octave_number):
        self._alteration_in_semitones = \
            named_pitch_class._alteration_in_semitones
        self._diatonic_pitch_class_number = \
            named_pitch_class._diatonic_pitch_class_number
        self._octave_number = octave_number

    def _init_by_pitch_class_name_and_octave_number(
        self, pitch_class_name, octave_number):
        from abjad.tools import pitchtools
        named_pitch_class = pitchtools.NamedPitchClass(pitch_class_name)
        self._init_by_named_pitch_class_and_octave_number(
            named_pitch_class, octave_number)

    def _init_by_pitch_class_name_octave_number_pair(self, pair):
        pitch_class_name, octave_number = pair
        self._init_by_pitch_class_name_and_octave_number(
            pitch_class_name, octave_number)

    def _init_by_pitch_class_octave_number_string(
        self, pitch_class_octave_number_string):
        from abjad.tools import pitchtools
        groups = self._pitch_class_octave_number_regex.match(
            pitch_class_octave_number_string).groups()
        named_pitch_class = pitchtools.NamedPitchClass(
            pitch_class_octave_number_string)
        octave_number = int(groups[2])
        self._init_by_named_pitch_class_and_octave_number(
            named_pitch_class, octave_number)

    def _init_by_pitch_name(self, pitch_string):
        from abjad.tools import pitchtools
        named_pitch_class = pitchtools.NamedPitchClass(pitch_string)
        octave_number = pitchtools.Octave.from_pitch_name(
            pitch_string).octave_number
        self._init_by_named_pitch_class_and_octave_number(
            named_pitch_class, octave_number)

    def _init_by_pitch_number(self, pitch_number):
        from abjad.tools import pitchtools
        named_pitch_class = pitchtools.NamedPitchClass(pitch_number)
        octave_number = pitch_number // 12 + 4
        self._init_by_named_pitch_class_and_octave_number(
            named_pitch_class, octave_number)

    def _init_by_pitch_number_and_diatonic_pitch_class_name(
        self, pitch_number, diatonic_pitch_class_name):
        from abjad.tools import pitchtools
        accidental, octave_number = \
            pitchtools.spell_pitch_number(
                pitch_number, diatonic_pitch_class_name)
        pitch_class_name = diatonic_pitch_class_name + \
            accidental.alphabetic_accidental_abbreviation
        named_pitch_class = pitchtools.NamedPitchClass(pitch_class_name)
        self._init_by_named_pitch_class_and_octave_number(
            named_pitch_class, octave_number)

    def _init_by_pitch_number_and_named_pitch_class(
        self, pitch_number, named_pitch_class):
        diatonic_pitch_class_name = named_pitch_class.diatonic_pitch_class_name
        self._init_by_pitch_number_and_diatonic_pitch_class_name(
            pitch_number, diatonic_pitch_class_name)

    ### PUBLIC METHODS ###

    def apply_accidental(self, accidental=None):
        '''Apply `accidental` to named pitch.

        ::

            >>> pitchtools.NamedPitch("cs''").apply_accidental('s')
            NamedPitch("css''")

        Returns new named pitch.
        '''
        from abjad.tools import pitchtools
        accidental = pitchtools.Accidental(accidental)
        new_accidental = self.accidental + accidental
        new_name = self.diatonic_pitch_class_name
        new_name += new_accidental.alphabetic_accidental_abbreviation
        return type(self)(new_name, self.octave_number)

    def invert(self, axis=None):
        r'''Invert pitch around `axis`.

        Not yet implemented.
        '''
        raise NotImplementedError

    def multiply(self, n=1):
        r'''Multiply pitch-class by `n`, maintaining octave.

        ::

            >>> pitchtools.NamedPitch('cs,').multiply(3)
            NamedPitch('ef,')

        Emit new numbered pitch.
        '''
        pitch_class_number = (self.pitch_class_number * n) % 12
        octave_floor = (self.octave_number - 4) * 12
        return type(self)(pitch_class_number + octave_floor)

    def respell_with_flats(self):
        from abjad.tools import pitchtools
        octave = pitchtools.Octave.from_pitch_number(
            abs(self.numbered_pitch)).octave_number
        name = pitchtools.PitchClass._pitch_class_number_to_pitch_class_name_with_flats[
            self.pitch_class_number]
        pitch = type(self)(name, octave)
        return pitch

    def respell_with_sharps(self):
        from abjad.tools import pitchtools
        octave = pitchtools.Octave.from_pitch_number(
            abs(self.numbered_pitch)).octave_number
        name = pitchtools.PitchClass._pitch_class_number_to_pitch_class_name_with_sharps[
            self.pitch_class_number]
        pitch = type(self)(name, octave)
        return pitch

    def transpose(self, expr):
        r'''Transpose by `expr`.

        Not yet implemented.
        '''
        raise NotImplementedError

    ### PUBLIC PROPERTIES ###

    @property
    def accidental(self):
        r'''Accidental.

        ::

            >>> pitchtools.NamedPitch("cs''").accidental
            Accidental('s')

        Returns accidental.
        '''
        from abjad.tools import pitchtools
        return pitchtools.Accidental(self._alteration_in_semitones)

    @property
    def alteration_in_semitones(self):
        r'''Alteration in semitones.

        ::

            >>> pitchtools.NamedPitch("cs''").alteration_in_semitones
            1

        Returns integer or float.
        '''
        return self._alteration_in_semitones

    @property
    def diatonic_pitch_class_name(self):
        r'''Diatonic pitch-class name.

        ::

            >>> pitchtools.NamedPitch("cs''").diatonic_pitch_class_name
            'c'

        Returns string.
        '''
        from abjad.tools import pitchtools
        return pitchtools.PitchClass._diatonic_pitch_class_number_to_diatonic_pitch_class_name[
            self._diatonic_pitch_class_number]

    @property
    def diatonic_pitch_class_number(self):
        r'''Diatonic pitch-class number.

        ::

            >>> pitchtools.NamedPitch("cs''").diatonic_pitch_class_number
            0

        Returns integer.
        '''
        return self._diatonic_pitch_class_number

    @property
    def diatonic_pitch_name(self):
        r'''Diatonic pitch name.

        ::

            >>> pitchtools.NamedPitch("cs''").diatonic_pitch_name
            "c''"

        Returns string.
        '''
        return '{}{}'.format(
            self.diatonic_pitch_class_name,
            self.octave.octave_tick_string,
            )

    @property
    def diatonic_pitch_number(self):
        r'''Diatonic pitch number.

        ::

            >>> pitchtools.NamedPitch("cs''").diatonic_pitch_number
            7

        Returns integer.
        '''
        return ((self._octave_number - 4) * 7) + \
            self._diatonic_pitch_class_number

    @property
    def lilypond_format(self):
        r'''LilyPond input format.

        ::

            >>> pitchtools.NamedPitch("cs''").lilypond_format
            "cs''"

        Returns string.
        '''
        return str(self)

    @property
    def named_pitch(self):
        r'''Named pitch.

        ::

            >>> pitchtools.NamedPitch("cs''").named_pitch
            NamedPitch("cs''")

        Returns named pitch.
        '''
        return type(self)(self)

    @property
    def named_pitch_class(self):
        r'''Named pitch-class.

        ::

            >>> pitchtools.NamedPitch("cs''").named_pitch_class
            NamedPitchClass('cs')

        Returns named pitch-class.
        '''
        from abjad.tools import pitchtools
        return pitchtools.NamedPitchClass(self)

    @property
    def numbered_pitch(self):
        r'''Numbered pitch.

        ::

            >>> pitchtools.NamedPitch("cs''").numbered_pitch
            NumberedPitch(13)

        Returns numbered pitch.
        '''
        from abjad.tools import pitchtools
        return pitchtools.NumberedPitch(self)

    @property
    def numbered_pitch_class(self):
        r'''Numbered pitch-class.

        ::

            >>> pitchtools.NamedPitch("cs''").numbered_pitch_class
            NumberedPitchClass(1)

        Returns numbered pitch-class.
        '''
        from abjad.tools import pitchtools
        return pitchtools.NumberedPitchClass(self)

    @property
    def octave(self):
        r'''Octave indication.

        ::

            >>> pitchtools.NamedPitch("cs''").octave
            Octave(5)

        Returns octave.
        '''
        from abjad.tools import pitchtools
        return pitchtools.Octave(self._octave_number)

    @property
    def octave_number(self):
        r'''Integer octave number.

        ::

            >>> pitchtools.NamedPitch("cs''").octave_number
            5

        Returns integer.
        '''
        return self._octave_number

    @property
    def pitch_class_name(self):
        r'''Pitch-class name.

        ::

            >>> pitchtools.NamedPitch("cs''").pitch_class_name
            'cs'

        Returns string.
        '''
        from abjad.tools import pitchtools
        return '{}{}'.format(
            self.diatonic_pitch_class_name,
            pitchtools.Accidental._semitones_to_alphabetic_accidental_abbreviation[
                self._alteration_in_semitones],
            )

    @property
    def pitch_class_number(self):
        r'''Pitch-class number.

        ::

            >>> pitchtools.NamedPitch("cs''").pitch_class_number
            1

        Returns integer or float.
        '''
        from abjad.tools import pitchtools
        return (pitchtools.PitchClass._diatonic_pitch_class_number_to_pitch_class_number[
            self._diatonic_pitch_class_number] + \
            self._alteration_in_semitones) % 12

    @property
    def pitch_class_octave_label(self):
        r'''Pitch-class / octave label.

        ::

            >>> pitchtools.NamedPitch("cs''").pitch_class_octave_label
            'C#5'

        Returns string.
        '''
        return '{}{}{}'.format(
            self.diatonic_pitch_class_name.upper(),
            self.accidental.symbolic_accidental_string,
            self.octave_number,
            )

    @property
    def pitch_name(self):
        r'''Pitch name.

        ::

            >>> pitchtools.NamedPitch("cs''").pitch_name
            "cs''"

        Returns string.
        '''
        return '{}{}'.format(
            self.pitch_class_name,
            self.octave.octave_tick_string,
            )

    @property
    def pitch_number(self):
        r'''Pitch-class number.

        ::

            >>> pitchtools.NamedPitch("cs''").pitch_number
            13

        ::

            >>> pitchtools.NamedPitch("cff''").pitch_number
            10

        Returns integer or float.
        '''
        from abjad.tools import pitchtools
        return pitchtools.PitchClass._diatonic_pitch_class_number_to_pitch_class_number[
            self.diatonic_pitch_class_number] + \
            self.alteration_in_semitones + \
            (12 * (self._octave_number - 4))
