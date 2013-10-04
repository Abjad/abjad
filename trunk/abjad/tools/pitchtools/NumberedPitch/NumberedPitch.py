# -*- encoding: utf-8 -*-
import functools
from abjad.tools.pitchtools.Pitch import Pitch


@functools.total_ordering
class NumberedPitch(Pitch):
    '''Abjad model of a numbered chromatic pitch:

    ::

        >>> pitch = pitchtools.NumberedPitch(13)
        >>> pitch
        NumberedPitch(13)

    Numbered chromatic pitches are immutable.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_chromatic_pitch_number',
        )

    ### INITIALIZER ###

    def __init__(self, arg):
        from abjad.tools import pitchtools
        if hasattr(arg, 'chromatic_pitch_number'):
            chromatic_pitch_number = arg.chromatic_pitch_number
        elif pitchtools.is_chromatic_pitch_number(arg):
            chromatic_pitch_number = arg
        elif pitchtools.is_pitch_name(arg):
            chromatic_pitch_number = \
                pitchtools.pitch_name_to_chromatic_pitch_number(arg)
        else:
            raise TypeError(
                'can not initialize numbered chromatic pitch from "%s".' % 
                arg)
        self._chromatic_pitch_number = chromatic_pitch_number

    ### SPECIAL METHODS ###

    def __abs__(self):
        return self._chromatic_pitch_number

    def __add__(self, arg):
        arg = type(self)(arg)
        semitones = abs(self) + abs(arg)
        return type(self)(semitones)

    def __eq__(self, expr):
        if isinstance(expr, type(self)):
            return self._chromatic_pitch_number == expr._chromatic_pitch_number
        return self._chromatic_pitch_number == expr

    def __float__(self):
        return float(self._chromatic_pitch_number)

    def __getnewargs__(self):
        return (self._chromatic_pitch_number, )

    def __hash__(self):
        return hash(repr(self))

    def __int__(self):
        return self._chromatic_pitch_number

    def __lt__(self, expr):
        if isinstance(expr, type(self)):
            return self._chromatic_pitch_number < expr._chromatic_pitch_number
        try:
            expr = type(self)(expr)
        except (ValueError, TypeError):
            return False
        return self._chromatic_pitch_number < expr._chromatic_pitch_number

    def __neg__(self):
        return type(self)(-abs(self))

    def __repr__(self):
        return '%s(%s)' % (self._class_name, abs(self))

    def __str__(self):
        return '%s' % abs(self)

    def __sub__(self, arg):
        from abjad.tools import pitchtools
        if isinstance(arg, type(self)):
            return pitchtools.NumberedInterval.from_pitch_carriers(
                self, arg)
        else:
            interval = arg
            return pitchtools.transpose_pitch_carrier_by_melodic_interval(
                self, -interval)

    ### PRIVATE PROPERTIES ###

    @property
    def _keyword_argument_names(self):
        return ()

    @property
    def _positional_argument_values(self):
        return (
            self.chromatic_pitch_number,
            )

    ### PUBLIC PROPERTIES ###

    @property
    def chromatic_pitch_number(self):
        r'''Chromatic pitch-class number:

        ::

            >>> pitch.chromatic_pitch_number
            13

        Return integer or float.
        '''
        return self._chromatic_pitch_number

    @property
    def diatonic_pitch_class_number(self):
        r'''Diatonic pitch-class number:

        ::

            >>> pitch.diatonic_pitch_class_number
            0

        Return integer.
        '''
        from abjad.tools import pitchtools
        return pitchtools.chromatic_pitch_number_to_diatonic_pitch_class_number(
            self.chromatic_pitch_number)

    @property
    def diatonic_pitch_number(self):
        r'''Diatonic pitch-class number:

        ::

            >>> pitch.diatonic_pitch_number
            7

        Return integer.
        '''
        from abjad.tools import pitchtools
        return pitchtools.chromatic_pitch_number_to_diatonic_pitch_number(
            self.chromatic_pitch_number)

    ### PUBLIC METHODS ###

    def apply_accidental(self, accidental=None):
        r'''Apply `accidental`:

        ::

            >>> pitch.apply_accidental('flat')
            NumberedPitch(12)

        Return numbered chromatic pitch.
        '''
        from abjad.tools.pitchtools.Accidental import Accidental
        accidental = Accidental(accidental)
        semitones = abs(self) + accidental.semitones
        return type(self)(semitones)

    def transpose(self, n=0):
        r'''Tranpose by `n` semitones:

        ::

            >>> pitch.transpose(1)
            NumberedPitch(14)

        Return numbered chromatic pitch.
        '''
        semitones = abs(self) + n
        return type(self)(semitones)
