# -*- coding: utf-8 -*-
import abc
import math
import re
from abjad.tools import mathtools
from abjad.tools import systemtools
from abjad.tools.abctools import AbjadValueObject
from abjad.tools.pitchtools.Accidental import Accidental
from abjad.tools.pitchtools.Octave import Octave
from abjad.tools.pitchtools.PitchClass import PitchClass


class Pitch(AbjadValueObject):
    '''Pitch base class.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    _diatonic_pitch_name_regex_body = '''
        {}  # exactly one diatonic pitch-class name
        {}  # followed by exactly one octave tick string
        '''.format(
        PitchClass._diatonic_pitch_class_name_regex_body,
        Octave._octave_tick_regex_body,
        )

    _diatonic_pitch_name_regex = re.compile(
        '^{}$'.format(_diatonic_pitch_name_regex_body),
        re.VERBOSE,
        )

    _pitch_class_octave_number_regex_body = '''
        ([A-G])         # exactly one diatonic pitch-class letter
        {}              # plus an optional symbolic accidental string
        ([-]?           # plus an optional negative sign
        [0-9]+)         # plus one or more digits
        '''.format(
        Accidental._symbolic_string_regex_body,
        )

    _pitch_class_octave_number_regex = re.compile(
        '^{}$'.format(_pitch_class_octave_number_regex_body),
        re.VERBOSE,
        )

    _pitch_name_regex_body = '''
        {}  # exactly one diatonic pitch-class name
        {}  # followed by exactly one alphabetic accidental name
        {}  # followed by exactly one octave tick string
        '''.format(
        PitchClass._diatonic_pitch_class_name_regex_body,
        Accidental._alphabetic_accidental_regex_body,
        Octave._octave_tick_regex_body,
        )

    _pitch_name_regex = re.compile(
        '^{}$'.format(_pitch_name_regex_body),
        re.VERBOSE,
        )

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self):
        pass

    ### SPECIAL METHODS ###

    @abc.abstractmethod
    def __float__(self):
        r'''Changes pitch to float.

        Returns float.
        '''
        message = 'TODO: all pitch-related classes must implement float.'
        raise NotImplementedError(message)

    def __format__(self, format_specification=''):
        r'''Formats pitch.

        Set `format_specification` to `''`, `'lilypond'` or `'storage'`.

        Returns string.
        '''
        from abjad.tools import systemtools
        if format_specification in ('', 'lilypond'):
            return self._lilypond_format
        elif format_specification == 'storage':
            return systemtools.StorageFormatAgent(self).get_storage_format()
        return str(self)

    def __illustrate__(self):
        r'''Illustrates pitch.

        Returns LilyPond file.
        '''
        from abjad.tools import durationtools
        from abjad.tools import indicatortools
        from abjad.tools import lilypondfiletools
        from abjad.tools import pitchtools
        from abjad.tools import scoretools
        from abjad.tools.topleveltools import attach
        from abjad.tools.topleveltools import override
        pitch = pitchtools.NamedPitch(self)
        note = scoretools.Note(pitch, 1)
        attach(durationtools.Multiplier(1, 4), note)
        clef = indicatortools.Clef.from_selection([pitch])
        staff = scoretools.Staff()
        attach(clef, staff)
        staff.append(note)
        override(staff).time_signature.stencil = False
        lilypond_file = lilypondfiletools.make_basic_lilypond_file(staff)
        lilypond_file.header_block.tagline = False
        return lilypond_file

    @abc.abstractmethod
    def __int__(self):
        r'''Changes pitch to integer.

        Returns integer.
        '''
        message = 'TODO: all pitch-related classes must implement int.'
        raise NotImplementedError(message)

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        if type(self).__name__.startswith('Named'):
            values = [str(self)]
        else:
            values = [
                mathtools.integer_equivalent_number_to_integer(float(self))
                ]
        return systemtools.FormatSpecification(
            client=self,
            coerce_for_equality=True,
            repr_is_indented=False,
            storage_format_is_indented=False,
            storage_format_args_values=values,
            template_names=['pitch_name'],
            )

    ### PUBLIC METHODS ###

    @abc.abstractmethod
    def apply_accidental(self, accidental=None):
        r'''Applies `accidental` to pitch.

        Returns new pitch.
        '''
        raise NotImplementedError

    @classmethod
    def from_hertz(class_, hertz):
        r'''Creates pitch from `hertz`.

        ::

            >>> pitchtools.NamedPitch.from_hertz(440)
            NamedPitch("a'")

        ::

            >>> pitchtools.NumberedPitch.from_hertz(440)
            NumberedPitch(9)

        ::

            >>> pitchtools.NamedPitch.from_hertz(519)
            NamedPitch("c'")

        Returns new pitch.
        '''
        hertz = float(hertz)
        midi = 9. + (12. * math.log(hertz / 440., 2))
        pitch = class_(midi)
        return pitch

    @abc.abstractmethod
    def invert(self, axis=None):
        r'''Inverts pitch about `axis`.

        Interprets `axis` of none equal to middle C.

        Returns new pitch.
        '''
        from abjad.tools import pitchtools
        axis = axis or pitchtools.NamedPitch("c'")
        axis = type(self)(axis)
        interval = self - axis
        result = axis.transpose(interval)
        return result

    @staticmethod
    def is_diatonic_pitch_name(expr):
        '''Is true when `expr` is a diatonic pitch name. Otherwise false.

        ::

            >>> pitchtools.Pitch.is_diatonic_pitch_name("c''")
            True

        The regex ``(^[a-g,A-G])(,+|'+|)$`` underlies this predicate.

        Returns true or false.
        '''
        if not isinstance(expr, str):
            return False
        return bool(Pitch._diatonic_pitch_name_regex.match(expr))

    @staticmethod
    def is_diatonic_pitch_number(expr):
        '''Is true when `expr` is a diatonic pitch number. Otherwise false.

        ::

            >>> pitchtools.Pitch.is_diatonic_pitch_number(7)
            True

        The diatonic pitch numbers are equal to the set of integers.

        Returns true or false.
        '''
        return isinstance(expr, int)

    @staticmethod
    def is_pitch_carrier(expr):
        '''Is true when `expr` is an Abjad pitch, note, note-head of chord
        instance. Otherwise false.

        ::

            >>> note = Note("c'4")
            >>> pitchtools.Pitch.is_pitch_carrier(note)
            True

        Returns true or false.
        '''
        from abjad.tools import scoretools
        from abjad.tools import pitchtools
        return isinstance(
            expr, (
                pitchtools.NamedPitch,
                scoretools.Note,
                scoretools.NoteHead,
                scoretools.Chord
                )
            )

    @staticmethod
    def is_pitch_class_octave_number_string(expr):
        '''Is true when `expr` is a pitch-class / octave number string. Otherwise
        false:

        ::

            >>> pitchtools.Pitch.is_pitch_class_octave_number_string('C#2')
            True

        Quartertone accidentals are supported.

        The regex ``^([A-G])([#]{1,2}|[b]{1,2}|[#]?[+]|[b]?[~]|)([-]?[0-9]+)$``
        underlies this predicate.

        Returns true or false.
        '''
        if not isinstance(expr, str):
            return False
        return bool(Pitch._pitch_class_octave_number_regex.match(expr))

    @staticmethod
    def is_pitch_name(expr):
        '''True `expr` is a pitch name. Otherwise false.

        ::

            >>> pitchtools.Pitch.is_pitch_name('c,')
            True

        The regex ``^([a-g,A-G])(([s]{1,2}|[f]{1,2}|t?q?[f,s]|)!?)(,+|'+|)$``
        underlies this predicate.

        Returns true or false.
        '''
        if not isinstance(expr, str):
            return False
        return bool(Pitch._pitch_name_regex.match(expr))

    @staticmethod
    def is_pitch_number(expr):
        '''Is true when `expr` is a pitch number. Otherwise false.

        ::

            >>> pitchtools.Pitch.is_pitch_number(13)
            True

        The pitch numbers are equal to the set of all integers in
        union with the set of all integers plus of minus ``0.5``.

        Returns true or false.
        '''
        if isinstance(expr, (int, float)):
            return expr % 0.5 == 0
        return False

    @abc.abstractmethod
    def multiply(self, n=1):
        r'''Multiplies pitch by `n`.
        '''
        raise NotImplementedError

    @abc.abstractmethod
    def transpose(self, expr):
        r'''Transposes pitch by `expr`.

        Returns new pitch.
        '''
        raise NotImplementedError

    ### PRIVATE PROPERTIES ###

    @abc.abstractproperty
    def _lilypond_format(self):
        r'''LilyPond input format.
        '''
        raise NotImplementedError

    ### PUBLIC PROPERTIES ###

    @abc.abstractproperty
    def accidental(self):
        r'''Accidental of pitch.
        '''
        raise NotImplementedError

    @property
    def accidental_spelling(self):
        r'''Accidental spelling of Abjad session.

        ::

            >>> NamedPitch("c").accidental_spelling
            'mixed'

        Returns string.
        '''
        from abjad import abjad_configuration
        return abjad_configuration['accidental_spelling']

    @abc.abstractproperty
    def alteration_in_semitones(self):
        r'''Alteration of pitch in semitones.
        '''
        raise NotImplementedError

    @abc.abstractproperty
    def diatonic_pitch_class_name(self):
        r'''Diatonic pitch-class name of pitch.
        '''
        raise NotImplementedError

    @abc.abstractproperty
    def diatonic_pitch_class_number(self):
        r'''Diatonic pitch-class number of pitch.
        '''
        raise NotImplementedError

    @abc.abstractproperty
    def diatonic_pitch_name(self):
        r'''Diatonic pitch name of pitch.
        '''
        raise NotImplementedError

    @abc.abstractproperty
    def diatonic_pitch_number(self):
        r'''Diatonic pitch number of pitch.
        '''
        raise NotImplementedError

    @property
    def hertz(self):
        r'''Gets hertz value of pitch.

        ::

            >>> pitchtools.NamedPitch("a'").hertz
            440.0

        ::

            >>> pitchtools.NamedPitch("c'").hertz
            261.62...

        ::

            >>> pitchtools.NamedPitch("c''").hertz
            523.25...

        Returns float.
        '''
        hertz = pow(2., (float(self) - 9.) / 12.) * 440.
        return hertz

    @abc.abstractproperty
    def named_pitch(self):
        r'''Named pitch corresponding to pitch.
        '''
        raise NotImplementedError

    @abc.abstractproperty
    def named_pitch_class(self):
        r'''Named pitch-class corresponding to pitch.
        '''
        raise NotImplementedError

    @abc.abstractproperty
    def numbered_pitch(self):
        r'''Numbered pitch corresponding to pitch.
        '''
        raise NotImplementedError

    @abc.abstractproperty
    def numbered_pitch_class(self):
        r'''Numbered pitch-class corresponding to pitch.
        '''
        raise NotImplementedError

    @abc.abstractproperty
    def octave(self):
        r'''Octave of pitch.

        Returns octave.
        '''
        raise NotImplementedError

    @abc.abstractproperty
    def octave_number(self):
        r'''Octave number of pitch.

        Returns integer.
        '''
        raise NotImplementedError

    @abc.abstractproperty
    def pitch_class_name(self):
        r'''Pitch-class name corresponding to pitch.

        Returns string.
        '''
        raise NotImplementedError

    @abc.abstractproperty
    def pitch_class_number(self):
        r'''Pitch-class number of pitch.

        Returns number
        '''
        raise NotImplementedError

    @abc.abstractproperty
    def pitch_class_octave_label(self):
        r'''Pitch-class / octave label of pitch.
        '''
        raise NotImplementedError

    @abc.abstractproperty
    def pitch_name(self):
        r'''Pitch name of pitch.

        Returns string.
        '''
        raise NotImplementedError

    @abc.abstractproperty
    def pitch_number(self):
        r'''Pitch number of pitch.

        Returns number.
        '''
        raise NotImplementedError
