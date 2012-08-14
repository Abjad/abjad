from abjad.tools.pitchtools.Accidental import Accidental
from abjad.tools.pitchtools.PitchObject import PitchObject
from abjad.tools.pitchtools.is_chromatic_pitch_name import chromatic_pitch_name_regex


class NamedChromaticPitch(PitchObject):
    '''.. versionadded:: 1.1

    Abjad model of named chromatic pitch::

        >>> pitchtools.NamedChromaticPitch("cs''")
        NamedChromaticPitch("cs''")

    Named chromatic pitches are immutable.
    '''

    ### CLASS ATTRIBUTES ###


    # calculate accidental_semitones, diatonic_pitch_number at init
    # so notehead sorting doesn't take forever later on
    __slots__ = (
        '_accidental_semitones', 
        '_chromatic_pitch_name', 
        '_deviation_in_cents', 
        '_diatonic_pitch_number',
        )

    ### INITIALIZER ###

    def __init__(self, *args, **kwargs):
        from abjad.tools import pitchtools
        _deviation_in_cents = kwargs.get('deviation_in_cents', None)
        object.__setattr__(self, '_deviation_in_cents', _deviation_in_cents)
        if len(args) == 1 and isinstance(args[0], (int, long, float)):
            self._init_by_chromatic_pitch_number(*args)
        elif len(args) == 1 and isinstance(args[0], type(self)):
            self._init_by_named_chromatic_pitch(*args)
        elif len(args) == 1 and hasattr(args[0], 'named_chromatic_pitch'):
            self._init_by_named_chromatic_pitch(args[0].named_chromatic_pitch)
        elif len(args) == 1 and pitchtools.is_chromatic_pitch_class_name_octave_number_pair(args[0]):
            self._init_by_chromatic_pitch_class_name_octave_number_pair(*args)
        elif len(args) == 1 and pitchtools.is_pitch_class_octave_number_string(args[0]):
            self._init_by_pitch_class_octave_number_string(*args)
        elif len(args) == 1 and isinstance(args[0], str):
            self._init_by_chromatic_pitch_name(*args)
        elif len(args) == 2 and isinstance(args[0], str):
            self._init_by_chromatic_pitch_class_name_and_octave_number(*args)
        elif len(args) == 2 and isinstance(args[0], pitchtools.NamedChromaticPitchClass):
            self._init_by_named_chromatic_pitch_class_and_octave_number(*args)
        elif len(args) == 2 and isinstance(args[0], (int, long, float)):
            if isinstance(args[1], str):
                self._init_by_chromatic_pitch_number_and_diatonic_pitch_class_name(*args)
            elif isinstance(args[1], pitchtools.NamedChromaticPitchClass):
                self._init_by_chromatic_pitch_number_and_named_chromatic_pitch_class(*args)
            else:
                raise TypeError
        elif len(args) == 3:
            self._init_by_chromatic_pitch_class_name_octave_number_and_deviation(*args)
        else:
            raise ValueError('\n\tNot a valid pitch token: "%s".' % str(args))
        assert hasattr(self, '_deviation_in_cents')
        assert hasattr(self, '_chromatic_pitch_name')
        diatonic_pitch_number = pitchtools.chromatic_pitch_name_to_diatonic_pitch_number(
            self._chromatic_pitch_name)
        object.__setattr__(self, '_diatonic_pitch_number', diatonic_pitch_number)
        groups = chromatic_pitch_name_regex.match(self._chromatic_pitch_name).groups()
        alphabetic_accidental_abbreviation = groups[1]
        accidental_semitones = Accidental._alphabetic_accidental_abbreviation_to_semitones[
            alphabetic_accidental_abbreviation]
        object.__setattr__(self, '_accidental_semitones', accidental_semitones)

    ### SPECIAL METHODS ###

    def __abs__(self):
        return abs(self.numbered_chromatic_pitch)

    def __add__(self, melodic_interval):
        '''.. versionadded:: 2.0'''
        from abjad.tools import pitchtools
        return pitchtools.transpose_pitch_carrier_by_melodic_interval(self, melodic_interval)

    def __copy__(self, *args):
        '''.. versionadded:: 2.0'''
        return type(self)(self)

    __deepcopy__ = __copy__

    def __eq__(self, arg):
        try:
            arg = type(self)(arg)
            if self._chromatic_pitch_name == arg._chromatic_pitch_name:
                if self.deviation_in_cents == arg.deviation_in_cents:
                    return True
            return False
        except (TypeError, ValueError):
            return False

    def __float__(self):
        return float(self.numbered_chromatic_pitch)

    def __ge__(self, arg):
        from abjad.tools import pitchtools
        try:
            arg = type(self)(arg)
            return self._diatonic_pitch_number > arg._diatonic_pitch_number or \
                (self._diatonic_pitch_number == arg._diatonic_pitch_number and
                self._accidental_semitones >= arg._accidental_semitones) or \
                (self._diatonic_pitch_number == arg._diatonic_pitch_number and
                self._accidental_semitones == arg._accidental_semitones and
                self._deviation_in_cents >= arg._deviation_in_cents)
        except (TypeError, ValueError):
            if isinstance(arg, pitchtools.PitchRange):
                return self >= arg.stop_pitch
        return False

    def __getnewargs__(self):
        return (self._chromatic_pitch_name, self._deviation_in_cents)

    def __gt__(self, arg):
        from abjad.tools import pitchtools
        if isinstance(arg, type(self)):
            return self._diatonic_pitch_number > arg._diatonic_pitch_number or \
                (self._diatonic_pitch_number == arg._diatonic_pitch_number and \
                self._accidental_semitones > arg._accidental_semitones) or \
                (self._diatonic_pitch_number == arg._diatonic_pitch_number and \
                self._accidental_semitones == arg._accidental_semitones and \
                self._deviation_in_cents > arg._deviation_in_cents)
        elif isinstance(arg, pitchtools.PitchRange):
            return self > arg.stop_pitch
        return False

    def __hash__(self):
        return hash(repr(self))

    def __int__(self):
        return int(self.numbered_chromatic_pitch)

    def __le__(self, arg):
        from abjad.tools import pitchtools
        if isinstance(arg, type(self)):
            if not self._diatonic_pitch_number == arg._diatonic_pitch_number:
                return self._diatonic_pitch_number <= arg._diatonic_pitch_number
            if not self._accidental_semitones == arg._accidental_semitones:
                return self._accidental_semitones <= arg._accidental_semitones
            return self._deviation_in_cents <= arg._deviation_in_cents
        elif isinstance(arg, pitchtools.PitchRange):
            return self <= arg.start_pitch
        return False

    def __lt__(self, arg):
        from abjad.tools import pitchtools
        if isinstance(arg, type(self)):
            return self._diatonic_pitch_number < arg._diatonic_pitch_number or \
                (self._diatonic_pitch_number == arg._diatonic_pitch_number and \
                self._accidental_semitones < arg._accidental_semitones) or \
                (self._diatonic_pitch_number == arg._diatonic_pitch_number and \
                self._accidental_semitones == arg._accidental_semitones and \
                self._deviation_in_cents < arg._deviation_in_cents)
        elif isinstance(arg, pitchtools.PitchRange):
            return self < arg.start_pitch
        return False

    def __ne__(self, arg):
        return not self == arg

    def __repr__(self):
        if self.chromatic_pitch_class_name and not self.octave_number is None:
            if self.deviation_in_cents is None:
                return '%s(%r)' % (type(self).__name__, str(self))
            else:
                return '%s(%r, deviation=%s)' % (type(self).__name__,
                    str(self), self.deviation_in_cents)
        else:
            return '%s()' % type(self).__name__

    def __str__(self):
        if self.chromatic_pitch_class_name and not self.octave_number is None:
            return '%s%s' % (self.chromatic_pitch_class_name, self._octave_tick_string)
        else:
            return ''

    def __sub__(self, arg):
        from abjad.tools import pitchtools
        if isinstance(arg, type(self)):
            return pitchtools.calculate_melodic_diatonic_interval(
                self, arg)
        else:
            interval = arg
            return pitchtools.transpose_pitch_carrier_by_melodic_interval(self, -interval)

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _accidental(self):
        from abjad.tools.pitchtools.Accidental import Accidental
        from abjad.tools.pitchtools.is_chromatic_pitch_name import chromatic_pitch_name_regex
        groups = chromatic_pitch_name_regex.match(self._chromatic_pitch_name).groups()
        alphabetic_accidental_abbreviation = groups[1]
        return Accidental(alphabetic_accidental_abbreviation)

    @property
    def _keyword_argument_names(self):
        return (
            'deviation_in_cents',
            )

    @property
    def _mandatory_argument_values(self):
        return (
            self.chromatic_pitch_name,
            )

    @property
    def _octave_tick_string(self):
        if self.octave_number is not None:
            if self.octave_number <= 2:
                return ',' * (3 - self.octave_number)
            elif self.octave_number == 3:
                return ''
            else:
                return "'" * (self.octave_number - 3)
        else:
            return None

    ### PRIVATE METHODS ###

    def _init_by_chromatic_pitch_class_name_and_octave_number(
        self, chromatic_pitch_class_name, octave_number):
        from abjad.tools import pitchtools
        octave_tick_string = pitchtools.octave_number_to_octave_tick_string(octave_number)
        chromatic_pitch_name = chromatic_pitch_class_name + octave_tick_string
        object.__setattr__(self, '_chromatic_pitch_name', chromatic_pitch_name)

    def _init_by_chromatic_pitch_class_name_octave_number_and_deviation(
        self, name, octave, deviation):
        self._init_by_chromatic_pitch_class_name_and_octave_number(name, octave)
        object.__setattr__(self, '_deviation_in_cents', deviation)

    def _init_by_chromatic_pitch_class_name_octave_number_pair(self, pair):
        from abjad.tools import pitchtools
        chromatic_pitch_class_name, octave_number = pair
        octave_tick_string = pitchtools.octave_number_to_octave_tick_string(octave_number)
        chromatic_pitch_name = chromatic_pitch_class_name + octave_tick_string
        object.__setattr__(self, '_chromatic_pitch_name', chromatic_pitch_name)

    def _init_by_chromatic_pitch_name(self, pitch_string):
        from abjad.tools import pitchtools
        name = pitchtools.chromatic_pitch_name_to_chromatic_pitch_class_name(pitch_string)
        octave_number = pitchtools.chromatic_pitch_name_to_octave_number(pitch_string)
        self._init_by_chromatic_pitch_class_name_and_octave_number(name, octave_number)

    def _init_by_chromatic_pitch_number(self, chromatic_pitch_number):
        from abjad.tools import pitchtools
        accidental_spelling = self.accidental_spelling
        chromatic_pitch_name = pitchtools.chromatic_pitch_number_to_chromatic_pitch_name(
            chromatic_pitch_number, accidental_spelling)
        object.__setattr__(self, '_chromatic_pitch_name', chromatic_pitch_name)

    def _init_by_chromatic_pitch_number_and_diatonic_pitch_class_name(
        self, chromatic_pitch_number, diatonic_pitch_class_name):
        from abjad.tools import pitchtools
        accidental, octave_number = \
            pitchtools.spell_chromatic_pitch_number(chromatic_pitch_number, diatonic_pitch_class_name)
        octave_tick_string = pitchtools.octave_number_to_octave_tick_string(octave_number)
        chromatic_pitch_class_name = diatonic_pitch_class_name + accidental.alphabetic_accidental_abbreviation
        chromatic_pitch_name = chromatic_pitch_class_name + octave_tick_string
        object.__setattr__(self, '_chromatic_pitch_name', chromatic_pitch_name)

    def _init_by_chromatic_pitch_number_and_named_chromatic_pitch_class(self, pitch_number, npc):
        diatonic_pitch_class_name = npc.name[:1]
        self._init_by_chromatic_pitch_number_and_diatonic_pitch_class_name(
            pitch_number, diatonic_pitch_class_name)

    def _init_by_named_chromatic_pitch(self, named_chromatic_pitch):
        object.__setattr__(self, '_chromatic_pitch_name', named_chromatic_pitch._chromatic_pitch_name)
        object.__setattr__(self, '_deviation_in_cents', named_chromatic_pitch.deviation_in_cents)

    def _init_by_named_chromatic_pitch_class_and_octave_number(self, npc, octave_number):
        self._init_by_chromatic_pitch_class_name_and_octave_number(npc._chromatic_pitch_class_name, octave_number)

    def _init_by_pitch_class_octave_number_string(self, pitch_class_octave_number_string):
        from abjad.tools import pitchtools
        chromatic_pitch_name = pitchtools.pitch_class_octave_number_string_to_chromatic_pitch_name(
            pitch_class_octave_number_string)
        object.__setattr__(self, '_chromatic_pitch_name', chromatic_pitch_name)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def accidental_spelling(self):
        '''Read-only accidental spelling::

            >>> pitchtools.NamedChromaticPitch("c").accidental_spelling
            'mixed'

        Return string.
        '''
        from abjad import ABJCFG
        return ABJCFG['accidental_spelling']

    @property
    def chromatic_pitch_class_name(self):
        '''Read-only chromatic pitch-class name::

            >>> named_chromatic_pitch = pitchtools.NamedChromaticPitch("cs''")
            >>> named_chromatic_pitch.chromatic_pitch_class_name
            'cs'

        Return string.
        '''
        return self.named_chromatic_pitch_class._chromatic_pitch_class_name

    @property
    def chromatic_pitch_class_number(self):
        '''Read-only chromatic pitch-class number::

            >>> named_chromatic_pitch = pitchtools.NamedChromaticPitch("cs''")
            >>> named_chromatic_pitch.chromatic_pitch_class_number
            1

        Return integer or float.
        '''
        return self.numbered_chromatic_pitch_class._chromatic_pitch_class_number

    @property
    def chromatic_pitch_name(self):
        '''Read-only chromatic pitch name::

            >>> named_chromatic_pitch = pitchtools.NamedChromaticPitch("cs''")
            >>> named_chromatic_pitch.chromatic_pitch_name
            "cs''"

        Return string.
        '''
        return self._chromatic_pitch_name

    @property
    def chromatic_pitch_number(self):
        '''Read-only chromatic pitch-class number::

            >>> named_chromatic_pitch = pitchtools.NamedChromaticPitch("cs''")
            >>> named_chromatic_pitch.chromatic_pitch_number
            13

        Return integer or float.
        '''
        return self.numbered_chromatic_pitch._chromatic_pitch_number

    @property
    def deviation_in_cents(self):
        '''Read-only deviation of named chromatic pitch in cents::

            >>> named_chromatic_pitch = pitchtools.NamedChromaticPitch("cs''")
            >>> named_chromatic_pitch.deviation_in_cents is None
            True

        Return integer or none.
        '''
        return self._deviation_in_cents

    @property
    def diatonic_pitch_class_name(self):
        '''Read-only diatonic pitch-class name::

            >>> named_diatonic_pitch = pitchtools.NamedChromaticPitch("cs''")
            >>> named_diatonic_pitch.diatonic_pitch_class_name
            'c'

        Return string.
        '''
        return self.named_diatonic_pitch_class._diatonic_pitch_class_name

    @property
    def diatonic_pitch_class_number(self):
        '''Read-only diatonic pitch-class number::

            >>> named_diatonic_pitch = pitchtools.NamedChromaticPitch("cs''")
            >>> named_diatonic_pitch.diatonic_pitch_class_number
            0

        Return integer.
        '''
        return self.numbered_diatonic_pitch_class._diatonic_pitch_class_number

    @property
    def diatonic_pitch_name(self):
        '''Read-only diatonic pitch name::

            >>> named_diatonic_pitch = pitchtools.NamedChromaticPitch("cs''")
            >>> named_diatonic_pitch.diatonic_pitch_name
            "c''"

        Return string.
        '''
        return self.named_diatonic_pitch._diatonic_pitch_name

    @property
    def diatonic_pitch_number(self):
        '''Read-only diatonic pitch number::

            >>> named_diatonic_pitch = pitchtools.NamedChromaticPitch("cs''")
            >>> named_diatonic_pitch.diatonic_pitch_number
            7

        Return integer.
        '''
        return self.numbered_diatonic_pitch._diatonic_pitch_number

    @property
    def lilypond_format(self):
        '''Read-only LilyPond input format of named chromatic pitch::

            >>> named_chromatic_pitch = pitchtools.NamedChromaticPitch("cs''")
            >>> named_chromatic_pitch.lilypond_format
            "cs''"

        Return string.
        '''
        return str(self)

    @property
    def named_chromatic_pitch_class(self):
        '''Read-only named pitch-class::

            >>> named_chromatic_pitch = pitchtools.NamedChromaticPitch("cs''")
            >>> named_chromatic_pitch.named_chromatic_pitch_class
            NamedChromaticPitchClass('cs')

        Return named chromatic pitch-class.
        '''
        from abjad.tools.pitchtools import NamedChromaticPitchClass
        return NamedChromaticPitchClass(self._chromatic_pitch_name)

    @property
    def named_diatonic_pitch(self):
        '''Read-only named diatonic pitch::

            >>> named_chromatic_pitch = pitchtools.NamedChromaticPitch("cs''")
            >>> named_chromatic_pitch.named_diatonic_pitch
            NamedDiatonicPitch("c''")

        Return named diatonic pitch.
        '''
        from abjad.tools import pitchtools
        tmp = pitchtools.chromatic_pitch_name_to_diatonic_pitch_name
        diatonic_pitch_name = tmp(self._chromatic_pitch_name)
        return pitchtools.NamedDiatonicPitch(diatonic_pitch_name)

    @property
    def named_diatonic_pitch_class(self):
        '''Read-only named diatonic pitch-class::

            >>> named_chromatic_pitch = pitchtools.NamedChromaticPitch("cs''")
            >>> named_chromatic_pitch.named_diatonic_pitch_class
            NamedDiatonicPitchClass('c')

        Return named diatonic pitch-class.
        '''
        from abjad.tools.pitchtools import NamedDiatonicPitchClass
        return NamedDiatonicPitchClass(self._chromatic_pitch_name)

    @property
    def numbered_chromatic_pitch(self):
        '''Read-only numbered chromatic pitch from named chromatic pitch::

            >>> named_chromatic_pitch = pitchtools.NamedChromaticPitch("cs''")
            >>> named_chromatic_pitch.numbered_chromatic_pitch_class
            NumberedChromaticPitchClass(1)

        Return numbered chromatic pitch-class.
        '''
        from abjad.tools import pitchtools
        return pitchtools.NumberedChromaticPitch(self._chromatic_pitch_name)

    @property
    def numbered_chromatic_pitch_class(self):
        '''Read-only numbered pitch-class::

            >>> named_chromatic_pitch = pitchtools.NamedChromaticPitch("cs''")
            >>> named_chromatic_pitch.numbered_chromatic_pitch_class
            NumberedChromaticPitchClass(1)

        Return numbered chromatic pitch-class.
        '''
        from abjad.tools.pitchtools import NumberedChromaticPitchClass
        return NumberedChromaticPitchClass(self._chromatic_pitch_name)

    @property
    def numbered_diatonic_pitch(self):
        '''Read-only numbered diatonic pitch::

            >>> named_chromatic_pitch = pitchtools.NamedChromaticPitch("cs''")
            >>> named_chromatic_pitch.numbered_diatonic_pitch
            NumberedDiatonicPitch(7)

        Return numbered diatonic pitch.
        '''
        from abjad.tools.pitchtools import NumberedDiatonicPitch
        return NumberedDiatonicPitch(self._chromatic_pitch_name)

    @property
    def numbered_diatonic_pitch_class(self):
        '''Read-only numbered diatonic pitch::

            >>> named_chromatic_pitch = pitchtools.NamedChromaticPitch("cs''")
            >>> named_chromatic_pitch.numbered_diatonic_pitch_class
            NumberedDiatonicPitchClass(0)

        Return numbered diatonic pitch-class.
        '''
        from abjad.tools.pitchtools import NumberedDiatonicPitchClass
        return NumberedDiatonicPitchClass(self._chromatic_pitch_name)

    @property
    def octave_number(self):
        '''Read-only integer octave number::

            >>> named_chromatic_pitch = pitchtools.NamedChromaticPitch("cs''")
            >>> named_chromatic_pitch.octave_number
            5

        Return integer.
        '''
        from abjad.tools import pitchtools
        from abjad.tools.pitchtools.is_chromatic_pitch_name import chromatic_pitch_name_regex
        groups = chromatic_pitch_name_regex.match(self._chromatic_pitch_name).groups()
        octave_tick_string = groups[-1]
        return pitchtools.octave_tick_string_to_octave_number(octave_tick_string)

    @property
    def pitch_class_octave_label(self):
        '''Read-only pitch-class / octave label::

            >>> named_chromatic_pitch = pitchtools.NamedChromaticPitch("cs''")
            >>> named_chromatic_pitch.pitch_class_octave_label
            'C#5'

        Return string.
        '''
        result = []
        result.append(self.diatonic_pitch_class_name.upper())
        result.append(self._accidental.symbolic_accidental_string)
        result.append(str(self.octave_number))
        result = ''.join(result)
        return result

