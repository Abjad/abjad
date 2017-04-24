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
        (
        (?P<diatonic_pitch_class_name>
            [A-G]   # exactly one diatonic pitch-class name
        )
        {}          # plus an optional symbolic accidental string
        (?P<octave_number>
            [-]?    # plus an optional negative sign
            [0-9]+  # plus one or more digits
        )
        )
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
        staff = abjad.Staff()
        abjad.attach(clef, staff)
        staff.append(note)
        abjad.override(staff).time_signature.stencil = False
        lilypond_file = abjad.lilypondfiletools.LilyPondFile.new(staff)
        lilypond_file.header_block.tagline = False
        return lilypond_file

    @abc.abstractmethod
    def __int__(self):
        r'''Changes pitch to integer.

        Returns integer.
        '''
        message = 'TODO: all pitch-related classes must implement int.'
        raise NotImplementedError(message)

    ### PRIVATE PROPERTIES ###

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

    ### PUBLIC PROPERTIES ###

    @abc.abstractproperty
    def alteration_in_semitones(self):
        r'''Gets alteration of pitch in semitones.
        '''
        raise NotImplementedError

    @abc.abstractproperty
    def diatonic_pitch_class_name(self):
        r'''Gets diatonic pitch-class name of pitch.

        ..  note:: Deprecated.
        '''
        raise NotImplementedError

    @abc.abstractproperty
    def diatonic_pitch_class_number(self):
        r'''Gets diatonic pitch-class number of pitch.

        ..  note:: Deprecated.
        '''
        raise NotImplementedError

    @abc.abstractproperty
    def diatonic_pitch_name(self):
        r'''Gets diatonic pitch name of pitch.

        ..  note:: Deprecated.
        '''
        raise NotImplementedError

    @abc.abstractproperty
    def diatonic_pitch_number(self):
        r'''Gets diatonic pitch number of pitch.

        ..  note:: Deprecated.
        '''
        raise NotImplementedError

    @property
    def hertz(self):
        r'''Gets frequency of pitch in Herz.

        ..  container:: example

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
    def name(self):
        r'''Gets pitch name.
        '''
        raise NotImplementedError

    @abc.abstractproperty
    def named_pitch(self):
        r'''Gets named pitch corresponding to pitch.

        ..  note:: Deprecated.
        '''
        raise NotImplementedError

    @abc.abstractproperty
    def named_pitch_class(self):
        r'''Gets named pitch-class corresponding to pitch.

        ..  note:: Deprecated.
        '''
        raise NotImplementedError

    @abc.abstractproperty
    def number(self):
        r'''Gets pitch number.
        '''
        raise NotImplementedError

    @abc.abstractproperty
    def numbered_pitch(self):
        r'''Gets numbered pitch corresponding to pitch.

        ..  note:: Deprecated.
        '''
        raise NotImplementedError

    @abc.abstractproperty
    def numbered_pitch_class(self):
        r'''Gets numbered pitch-class corresponding to pitch.

        ..  note:: Deprecated.
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
        r'''Gets pitch-class.

        Returns pitch-class.
        '''
        raise NotImplementedError

    @abc.abstractproperty
    def pitch_class_name(self):
        r'''Gets pitch-class name corresponding to pitch.

        ..  note:: Deprecated.
        '''
        raise NotImplementedError

    @abc.abstractproperty
    def pitch_class_number(self):
        r'''Gets pitch-class number of pitch.

        ..  note:: Deprecated.
        '''
        raise NotImplementedError

    @abc.abstractproperty
    def pitch_class_octave_label(self):
        r'''Gets pitch-class / octave label of pitch.

        ..  note:: Deprecated.
        '''
        raise NotImplementedError

    @abc.abstractproperty
    def pitch_name(self):
        r'''Gets pitch name of pitch.

        ..  note:: Deprecated.
        '''
        raise NotImplementedError

    @abc.abstractproperty
    def pitch_number(self):
        r'''Get pitch number of pitch.

        ..  note:: Deprecated.
        '''
        raise NotImplementedError

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

        ..  container:: example

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
    def is_diatonic_pitch_name(argument):
        '''Is true when `argument` is a diatonic pitch name. Otherwise false.

        ..  container:: example

            ::

                >>> pitchtools.Pitch.is_diatonic_pitch_name("c''")
                True

        ..  container:: example

            ::

                >>> pitchtools.Pitch.is_diatonic_pitch_name("cs''")
                False

        The regex ``(^[a-g,A-G])(,+|'+|)$`` underlies this predicate.

        Returns true or false.
        '''
        if not isinstance(argument, str):
            return False
        return bool(Pitch._diatonic_pitch_name_regex.match(argument))

    @staticmethod
    def is_diatonic_pitch_number(argument):
        '''Is true when `argument` is a diatonic pitch number. Otherwise false.

        ..  container:: example

            ::

                >>> pitchtools.Pitch.is_diatonic_pitch_number(7)
                True

        ..  container:: example

            ::

                >>> pitchtools.Pitch.is_diatonic_pitch_number(7.5)
                False

        Diatonic pitch numbers are equal to the set of integers.

        Returns true or false.
        '''
        return isinstance(argument, int)

    @staticmethod
    def is_pitch_carrier(argument):
        '''Is true when `argument` is an Abjad pitch, note, note-head of chord
        instance. Otherwise false.

        ..  container:: example

            ::

                >>> note = Note("c'4")
                >>> pitchtools.Pitch.is_pitch_carrier(note)
                True

        ..  container:: example

            ::

                >>> pitchtools.Pitch.is_pitch_carrier('text')
                False

        Returns true or false.
        '''
        from abjad.tools import scoretools
        from abjad.tools import pitchtools
        return isinstance(
            argument, (
                pitchtools.NamedPitch,
                scoretools.Note,
                scoretools.NoteHead,
                scoretools.Chord
                )
            )

    @staticmethod
    def is_pitch_class_octave_number_string(argument):
        '''Is true when `argument` is a pitch-class / octave number string.
        Otherwise false.

        ..  container:: example

            ::

                >>> pitchtools.Pitch.is_pitch_class_octave_number_string('C#2')
                True

        ..  container:: example

            Supports quartertone accidentals:

            ::

                >>> pitchtools.Pitch.is_pitch_class_octave_number_string('C#2')
                True

        ..  container:: example

            ::

                >>> pitchtools.Pitch.is_pitch_class_octave_number_string('C#')
                False

        The regex ``^([A-G])([#]{1,2}|[b]{1,2}|[#]?[+]|[b]?[~]|)([-]?[0-9]+)$``
        underlies this predicate.

        Returns true or false.
        '''
        if not isinstance(argument, str):
            return False
        return bool(Pitch._pitch_class_octave_number_regex.match(argument))

    @staticmethod
    def is_pitch_name(argument):
        '''Is true when `argument` is a pitch name. Otherwise false.

        ..  container:: example

            ::

                >>> pitchtools.Pitch.is_pitch_name('c,')
                True

        ..  container:: example

            ::

                >>> pitchtools.Pitch.is_pitch_name('z')
                False

        The regex ``^([a-g,A-G])(([s]{1,2}|[f]{1,2}|t?q?[f,s]|)!?)(,+|'+|)$``
        underlies this predicate.

        Returns true or false.
        '''
        if not isinstance(argument, str):
            return False
        return bool(Pitch._pitch_name_regex.match(argument))

    @staticmethod
    def is_pitch_number(argument):
        '''Is true when `argument` is a pitch number. Otherwise false.

        ..  container:: example

            ::

                >>> pitchtools.Pitch.is_pitch_number(13)
                True

        ..  container:: example

            ::

                >>> pitchtools.Pitch.is_pitch_number('text')
                False

        Pitch numbers are equal to the set of all integers in union with the
        set of all integers plus of minus 0.5.

        Returns true or false.
        '''
        if isinstance(argument, (int, float)):
            return argument % 0.5 == 0
        return False

    @abc.abstractmethod
    def multiply(self, n=1):
        r'''Multiplies pitch by `n`.
        '''
        raise NotImplementedError

    @abc.abstractmethod
    def transpose(self, n):
        r'''Transposes pitch by index `n`.

        Returns new pitch.
        '''
        raise NotImplementedError
