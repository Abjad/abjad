# -*- encoding: utf-8 -*-
from abjad.tools.pitchtools.PitchClass import PitchClass


class NumberedPitchClass(PitchClass):
    '''Abjad model of a numbered chromatic pitch-class:

    ::

        >>> pitchtools.NumberedPitchClass(13)
        NumberedPitchClass(1)

    Numbered chromatic pitch-classes are immutable.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_chromatic_pitch_class_number',
        )

    ### INITIALIZER ###

    def __init__(self, expr):
        from abjad.tools import pitchtools
        if pitchtools.is_chromatic_pitch_number(expr):
            number = \
                pitchtools.chromatic_pitch_number_to_chromatic_pitch_class_number(
                    expr)
        elif isinstance(expr, type(self)):
            number = abs(expr)
        elif pitchtools.is_chromatic_pitch_name(expr):
            number = \
                pitchtools.chromatic_pitch_name_to_chromatic_pitch_class_number(
                    expr)
        elif isinstance(expr, pitchtools.NamedPitch):
            number = abs(expr.numbered_chromatic_pitch) % 12
        elif isinstance(expr, pitchtools.NamedPitchClass):
            number = abs(expr.numbered_chromatic_pitch_class)
        else:
            pitch = \
                pitchtools.get_named_chromatic_pitch_from_pitch_carrier(expr)
            number = abs(pitch.numbered_chromatic_pitch) % 12
        self._chromatic_pitch_class_number = number

    ### SPECIAL METHODS ###

    def __abs__(self):
        return self._chromatic_pitch_class_number

    def __add__(self, expr):
        r'''Addition defined against melodic chromatic intervals only.
        '''
        from abjad.tools import pitchtools
        interval = pitchtools.NumberedMelodicInterval(expr)
        return type(self)(abs(self) + interval.number % 12)

    def __copy__(self, *args):
        return type(self)(self)

    # TODO: remove?
    __deepcopy__ = __copy__

    def __eq__(self, expr):
        if isinstance(expr, type(self)):
            return self._chromatic_pitch_class_number == \
                expr._chromatic_pitch_class_number
        return self._chromatic_pitch_class_number == expr

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

    def __sub__(self, expr):
        r'''Subtraction defined against both melodic chromatic intervals
        and against other pitch-classes.
        '''
        from abjad.tools import pitchtools
        if isinstance(expr, type(self)):
            interval_class_number = abs(abs(self) - abs(expr))
            if 6 < interval_class_number:
                interval_class_number = 12 - interval_class_number
            return pitchtools.NumberedInversionEquivalentIntervalClass(
                interval_class_number)
        interval_class = pitchtools.NumberedInversionEquivalentIntervalClass(
            expr)
        return type(self)(abs(self) - interval_class.number % 12)

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
