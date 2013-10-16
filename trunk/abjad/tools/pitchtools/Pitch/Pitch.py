# -*- encoding: utf-8 -*-
import abc
import re
from abjad.tools.abctools.AbjadObject import AbjadObject
from abjad.tools.pitchtools.PitchClass import PitchClass
from abjad.tools.pitchtools.Accidental import Accidental
from abjad.tools.pitchtools.OctaveIndication import OctaveIndication


class Pitch(AbjadObject):
    '''Pitch base class.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_pitch_class',
        '_octave_indication',
        )

    _diatonic_pitch_name_regex_body = '''
        {}  # exactly one diatonic pitch-class name
        {}  # followed by exactly one octave tick string
        '''.format(
        PitchClass._diatonic_pitch_class_name_regex_body,
        OctaveIndication._octave_tick_regex_body,
        )

    _diatonic_pitch_name_regex = re.compile(
        '^{}$'.format(_diatonic_pitch_name_regex_body),
        re.VERBOSE,
        )

    _pitch_class_octave_number_regex_body = '''
        ([A-G])         # exactly one diatonic pitch-class letter
        {}                # plus an optional symbolic accidental string
        ([-]?           # plus an optional negative sign
        [0-9]+)         # plus one or more digits
        '''.format(
        Accidental._symbolic_accidental_string_regex_body,
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
        OctaveIndication._octave_tick_regex_body,
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
    def __abs__(self):
        raise NotImplementedError(
            'TODO: all pitch-related classes must implement abs.')

    @abc.abstractmethod
    def __float__(self):
        raise NotImplementedError(
            'TODO: all pitch-related classes must implement float.')

    def __hash__(self):
        return hash(repr(self))

    @abc.abstractmethod
    def __int__(self):
        raise NotImplementedError(
            'TODO: all pitch-related classes must implement int.')

    def __repr__(self):
        return '{}({})'.format(self._class_name, self._format_string)

    ### PRIVATE METHODS ###

    # do not indent in storage
    def _get_tools_package_qualified_repr_pieces(self, is_indented=True):
        from abjad.tools import abctools
        return [''.join(
            abctools.AbjadObject._get_tools_package_qualified_repr_pieces(
                self, is_indented=False))]

    ### PUBLIC METHODS ###

    @abc.abstractmethod
    def apply_accidental(self, accidental=None):
        raise NotImplementedError

    @abc.abstractmethod
    def invert(self, axis=None):
        raise NotImplementedError

    @staticmethod
    def is_diatonic_pitch_name(expr):
        '''True when `expr` is a diatonic pitch name, otherwise false.

        ::

            >>> pitchtools.Pitch.is_diatonic_pitch_name("c''")
            True

        The regex ``(^[a-g,A-G])(,+|'+|)$`` underlies this predicate.

        Return boolean.
        '''
        if not isinstance(expr, str):
            return False
        return bool(Pitch._diatonic_pitch_name_regex.match(expr))

    @staticmethod
    def is_diatonic_pitch_number(expr):
        '''True when `expr` is a diatonic pitch number, otherwise false.

        ::

            >>> pitchtools.Pitch.is_diatonic_pitch_number(7)
            True

        The diatonic pitch numbers are equal to the set of integers.

        Return boolean.
        '''
        return isinstance(expr, (int, long))

    @staticmethod
    def is_pitch_carrier(expr):
        '''True when `expr` is an Abjad pitch, note, note-head of chord
        instance, otherwise false.

        ::

            >>> note = Note("c'4")
            >>> pitchtools.Pitch.is_pitch_carrier(note)
            True

        Return boolean.
        '''
        from abjad.tools import chordtools
        from abjad.tools import notetools
        from abjad.tools import pitchtools
        return isinstance(
            expr, (
                pitchtools.NamedPitch,
                notetools.Note,
                notetools.NoteHead,
                chordtools.Chord
                )
            )

    @staticmethod
    def is_pitch_class_octave_number_string(expr):
        '''True when `expr` is a pitch-class / octave number string, otherwise 
        false:

        ::

            >>> pitchtools.Pitch.is_pitch_class_octave_number_string('C#2')
            True

        Quartertone accidentals are supported.

        The regex ``^([A-G])([#]{1,2}|[b]{1,2}|[#]?[+]|[b]?[~]|)([-]?[0-9]+)$``
        underlies this predicate.

        Return boolean.
        '''
        if not isinstance(expr, str):
            return False
        return bool(Pitch._pitch_class_octave_number_regex.match(expr))

    @staticmethod
    def is_pitch_name(expr):
        '''True `expr` is a pitch name, otherwise false.

        ::

            >>> pitchtools.Pitch.is_pitch_name('c,')
            True

        The regex ``^([a-g,A-G])(([s]{1,2}|[f]{1,2}|t?q?[f,s]|)!?)(,+|'+|)$``
        underlies this predicate.

        Return boolean.
        '''
        if not isinstance(expr, str):
            return False
        return bool(Pitch._pitch_name_regex.match(expr))

    @staticmethod
    def is_pitch_number(expr):
        '''True `expr` is a pitch number, otherwise false.

        ::

            >>> pitchtools.Pitch.is_pitch_number(13)
            True

        The pitch numbers are equal to the set of all integers in
        union with the set of all integers plus of minus ``0.5``.

        Return boolean.
        '''
        if isinstance(expr, (int, long, float)):
            return expr % 0.5 == 0
        return False

    @abc.abstractmethod
    def multiply(self, n=1):
        raise NotImplementedError

    @abc.abstractmethod
    def transpose(self, expr):
        raise NotImplementedError

    ### PUBLIC PROPERTIES ###

    @abc.abstractproperty
    def accidental(self):
        r'''Accidental.'''
        raise NotImplementedError

    @property
    def accidental_spelling(self):
        r'''Accidental spelling.

        ::

            >>> pitchtools.NamedPitch("c").accidental_spelling
            'mixed'

        Return string.
        '''
        from abjad import abjad_configuration
        return abjad_configuration['accidental_spelling']

    @abc.abstractproperty
    def alteration_in_semitones(self):
        r'''Alteration in semitones.'''
        raise NotImplementedError

    @abc.abstractproperty
    def diatonic_pitch_class_name(self):
        r'''Diatonic pitch-class name.'''
        raise NotImplementedError

    @abc.abstractproperty
    def diatonic_pitch_class_number(self):
        r'''Diatonic pitch-class number.'''
        raise NotImplementedError

    @abc.abstractproperty
    def diatonic_pitch_name(self):
        r'''Diatonic pitch name.'''
        raise NotImplementedError

    @abc.abstractproperty
    def diatonic_pitch_number(self):
        r'''Diatonic pitch number.'''
        raise NotImplementedError

    @abc.abstractproperty
    def lilypond_format(self):
        r'''LilyPond input format.'''
        raise NotImplementedError

    @abc.abstractproperty
    def named_pitch(self):
        r'''Named pitch.'''
        raise NotImplementedError

    @abc.abstractproperty
    def named_pitch_class(self):
        r'''Named pitch-class.'''
        raise NotImplementedError

    @abc.abstractproperty
    def numbered_pitch(self):
        r'''Numbered pitch.'''
        raise NotImplementedError

    @abc.abstractproperty
    def numbered_pitch_class(self):
        r'''Numbered pitch-class.'''
        raise NotImplementedError

    @abc.abstractproperty
    def octave_indication(self):
        r'''Octave indication.'''
        raise NotImplementedError

    @abc.abstractproperty
    def octave_number(self):
        r'''Octave number.'''
        raise NotImplementedError

    @abc.abstractproperty
    def pitch_class_name(self):
        r'''Pitch-class name.'''
        raise NotImplementedError

    @abc.abstractproperty
    def pitch_class_number(self):
        r'''Pitch-class number.'''
        raise NotImplementedError

    @abc.abstractproperty
    def pitch_class_octave_label(self):
        r'''Pitch-class / octave label.'''
        raise NotImplementedError

    @abc.abstractproperty
    def pitch_name(self):
        r'''Pitch name.'''
        raise NotImplementedError

    @abc.abstractproperty
    def pitch_number(self):
        r'''Pitch number.'''
        raise NotImplementedError
