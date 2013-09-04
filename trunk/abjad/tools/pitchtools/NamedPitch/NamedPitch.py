# -*- encoding: utf-8 -*-
from abjad.tools.pitchtools.Accidental import Accidental
from abjad.tools.pitchtools.Pitch import Pitch
from abjad.tools.pitchtools.is_chromatic_pitch_name \
	import chromatic_pitch_name_regex


class NamedPitch(Pitch):
    '''Abjad model of named chromatic pitch:

    ::

        >>> pitch = pitchtools.NamedPitch("cs''")
        >>> pitch
        NamedPitch("cs''")

    Named chromatic pitches are immutable.
    '''

    ### CLASS VARIABLES ###


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
        self._deviation_in_cents = _deviation_in_cents
        if len(args) == 1 and isinstance(args[0], (int, long, float)):
            self._init_by_chromatic_pitch_number(*args)
        elif len(args) == 1 and isinstance(args[0], type(self)):
            self._init_by_named_chromatic_pitch(*args)
        elif len(args) == 1 and isinstance(args[0], pitchtools.NumberedPitch):
            self._init_by_chromatic_pitch_number(
                args[0].chromatic_pitch_number)
        elif len(args) == 1 and hasattr(args[0], 'named_chromatic_pitch'):
            self._init_by_named_chromatic_pitch(args[0].named_chromatic_pitch)
        elif len(args) == 1 and \
            pitchtools.is_chromatic_pitch_class_name_octave_number_pair(
            args[0]):
            self._init_by_chromatic_pitch_class_name_octave_number_pair(*args)
        elif len(args) == 1 and \
            pitchtools.is_pitch_class_octave_number_string(args[0]):
            self._init_by_pitch_class_octave_number_string(*args)
        elif len(args) == 1 and isinstance(args[0], str):
            self._init_by_chromatic_pitch_name(*args)
        elif len(args) == 2 and isinstance(args[0], str):
            self._init_by_chromatic_pitch_class_name_and_octave_number(*args)
        elif len(args) == 2 and \
            isinstance(args[0], pitchtools.NamedPitchClass):
            self._init_by_named_chromatic_pitch_class_and_octave_number(*args)
        elif len(args) == 2 and isinstance(args[0], (int, long, float)):
            if isinstance(args[1], str):
                self._init_by_chromatic_pitch_number_and_diatonic_pitch_class_name(*args)
            elif isinstance(args[1], pitchtools.NamedPitchClass):
                self._init_by_chromatic_pitch_number_and_named_chromatic_pitch_class(*args)
            else:
                raise TypeError
        elif len(args) == 3:
            self._init_by_chromatic_pitch_class_name_octave_number_and_deviation(*args)
        else:
            raise ValueError('\n\tNot a valid pitch token: "%s".' % str(args))
        assert hasattr(self, '_deviation_in_cents')
        assert hasattr(self, '_chromatic_pitch_name')
        diatonic_pitch_number = \
            pitchtools.chromatic_pitch_name_to_diatonic_pitch_number(
            self._chromatic_pitch_name)
        self._diatonic_pitch_number = diatonic_pitch_number
        groups = \
            chromatic_pitch_name_regex.match(self._chromatic_pitch_name).groups()
        alphabetic_accidental_abbreviation = groups[1]
        accidental_semitones = \
            Accidental._alphabetic_accidental_abbreviation_to_semitones[
            alphabetic_accidental_abbreviation]
        self._accidental_semitones = accidental_semitones

    ### SPECIAL METHODS ###

    def __abs__(self):
        return abs(self.numbered_chromatic_pitch)

    def __add__(self, melodic_interval):
        from abjad.tools import pitchtools
        return pitchtools.transpose_pitch_carrier_by_melodic_interval(
            self, melodic_interval)

    def __copy__(self, *args):
        return type(self)(self)

    # TODO: remove?
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
                return '%s(%r)' % (self._class_name, str(self))
            else:
                return '%s(%r, deviation=%s)' % (self._class_name,
                    str(self), self.deviation_in_cents)
        else:
            return '%s()' % self._class_name

    def __str__(self):
        if self.chromatic_pitch_class_name and not self.octave_number is None:
            return '%s%s' % (
                self.chromatic_pitch_class_name, self._octave_tick_string)
        else:
            return ''

    def __sub__(self, arg):
        from abjad.tools import pitchtools
        if isinstance(arg, type(self)):
            return pitchtools.NamedInterval.from_pitch_carriers(
                self, arg)
        else:
            interval = arg
            return pitchtools.transpose_pitch_carrier_by_melodic_interval(
                self, -interval)

    ### PRIVATE PROPERTIES ###

    @property
    def _accidental(self):
        from abjad.tools.pitchtools.Accidental import Accidental
        from abjad.tools.pitchtools.is_chromatic_pitch_name \
            import chromatic_pitch_name_regex
        groups = \
            chromatic_pitch_name_regex.match(self._chromatic_pitch_name).groups()
        alphabetic_accidental_abbreviation = groups[1]
        return Accidental(alphabetic_accidental_abbreviation)

    @property
    def _keyword_argument_names(self):
        return (
            'deviation_in_cents',
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

    @property
    def _positional_argument_values(self):
        return (
            self.chromatic_pitch_name,
            )

    ### PRIVATE METHODS ###

    def _init_by_chromatic_pitch_class_name_and_octave_number(
        self, chromatic_pitch_class_name, octave_number):
        from abjad.tools import pitchtools
        octave_tick_string = str(pitchtools.OctaveIndication(octave_number))
        chromatic_pitch_name = chromatic_pitch_class_name + octave_tick_string
        self._chromatic_pitch_name = chromatic_pitch_name

    def _init_by_chromatic_pitch_class_name_octave_number_and_deviation(
        self, name, octave, deviation):
        self._init_by_chromatic_pitch_class_name_and_octave_number(name, octave)
        self._deviation_in_cents = deviation

    def _init_by_chromatic_pitch_class_name_octave_number_pair(self, pair):
        from abjad.tools import pitchtools
        chromatic_pitch_class_name, octave_number = pair
        octave_tick_string = str(pitchtools.OctaveIndication(octave_number))
        chromatic_pitch_name = chromatic_pitch_class_name + octave_tick_string
        self._chromatic_pitch_name = chromatic_pitch_name

    def _init_by_chromatic_pitch_name(self, pitch_string):
        from abjad.tools import pitchtools
        name = pitchtools.chromatic_pitch_name_to_chromatic_pitch_class_name(
            pitch_string)
        octave_number = pitchtools.OctaveIndication.from_pitch_name(
            pitch_string).octave_number
        self._init_by_chromatic_pitch_class_name_and_octave_number(
            name, octave_number)

    def _init_by_chromatic_pitch_number(self, chromatic_pitch_number):
        from abjad.tools import pitchtools
        accidental_spelling = self.accidental_spelling
        chromatic_pitch_name = \
            pitchtools.chromatic_pitch_number_to_chromatic_pitch_name(
            chromatic_pitch_number, accidental_spelling)
        self._chromatic_pitch_name = chromatic_pitch_name

    def _init_by_chromatic_pitch_number_and_diatonic_pitch_class_name(
        self, chromatic_pitch_number, diatonic_pitch_class_name):
        from abjad.tools import pitchtools
        accidental, octave_number = \
            pitchtools.spell_chromatic_pitch_number(
                chromatic_pitch_number, diatonic_pitch_class_name)
        octave_tick_string = str(pitchtools.OctaveIndication(octave_number))
        chromatic_pitch_class_name = diatonic_pitch_class_name + \
            accidental.alphabetic_accidental_abbreviation
        chromatic_pitch_name = chromatic_pitch_class_name + octave_tick_string
        self._chromatic_pitch_name = chromatic_pitch_name

    def _init_by_chromatic_pitch_number_and_named_chromatic_pitch_class(
        self, pitch_number, npc):
        diatonic_pitch_class_name = npc.name[:1]
        self._init_by_chromatic_pitch_number_and_diatonic_pitch_class_name(
            pitch_number, diatonic_pitch_class_name)

    def _init_by_named_chromatic_pitch(self, named_chromatic_pitch):
        self._chromatic_pitch_name = \
            named_chromatic_pitch._chromatic_pitch_name
        self._deviation_in_cents = \
            named_chromatic_pitch.deviation_in_cents

    def _init_by_named_chromatic_pitch_class_and_octave_number(
        self, npc, octave_number):
        self._init_by_chromatic_pitch_class_name_and_octave_number(
            npc._chromatic_pitch_class_name, octave_number)

    def _init_by_pitch_class_octave_number_string(
        self, pitch_class_octave_number_string):
        from abjad.tools import pitchtools
        chromatic_pitch_name = \
            pitchtools.pitch_class_octave_number_string_to_chromatic_pitch_name(
            pitch_class_octave_number_string)
        self._chromatic_pitch_name = chromatic_pitch_name

    ### PUBLIC PROPERTIES ###

    @property
    def accidental_spelling(self):
        r'''Accidental spelling:

        ::

            >>> pitchtools.NamedPitch("c").accidental_spelling
            'mixed'

        Return string.
        '''
        from abjad import abjad_configuration
        return abjad_configuration['accidental_spelling']

    @property
    def chromatic_pitch_class_name(self):
        r'''Chromatic pitch-class name:

        ::

            >>> pitch.chromatic_pitch_class_name
            'cs'

        Return string.
        '''
        return self.named_chromatic_pitch_class._chromatic_pitch_class_name

    @property
    def chromatic_pitch_class_number(self):
        r'''Chromatic pitch-class number:

        ::

            >>> pitch.chromatic_pitch_class_number
            1

        Return integer or float.
        '''
        return self.numbered_chromatic_pitch_class._chromatic_pitch_class_number

    @property
    def chromatic_pitch_name(self):
        r'''Chromatic pitch name:

        ::

            >>> pitch.chromatic_pitch_name
            "cs''"

        Return string.
        '''
        return self._chromatic_pitch_name

    @property
    def chromatic_pitch_number(self):
        r'''Chromatic pitch-class number:

        ::

            >>> pitch.chromatic_pitch_number
            13

        Return integer or float.
        '''
        return self.numbered_chromatic_pitch._chromatic_pitch_number

    @property
    def deviation_in_cents(self):
        r'''Deviation of named chromatic pitch in cents:

        ::

            >>> pitch.deviation_in_cents is None
            True

        Return integer or none.
        '''
        return self._deviation_in_cents

    @property
    def diatonic_pitch_class_name(self):
        r'''Diatonic pitch-class name:

        ::

            >>> pitch.diatonic_pitch_class_name
            'c'

        Return string.
        '''
        from abjad.tools import pitchtools
        number = pitchtools.diatonic_pitch_number_to_diatonic_pitch_class_number(
            self._diatonic_pitch_number)
        name = pitchtools.diatonic_pitch_class_number_to_diatonic_pitch_class_name(
            number)
        return name

    @property
    def diatonic_pitch_class_number(self):
        r'''Diatonic pitch-class number:

        ::

            >>> pitch.diatonic_pitch_class_number
            0

        Return integer.
        '''
        from abjad.tools import pitchtools
        return pitchtools.diatonic_pitch_number_to_diatonic_pitch_class_number(
            self._diatonic_pitch_number)
        #return self.numbered_diatonic_pitch_class._diatonic_pitch_class_number

    @property
    def diatonic_pitch_name(self):
        r'''Diatonic pitch name:

        ::

            >>> pitch.diatonic_pitch_name
            "c''"

        Return string.
        '''
        from abjad.tools import pitchtools
        number = self._diatonic_pitch_number
        name = pitchtools.diatonic_pitch_number_to_diatonic_pitch_name(number)
        return name

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
    def lilypond_format(self):
        r'''LilyPond input format of named chromatic pitch:

        ::

            >>> pitch.lilypond_format
            "cs''"

        Return string.
        '''
        return str(self)

    @property
    def named_chromatic_pitch_class(self):
        r'''Named pitch-class:

        ::

            >>> pitch.named_chromatic_pitch_class
            NamedPitchClass('cs')

        Return named chromatic pitch-class.
        '''
        from abjad.tools.pitchtools import NamedPitchClass
        return NamedPitchClass(self._chromatic_pitch_name)

    @property
    def numbered_chromatic_pitch(self):
        r'''Numbered chromatic pitch from named chromatic pitch:

        ::

            >>> pitch.numbered_chromatic_pitch_class
            NumberedPitchClass(1)

        Return numbered chromatic pitch-class.
        '''
        from abjad.tools import pitchtools
        return pitchtools.NumberedPitch(self._chromatic_pitch_name)

    @property
    def numbered_chromatic_pitch_class(self):
        r'''Numbered pitch-class:

        ::

            >>> pitch.numbered_chromatic_pitch_class
            NumberedPitchClass(1)

        Return numbered chromatic pitch-class.
        '''
        from abjad.tools.pitchtools import NumberedPitchClass
        return NumberedPitchClass(self._chromatic_pitch_name)

    @property
    def octave_number(self):
        r'''Integer octave number:

        ::

            >>> pitch.octave_number
            5

        Return integer.
        '''
        from abjad.tools import pitchtools
        from abjad.tools.pitchtools.is_chromatic_pitch_name \
            import chromatic_pitch_name_regex
        groups = \
            chromatic_pitch_name_regex.match(
                self._chromatic_pitch_name).groups()
        octave_tick_string = groups[-1]
        return pitchtools.octave_tick_string_to_octave_number(
            octave_tick_string)

    @property
    def pitch_class_octave_label(self):
        r'''Pitch-class / octave label:

        ::

            >>> pitch.pitch_class_octave_label
            'C#5'

        Return string.
        '''
        result = []
        result.append(self.diatonic_pitch_class_name.upper())
        result.append(self._accidental.symbolic_accidental_string)
        result.append(str(self.octave_number))
        result = ''.join(result)
        return result
