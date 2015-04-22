# -*- encoding: utf-8 -*-
from __future__ import print_function
import re
from abjad.tools.abctools import AbjadValueObject


class EnharmonicInterval(AbjadValueObject):
    r'''An enharmonic interval.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_semitones',
        '_staff_spaces',
        )

    _named_interval_quality_abbreviation_regex_body = '''
        (M|     # major
        m|      # minor
        P|      # perfect
        A+|     # augmented
        d+      # diminished
        )
        '''

    _named_interval_quality_abbreviation_regex = re.compile(
        '^{}$'.format(_named_interval_quality_abbreviation_regex_body),
        re.VERBOSE,
        )

    _interval_name_abbreviation_regex_body = '''
        ([+,-]?)    # one plus, one minus, or neither
        {}          # exactly one diatonic quality abbreviation
        (\d+)       # followed by one or more digits
        '''.format(
        _named_interval_quality_abbreviation_regex_body,
        )

    _interval_name_abbreviation_regex = re.compile(
        '^{}$'.format(_interval_name_abbreviation_regex_body),
        re.VERBOSE,
        )

    _scale = (0, 2, 4, 5, 7, 9, 11)

    ### PUBLIC METHODS ###

    @staticmethod
    def numbers_to_string(staff_spaces, semitones):
        r'''Converts `staff_spaces` and `semitones` to an enharmonic interval
        string.
        '''
        pass

    @staticmethod
    def string_to_numbers(string):
        r'''Converts an enharmonic interval string to a tuple of integers.
        '''
        match = EnharmonicInterval._interval_name_abbreviation_regex.match(
            string)
        (
            direction,
            quality,
            staff_spaces,
            ) = match.groups()
        direction = int('{}1'.format(direction))
        staff_spaces = int(staff_spaces) - 1
        octaves, staff_spaces = divmod(staff_spaces, 7)
        print(octaves, staff_spaces + 1, quality, direction)
        semitones = EnharmonicInterval._scale[staff_spaces]
        if staff_spaces + 1 in (1, 4, 5):
            assert quality not in ('m', 'M')
            if 'A' in quality:
                semitones += len(quality)
            elif 'd' in quality:
                semitones -= len(quality)
        else:
            assert quality != 'P'
            if quality == 'm':
                semitones -= 1
            elif 'A' in quality:
                semitones += len(quality)
            elif 'd' in quality:
                semitones -= 1
                semitones -= len(quality)
        print(direction, octaves, staff_spaces + 1, quality, semitones)