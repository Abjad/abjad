# -*- coding: utf-8 -*-
import re
from abjad.tools import systemtools
from abjad.tools.abctools import AbjadValueObject


class Accidental(AbjadValueObject):
    '''Accidental.

    ..  container:: example

        **Example 1.** Sharp:

        ::

            >>> pitchtools.Accidental('s')
            Accidental('s')

    ..  container:: example

        **Example 2.** Quarter-sharp:

        ::

            >>> pitchtools.Accidental('qs')
            Accidental('qs')

    Accidentals are immutable.
    '''

    ### CLASS VARIABLES ###

    _abbreviation_to_name = {
        'ss': 'double sharp',
        'tqs': 'three-quarters sharp',
        's': 'sharp',
        'qs': 'quarter-sharp',
        '': 'natural',
        '!': 'forced natural',
        'qf': 'quarter-flat',
        'f': 'flat',
        'tqf': 'three-quarters flat',
        'ff': 'double flat',
        }

    _abbreviation_to_semitones = {
        'ff': -2,
        'tqf': -1.5,
        'f': -1,
        'qf': -0.5,
        '': 0,
        '!': 0,
        'qs': 0.5,
        's': 1,
        'tqs': 1.5,
        'ss': 2,
        }

    _abbreviation_to_symbolic_string = {
        'ff': 'bb',
        'tqf': 'b~',
        'f': 'b',
        'qf': '~',
        '': '',
        '!': '!',
        'qs': '+',
        's': '#',
        'tqs': '#+',
        'ss': '##',
        }

    _alphabetic_accidental_regex_body = """
        ([s]{1,2}   # s or ss for sharp or double sharp
        |[f]{1,2}   # or f or ff for flat or double flat
        |t?q?[fs]   # or qs, qf, tqs, tqf for quartertone accidentals
        |           # or empty string for no natural
        )!?         # plus optional ! for forced printing of accidental
        """

    _alphabetic_accidental_regex = re.compile(
        '^{}$'.format(_alphabetic_accidental_regex_body),
        re.VERBOSE,
        )

    _name_to_abbreviation = {
        'double sharp': 'ss',
        'three-quarters sharp': 'tqs',
        'sharp': 's',
        'quarter sharp': 'qs',
        'natural': '',
        'forced natural': '!',
        'quarter flat': 'qf',
        'flat': 'f',
        'three-quarters flat': 'tqf',
        'double flat':  'ff',
    }

    _semitones_to_abbreviation = {
        -2: 'ff',
        -1.5: 'tqf',
        -1: 'f',
        -0.5: 'qf',
        0: '',
        0.5: 'qs',
        1: 's',
        1.5: 'tqs',
        2: 'ss',
    }

    _symbolic_string_regex_body = '''
        ([#]{1,2}   # # or ## for sharp or double sharp
        |[b]{1,2}   # or b or bb for flat or double flat
        |[#]?[+]    # or + or #+ for qs and tqs
        |[b]?[~]    # or ~ and b~ for qf and tqf
        |           # or empty string for no symbolic string
        )
        '''

    _symbolic_string_regex = re.compile(
        '^{}$'.format(_symbolic_string_regex_body),
        re.VERBOSE,
        )

    _symbolic_string_to_abbreviation = {
        'bb': 'ff',
        'b~': 'tqf',
        'b': 'f',
        '~': 'qf',
        '': '',
        '!': '!',
        '+': 'qs',
        '#': 's',
        '#+': 'tqs',
        '##': 'ss',
        }

    _symbolic_string_to_semitones = {
        'bb': -2,
        'b~': -1.5,
        'b': -1,
        '~': -0.5,
        '': 0,
        '+': 0.5,
        '#': 1,
        '#+': 1.5,
        '##': 2,
        }

    __slots__ = (
        '_abbreviation',
        '_is_adjusted',
        '_name',
        '_semitones',
        '_symbolic_string',
        )

    ### INITIALIZER ##

    def __init__(self, arg=''):
        # initialize symbolic string from arg
        if self.is_abbreviation(arg):
            _abbreviation = arg
        elif self.is_symbolic_string(arg):
            _abbreviation = \
                self._symbolic_string_to_abbreviation[
                    arg]
        elif arg in self._all_accidental_names:
            _abbreviation = \
                self._name_to_abbreviation[arg]
        elif arg in self._all_accidental_semitone_values:
            _abbreviation = \
                self._semitones_to_abbreviation[arg]
        elif isinstance(arg, type(self)):
            _abbreviation = \
                arg.abbreviation
        elif isinstance(arg, type(None)):
            _abbreviation = ''
        else:
            message = 'can not initialize accidental from value: %s'
            raise ValueError(message % arg)
        self._abbreviation = \
            _abbreviation
        # initialize derived attributes
        _semitones = self._abbreviation_to_semitones[
            self.abbreviation]
        self._semitones = _semitones
        _name = self._abbreviation_to_name[
            self.abbreviation]
        self._name = _name
        _is_adjusted = not self.semitones == 0
        self._is_adjusted = _is_adjusted
        _symbolic_string = \
            self._abbreviation_to_symbolic_string[
                self.abbreviation]
        self._symbolic_string = _symbolic_string

    ### SPECIAL METHODS ###

    def __add__(self, arg):
        r'''Adds `arg` to accidental.

        Returns new accidental.
        '''
        if not isinstance(arg, type(self)):
            message = 'can only add accidental to other accidental.'
            raise TypeError(message)
        semitones = self.semitones + arg.semitones
        return type(self)(semitones)

    def __ge__(self, arg):
        r'''Is true when `arg` is an accidental with semitones less than or equal
        to those of this accidental. Otherwise false.

        Returns true or false.
        '''
        return self.semitones >= arg.semitones

    def __gt__(self, arg):
        r'''Is true when `arg` is an accidental with semitones less than
        those of this accidental. Otherwise false.

        Returns true or false.
        '''
        return self.semitones > arg.semitones

    def __le__(self, arg):
        r'''Is true when `arg` is an accidental with semitones greater than or
        equal to those of this accidental. Otherwise false.

        Returns true or false.
        '''
        return self.semitones <= arg.semitones

    def __lt__(self, arg):
        r'''Is true when `arg` is an accidental with semitones greater than those
        of this accidental. Otherwise false.

        Returns true or false.
        '''
        return self.semitones < arg.semitones

    def __ne__(self, arg):
        r'''Is true when accidental does not equal `arg`. Otherwise false.

        Returns true or false.
        '''
        return not self == arg

    def __neg__(self):
        r'''Negates accidental.

        Returns new accidental.
        '''
        return type(self)(-self.semitones)

    def __nonzero__(self):
        r'''Defined equal to true.

        Returns true.
        '''
        return True

    def __str__(self):
        r'''String representation of accidental.

        Returns string.
        '''
        return self.abbreviation

    def __sub__(self, arg):
        r'''Subtracts `arg` from accidental.

        Returns new accidental.
        '''
        if not isinstance(arg, type(self)):
            message = 'can only subtract accidental from other accidental.'
            raise TypeError(message)
        semitones = self.semitones - arg.semitones
        return type(self)(semitones)

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        return systemtools.FormatSpecification(
            client=self,
            repr_is_indented=False,
            storage_format_args_values=[self.abbreviation],
            storage_format_is_indented=False,
            storage_format_kwargs_names=[],
            template_names=['abbreviation'],
            )

    ### PUBLIC METHODS ###

    @staticmethod
    def is_abbreviation(expr):
        '''Is true when `expr` is an alphabetic accidental abbrevation. Otherwise
        false:

        ::

            >>> pitchtools.Accidental.is_abbreviation('tqs')
            True

        The regex ``^([s]{1,2}|[f]{1,2}|t?q?[fs])!?$`` underlies this
        predicate.

        Returns true or false.
        '''
        if not isinstance(expr, str):
            return False
        return bool(Accidental._alphabetic_accidental_regex.match(expr))

    @staticmethod
    def is_symbolic_string(expr):
        '''Is true when `expr` is a symbolic accidental string. Otherwise false:

        ::

            >>> pitchtools.Accidental.is_symbolic_string('#+')
            True

        True on empty string.

        The regex ``^([#]{1,2}|[b]{1,2}|[#]?[+]|[b]?[~]|)$`` underlies this
        predicate.

        Returns true or false.
        '''
        if not isinstance(expr, str):
            return False
        return bool(Accidental._symbolic_string_regex.match(expr))

    ### PRIVATE PROPERTIES ###

    @property
    def _all_accidental_abbreviations(self):
        return list(self._abbreviation_to_symbolic_string.keys())

    @property
    def _all_accidental_names(self):
        return list(self._name_to_abbreviation.keys())

    @property
    def _all_accidental_semitone_values(self):
        return list(self._semitones_to_abbreviation.keys())

    @property
    def _lilypond_format(self):
        return self._abbreviation

    ### PUBLIC PROPERTIES ###

    @property
    def abbreviation(self):
        r'''Abbreviation of accidental.

        ::

            >>> accidental = pitchtools.Accidental('s')
            >>> accidental.abbreviation
            's'

        Returns string.
        '''
        return self._abbreviation

    @property
    def is_adjusted(self):
        r'''True for all accidentals equal to a nonzero number of semitones.
        Otherwise false:

        ::

            >>> accidental = pitchtools.Accidental('s')
            >>> accidental.is_adjusted
            True

        Returns true or false.
        '''
        return self._is_adjusted

    @property
    def name(self):
        r'''Name of accidental.

        ::

            >>> accidental = pitchtools.Accidental('s')
            >>> accidental.name
            'sharp'

        Returns string.
        '''
        return self._name

    @property
    def semitones(self):
        r'''Semitones of accidental.

        ::

            >>> accidental = pitchtools.Accidental('s')
            >>> accidental.semitones
            1

        Returns number.
        '''
        return self._semitones

    @property
    def symbolic_string(self):
        r'''Symbolic string of accidental.

        ::

            >>> accidental = pitchtools.Accidental('s')
            >>> accidental.symbolic_string
            '#'

        Returns string.
        '''
        return self._symbolic_string
