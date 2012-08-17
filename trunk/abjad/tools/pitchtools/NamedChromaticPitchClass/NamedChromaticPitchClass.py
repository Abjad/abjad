from abjad.tools.pitchtools.PitchClassObject import PitchClassObject


class NamedChromaticPitchClass(PitchClassObject):
    '''.. versionadded:: 2.0

    Abjad model of named chromatic pitch-class::

        >>> ncpc = pitchtools.NamedChromaticPitchClass('cs')

    ::

        >>> ncpc
        NamedChromaticPitchClass('cs')

    Named chromatic pitch-classes are immutable.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_chromatic_pitch_class_name', )

    ### INITIALIZER ###

    # Why is this not __new__?
    def __init__(self, arg):
        from abjad.tools import pitchtools
        if hasattr(arg, '_chromatic_pitch_class_name'):
            chromatic_pitch_class_name = arg._chromatic_pitch_class_name
        elif pitchtools.is_chromatic_pitch_name(arg):
            chromatic_pitch_class_name = pitchtools.chromatic_pitch_name_to_chromatic_pitch_class_name(arg)
        else:
            try:
                named_chromatic_pitch_carrier = pitchtools.get_named_chromatic_pitch_from_pitch_carrier(arg)
            except (ValueError, TypeError):
                raise ValueError
            if hasattr(named_chromatic_pitch_carrier, '_chromatic_pitch_name'):
                chromatic_pitch_name = named_chromatic_pitch_carrier._chromatic_pitch_name
            elif hasattr(named_chromatic_pitch_carrier, 'pitch'):
                named_chromatic_pitch = named_chromatic_pitch_carrier.pitch
                chromatic_pitch_name = named_chromatic_pitch._chromatic_pitch_name
            else:
                raise TypeError
            chromatic_pitch_class_name = \
                pitchtools.chromatic_pitch_name_to_chromatic_pitch_class_name(chromatic_pitch_name)
        chromatic_pitch_class_name = chromatic_pitch_class_name.lower()
        object.__setattr__(self, '_chromatic_pitch_class_name', chromatic_pitch_class_name)
        object.__setattr__(self, '_comparison_attribute', chromatic_pitch_class_name)

    ### SPECIAL METHODS ###

    def __abs__(self):
        return abs(self.numbered_chromatic_pitch_class)

    def __add__(self, melodic_diatonic_interval):
        from abjad.tools import pitchtools
        dummy = pitchtools.NamedChromaticPitch(self._chromatic_pitch_class_name, 4)
        mdi = melodic_diatonic_interval
        new = pitchtools.transpose_pitch_carrier_by_melodic_interval(dummy, mdi)
        return new.named_chromatic_pitch_class

    def __copy__(self, *args):
        return type(self)(self)

    __deepcopy__ = __copy__

    def __float__(self):
        return float(self.numbered_chromatic_pitch_class)

    def __int__(self):
        return int(self.numbered_chromatic_pitch_class)

    def __repr__(self):
        return '%s(%s)' % (type(self).__name__, self._repr_string)

    def __str__(self):
        return '%s' % self._chromatic_pitch_class_name

    def __sub__(self, arg):
        if not isinstance(arg, type(self)):
            raise TypeError('%s must be named pitch-class.' % arg)
        from abjad.tools import pitchtools
        pitch_1 = pitchtools.NamedChromaticPitch(self, 4)
        pitch_2 = pitchtools.NamedChromaticPitch(arg, 4)
        mdi = pitchtools.calculate_melodic_diatonic_interval(
            pitch_1, pitch_2)
        dic = pitchtools.InversionEquivalentDiatonicIntervalClass(mdi.quality_string, mdi.number)
        return dic

    ### PRIVATE PROPERTIES ###

    @property
    def _accidental(self):
        '''Read-only accidental string of pitch-class name.'''
        from abjad.tools import pitchtools
        return pitchtools.Accidental(str(self)[1:])

    @property
    def _accidental_string(self):
        return str(self)[1:]

    @property
    def _diatonic_pitch_class_name(self):
        '''Read-only first letter of pitch-class name.'''
        return str(self)[0]

    @property
    def _repr_string(self):
        return repr(str(self))

    @property
    def _symbolic_name(self):
        '''Read-only letter plus punctuation of pitch name.'''
        accidental_to_symbol = {
            '': '', 's': '#', 'f': 'b', 'ss': '###', 'ff': 'bb',
            'qs': 'qs', 'qf': 'qf', 'tqs': 'tqs', 'tqf': 'tqf'}
        symbol = accidental_to_symbol[self._accidental.alphabetic_accidental_abbreviation]
        return self._diatonic_pitch_class_name + symbol

    ### PRIVATE METHODS ###

    def _init_by_name(self, name):
        if not self._is_acceptable_name(name.lower()):
            raise ValueError("unknown pitch-class name '%s'." % name)
        object.__setattr__(self, '_chromatic_pitch_class_name', name.lower())

    def _is_acceptable_name(self, name):
        return name in (
            'c', 'cf', 'cs', 'cqf', 'cqs', 'ctqf', 'ctqs', 'cff', 'css',
            'd', 'df', 'ds', 'dqf', 'dqs', 'dtqf', 'dtqs', 'dff', 'dss',
            'e', 'ef', 'es', 'eqf', 'eqs', 'etqf', 'etqs', 'eff', 'ess',
            'f', 'ff', 'fs', 'fqf', 'fqs', 'ftqf', 'ftqs', 'fff', 'fss',
            'g', 'gf', 'gs', 'gqf', 'gqs', 'gtqf', 'gtqs', 'gff', 'gss',
            'a', 'af', 'as', 'aqf', 'aqs', 'atqf', 'atqs', 'aff', 'ass',
            'b', 'bf', 'bs', 'bqf', 'bqs', 'btqf', 'btqs', 'bff', 'bss')

    ### PUBLIC PROPERTIES ###

    @property
    def numbered_chromatic_pitch_class(self):
        '''Read-only numbered chromatic pitch-class::

            >>> ncpc.numbered_chromatic_pitch_class
            NumberedChromaticPitchClass(1)

        Return numbered chromatic pitch-class.
        '''
        from abjad.tools import pitchtools
        return pitchtools.NumberedChromaticPitchClass(self._chromatic_pitch_class_name)

    ### PUBLIC METHODS ###

    def apply_accidental(self, accidental):
        '''Apply `accidental`::

            >>> ncpc.apply_accidental('qs')
            NamedChromaticPitchClass('ctqs')

        Return named chromatic pitch-class.
        '''
        from abjad.tools import pitchtools
        accidental = pitchtools.Accidental(accidental)
        new_accidental = self._accidental + accidental
        new_name = self._diatonic_pitch_class_name + new_accidental.alphabetic_accidental_abbreviation
        return type(self)(new_name)

    def transpose(self, melodic_diatonic_interval):
        '''Transpose named chromatic pitch-class by `melodic_diatonic_interval`::

            >>> ncpc.transpose(pitchtools.MelodicDiatonicInterval('major', 2))
            NamedChromaticPitchClass('ds')

        Return named chromatic pitch-class.
        '''
        from abjad.tools import pitchtools
        pitch = pitchtools.NamedChromaticPitch(self, 4)
        transposed_pitch = pitchtools.transpose_pitch_carrier_by_melodic_interval(
            pitch, melodic_diatonic_interval)
        transposed_named_chromatic_pitch_class = transposed_pitch.named_chromatic_pitch_class
        return transposed_named_chromatic_pitch_class
