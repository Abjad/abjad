# -*- encoding: utf-8 -*-
from abjad.tools.pitchtools.Pitch import Pitch


class NumberedDiatonicPitch(Pitch):
    '''Abjad model of a numbered diatonic pitch:

    ::

        >>> pitch = pitchtools.NumberedDiatonicPitch(7)
        >>> pitch
        NumberedDiatonicPitch(7)

    Numbered diatonic pitches are immutable.
    '''

    ### CLASS VARIABLES ##

    __slots__ = (
        '_diatonic_pitch_number', 
        '_number',
        )

    ### INITIALIZER ###

    def __init__(self, arg):
        from abjad.tools import mathtools
        from abjad.tools import pitchtools
        if hasattr(arg, '_diatonic_pitch_number'):
            diatonic_pitch_number = arg._diatonic_pitch_number
        elif mathtools.is_integer_equivalent_number(arg):
            diatonic_pitch_number = arg
        elif pitchtools.is_diatonic_pitch_name(arg):
            diatonic_pitch_number = \
                pitchtools.diatonic_pitch_name_to_diatonic_pitch_number(arg)
        elif pitchtools.is_chromatic_pitch_name(arg):
            diatonic_pitch_number = \
                pitchtools.chromatic_pitch_name_to_diatonic_pitch_number(arg)
        else:
            raise TypeError
        object.__setattr__(
            self, '_diatonic_pitch_number', diatonic_pitch_number)
        object.__setattr__(self, '_number', diatonic_pitch_number)
        object.__setattr__(
            self, '_comparison_attribute', diatonic_pitch_number)
        object.__setattr__(self, '_format_string', diatonic_pitch_number)

    ### SPECIAL METHODS ###

    def __abs__(self):
        return self._diatonic_pitch_number

    def __float__(self):
        return float(self._number)

    def __int__(self):
        return self._number

    def __repr__(self):
        return '%s(%s)' % (self._class_name, str(self))

    def __str__(self):
        return str(self._diatonic_pitch_number)

    ### PUBLIC PROPERTIES ###

    @property
    def chromatic_pitch_number(self):
        r'''Chromatic pitch number:

        ::

            >>> pitch.chromatic_pitch_number
            12

        Return integer.
        '''
        from abjad.tools import pitchtools
        return pitchtools.diatonic_pitch_number_to_chromatic_pitch_number(
            self.diatonic_pitch_number)

    @property
    def diatonic_pitch_number(self):
        r'''Diatonic pitch number:

        ::

            >>> pitch.diatonic_pitch_number
            7

        Return integer.
        '''
        return self._diatonic_pitch_number

    @property
    def named_diatonic_pitch(self):
        r'''Named diatonic pitch:

        ::

            >>> pitch.named_diatonic_pitch
            NamedDiatonicPitch("c''")

        Return named diatonic pitch.
        '''
        from abjad.tools import pitchtools
        tmp = pitchtools.diatonic_pitch_number_to_diatonic_pitch_name
        diatonic_pitch_name = tmp(self._diatonic_pitch_number)
        return pitchtools.NamedDiatonicPitch(diatonic_pitch_name)

    @property
    def named_diatonic_pitch_class(self):
        r'''Named diatonic pitch-class:

        ::

            >>> pitch.named_diatonic_pitch_class
            NamedDiatonicPitchClass('c')

        Return named diatonic pitch-class.
        '''
        from abjad.tools import pitchtools
        tmp = pitchtools.diatonic_pitch_number_to_diatonic_pitch_class_name
        diatonic_pitch_class_name = tmp(self._diatonic_pitch_number)
        return pitchtools.NamedDiatonicPitchClass(diatonic_pitch_class_name)

    @property
    def numbered_diatonic_pitch_class(self):
        r'''Numbered diatonic pitch-class:

        ::

            >>> pitch.numbered_diatonic_pitch_class
            NumberedDiatonicPitchClass(0)

        Return numbered diatonic pitch-class.
        '''
        from abjad.tools import pitchtools
        tmp = pitchtools.diatonic_pitch_number_to_diatonic_pitch_class_number
        diatonic_pitch_class_number = tmp(self._diatonic_pitch_number)
        return pitchtools.NumberedDiatonicPitchClass(
            diatonic_pitch_class_number)
