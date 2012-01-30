from abjad.tools.pitchtools._DiatonicPitch import _DiatonicPitch


class NamedDiatonicPitch(_DiatonicPitch):
    '''.. versionadded:: 2.0

    Abjad model of a named diatonic pitch::

        abjad> named_diatonic_pitch = pitchtools.NamedDiatonicPitch("c''")

    ::

        abjad> named_diatonic_pitch
        NamedDiatonicPitch("c''")

    ::

        abjad> print named_diatonic_pitch
        c''

    Named diatonic pitches are immutable.
    '''

    __slots__ = ('_diatonic_pitch_name', )

    def __new__(klass, arg):
        from abjad.tools import pitchtools
        self = object.__new__(klass)
        if hasattr(arg, '_diatonic_pitch_name'):
            diatonic_pitch_name = arg._diatonic_pitch_name
        elif hasattr(arg, '_diatonic_pitch_number'):
            tmp = pitchtools.diatonic_pitch_number_to_diatonic_pitch_name
            diatonic_pitch_name = tmp(arg._diatonic_pitch_number)
        elif pitchtools.is_diatonic_pitch_name(arg):
            diatonic_pitch_name = arg
        elif pitchtools.is_diatonic_pitch_number(arg):
            diatonic_pitch_name = pitchtools.diatonic_pitch_number_to_diatonic_pitch_name(arg)
        else:
            raise TypeError('\n\tCan not initialize named diatonic pitch: "%s".' % arg)
        tmp = pitchtools.diatonic_pitch_name_to_diatonic_pitch_number
        diatonic_pitch_number = tmp(diatonic_pitch_name)
        object.__setattr__(self, '_diatonic_pitch_name', diatonic_pitch_name)
        object.__setattr__(self, '_comparison_attribute', diatonic_pitch_number)
        object.__setattr__(self, '_format_string', repr(diatonic_pitch_name))
        return self

    ### OVERLOADS ###

    def __abs__(self):
        return abs(self.numbered_diatonic_pitch)

    def __float__(self):
        return float(self.numbered_diatonic_pitch)

    def __int__(self):
        return int(self.numbered_diatonic_pitch)

    def __repr__(self):
        return '%s(%r)' % (type(self).__name__, str(self))

    def __str__(self):
        return self._diatonic_pitch_name

    ### PUBLIC ATTRIBUTES ###

    @property
    def chromatic_pitch_class_name(self):
        '''Read-only chromatic pitch-class name::

            abjad> pitchtools.NamedDiatonicPitch("c''").chromatic_pitch_class_name
            'c'

        Return string.
        '''
        from abjad.tools import pitchtools
        return pitchtools.diatonic_pitch_name_to_chromatic_pitch_class_name(self.diatonic_pitch_name)

    @property
    def chromatic_pitch_class_number(self):
        '''Read-only chromatic pitch-class number::

            abjad> pitchtools.NamedDiatonicPitch("c''").chromatic_pitch_class_number
            0

        Return integer.
        '''
        from abjad.tools import pitchtools
        return pitchtools.diatonic_pitch_name_to_chromatic_pitch_class_number(
            self.diatonic_pitch_name)

    @property
    def chromatic_pitch_name(self):
        '''Read-only chromatic pitch name::

            abjad> pitchtools.NamedDiatonicPitch("c''").chromatic_pitch_name
            "c''"

        Return string.
        '''
        from abjad.tools import pitchtools
        return pitchtools.diatonic_pitch_name_to_chromatic_pitch_name(self.diatonic_pitch_name)

    @property
    def chromatic_pitch_number(self):
        '''Read-only chromatic pitch number::

            abjad> pitchtools.NamedDiatonicPitch("c''").chromatic_pitch_number
            12

        Return integer.
        '''
        from abjad.tools import pitchtools
        return pitchtools.diatonic_pitch_name_to_chromatic_pitch_number(self.diatonic_pitch_name)

    @property
    def diatonic_pitch_class_name(self):
        '''Read-only diatonic pitch-class name::

            abjad> pitchtools.NamedDiatonicPitch("c''").diatonic_pitch_class_name
            'c'

        Return string.
        '''
        from abjad.tools import pitchtools
        return pitchtools.diatonic_pitch_name_to_diatonic_pitch_class_name(self.diatonic_pitch_name)

    @property
    def diatonic_pitch_class_number(self):
        '''Read-only diatonic pitch-class number::

            abjad> pitchtools.NamedDiatonicPitch("c''").diatonic_pitch_class_number
            0

        Return integer.
        '''
        from abjad.tools import pitchtools
        return pitchtools.diatonic_pitch_name_to_diatonic_pitch_class_number(self.diatonic_pitch_name)

    @property
    def diatonic_pitch_name(self):
        '''Read-only diatonic pitch name::

            abjad> pitchtools.NamedDiatonicPitch("c''").diatonic_pitch_name
            "c''"

        Return string.
        '''
        return self._diatonic_pitch_name

    @property
    def diatonic_pitch_number(self):
        '''Read-only diatonic pitch number::

            abjad> pitchtools.NamedDiatonicPitch("c''").diatonic_pitch_number
            7

        Return integer.
        '''
        from abjad.tools import pitchtools
        return pitchtools.diatonic_pitch_name_to_diatonic_pitch_number(self.diatonic_pitch_name)

    @property
    def format(self):
        '''Read-only LilyPond input format of named diatonic pitch::

            abjad> pitchtools.NamedDiatonicPitch("c''").format
            "c''"

        Return string.
        '''
        return self._diatonic_pitch_name

    @property
    def named_chromatic_pitch(self):
        '''Read-only named chromatic pitch::

            abjad> pitchtools.NamedDiatonicPitch("c''").named_chromatic_pitch
            NamedChromaticPitch("c''")

        Return named chromatic pitch.
        '''
        from abjad.tools import pitchtools
        return pitchtools.NamedChromaticPitch(self.chromatic_pitch_name)

    @property
    def named_chromatic_pitch_class(self):
        '''Read-only named chromatic pitch-class::

            abjad> pitchtools.NamedDiatonicPitch("c''").named_chromatic_pitch_class
            NamedChromaticPitchClass('c')

        Return named chromatic pitch-class.
        '''
        from abjad.tools import pitchtools
        return pitchtools.NamedChromaticPitchClass(self.chromatic_pitch_class_name)

    @property
    def named_diatonic_pitch_class(self):
        '''Read-only named diatonic pitch-class::

            abjad> pitchtools.NamedDiatonicPitch("c''").named_diatonic_pitch_class
            NamedDiatonicPitchClass('c')

        Return named diatonic pitch-class.
        '''
        from abjad.tools import pitchtools
        tmp = pitchtools.diatonic_pitch_name_to_diatonic_pitch_class_name
        return pitchtools.NamedDiatonicPitchClass(tmp(self._diatonic_pitch_name))

    @property
    def numbered_chromatic_pitch(self):
        '''Read-only numbered chromatic pitch::

            abjad> pitchtools.NamedDiatonicPitch("c''").numbered_chromatic_pitch
            NumberedChromaticPitch(12)

        Return numbered chromatic pitch.
        '''
        from abjad.tools import pitchtools
        return pitchtools.NumberedChromaticPitch(self.chromatic_pitch_number)

    @property
    def numbered_chromatic_pitch_class(self):
        '''Read-only numbered chromatic pitch-class::

            abjad> pitchtools.NamedDiatonicPitch("c''").numbered_chromatic_pitch_class
            NumberedChromaticPitchClass(0)

        Return numbered chromatic pitch-class.
        '''
        from abjad.tools import pitchtools
        return pitchtools.NumberedChromaticPitchClass(self.chromatic_pitch_class_number)

    @property
    def numbered_diatonic_pitch(self):
        '''Read-only numbered diatonic pitch::

            abjad> pitchtools.NamedDiatonicPitch("c''").numbered_diatonic_pitch
            NumberedDiatonicPitch(7)

        Return numbered diatonic pitch.
        '''
        from abjad.tools import pitchtools
        tmp = pitchtools.diatonic_pitch_name_to_diatonic_pitch_number
        return pitchtools.NumberedDiatonicPitch(tmp(self._diatonic_pitch_name))

    @property
    def numbered_diatonic_pitch_class(self):
        '''Read-only numbered diatonic pitch-class::

            abjad> pitchtools.NamedDiatonicPitch("c''").numbered_diatonic_pitch_class
            NumberedDiatonicPitchClass(0)

        Return numbered diatonic pitch-class.
        '''
        from abjad.tools import pitchtools
        tmp = pitchtools.diatonic_pitch_name_to_diatonic_pitch_class_number
        return pitchtools.NumberedDiatonicPitchClass(tmp(self._diatonic_pitch_name))
