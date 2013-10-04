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
