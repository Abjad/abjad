from abjad.tools.pitchtools._DiatonicPitch import _DiatonicPitch
from abjad.tools.pitchtools._NumberedPitch import _NumberedPitch


class NumberedDiatonicPitch(_DiatonicPitch, _NumberedPitch):
    '''.. versionadded:: 2.0

    Abjad model of a numbered diatonic pitch::

        abjad> pitchtools.NumberedDiatonicPitch(7)
        NumberedDiatonicPitch(7)

    Numbered diatonic pitches are immutable.
    '''

    __slots__ = ('_diatonic_pitch_number', '_number')

    def __new__(klass, arg):
        from abjad.tools import mathtools
        from abjad.tools import pitchtools
        self = object.__new__(klass)
        if hasattr(arg, '_diatonic_pitch_number'):
            diatonic_pitch_number = arg._diatonic_pitch_number
        elif mathtools.is_integer_equivalent_number(arg):
            diatonic_pitch_number = arg
        elif pitchtools.is_diatonic_pitch_name(arg):
            diatonic_pitch_number = pitchtools.diatonic_pitch_name_to_diatonic_pitch_number(arg)
        elif pitchtools.is_chromatic_pitch_name(arg):
            diatonic_pitch_number = pitchtools.chromatic_pitch_name_to_diatonic_pitch_number(arg)
        else:
            raise TypeError
        object.__setattr__(self, '_diatonic_pitch_number', diatonic_pitch_number)
        object.__setattr__(self, '_number', diatonic_pitch_number)
        object.__setattr__(self, '_comparison_attribute', diatonic_pitch_number)
        object.__setattr__(self, '_format_string', diatonic_pitch_number)
        return self

    ### OVERLOADS ###

    def __abs__(self):
        return self._diatonic_pitch_number

    def __repr__(self):
        return '%s(%s)' % (type(self).__name__, str(self))

    def __str__(self):
        return str(self._diatonic_pitch_number)

    ### PUBLIC ATTRIBUTES ###

    @property
    def chromatic_pitch_number(self):
        '''Read-only chromatic pitch number::

            abjad> pitchtools.NumberedDiatonicPitch(7).chromatic_pitch_number
            12

        Return integer.
        '''
        from abjad.tools import pitchtools
        return pitchtools.diatonic_pitch_number_to_chromatic_pitch_number(self.diatonic_pitch_number)

    @property
    def diatonic_pitch_number(self):
        '''Read-only diatonic pitch number::

            abjad> pitchtools.NumberedDiatonicPitch(7).diatonic_pitch_number
            7

        Return integer.
        '''
        return self._diatonic_pitch_number

    @property
    def named_diatonic_pitch(self):
        '''Read-only named diatonic pitch::

            abjad> pitchtools.NumberedDiatonicPitch(7).named_diatonic_pitch
            NamedDiatonicPitch("c''")

        Return named diatonic pitch.
        '''
        from abjad.tools import pitchtools
        tmp = pitchtools.diatonic_pitch_number_to_diatonic_pitch_name
        diatonic_pitch_name = tmp(self._diatonic_pitch_number)
        return pitchtools.NamedDiatonicPitch(diatonic_pitch_name)

    @property
    def named_diatonic_pitch_class(self):
        '''Read-only named diatonic pitch-class::

            abjad> pitchtools.NumberedDiatonicPitch(7).named_diatonic_pitch_class
            NamedDiatonicPitchClass('c')

        Return named diatonic pitch-class.
        '''
        from abjad.tools import pitchtools
        tmp = pitchtools.diatonic_pitch_number_to_diatonic_pitch_class_name
        diatonic_pitch_class_name = tmp(self._diatonic_pitch_number)
        return pitchtools.NamedDiatonicPitchClass(diatonic_pitch_class_name)

    @property
    def numbered_diatonic_pitch_class(self):
        '''Read-only numbered diatonic pitch-class::

            abjad> pitchtools.NumberedDiatonicPitch(7).numbered_diatonic_pitch_class
            NumberedDiatonicPitchClass(0)

        Return numbered diatonic pitch-class.
        '''
        from abjad.tools import pitchtools
        tmp = pitchtools.diatonic_pitch_number_to_diatonic_pitch_class_number
        diatonic_pitch_class_number = tmp(self._diatonic_pitch_number)
        return pitchtools.NumberedDiatonicPitchClass(diatonic_pitch_class_number)
