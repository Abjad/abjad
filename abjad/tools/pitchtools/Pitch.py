# -*- coding: utf-8 -*-
import abc
import functools
import math
import numbers
import re
from abjad.tools import mathtools
from abjad.tools import systemtools
from abjad.tools.abctools import AbjadValueObject
from abjad.tools.pitchtools.Accidental import Accidental
from abjad.tools.pitchtools.Octave import Octave
from abjad.tools.pitchtools.PitchClass import PitchClass


@functools.total_ordering
class Pitch(AbjadValueObject):
    '''Abstract pitch.

    ::

        >>> import abjad

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_arrow',
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
        (
        (?P<diatonic_pitch_class_name>
            [A-G]   # exactly one diatonic pitch-class name
        )
        {}          # plus an optional accidental symbol 
        (?P<octave_number>
            [-]?    # plus an optional negative sign
            [0-9]+  # plus one or more digits
        )
        )
        '''.format(
        Accidental._symbol_regex_body,
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

    def __float__(self):
        r'''Coerce to float.

        Returns float.
        '''
        return float(self.number)

    def __format__(self, format_specification=''):
        r'''Formats pitch.

        Set `format_specification` to `''`, `'lilypond'` or `'storage'`.

        Returns string.
        '''
        from abjad.tools import systemtools
        if format_specification in ('', 'lilypond'):
            return self._get_lilypond_format()
        elif format_specification == 'storage':
            return systemtools.StorageFormatAgent(self).get_storage_format()
        return str(self)

    def __illustrate__(self):
        r'''Illustrates pitch.

        Returns LilyPond file.
        '''
        import abjad
        pitch = abjad.NamedPitch(self)
        note = abjad.Note(pitch, 1)
        abjad.attach(abjad.Multiplier(1, 4), note)
        clef = abjad.Clef.from_selection([pitch])
        abjad.attach(clef, note)
        staff = abjad.Staff()
        staff.append(note)
        abjad.override(staff).time_signature.stencil = False
        lilypond_file = abjad.lilypondfiletools.LilyPondFile.new(staff)
        lilypond_file.header_block.tagline = False
        return lilypond_file

    @abc.abstractmethod
    def __lt__(self, argument):
        r'''Is true when pitch is less than `argument`.

        Returns true or false.
        '''
        raise NotImplementedError

    ### PRIVATE PROPERTIES ###

    @abc.abstractmethod
    def _get_lilypond_format(self):
        raise NotImplementedError

    @staticmethod
    def _to_pitch_class_item_class(item_class):
        import abjad
        item_class = item_class or abjad.NumberedPitch
        if item_class in (abjad.NamedPitchClass, abjad.NumberedPitchClass):
            return item_class
        elif item_class is abjad.NamedPitch:
            return abjad.NamedPitchClass
        elif item_class is abjad.NumberedPitch:
            return abjad.NumberedPitchClass
        else:
            raise TypeError(item_class)

    @staticmethod
    def _to_pitch_item_class(item_class):
        import abjad
        item_class = item_class or abjad.NumberedPitch
        if item_class in (abjad.NamedPitch, abjad.NumberedPitch):
            return item_class
        elif item_class is abjad.NamedPitchClass:
            return abjad.NamedPitch
        elif item_class is abjad.NumberedPitchClass:
            return abjad.NumberedPitch
        else:
            raise TypeError(item_class)

    ### PRIVATE METHODS ###

    @staticmethod
    def _is_diatonic_pitch_name(argument):
        if not isinstance(argument, str):
            return False
        return bool(Pitch._diatonic_pitch_name_regex.match(argument))

    @staticmethod
    def _is_diatonic_pitch_number(argument):
        return isinstance(argument, int)

    @staticmethod
    def _is_pitch_carrier(argument):
        import abjad
        prototype = (
            abjad.Chord,
            abjad.NamedPitch,
            abjad.Note,
            abjad.NoteHead,
            )
        return isinstance(argument, prototype)

    @staticmethod
    def _is_pitch_class_octave_number_string(argument):
        if not isinstance(argument, str):
            return False
        return bool(Pitch._pitch_class_octave_number_regex.match(argument))

    @staticmethod
    def _is_pitch_name(argument):
        if not isinstance(argument, str):
            return False
        return bool(Pitch._pitch_name_regex.match(argument))

    @staticmethod
    def _is_pitch_number(argument):
        if isinstance(argument, (int, float)):
            return argument % 0.5 == 0
        return False

    ### PUBLIC PROPERTIES ###

    @abc.abstractproperty
    def arrow(self):
        r'''Gets arrow of pitch.
        '''
        raise NotImplementedError

    @abc.abstractproperty
    def hertz(self):
        r'''Gets frequency of pitch in Hertz.

        Returns float.
        '''
        hertz = pow(2., (float(self.number) - 9.) / 12.) * 440.
        return hertz

    @abc.abstractproperty
    def name(self):
        r'''Gets name of pitch.

        Returns string.
        '''
        raise NotImplementedError

    @abc.abstractproperty
    def number(self):
        r'''Gets number of pitch.

        Returns number.
        '''
        raise NotImplementedError

    @abc.abstractproperty
    def octave(self):
        r'''Gets octave of pitch.

        Returns octave.
        '''
        raise NotImplementedError
            
    @abc.abstractproperty
    def pitch_class(self):
        r'''Gets pitch-class of pitch.

        Returns pitch-class.
        '''
        raise NotImplementedError

    ### PUBLIC METHODS ###

    @classmethod
    @abc.abstractmethod
    def from_hertz(class_, hertz):
        r'''Creates pitch from `hertz`.

        Returns new pitch.
        '''
        hertz = float(hertz)
        midi = 9. + (12. * math.log(hertz / 440., 2))
        pitch = class_(midi)
        return pitch

    @classmethod
    @abc.abstractmethod
    def from_pitch_carrier(class_, pitch_carrier):
        r'''Makes new pitch from `pitch_carrier`.

        Returns new pitch.
        '''
        import abjad
        if isinstance(pitch_carrier, abjad.NamedPitch):
            return class_(pitch_carrier)
        elif isinstance(pitch_carrier, abjad.NumberedPitch):
            return class_(pitch_carrier)
        elif isinstance(pitch_carrier, numbers.Number):
            return class_(pitch_carrier)
        elif isinstance(pitch_carrier, abjad.Note):
            pitch = pitch_carrier.written_pitch
            if pitch is not None:
                return class_.from_pitch_carrier(pitch)
            else:
                message = 'no pitch found on {!r}.'
                message = message.format(pitch_carrier)
                raise ValueError(message)
        elif isinstance(pitch_carrier, abjad.NoteHead):
            pitch = pitch_carrier.written_pitch
            if pitch is not None:
                return class_.from_pitch_carrier(pitch)
            else:
                message = 'no pitch found on {!r}.'
                message = message.format(pitch_carrier)
                raise ValueError(message)
        elif isinstance(pitch_carrier, abjad.Chord):
            pitches = pitch_carrier.written_pitches
            if len(pitches) == 0:
                message = 'no pitch found on {!r}.'
                message = message.format(pitch_carrier)
                raise ValueError(message)
            elif len(pitches) == 1:
                return class_.from_pitch_carrier(pitches[0])
            else:
                message = 'multiple pitches found on {!r}.'
                message = message.format(pitch_carrier)
                raise ValueError(message)
        elif isinstance(pitch_carrier, abjad.NumberedPitchClass):
            named_pitch = class_((pitch_carrier.name, 4))
            return named_pitch
        else:
            message = 'pitch carrier {!r} must be'
            message += ' pitch, note, note-head or chord.'
            message = message.format(pitch_carrier)
            raise TypeError(message)

    @abc.abstractmethod
    def get_name(self, locale=None):
        r'''Gets name of pitch according to `locale`.

        Returns string.
        '''
        raise NotImplementedError

    @abc.abstractmethod
    def invert(self, axis=None):
        r'''Inverts pitch about `axis`.

        Interprets `axis` of none equal to middle C.

        Returns new pitch.
        '''
        import abjad
        axis = axis or abjad.NamedPitch("c'")
        axis = type(self)(axis)
        interval = self - axis
        result = axis.transpose(interval)
        return result

    @abc.abstractmethod
    def multiply(self, n=1):
        r'''Multiplies pitch by `n`.

        Returns new pitch.
        '''
        return type(self)(n * self.number)

    @abc.abstractmethod
    def transpose(self, n):
        r'''Transposes pitch by index `n`.

        Returns new pitch.
        '''
        raise NotImplementedError
