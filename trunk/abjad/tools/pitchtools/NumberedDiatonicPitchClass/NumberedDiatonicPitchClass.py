from abjad.tools.pitchtools.DiatonicPitchClassObject import DiatonicPitchClassObject
from abjad.tools.pitchtools.NumberedPitchClassObject import NumberedPitchClassObject


class NumberedDiatonicPitchClass(NumberedPitchClassObject, DiatonicPitchClassObject):
    '''.. versionadded:: 2.0

    Abjad model of a numbered diatonic pitch-class::

        >>> pitchtools.NumberedDiatonicPitchClass(0)
        NumberedDiatonicPitchClass(0)

    Numbered diatonic pitch-classes are immutable.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_comparison_attribute', '_diatonic_pitch_class_number', '_format_string',
        '_number')
    
    _default_mandatory_input_arguments = (0, )

    ### INITIALIZER ###

    def __init__(self, arg):
        from abjad.tools import mathtools
        from abjad.tools import pitchtools
        if hasattr(arg, '_diatonic_pitch_class_number'):
            diatonic_pitch_class_number = arg._diatonic_pitch_class_number
        elif pitchtools.is_chromatic_pitch_name(arg):
            tmp = pitchtools.chromatic_pitch_name_to_diatonic_pitch_class_number
            diatonic_pitch_class_number = tmp(arg)
        elif mathtools.is_integer_equivalent_number(arg):
            diatonic_pitch_class_number = int(arg) % 7
        else:
            raise TypeError
        object.__setattr__(self, '_diatonic_pitch_class_number', diatonic_pitch_class_number)
        object.__setattr__(self, '_number', diatonic_pitch_class_number)
        object.__setattr__(self, '_comparison_attribute', diatonic_pitch_class_number)
        object.__setattr__(self, '_format_string', diatonic_pitch_class_number)

    ### SPECIAL METHODS ###

    def __repr__(self):
        return '%s(%s)' % (type(self).__name__, str(self))

    def __str__(self):
        return str(self._diatonic_pitch_class_number)

    @property
    def named_diatonic_pitch_class(self):
        '''Read-only named diatonic pitch-class from numbered diatonic pitch-class::

            >>> numbered_diatonic_pitch_class = pitchtools.NumberedDiatonicPitchClass(0)
            >>> numbered_diatonic_pitch_class.named_diatonic_pitch_class
            NamedDiatonicPitchClass('c')

        Return named diatonic pitch-class.
        '''
        from abjad.tools import pitchtools
        return pitchtools.NamedDiatonicPitchClass(int(self))
