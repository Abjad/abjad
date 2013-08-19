# -*- encoding: utf-8 -*-
from abjad.tools.pitchtools.PitchClass import PitchClass


class NumberedChromaticPitchClass(PitchClass):
    '''Abjad model of a numbered chromatic pitch-class:

    ::

        >>> pitchtools.NumberedChromaticPitchClass(13)
        NumberedChromaticPitchClass(1)

    Numbered chromatic pitch-classes are immutable.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_chromatic_pitch_class_number',
        )

    ### INITIALIZER ###

    def __init__(self, arg):
        from abjad.tools import pitchtools
        if pitchtools.is_chromatic_pitch_number(arg):
            number = \
                pitchtools.chromatic_pitch_number_to_chromatic_pitch_class_number(
                    arg)
        elif isinstance(arg, type(self)):
            number = abs(arg)
        elif pitchtools.is_chromatic_pitch_name(arg):
            number = \
                pitchtools.chromatic_pitch_name_to_chromatic_pitch_class_number(
                    arg)
        elif isinstance(arg, pitchtools.NamedPitch):
            number = abs(arg.numbered_chromatic_pitch) % 12
        elif isinstance(arg, pitchtools.NamedPitchClass):
            number = abs(arg.numbered_chromatic_pitch_class)
        else:
            pitch = \
                pitchtools.get_named_chromatic_pitch_from_pitch_carrier(arg)
            number = abs(pitch.numbered_chromatic_pitch) % 12
        object.__setattr__(self, '_chromatic_pitch_class_number', number)
        object.__setattr__(self, '_comparison_attribute', number)

    ### SPECIAL METHODS ###

    def __abs__(self):
        return self._chromatic_pitch_class_number

    def __add__(self, arg):
        r'''Addition defined against melodic chromatic intervals only.
        '''
        from abjad.tools import pitchtools
        if not isinstance(arg, pitchtools.MelodicChromaticInterval):
            raise TypeError('must be melodic chromatic interval.')
        return type(self)(abs(self) + arg.number % 12)

    def __copy__(self, *args):
        return type(self)(self)

    # TODO: remove?
    __deepcopy__ = __copy__

    def __float__(self):
        return float(self._chromatic_pitch_class_number)

    def __int__(self):
        return self._chromatic_pitch_class_number

    def __neg__(self):
        return type(self)(-abs(self))

    def __repr__(self):
        return '%s(%s)' % (self._class_name, abs(self))

    def __str__(self):
        return str(abs(self))

    def __sub__(self, arg):
        r'''Subtraction defined against both melodic chromatic intervals
        and against other pitch-classes.
        '''
        from abjad.tools import pitchtools
        if isinstance(arg, type(self)):
            interval_class_number = abs(abs(self) - abs(arg))
            if 6 < interval_class_number:
                interval_class_number = 12 - interval_class_number
            return pitchtools.InversionEquivalentChromaticIntervalClass(
                interval_class_number)
        elif isinstance(arg, 
            pitchtools.InversionEquivalentChromaticIntervalClass):
            return type(self)(abs(self) - arg.number % 12)
        else:
            raise TypeError('must be pitch-class or interval-class.')

    ### PUBLIC METHODS ###

    def apply_accidental(self, accidental=None):
        r'''Emit new numbered chromatic pitch-class as sum 
        of self and accidental.
        '''
        from abjad.tools import pitchtools
        accidental = pitchtools.Accidental(accidental)
        semitones = abs(self) + accidental.semitones
        return type(self)(semitones)

    def invert(self):
        r'''Invert pitch-class.
        '''
        return type(self)(12 - abs(self))

    def multiply(self, n):
        r'''Multiply pitch-class by n.
        '''
        return type(self)(abs(self) * n)

    def transpose(self, n):
        r'''Transpose pitch-class by n.
        '''
        return type(self)(abs(self) + n)
