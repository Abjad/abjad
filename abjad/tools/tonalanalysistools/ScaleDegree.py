# -*- coding: utf-8 -*-
import re
from abjad.tools.abctools import AbjadValueObject


class ScaleDegree(AbjadValueObject):
    '''Scale degree.
    
    ::

        >>> from abjad.tools import tonalanalysistools

    ..  container:: example

        ::

            >>> tonalanalysistools.ScaleDegree('#4')
            ScaleDegree('#4')

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_accidental',
        '_number',
        )

    _acceptable_numbers = tuple(range(1, 16))

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

    _publish_storage_format = True

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

    _string_regex = re.compile(r'([#|b]*)([i|I|v|V|\d]+)')

    ### INITIALIZER ###

    def __init__(self, string=1):
        import abjad
        assert isinstance(string, (str, int, type(self))), repr(string)
        string = str(string)
        match = self._string_regex.match(string)
        if match is None:
            raise Exception(repr(string))
        groups = match.groups()
        accidental, roman_numeral = groups
        accidental = abjad.Accidental(accidental)
        roman_numeral = roman_numeral.upper()
        try:
            number = self._roman_numeral_string_to_scale_degree_number[
                roman_numeral]
        except KeyError:
            number = int(roman_numeral)
        self._accidental = accidental
        self._number = number

    ### SPECIAL METHODS ###

    def __eq__(self, argument):
        r'''Is true when `argument` is a scale degree with number and
        accidental equal to those of this scale degree.

        ..  container:: example

            ::

                >>> degree_1 = tonalanalysistools.ScaleDegree('#4')
                >>> degree_2 = tonalanalysistools.ScaleDegree('#4')
                >>> degree_3 = tonalanalysistools.ScaleDegree(5)

            ::

                >>> degree_1 == degree_1
                True
                >>> degree_1 == degree_2
                True
                >>> degree_1 == degree_3
                False

            ::

                >>> degree_2 == degree_1
                True
                >>> degree_2 == degree_2
                True
                >>> degree_2 == degree_3
                False

            ::

                >>> degree_3 == degree_1
                False
                >>> degree_3 == degree_2
                False
                >>> degree_3 == degree_3
                True

        Returns true or false.
        '''
        return super(ScaleDegree, self).__eq__(argument)

    def __hash__(self):
        r'''Hashes scale degree.

        Returns integer.
        '''
        return super(ScaleDegree, self).__hash__()

    def __str__(self):
        r'''Gets string representation of scale degree.

        ..  container:: example

            ::

                >>> str(tonalanalysistools.ScaleDegree('#4'))
                '#4'

        Returns string.
        '''
        return '{}{}'.format(self.accidental.symbol, self.number)
    
    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        import abjad
        values = [self.string]
        return abjad.FormatSpecification(
            client=self,
            repr_is_indented=False,
            storage_format_is_indented=False,
            storage_format_args_values=values,
            )

    ### PUBLIC METHODS ###

    @staticmethod
    def from_accidental_and_number(accidental, number):
        r'''Makes scale degree from `accidental` and `number`.

        ..  container:: example

            ::

                >>> class_ = tonalanalysistools.ScaleDegree
                >>> class_.from_accidental_and_number('sharp', 4)
                ScaleDegree('#4')

        Returns new scale degree.
        '''
        import abjad
        accidental = abjad.Accidental(accidental)
        string = '{}{}'.format(accidental.symbol, number)
        return ScaleDegree(string=string)

    ### PUBLIC PROPERTIES ###

    @property
    def accidental(self):
        r'''Gets accidental.

        ..  container:: example

            ::

                >>> tonalanalysistools.ScaleDegree('#4').accidental
                Accidental('sharp')

        Returns accidental.
        '''
        return self._accidental

    @property
    def name(self):
        r'''Gets name.

        ..  container:: example

            ::

                >>> tonalanalysistools.ScaleDegree(1).name
                'tonic'
                >>> tonalanalysistools.ScaleDegree(2).name
                'superdominant'
                >>> tonalanalysistools.ScaleDegree(3).name
                'mediant'
                >>> tonalanalysistools.ScaleDegree(4).name
                'subdominant'
                >>> tonalanalysistools.ScaleDegree(5).name
                'dominant'
                >>> tonalanalysistools.ScaleDegree(6).name
                'submediant'
                >>> tonalanalysistools.ScaleDegree(7).name
                'leading tone'

        Returns string.
        '''
        if self.accidental.semitones == 0:
            return self._scale_degree_number_to_scale_degree_name[self.number]
        else:
            raise NotImplementedError

    @property
    def number(self):
        r'''Gets number.

        ..  container:: example

            ::

                >>> tonalanalysistools.ScaleDegree('#4').number
                4

        Returns integer from 1 to 7, inclusive.
        '''
        return self._number

    @property
    def roman_numeral_string(self):
        r'''Gets Roman numeral string.

        ..  container:: example

            ::

                >>> degree = tonalanalysistools.ScaleDegree('#4')
                >>> degree.roman_numeral_string
                'IV'

        Returns string.
        '''
        string = self._scale_degree_number_to_roman_numeral_string[self.number]
        return string

    @property
    def string(self):
        r'''Gets string.

        ..  container:: example

            ::

                >>> tonalanalysistools.ScaleDegree('b4').string
                'b4'

            ::

                >>> tonalanalysistools.ScaleDegree('4').string
                '4'

            ::

                >>> tonalanalysistools.ScaleDegree('#4').string
                '#4'

        Returns string.
        '''
        return '{}{}'.format(
            self.accidental.symbol,
            self.number,
            )

    @property
    def title_string(self):
        r'''Gets title string.

        ..  container:: example

            ::

                >>> tonalanalysistools.ScaleDegree('b4').title_string
                'FlatFour'

            ::

                >>> tonalanalysistools.ScaleDegree('4').title_string
                'Four'

            ::

                >>> tonalanalysistools.ScaleDegree('#4').title_string
                'SharpFour'

        Returns string.
        '''
        if not self.accidental.name == 'natural':
            accidental = self.accidental.name
        else:
            accidental = ''
        number = self._numeral_to_number_name[self.number]
        return '{}{}'.format(accidental.title(), number.title())
