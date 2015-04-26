# -*- encoding: utf-8 -*-
from __future__ import print_function
import re
from abjad.tools import mathtools
from abjad.tools.abctools import AbjadValueObject


class EnharmonicInterval(AbjadValueObject):
    r'''An enharmonic interval.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_quality_string',
        '_number',
        )

    _named_interval_quality_abbreviation_regex_body = '''
        ([+,-]?)    # one plus, one minus, or neither
        (M      # major
        |m      # minor
        |P      # perfect
        |A+     # augmented
        |d+)    # diminished
        ([+~]?) # optional quarter-tone inflection
        '''

    _named_interval_quality_abbreviation_regex = re.compile(
        '^{}$'.format(_named_interval_quality_abbreviation_regex_body),
        re.VERBOSE,
        )

    _interval_name_abbreviation_regex_body = '''
        {}          # quality abbreviation with quarter-tone alteration
        (\d+)       # followed by one or more digits
        '''.format(
        _named_interval_quality_abbreviation_regex_body,
        )

    _interval_name_abbreviation_regex = re.compile(
        '^{}$'.format(_interval_name_abbreviation_regex_body),
        re.VERBOSE,
        )

    _scale = (0, 2, 4, 5, 7, 9, 11)

    ### INITIALIZER ###

    def __init__(self, *args):
        from abjad.tools import pitchtools
        if len(args) == 1:
            expr = args[0]
            if isinstance(expr, type(self)):
                quality_string = expr.quality_string
                number = expr.number
            elif isinstance(expr, str):
                match = self._interval_name_abbreviation_regex.match(expr)
                if match is None:
                    message = 'can not initialize {}: {!r}'
                    message = message.format(type(self).__init__, args)
                    raise ValueError(message)
                (
                    direction,
                    quality,
                    staff_spaces,
                    quarter_tone,
                    ) = match.groups()
            elif isinstance(expr, (
                int,
                float,
                int,
                pitchtools.NumberedInterval,
                pitchtools.NumberedIntervalClass,
                )):
                number = int(expr)
                sign = mathtools.sign(number)
                octave, semitones = divmod(abs(number), 12)
            else:
                message = 'can not initialize {}: {!r}'
                message = message.format(type(self).__init__, args)
                raise ValueError(message)
        elif len(args) == 2:
            quality_string, number = args
        elif len(args) == 0:
            quality_string = 'P'
            number = 1
        else:
            message = 'can not initialize {}: {!r}'
            message = message.format(type(self).__init__, args)
            raise ValueError(message)
        assert isinstance(quality_string, str)
        assert self._named_interval_quality_abbreviation_regex.match(
            quality_string) is not None
        self._quality_string = quality_string
        number = int(number)
        assert number != 0
        self._number = number

    ### PUBLIC METHODS ###

    @staticmethod
    def numbers_to_string(direction, octaves, staff_spaces, semitones):
        r'''Converts `staff_spaces` and `semitones` to an enharmonic interval
        string.
        '''
        while 7 < staff_spaces:
            staff_spaces -= 7
            semitones -= 12
            octaves += 1
        staff_spaces -= 1
        unaltered_semitones = EnharmonicInterval._scale[staff_spaces]
        alteration = semitones - unaltered_semitones
        quarter_tone = 0
        if 0 < alteration:
            alteration, quarter_tone = divmod(alteration, 1)
        elif alteration < 0:
            alteration, quarter_tone = divmod(abs(alteration), 1)
            alteration *= -1
            quarter_tone *= -1
        if staff_spaces + 1 in (1, 4, 5):
            if alteration == 0:
                quality = 'P'
            elif 0 < alteration:
                quality = 'A' * alteration
            else:
                quality = 'd' * abs(alteration)
        else:
            if alteration == 0:
                quality = 'M'
            elif alteration == -1:
                quality = 'm'
            elif 0 < alteration:
                quality = 'A' * alteration
            else:
                quality = 'd' * (abs(alteration) - 1)
        if direction == 1:
            direction = ''
        else:
            direction = '-'
        if 0 < quarter_tone:
            quarter_tone = '+'
        elif quarter_tone < 0:
            quarter_tone = '~'
        else:
            quarter_tone = ''
        return '{}{}{}{}'.format(
            direction,
            quality,
            (staff_spaces + 1) + 7 * octaves,
            quarter_tone
            )

    @staticmethod
    def string_from_pitch_carriers(pitch_carrier_1, pitch_carrier_2):
        r'''Converts pitch carriers to enharmonic interval string.

        ::

            >>> interval = pitchtools.EnharmonicInterval

        ::

            >>> interval.string_from_pitch_carriers('C4', 'G4')
            'P5'

        ::

            >>> interval.string_from_pitch_carriers("cff'", "css'")
            'AAAA1'

        ::

            >>> interval.string_from_pitch_carriers('d', 'aqs')
            'P5+'

        '''
        from abjad.tools import pitchtools
        pitch_1 = pitchtools.NamedPitch.from_pitch_carrier(pitch_carrier_1)
        pitch_2 = pitchtools.NamedPitch.from_pitch_carrier(pitch_carrier_2)
        degree_1 = pitch_1.diatonic_pitch_number
        degree_2 = pitch_2.diatonic_pitch_number
        staff_spaces = abs(degree_1 - degree_2) + 1
        semitones = abs(
            pitchtools.NumberedPitch(pitch_1).pitch_number -
            pitchtools.NumberedPitch(pitch_2).pitch_number
            )
        direction = 1
        if pitch_2 < pitch_1:
            direction = -1
        return EnharmonicInterval.numbers_to_string(
            direction,
            0,
            staff_spaces,
            semitones,
            )

    @staticmethod
    def string_to_numbers(string):
        r'''Converts an enharmonic interval string to a tuple of integers.

        ::

            >>> interval = pitchtools.EnharmonicInterval

        ::

            >>> interval.string_to_numbers('P5')
            (1, 0, 5, 7)

        ::

            >>> interval.string_to_numbers('P+5')
            (1, 0, 5, 7.5)

        ::

            >>> interval.string_to_numbers('AAAA1')
            (1, 0, 1, 4)

        '''
        match = EnharmonicInterval._interval_name_abbreviation_regex.match(
            string)
        (
            direction,
            quality,
            quarter_tone,
            staff_spaces,
            ) = match.groups()
        direction = int('{}1'.format(direction))
        staff_spaces = int(staff_spaces) - 1
        octaves, staff_spaces = divmod(staff_spaces, 7)
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
        if quarter_tone == '+':
            semitones += 0.5
        elif quarter_tone == '~':
            semitones -= 0.5
        return (
            direction,
            octaves,
            staff_spaces + 1,
            semitones,
            )