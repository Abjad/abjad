# -*- encoding: utf-8 -*-
import numbers
from abjad.tools.pitchtools.PitchClass import PitchClass


class NamedPitchClass(PitchClass):
    '''Abjad model of named pitch-class:

    ::

        >>> named_pitch_class = pitchtools.NamedPitchClass('cs')

    ::

        >>> named_pitch_class
        NamedPitchClass('cs')

    Return named pitch-class.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_chromatic_pitch_class_name',
        )

    ### INITIALIZER ###

    def __init__(self, expr):
        from abjad.tools import pitchtools
        # from named objects
        if isinstance(expr, (
            pitchtools.NamedPitch,
            pitchtools.NamedPitchClass,
            )) or pitchtools.is_chromatic_pitch_name(expr):
            pitch_class_name = \
                pitchtools.chromatic_pitch_name_to_chromatic_pitch_class_name(
                    str(expr))
        # from numbered objects
        elif isinstance(expr, (
            numbers.Number,
            pitchtools.NumberedPitch,
            pitchtools.NumberedPitchClass,
            )):
            pitch_number = \
                pitchtools.chromatic_pitch_number_to_chromatic_pitch_class_number(
                    float(expr))
            pitch_class_name = \
                pitchtools.chromatic_pitch_class_number_to_chromatic_pitch_class_name(
                    pitch_number)
        # from pitch carriers
        elif pitchtools.is_pitch_carrier(expr):
            named_pitch = pitchtools.get_named_pitch_from_pitch_carrier(
                expr)
            pitch_class_name = named_pitch.chromatic_pitch_class_name
        else:
            raise TypeError('Cannot instantiate {} from '
                '{!r}.'.format(self._class_name, expr))
        self._chromatic_pitch_class_name = pitch_class_name.lower()

    ### SPECIAL METHODS ###

    def __abs__(self):
        return abs(self.numbered_pitch_class)

    def __add__(self, melodic_diatonic_interval):
        from abjad.tools import pitchtools
        dummy = pitchtools.NamedPitch(
            self._chromatic_pitch_class_name, 4)
        mdi = melodic_diatonic_interval
        new = pitchtools.transpose_pitch_carrier_by_melodic_interval(
            dummy, mdi)
        return new.named_pitch_class

    def __copy__(self, *args):
        return type(self)(self)

    # TODO: remove?
    __deepcopy__ = __copy__

    def __eq__(self, expr):
        if isinstance(expr, type(self)):
            return self._chromatic_pitch_class_name == \
                expr._chromatic_pitch_class_name
        return self._chromatic_pitch_class_name == expr

    def __float__(self):
        return float(self.numbered_pitch_class)

    def __int__(self):
        return int(self.numbered_pitch_class)

    def __repr__(self):
        return '%s(%s)' % (self._class_name, self._repr_string)

    def __str__(self):
        return '%s' % self._chromatic_pitch_class_name

    def __sub__(self, arg):
        if not isinstance(arg, type(self)):
            raise TypeError('%s must be named pitch-class.' % arg)
        from abjad.tools import pitchtools
        pitch_1 = pitchtools.NamedPitch(self, 4)
        pitch_2 = pitchtools.NamedPitch(arg, 4)
        mdi = pitchtools.NamedInterval.from_pitch_carriers(
            pitch_1, pitch_2)
        dic = pitchtools.NamedInversionEquivalentIntervalClass(
            mdi.quality_string, mdi.number)
        return dic

    ### PRIVATE PROPERTIES ###

    @property
    def _accidental(self):
        r'''Accidental string of pitch-class name.
        '''
        from abjad.tools import pitchtools
        return pitchtools.Accidental(str(self)[1:])

    @property
    def _accidental_string(self):
        return str(self)[1:]

    @property
    def _diatonic_pitch_class_name(self):
        r'''First letter of pitch-class name.
        '''
        return str(self)[0]

    @property
    def _repr_string(self):
        return repr(str(self))

    @property
    def _symbolic_name(self):
        r'''Letter plus punctuation of pitch name.
        '''
        accidental_to_symbol = {
            '': '', 
            's': '#', 
            'f': 'b', 
            'ss': '###', 
            'ff': 'bb',
            'qs': 'qs', 
            'qf': 'qf', 
            'tqs': 'tqs', 
            'tqf': 'tqf',
            }
        symbol = accidental_to_symbol[
            self._accidental.alphabetic_accidental_abbreviation]
        return self._diatonic_pitch_class_name + symbol

    ### PRIVATE METHODS ###

    def _init_by_name(self, name):
        if not self._is_acceptable_name(name.lower()):
            raise ValueError("unknown pitch-class name '%s'." % name)
        self._chromatic_pitch_class_name = name.lower()

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
    def numbered_pitch_class(self):
        r'''Numbered chromatic pitch-class:

        ::

            >>> named_pitch_class.numbered_pitch_class
            NumberedPitchClass(1)

        Return numbered chromatic pitch-class.
        '''
        from abjad.tools import pitchtools
        return pitchtools.NumberedPitchClass(
            self._chromatic_pitch_class_name)

    ### PUBLIC METHODS ###

    def apply_accidental(self, accidental):
        r'''Apply `accidental`:

        ::

            >>> named_pitch_class.apply_accidental('qs')
            NamedPitchClass('ctqs')

        Return named chromatic pitch-class.
        '''
        from abjad.tools import pitchtools
        accidental = pitchtools.Accidental(accidental)
        new_accidental = self._accidental + accidental
        new_name = self._diatonic_pitch_class_name + \
            new_accidental.alphabetic_accidental_abbreviation
        return type(self)(new_name)

    def transpose(self, melodic_diatonic_interval):
        r'''Transpose named chromatic pitch-class by 
        `melodic_diatonic_interval`:

        ::

            >>> named_pitch_class.transpose(
            ...     pitchtools.NamedInterval('major', 2))
            NamedPitchClass('ds')

        Return named chromatic pitch-class.
        '''
        from abjad.tools import pitchtools
        pitch = pitchtools.NamedPitch(self, 4)
        transposed_pitch = \
            pitchtools.transpose_pitch_carrier_by_melodic_interval(
            pitch, melodic_diatonic_interval)
        transposed_named_pitch_class = \
            transposed_pitch.named_pitch_class
        return transposed_named_pitch_class
