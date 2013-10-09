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

    __slots__ = ()

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self):
        pass

    ### SPECIAL METHODS ###

    def __abs__(self):
        raise NotImplementedError(
            'TODO: all pitch-related classes must implement abs.')

    def __float__(self):
        raise NotImplementedError(
            'TODO: all pitch-related classes must implement float.')

    def __hash__(self):
        return hash(repr(self))

    def __int__(self):
        raise NotImplementedError(
            'TODO: all pitch-related classes must implement int.')

    def __repr__(self):
        return '%s(%s)' % (self._class_name, self._format_string)

    ### PRIVATE METHODS ###

    # do not indent in storage
    def _get_tools_package_qualified_repr_pieces(self, is_indented=True):
        from abjad.tools import abctools
        return [''.join(
            abctools.AbjadObject._get_tools_package_qualified_repr_pieces(
                self, is_indented=False))]

    ### PUBLIC METHODS ###

    @staticmethod
    def is_diatonic_pitch_name(expr):
        '''True when `expr` is a diatonic pitch name. Otherwise false:

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
        '''True when `expr` is a diatonic pitch number. Otherwise false:

        ::

            >>> pitchtools.Pitch.is_diatonic_pitch_number(7)
            True

        The diatonic pitch numbers are equal to the set of integers.

        Return boolean.
        '''
        return isinstance(expr, (int, long))

    @staticmethod
    def is_pitch_name(expr):
        '''True `expr` is a chromatic pitch name. Otherwise false:

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
        '''True `expr` is a chromatic pitch number. Otherwise false:

        ::

            >>> pitchtools.Pitch.is_pitch_number(13)
            True

        The chromatic pitch numbers are equal to the set of all integers in
        union with the set of all integers plus of minus ``0.5``.

        Return boolean.
        '''
        if isinstance(expr, (int, long, float)):
            return expr % 0.5 == 0
        return False

    ### PUBLIC PROPERTIES ###

#    @abc.abstractproperty
#    def diatonic_pitch_class_name(self):
#        raise NotImplementedError
#
#    @abc.abstractproperty
#    def diatonic_pitch_class_number(self):
#        raise NotImplementedError
#
#    @abc.abstractproperty
#    def diatonic_pitch_name(self):
#        raise NotImplementedError
#
#    @abc.abstractproperty
#    def diatonic_pitch_number(self):
#        raise NotImplementedError
#
#    @abc.abstractproperty
#    def octave_indication(self):
#        raise NotImplementedError
#
#    @abc.abstractproperty
#    def pitch_class_name(self):
#        raise NotImplementedError
#
#    @abc.abstractproperty
#    def pitch_class_number(self):
#        raise NotImplementedError
#
#    @abc.abstractproperty
#    def pitch_name(self):
#        raise NotImplementedError
#
#    @abc.abstractproperty
#    def pitch_number(self):
#        raise NotImplementedError
