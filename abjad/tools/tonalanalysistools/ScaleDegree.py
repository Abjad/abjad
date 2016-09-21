# -*- coding: utf-8 -*-
import re
from abjad.tools import pitchtools
from abjad.tools import systemtools
from abjad.tools.abctools import AbjadObject


class ScaleDegree(AbjadObject):
    '''A diatonic scale degree such as 1, 2, 3, 4, 5, 6, 7 and
    also chromatic alterations including flat-2, flat-3, flat-6, etc.

    ::

        >>> scale_degree = tonalanalysistools.ScaleDegree('#4')
        >>> scale_degree
        ScaleDegree('sharp', 4)

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_accidental',
        '_number',
        )

    _numeral_to_number_name = {
        1: 'one',
        2: 'two',
        3: 'three',
        4: 'four',
        5: 'five',
        6: 'six',
        7: 'seven',
        8: 'eight',
        9: 'nine',
        10: 'ten',
        11: 'eleven',
        12: 'twelve',
        13: 'thirteen',
        14: 'fourteen',
        15: 'fifteen',
        }

    _roman_numeral_string_to_scale_degree_number = {
        'I': 1,
        'II': 2,
        'III': 3,
        'IV': 4,
        'V': 5,
        'VI': 6,
        'VII': 7,
        }

    _scale_degree_number_to_roman_numeral_string = {
        1: 'I',
        2: 'II',
        3: 'III',
        4: 'IV',
        5: 'V',
        6: 'VI',
        7: 'VII',
        }

    _scale_degree_number_to_scale_degree_name = {
        1: 'tonic',
        2: 'superdominant',
        3: 'mediant',
        4: 'subdominant',
        5: 'dominant',
        6: 'submediant',
        7: 'leading tone',
        }

    _symbolic_string_regex = re.compile(r'([#|b]*)([i|I|v|V|\d]+)')

    ### INITIALIZER ###

    def __init__(self, *args):
        if len(args) == 0:
            accidental, number = self._initialize_by_number(1)
        elif len(args) == 1 and isinstance(args[0], type(self)):
            accidental, number = self._initialize_by_scale_degree(*args)
        elif len(args) == 1 and args[0] in self._acceptable_numbers:
            accidental, number = self._initialize_by_number(*args)
        elif len(args) == 1 and isinstance(args[0], tuple):
            accidental, number = self._initialize_by_pair(*args)
        elif len(args) == 1 and isinstance(args[0], str):
            accidental, number = self._initialize_by_symbolic_string(*args)
        elif len(args) == 2 and args[1] in self._acceptable_numbers:
            accidental, number = \
                self._initialize_by_accidental_and_number(*args)
        else:
            arg_string = ', '.join([str(x) for x in args])
            message = 'can not initialize scale degree: {}.'
            raise ValueError(message.format(arg_string))
        self._accidental = accidental
        self._number = number

    ### SPECIAL METHODS ###

    def __eq__(self, arg):
        r'''Is true when `arg` is a scale degree with number and accidental equal
        to those of this scale degree.

        ::

            >>> scale_degree == tonalanalysistools.ScaleDegree('#4')
            True

        Otherwise false:

        ::

            >>> scale_degree == tonalanalysistools.ScaleDegree(4)
            False

        Returns true or false.
        '''
        if isinstance(arg, type(self)):
            if self.number == arg.number:
                if self.accidental == arg.accidental:
                    return True
        return False

    def __hash__(self):
        r'''Hashes scale degree.

        Required to be explicitly redefined on Python 3 if __eq__ changes.

        Returns integer.
        '''
        return super(ScaleDegree, self).__hash__()

    def __ne__(self, arg):
        r'''Is true when `arg` does not equal scale degree. Otherwise false.

        Returns true or false.
        '''
        return not self == arg

    def __repr__(self):
        r'''Gets interpreter representation of scale degree.

        ::

            >>> scale_degree
            ScaleDegree('sharp', 4)

        Returns string.
        '''
        return systemtools.StorageFormatAgent(self).get_repr_format()

    def __str__(self):
        r'''String representation of scale degree.

        ::

            >>> str(scale_degree)
            '#4'

        Returns string.
        '''
        return '{}{}'.format(
            self.accidental.symbolic_string, self.number)

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        values = [self.number]
        if self.accidental.is_adjusted:
            values = [self.accidental.name, self.number]
        return systemtools.FormatSpecification(
            client=self,
            repr_is_indented=False,
            storage_format_is_indented=False,
            storage_format_args_values=values,
            )

    def _initialize_by_accidental_and_number(self, accidental, number):
        accidental = pitchtools.Accidental(accidental)
        return accidental, number

    def _initialize_by_number(self, number):
        accidental = pitchtools.Accidental(None)
        return accidental, number

    def _initialize_by_pair(self, pair):
        accidental, number = pair
        return self._initialize_by_accidental_and_number(accidental, number)

    def _initialize_by_scale_degree(self, scale_degree):
        accidental = scale_degree.accidental
        number = scale_degree.number
        return self._initialize_by_accidental_and_number(accidental, number)

    def _initialize_by_symbolic_string(self, symbolic_string):
        groups = self._symbolic_string_regex.match(symbolic_string).groups()
        accidental, roman_numeral = groups
        accidental = pitchtools.Accidental(accidental)
        roman_numeral = roman_numeral.upper()
        try:
            number = self._roman_numeral_string_to_scale_degree_number[
                roman_numeral]
        except KeyError:
            number = int(roman_numeral)
        return accidental, number

    ### PUBLIC METHODS ###

    def apply_accidental(self, accidental):
        r'''Applies accidental to scale degree.

        ::

            >>> scale_degree.apply_accidental('ff')
            ScaleDegree('flat', 4)

        Returns new scale degree.
        '''
        accidental = pitchtools.Accidental(accidental)
        new_accidental = self.accidental + accidental
        return type(self)(new_accidental, self.number)

    ### PRIVATE PROPERTIES ###

    @property
    def _acceptable_numbers(self):
        return tuple(range(1, 16))

    ### PUBLIC PROPERTIES ###

    @property
    def accidental(self):
        r'''Accidental of scale degree.

        ::

            >>> scale_degree.accidental
            Accidental('s')

        Returns accidental.
        '''
        return self._accidental

    @property
    def name(self):
        r'''Name of scale degree.

        ::

            >>> tonalanalysistools.ScaleDegree(4).name
            'subdominant'

        Returns string.
        '''
        if not self.accidental.is_adjusted:
            return self._scale_degree_number_to_scale_degree_name[self.number]
        else:
            raise NotImplementedError

    @property
    def number(self):
        r'''Number of scale degree.

        ::

            >>> scale_degree.number
            4

        Returns integer from 1 to 7, inclusive.
        '''
        return self._number

    @property
    def roman_numeral_string(self):
        r'''Roman numeral string of scale degree.

        ::

            >>> scale_degree.roman_numeral_string
            'IV'

        Returns string.
        '''
        string = self._scale_degree_number_to_roman_numeral_string[self.number]
        return string

    @property
    def symbolic_string(self):
        r'''Symbolic string of scale degree.

        ::

            >>> scale_degree.symbolic_string
            '#IV'

        Returns string.
        '''
        return '{}{}'.format(self.accidental.symbolic_string,
            self.roman_numeral_string)

    @property
    def title_string(self):
        r'''Title string of scale degree.

        ::

            >>> scale_degree.title_string
            'SharpFour'

        Returns string.
        '''
        if not self.accidental.name == 'natural':
            accidental = self.accidental.name
        else:
            accidental = ''
        number = self._numeral_to_number_name[self.number]
        return '{}{}'.format(accidental.title(), number.title())
