# -*- coding: utf-8 -*-
import re
from abjad.tools import mathtools
from abjad.tools import systemtools
from abjad.tools.abctools import AbjadValueObject


class Accidental(AbjadValueObject):
    '''Accidental.

    ..  container:: example

        Sharp:

        ::

            >>> pitchtools.Accidental('s')
            Accidental('s')

    ..  container:: example

        Quarter-sharp:

        ::

            >>> pitchtools.Accidental('qs')
            Accidental('qs')

    ..  container:: example

        Three-quarters-flat:

        ::

            >>> pitchtools.Accidental('tqf')
            Accidental('tqf')

    ..  container:: example

        Three-quarters-sharp:

        ::

            >>> pitchtools.Accidental('#+')
            Accidental('tqs')

    ..  container:: example

        Flat:

        ::

            >>> pitchtools.Accidental('flat')
            Accidental('f')

    ..  container:: example

        Double-sharp:

        ::

            >>> pitchtools.Accidental(2)
            Accidental('ss')

    ..  container:: example

        Four-and-a-half-sharps:

        ::

            >>> pitchtools.Accidental('ssssqs')
            Accidental('ssssqs')

    '''

    ### CLASS VARIABLES ###

    _abbreviation_to_name = {
        'ss': 'double sharp',
        'tqs': 'three-quarters sharp',
        's': 'sharp',
        'qs': 'quarter-sharp',
        '': 'natural',
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
        'qs': '+',
        's': '#',
        'tqs': '#+',
        'ss': '##',
        }

    _alphabetic_accidental_regex_body = """
        (?P<alphabetic_accidental>
        [s]*(qs)?
        |[f]*(qf)?
        |t?q?[fs]
        |)
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
        'quarter flat': 'qf',
        'flat': 'f',
        'three-quarters flat': 'tqf',
        'double flat': 'ff',
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
        (?P<symbolic_string>
        [#]+[+]?
        |[b]+[~]?
        |[+]
        |[~]
        |
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
        '_semitones',
        )

    ### INITIALIZER ##

    def __init__(self, argument=None):
        if argument is None:
            semitones = 0
        elif isinstance(argument, str):
            semitones = 0
            if self.is_abbreviation(argument):
                if argument in self._abbreviation_to_semitones:
                    semitones = self._abbreviation_to_semitones[argument]
                else:
                    while argument and argument.startswith(('f', 's')):
                        if argument[0] == 's':
                            semitones += 1
                        else:
                            semitones -= 1
                        argument = argument[1:]
                    if argument == 'qs':
                        semitones += 0.5
                    elif argument == 'qf':
                        semitones -= 0.5
            elif self.is_symbolic_string(argument):
                if argument in self._symbolic_string_to_semitones:
                    semitones = self._symbolic_string_to_semitones[argument]
                else:
                    while argument and argument.startswith(('b', '#')):
                        if argument[0] == '#':
                            semitones += 1
                        else:
                            semitones -= 1
                        argument = argument[1:]
                    if argument == '+':
                        semitones += 0.5
                    elif argument == '~':
                        semitones -= 0.5
            elif argument in self._name_to_abbreviation:
                abbreviation = self._name_to_abbreviation[argument]
                semitones = self._abbreviation_to_semitones[abbreviation]
            else:
                message = 'can not initialize accidental from value: {!r}'
                message = message.format(argument)
                raise ValueError(message)
        elif isinstance(argument, type(self)):
            semitones = argument.semitones
        elif isinstance(argument, (int, float)):
            semitones = float(argument)
            assert (semitones % 1.) in (0., 0.5)
        elif hasattr(argument, 'accidental'):
            semitones = argument.accidental.semitones
        else:
            message = 'can not initialize accidental from value: {!r}'
            message = message.format(argument)
            raise ValueError(message)
        semitones = mathtools.integer_equivalent_number_to_integer(semitones)
        self._semitones = semitones

    ### SPECIAL METHODS ###

    def __add__(self, argument):
        r'''Adds `argument` to accidental.

        Returns new accidental.
        '''
        if not isinstance(argument, type(self)):
            message = 'can only add accidental to other accidental.'
            raise TypeError(message)
        semitones = self.semitones + argument.semitones
        return type(self)(semitones)

    def __ge__(self, argument):
        r'''Is true when `argument` is an accidental with semitones less than or equal
        to those of this accidental. Otherwise false.

        Returns true or false.
        '''
        return self.semitones >= argument.semitones

    def __gt__(self, argument):
        r'''Is true when `argument` is an accidental with semitones less than
        those of this accidental. Otherwise false.

        Returns true or false.
        '''
        return self.semitones > argument.semitones

    def __le__(self, argument):
        r'''Is true when `argument` is an accidental with semitones greater than or
        equal to those of this accidental. Otherwise false.

        Returns true or false.
        '''
        return self.semitones <= argument.semitones

    def __lt__(self, argument):
        r'''Is true when `argument` is an accidental with semitones greater than those
        of this accidental. Otherwise false.

        Returns true or false.
        '''
        return self.semitones < argument.semitones

    def __ne__(self, argument):
        r'''Is true when accidental does not equal `argument`. Otherwise false.

        Returns true or false.
        '''
        return not self == argument

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

    def __sub__(self, argument):
        r'''Subtracts `argument` from accidental.

        Returns new accidental.
        '''
        if not isinstance(argument, type(self)):
            message = 'can only subtract accidental from other accidental.'
            raise TypeError(message)
        semitones = self.semitones - argument.semitones
        return type(self)(semitones)

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

    def _get_lilypond_format(self):
        return self._abbreviation

    ### PUBLIC PROPERTIES ###

    @property
    def abbreviation(self):
        r'''Gets abbreviation of accidental.

        ..  container:: example

            ::

                >>> accidental = pitchtools.Accidental('s')
                >>> accidental.abbreviation
                's'

        Returns string.
        '''
        if self.semitones in self._semitones_to_abbreviation:
            return self._semitones_to_abbreviation[self.semitones]
        character = 's'
        if self.semitones < 0:
            character = 'f'
        semitones = abs(self.semitones)
        semitones, remainder = divmod(semitones, 1.0)
        abbreviation = character * int(semitones)
        if remainder:
            abbreviation += 'q{}'.format(character)
        return abbreviation

    @property
    def is_adjusted(self):
        r'''Is true for all accidentals equal to a nonzero number of semitones.
        Otherwise false.

        ..  container:: example

            ::

                >>> accidental = pitchtools.Accidental('s')
                >>> accidental.is_adjusted
                True

        Returns true or false.
        '''
        return self._semitones != 0

    @property
    def name(self):
        r'''Gets name of accidental.

        ..  container:: example

            ::

                >>> accidental = pitchtools.Accidental('s')
                >>> accidental.name
                'sharp'

        Returns string.
        '''
        abbreviation = self._semitones_to_abbreviation[self.semitones]
        name = self._abbreviation_to_name[abbreviation]
        return name

    @property
    def semitones(self):
        r'''Gets semitones of accidental.

        ..  container:: example

            ::

                >>> accidental = pitchtools.Accidental('s')
                >>> accidental.semitones
                1

        Returns number.
        '''
        return self._semitones

    @property
    def symbolic_string(self):
        r'''Gets symbolic string of accidental.

        ..  container:: example

            ::

                >>> accidental = pitchtools.Accidental('s')
                >>> accidental.symbolic_string
                '#'

        Returns string.
        '''
        abbreviation = self._semitones_to_abbreviation[self.semitones]
        symbolic_string = self._abbreviation_to_symbolic_string[abbreviation]
        return symbolic_string

    ### PUBLIC METHODS ###

    @staticmethod
    def is_abbreviation(argument):
        '''Is true when `argument` is an alphabetic accidental abbreviation.
        Otherwise false.

        ..  container:: example

            ::

                >>> pitchtools.Accidental.is_abbreviation('tqs')
                True

        The regex ``^([s]{1,2}|[f]{1,2}|t?q?[fs])!?$`` underlies this
        predicate.

        Returns true or false.
        '''
        if not isinstance(argument, str):
            return False
        return bool(Accidental._alphabetic_accidental_regex.match(argument))

    @staticmethod
    def is_symbolic_string(argument):
        '''Is true when `argument` is a symbolic accidental string.
        Otherwise false.

        ..  container:: example

            ::

                >>> pitchtools.Accidental.is_symbolic_string('#+')
                True

        Empty string returns true.

        The regex ``^([#]{1,2}|[b]{1,2}|[#]?[+]|[b]?[~]|)$`` underlies this
        predicate.

        Returns true or false.
        '''
        if not isinstance(argument, str):
            return False
        return bool(Accidental._symbolic_string_regex.match(argument))
