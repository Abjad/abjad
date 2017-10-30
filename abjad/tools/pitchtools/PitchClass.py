import abc
import functools
import re
from abjad.tools.abctools import AbjadValueObject
from abjad.tools.pitchtools.Accidental import Accidental


@functools.total_ordering
class PitchClass(AbjadValueObject):
    '''Abstract pitch-class.
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

    _pitch_class_number_to_diatonic_pitch_class_number = {
        0: 0,
        2: 1,
        4: 2,
        5: 3,
        7: 4,
        9: 5,
        11: 6,
        }

    _pitch_class_number_to_pitch_class_name = {
        0:    'c',
        0.5:  'cqs',
        1:    'cs',
        1.5:  'dqf',
        2:    'd',
        2.5:  'dqs',
        3:    'ef',
        3.5:  'eqf',
        4:    'e',
        4.5:  'eqs',
        5:    'f',
        5.5:  'fqs',
        6:    'fs',
        6.5:  'gqf',
        7:    'g',
        7.5:  'gqs',
        8:    'af',
        8.5:  'aqf',
        9:    'a',
        9.5:  'aqs',
        10:   'bf',
        10.5: 'bqf',
        11:   'b',
        11.5: 'bqs',
        }

    _pitch_class_number_to_pitch_class_name_with_flats = {
        0:    'c',
        0.5:  'dtqf',
        1:    'df',
        1.5:  'dqf',
        2:    'd',
        2.5:  'etqf',
        3:    'ef',
        3.5:  'eqf',
        4:    'e',
        4.5:  'fqf',
        5:    'f',
        5.5:  'gtqf',
        6:    'gf',
        6.5:  'gqf',
        7:    'g',
        7.5:  'atqf',
        8:    'af',
        8.5:  'aqf',
        9:    'a',
        9.5:  'btqf',
        10:   'bf',
        10.5: 'bqf',
        11:   'b',
        11.5: 'cqf',
        }

    _pitch_class_number_to_pitch_class_name_with_sharps = {
        0:    'c',
        0.5:  'cqs',
        1:    'cs',
        1.5:  'ctqs',
        2:    'd',
        2.5:  'dqs',
        3:    'ds',
        3.5:  'dtqs',
        4:    'e',
        4.5:  'eqs',
        5:    'f',
        5.5:  'fqs',
        6:    'fs',
        6.5:  'ftqs',
        7:    'g',
        7.5:  'gqs',
        8:    'gs',
        8.5:  'gtqs',
        9:    'a',
        9.5:  'aqs',
        10:   'as',
        10.5: 'atqs',
        11:   'b',
        11.5: 'bqs',
        }

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
        r'''Formats pitch-class.

        Set `format_specification` to `''`, `'lilypond'` or `'storage'`.

        Returns string.
        '''
        return super(PitchClass, self).__format__(
            format_specification=format_specification
            )

    @abc.abstractmethod
    def __lt__(self, argument):
        r'''Is true when pitch-class is less than `argument`.

        Returns true or false.
        '''
        raise NotImplementedError

    ### PUBLIC PROPERTIES ###

    @abc.abstractproperty
    def accidental(self):
        r'''Gets accidental of pitch-class.
        '''
        raise NotImplementedError

    @abc.abstractproperty
    def pitch_class_label(self):
        r'''Gets pitch-class label of pitch-class.
        '''
        raise NotImplementedError

    ### PUBLIC METHODS ###

    @abc.abstractmethod
    def invert(self, axis=None):
        r'''Inverts pitch-class about `axis`.

        Returns new pitch-class.
        '''
        raise NotImplementedError

    # TODO: make private
    @staticmethod
    def is_diatonic_pitch_class_name(argument):
        '''Is true when `argument` is a diatonic pitch-class name.
        Otherwise false.

        ..  container:: example

            >>> abjad.PitchClass.is_diatonic_pitch_class_name('g')
            True

            >>> abjad.PitchClass.is_diatonic_pitch_class_name('G')
            True

            >>> abjad.PitchClass.is_diatonic_pitch_class_name('Allegro')
            False

        The regex ``^[a-g,A-G]$`` underlies this predicate.

        Returns true or false.
        '''
        if not isinstance(argument, str):
            return False
        return bool(PitchClass._diatonic_pitch_class_name_regex.match(argument))

    # TODO: make private
    @staticmethod
    def is_diatonic_pitch_class_number(argument):
        '''Is true when `argument` is a diatonic pitch-class number.
        Otherwise false.

        ..  container:: example

            >>> abjad.PitchClass.is_diatonic_pitch_class_number(0)
            True

            >>> abjad.PitchClass.is_diatonic_pitch_class_number(-5)
            False

        The diatonic pitch-class numbers are equal to the set
        ``[0, 1, 2, 3, 4, 5, 6]``.

        Returns true or false.
        '''
        if argument in range(7):
            return True
        return False

    # TODO: make private
    @staticmethod
    def is_pitch_class_name(argument):
        '''Is true when `argument` is a pitch-class name. Otherwise false.

        ..  container:: example

            >>> abjad.PitchClass.is_pitch_class_name('fs')
            True

            >>> abjad.PitchClass.is_pitch_class_name('fqs')
            True

            >>> abjad.PitchClass.is_pitch_class_name('f,,')
            False

        The regex ``^([a-g,A-G])(([s]{1,2}|[f]{1,2}|t?q?[fs]|)!?)$`` underlies
        this predicate.

        Returns true or false.
        '''
        if not isinstance(argument, str):
            return False
        return bool(PitchClass._pitch_class_name_regex.match(argument))

    # TODO: make private
    @staticmethod
    def is_pitch_class_number(argument):
        '''Is true when `argument` is a pitch-class number. Otherwise false.

        ..  container:: example

            >>> abjad.PitchClass.is_pitch_class_number(1)
            True

            >>> abjad.PitchClass.is_pitch_class_number(1.5)
            True

            >>> abjad.PitchClass.is_pitch_class_number(12)
            False

        The pitch-class numbers are equal to the set
        ``[0, 0.5, ..., 11, 11.5]``.

        Returns true or false.
        '''
        return argument in [(n).__truediv__(2) for n in range(24)]

    @abc.abstractmethod
    def multiply(self, n=1):
        r'''Multiplies pitch-class by `n`.

        Returns new pitch-class.
        '''
        raise NotImplementedError

    @abc.abstractmethod
    def transpose(self, n=0):
        r'''Transposes pitch-class by index `n`.

        Returns new pitch-class.
        '''
        raise NotImplementedError
