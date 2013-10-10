# -*- encoding: utf-8 -*-
import re
from abjad.tools.abctools import AbjadObject


class Accidental(AbjadObject):
    '''Abjad model of the accidental:

    ::

        >>> pitchtools.Accidental('s')
        Accidental('s')

    Accidentals are immutable.
    '''

    ### CLASS VARIABLES ###

    _alphabetic_accidental_abbreviation_to_name = {
        'ss'  : 'double sharp',
        'tqs' : 'three-quarters sharp',
        's'   : 'sharp',
        'qs'  : 'quarter-sharp',
        ''    : 'natural',
        '!'   : 'forced natural',
        'qf'  : 'quarter-flat',
        'f'   : 'flat',
        'tqf' : 'three-quarters flat',
        'ff'  : 'double flat',
    }

    _alphabetic_accidental_abbreviation_to_semitones = {
        'ff'  : -2,
        'tqf' : -1.5,
        'f'   : -1,
        'qf'  : -0.5,
        ''    : 0,
        '!'   : 0,
        'qs'  : 0.5,
        's'   : 1,
        'tqs' : 1.5,
        'ss'  : 2,
    }

    _alphabetic_accidental_abbreviation_to_symbolic_accidental_string = {
        'ff'  : 'bb',
        'tqf' : 'b~',
        'f'   : 'b',
        'qf'  : '~',
        ''    : '',
        '!'   : '!',
        'qs'  : '+',
        's'   : '#',
        'tqs' : '#+',
        'ss'  : '##',
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

    _name_to_alphabetic_accidental_abbreviation = {
        'double sharp'            : 'ss',
        'three-quarters sharp'    : 'tqs',
        'sharp'                   : 's',
        'quarter sharp'           : 'qs',
        'natural'                 : '',
        'forced natural'          : '!',
        'quarter flat'            : 'qf',
        'flat'                    : 'f',
        'three-quarters flat'     : 'tqf',
        'double flat'             :  'ff',
    }

    _semitones_to_alphabetic_accidental_abbreviation = {
        -2   : 'ff',
        -1.5 : 'tqf',
        -1   : 'f',
        -0.5 : 'qf',
        0    : '',
        0.5  : 'qs',
        1    : 's',
        1.5  : 'tqs',
        2    : 'ss',
    }

    _symbolic_accidental_string_regex_body = '''
        ([#]{1,2}   # # or ## for sharp or double sharp
        |[b]{1,2}   # or b or bb for flat or double flat
        |[#]?[+]    # or + or #+ for qs and tqs
        |[b]?[~]    # or ~ and b~ for qf and tqf
        |           # or empty string for no symbolic string
        )
        '''

    _symbolic_accidental_string_regex = re.compile(
        '^{}$'.format(_symbolic_accidental_string_regex_body),
        re.VERBOSE,
        )

    _symbolic_accidental_string_to_alphabetic_accidental_abbreviation = {
        'bb' : 'ff',
        'b~' : 'tqf',
        'b'  : 'f',
        '~'  : 'qf',
        ''   : '',
        '!'  : '!',
        '+'  : 'qs',
        '#'  : 's',
        '#+' : 'tqs',
        '##' : 'ss',
        }

    _symbolic_accidental_string_to_semitones = {
        'bb' : -2,
        'b~' : -1.5,
        'b'  : -1,
        '~'  : -0.5,
        ''   : 0,
        '+'  : 0.5,
        '#'  : 1,
        '#+' : 1.5,
        '##' : 2,
        }

    __slots__ = (
        '_alphabetic_accidental_abbreviation',
        '_is_adjusted',
        '_name',
        '_semitones',
        '_symbolic_accidental_string',
        )

    ### INITIALIZER ##

    def __init__(self, arg=''):
        from abjad.tools import pitchtools
        # initialize symbolic string from arg
        if self.is_alphabetic_accidental_abbreviation(arg):
            _alphabetic_accidental_abbreviation = arg
        elif self.is_symbolic_accidental_string(arg):
            _alphabetic_accidental_abbreviation = \
                self._symbolic_accidental_string_to_alphabetic_accidental_abbreviation[
                    arg]
        elif arg in self._all_accidental_names:
            _alphabetic_accidental_abbreviation = \
                self._name_to_alphabetic_accidental_abbreviation[arg]
        elif arg in self._all_accidental_semitone_values:
            _alphabetic_accidental_abbreviation = \
                self._semitones_to_alphabetic_accidental_abbreviation[arg]
        elif isinstance(arg, type(self)):
            _alphabetic_accidental_abbreviation = \
                arg.alphabetic_accidental_abbreviation
        elif isinstance(arg, type(None)):
            _alphabetic_accidental_abbreviation = ''
        else:
            message = 'can not initialize accidental from value: %s'
            raise ValueError(message % arg)
        self._alphabetic_accidental_abbreviation = \
            _alphabetic_accidental_abbreviation
        # initialize derived attributes
        _semitones = self._alphabetic_accidental_abbreviation_to_semitones[
            self.alphabetic_accidental_abbreviation]
        self._semitones = _semitones
        _name = self._alphabetic_accidental_abbreviation_to_name[
            self.alphabetic_accidental_abbreviation]
        self._name = _name
        _is_adjusted = not self.semitones == 0
        self._is_adjusted = _is_adjusted
        _symbolic_accidental_string = \
            self._alphabetic_accidental_abbreviation_to_symbolic_accidental_string[
                self.alphabetic_accidental_abbreviation]
        self._symbolic_accidental_string = _symbolic_accidental_string

    ### SPECIAL METHODS ###

    def __add__(self, arg):
        if not isinstance(arg, type(self)):
            raise TypeError('can only add accidental to other accidental.')
        semitones = self.semitones + arg.semitones
        return type(self)(semitones)

    def __eq__(self, arg):
        if isinstance(arg, type(self)):
            if self.alphabetic_accidental_abbreviation == \
                arg.alphabetic_accidental_abbreviation:
                return True
        return False

    def __ge__(self, arg):
        return self.semitones >= arg.semitones

    def __getnewargs__(self):
        return (self.alphabetic_accidental_abbreviation,)

    def __gt__(self, arg):
        return self.semitones > arg.semitones

    def __le__(self, arg):
        return self.semitones <= arg.semitones

    def __lt__(self, arg):
        return self.semitones < arg.semitones

    def __ne__(self, arg):
        return not self == arg

    def __neg__(self):
        return type(self)(-self.semitones)

    def __nonzero__(self):
        return True

    def __repr__(self):
        return "%s('%s')" % (
            self._class_name, self.alphabetic_accidental_abbreviation)

    def __str__(self):
        return self.alphabetic_accidental_abbreviation

    def __sub__(self, arg):
        if not isinstance(arg, type(self)):
            raise TypeError('can only sub accidental from other accidental.')
        semitones = self.semitones - arg.semitones
        return type(self)(semitones)

    ### PRIVATE PROPERTIES ###

    @property
    def _all_accidental_alphabetic_accidental_abbreviations(self):
        return self._alphabetic_accidental_abbreviation_to_symbolic_accidental_string.keys()

    @property
    def _all_accidental_names(self):
        return self._name_to_alphabetic_accidental_abbreviation.keys()

    @property
    def _all_accidental_semitone_values(self):
        return self._semitones_to_alphabetic_accidental_abbreviation.keys()

    ### PUBLIC METHODS ###

    @staticmethod
    def is_alphabetic_accidental_abbreviation(expr):
        '''True when `expr` is an alphabetic accidental abbrevation. Otherwise
        false:

        ::

            >>> pitchtools.Accidental.is_alphabetic_accidental_abbreviation('tqs')
            True

        The regex ``^([s]{1,2}|[f]{1,2}|t?q?[fs])!?$`` underlies this
        predicate.

        Return boolean.
        '''
        if not isinstance(expr, str):
            return False
        return bool(Accidental._alphabetic_accidental_regex.match(expr))

    @staticmethod
    def is_symbolic_accidental_string(expr):
        '''True when `expr` is a symbolic accidental string. Otherwise false:

        ::

            >>> pitchtools.Accidental.is_symbolic_accidental_string('#+')
            True

        True on empty string.

        The regex ``^([#]{1,2}|[b]{1,2}|[#]?[+]|[b]?[~]|)$`` underlies this
        predicate.

        Return boolean.
        '''
        if not isinstance(expr, str):
            return False
        return bool(Accidental._symbolic_accidental_string_regex.match(expr))

    ### PUBLIC PROPERTIES ###

    @property
    def alphabetic_accidental_abbreviation(self):
        r'''Alphabetic string:

        ::

            >>> accidental = pitchtools.Accidental('s')
            >>> accidental.alphabetic_accidental_abbreviation
            's'

        Return string.
        '''
        return self._alphabetic_accidental_abbreviation

    @property
    def is_adjusted(self):
        r'''True for all accidentals equal to a nonzero number of semitones.
        False otherwise:

        ::

            >>> accidental = pitchtools.Accidental('s')
            >>> accidental.is_adjusted
            True

        Return boolean.
        '''
        return self._is_adjusted

    @property
    def lilypond_format(self):
        r'''LilyPond input format of accidental:

        ::

            >>> accidental = pitchtools.Accidental('s')
            >>> accidental.lilypond_format
            's'

        Return string.
        '''
        return self._alphabetic_accidental_abbreviation

    @property
    def name(self):
        r'''Name of accidental:

        ::

            >>> accidental = pitchtools.Accidental('s')
            >>> accidental.name
            'sharp'

        Return string.
        '''
        return self._name

    @property
    def semitones(self):
        r'''Semitones of accidental:

        ::

            >>> accidental = pitchtools.Accidental('s')
            >>> accidental.semitones
            1

        Return number.
        '''
        return self._semitones

    @property
    def symbolic_accidental_string(self):
        r'''Symbolic string of accidental:

        ::

            >>> accidental = pitchtools.Accidental('s')
            >>> accidental.symbolic_accidental_string
            '#'

        Return string.
        '''
        return self._symbolic_accidental_string
