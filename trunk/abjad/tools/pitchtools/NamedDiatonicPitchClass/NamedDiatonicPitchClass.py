from abjad.tools.pitchtools._DiatonicPitchClass import _DiatonicPitchClass


class NamedDiatonicPitchClass(_DiatonicPitchClass):
    '''.. versionadded:: 2.0

    Abjad model of a named diatonic pitch-class::

        abjad> pitchtools.NamedDiatonicPitchClass('c')
        NamedDiatonicPitchClass('c')

    Named diatonic pitch-classes are immutable.
    '''

    __slots__ = ('_diatonic_pitch_class_name', )

    def __new__(klass, arg):
        from abjad.tools import pitchtools
        self = object.__new__(klass)
        if hasattr(arg, '_diatonic_pitch_class_name'):
            diatonic_pitch_class_name = arg._diatonic_pitch_class_name
        elif hasattr(arg, '_diatonic_pitch_class_number'):
            tmp = pitchtools.diatonic_pitch_class_number_to_diatonic_pitch_class_name
            diaotnic_pitch_class_name = tmp(arg._diatonic_pitch_class_number)
        elif pitchtools.is_chromatic_pitch_name(arg):
            tmp = pitchtools.chromatic_pitch_name_to_diatonic_pitch_class_name
            diatonic_pitch_class_name = tmp(arg)
        elif pitchtools.is_diatonic_pitch_number(arg):
            tmp = pitchtools.diatonic_pitch_number_to_diatonic_pitch_class_name
            diatonic_pitch_class_name = tmp(arg)
        else:
            raise TypeError('\n\tCan not initialize named diatonic pitch-class from %r.' % arg)
        object.__setattr__(self, '_diatonic_pitch_class_name', diatonic_pitch_class_name)
        object.__setattr__(self, '_comparison_attribute', diatonic_pitch_class_name)
        object.__setattr__(self, '_format_string', repr(diatonic_pitch_class_name))
        return self

    ### OVERLOADS ###

    def __abs__(self):
        return abs(self.numbered_diatonic_pitch_class)

    def __float__(self):
        return float(self.numbered_diatonic_pitch_class)

    def __int__(self):
        return int(self.numbered_diatonic_pitch_class)

    def __repr__(self):
        return '%s(%r)' % (type(self).__name__, str(self))

    def __str__(self):
        return self._diatonic_pitch_class_name

    ### PUBLIC ATTRIBUTES ###

    @property
    def numbered_diatonic_pitch_class(self):
        '''Read-only numbered diatonic pitch-class from named diatonic pitch-class::

            abjad> named_diatonic_pitch_class = pitchtools.NamedDiatonicPitchClass('c')
            abjad> named_diatonic_pitch_class.numbered_diatonic_pitch_class
            NumberedDiatonicPitchClass(0)

        Return numbered diatonic pitch-class.
        '''
        from abjad.tools import pitchtools
        tmp = pitchtools.diatonic_pitch_class_name_to_diatonic_pitch_class_number
        return pitchtools.NumberedDiatonicPitchClass(tmp(self._diatonic_pitch_class_name))
