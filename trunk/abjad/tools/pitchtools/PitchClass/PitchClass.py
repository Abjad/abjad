# -*- encoding: utf-8 -*-
import abc
import re
from abjad.tools.abctools import AbjadObject
from abjad.tools.pitchtools.Accidental import Accidental


class PitchClass(AbjadObject):
    '''Pitch-class base class.
    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    _diatonic_pitch_class_name_regex_body = '''
        ([a-g,A-G]) # exactly one lowercase a - g or uppercase A - G
        '''

    _diatonic_pitch_class_name_regex = re.compile(
        '^{}$'.format(_diatonic_pitch_class_name_regex_body),
        re.VERBOSE,
        )

    _diatonic_pitch_class_name_to_diatonic_pitch_class_number = {
        'c': 0,
        'd': 1,
        'e': 2,
        'f': 3,
        'g': 4,
        'a': 5,
        'b': 6,
        }

    _diatonic_pitch_class_name_to_pitch_class_number = {
        'c': 0,
        'd': 2,
        'e': 4,
        'f': 5,
        'g': 7,
        'a': 9,
        'b': 11,
        }

    _diatonic_pitch_class_number_to_diatonic_pitch_class_name = {
        0: 'c',
        1: 'd',
        2: 'e',
        3: 'f',
        4: 'g',
        5: 'a',
        6: 'b',
        }

    _diatonic_pitch_class_number_to_pitch_class_number = {
        0: 0,
        1: 2,
        2: 4,
        3: 5,
        4: 7,
        5: 9,
        6: 11,
        }

    _pitch_class_name_regex_body = '''
        {}          # exactly one diatonic pitch-class name
        {}          # followed by exactly one alphabetic accidental name
        '''.format(
        _diatonic_pitch_class_name_regex_body,
        Accidental._alphabetic_accidental_regex_body,
        )

    _pitch_class_name_regex = re.compile(
        '^{}$'.format(_pitch_class_name_regex_body),
        re.VERBOSE,
        )

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self):
        pass

    ### SPECIAL METHODS ###

    def __hash__(self):
        return hash(repr(self))

    ### PRIVATE METHODS ###

    # do not indent in storage
    def _get_tools_package_qualified_repr_pieces(self, is_indented=True):
        from abjad.tools import abctools
        return [''.join(
            abctools.AbjadObject._get_tools_package_qualified_repr_pieces(
                self, is_indented=False))]

    ### PUBLIC METHODS ###

    @staticmethod
    def is_diatonic_pitch_class_name(expr):
        '''True when `expr` is a diatonic pitch-class name. Otherwise false:

        ::

            >>> pitchtools.PitchClass.is_diatonic_pitch_class_name('c')
            True

        The regex ``^[a-g,A-G]$`` underlies this predicate.

        Return boolean.
        '''
        if not isinstance(expr, str):
            return False
        return bool(PitchClass._diatonic_pitch_class_name_regex.match(expr))

    @staticmethod
    def is_diatonic_pitch_class_number(expr):
        '''True when `expr` is a diatonic pitch-class number. Otherwise false:

        ::

            >>> pitchtools.PitchClass.is_diatonic_pitch_class_number(0)
            True

        ::

            >>> pitchtools.PitchClass.is_diatonic_pitch_class_number(-5)
            False

        The diatonic pitch-class numbers are equal to the set
        ``[0, 1, 2, 3, 4, 5, 6]``.

        Return boolean.
        '''
        if expr in range(7):
            return True
        return False
