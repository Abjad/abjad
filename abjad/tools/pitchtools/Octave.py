# -*- coding: utf-8 -*-
import math
import numbers
import re
from abjad.tools import systemtools
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class Octave(AbjadValueObject):
    r'''Octave.

    ..  container:: example:

        **Example 1.** Initializes octave from integer:

        ::

            >>> pitchtools.Octave(4)
            Octave(4)

    ..  container:: example

        **Example 2.** Initializes octave from octave-tick string:

        ::

            >>> pitchtools.Octave(",,")
            Octave(1)

    ..  container:: example

        **Example 3.** Initializes octave from named pitch:

        ::

            >>> pitchtools.Octave(NamedPitch("cs''"))
            Octave(5)

    ..  container:: example

        **Example 4.** Initializes octave from other octave:

        ::

            >>> pitchtools.Octave(pitchtools.Octave(2))
            Octave(2)

    '''

    ### CLASS VARIABLES ###

    _octave_tick_regex_body = """
        (,+     # one or more commas for octaves below the bass clef
        |'+     # or one or more apostrophes for the octave of the treble clef
        |)      # or empty string for the octave of the bass clef
        """

    _octave_tick_regex = re.compile(
        '^{}$'.format(_octave_tick_regex_body),
        re.VERBOSE,
        )

    __slots__ = (
        '_octave_number',
        )

    ### INITIALIZER ###

    def __init__(self, octave_number=None):
        from abjad.tools import pitchtools
        expr = octave_number
        if isinstance(expr, numbers.Number):
            octave_number = int(expr)
        elif isinstance(expr, str):
            match = self._octave_tick_regex.match(expr)
            if match is None:
                message = 'can not instantiate octave: {!r}.'
                message = message.format(expr)
                raise Exception(message)
            group = match.group()
            if group == '':
                octave_number = 3
            elif group.startswith("'"):
                octave_number = 3 + len(group)
            else:
                octave_number = 3 - len(group)
        elif isinstance(expr, pitchtools.Pitch):
            octave_number = expr.octave_number
        elif isinstance(expr, type(self)):
            octave_number = expr.octave_number
        elif expr is None:
            octave_number = 4
        else:
            message = 'can not instantiate {}: {!r}.'
            message = message.format(type(self), expr)
            raise Exception(message)
        self._octave_number = octave_number

    ### SPECIAL METHODS ###

    def __eq__(self, other):
        r'''Is true when `other` is octave with same octave number.
        Otherwise False.

        ..  container:: example

            ::

                >>> octave = pitchtools.Octave(4)
                >>> octave == pitchtools.Octave(4)
                True

            ::

                >>> octave == pitchtools.Octave(3)
                False

            ::

                >>> octave == 'foo'
                False

        Returns true or false.
        '''
        try:
            other = type(self)(other)
            return self.octave_number == other.octave_number
        except:
            return False

    def __float__(self):
        r'''Casts octave as floating-point number.

        ..  container:: example

            ::

                >>> float(pitchtools.Octave(3))
                3.0

        Returns floating-point number.
        '''
        return float(self.octave_number)

    def __hash__(self):
        r'''Hashes octave.

        Returns integer.
        '''
        return hash(repr(self))

    def __int__(self):
        r'''Changes octave to integer.

        ..  container:: example

            ::

                >>> int(pitchtools.Octave(3))
                3

        Returns integer.
        '''
        return self.octave_number

    def __str__(self):
        r'''Gets string representation of octave.

        Defined equal to LilyPond octave / tick representation of octave.

        ..  container:: example

            ::

                >>> str(pitchtools.Octave(4))
                "'"

            ::

                >>> str(pitchtools.Octave(1))
                ',,'

            ::

                >>> str(pitchtools.Octave(3))
                ''

        Returns string.
        '''
        if 3 < self.octave_number:
            return "'" * (self.octave_number - 3)
        elif self.octave_number < 3:
            return ',' * abs(3 - self.octave_number)
        return ''

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        return systemtools.FormatSpecification(
            client=self,
            repr_is_indented=False,
            storage_format_is_indented=False,
            storage_format_args_values=[self.octave_number],
            storage_format_kwargs_names=[],
            )

    ### PUBLIC METHODS ###

    @classmethod
    def from_pitch_name(class_, pitch_name):
        '''Makes octave from `pitch_name`.

        ..  container:: example

            ::

                >>> pitchtools.Octave.from_pitch_name('cs')
                Octave(3)

        Returns integer.
        '''
        if not isinstance(pitch_name, str):
            message = 'must be string: {!r}.'
            message = message.format(pitch_name)
            raise TypeError(message)
        match = re.match('^([a-z]+)(\,*|\'*)$', pitch_name)
        if match is None:
            message = 'incorrect pitch string format.'
            raise TypeError(message)
        name, tick_string = match.groups()
        return class_(tick_string)

    @classmethod
    def from_pitch_number(class_, pitch_number):
        r'''Makes octave from `pitch_number`.

        ..  container:: example

            ::

                >>> pitchtools.Octave.from_pitch_number(13)
                Octave(5)

        Returns octave.
        '''
        octave_number = int(math.floor(pitch_number / 12)) + 4
        return class_(octave_number)

    @classmethod
    def is_octave_tick_string(class_, expr):
        '''Is true when `expr` is an octave tick string. Otherwise false.

        ..  container:: example

            ::

                >>> pitchtools.Octave.is_octave_tick_string(',,,')
                True

        The regex ``^,+|'+|$`` underlies this predicate.

        Returns true or false.
        '''
        if not isinstance(expr, str):
            return False
        return bool(class_._octave_tick_regex.match(expr))

    ### PUBLIC PROPERTIES ###

    @property
    def octave_number(self):
        r'''Gets octave number of octave.

        ..  container:: example

            ::

                >>> pitchtools.Octave(5).octave_number
                5

        Returns integer.
        '''
        return self._octave_number

    @property
    def octave_tick_string(self):
        r"""Gets LilyPond octave tick representation of octave.

        ..  container:: example

            ::

                >>> for i in range(-1, 9):
                ...     print(i, pitchtools.Octave(i).octave_tick_string)
                -1 ,,,,
                0  ,,,
                1  ,,
                2  ,
                3
                4  '
                5  ''
                6  '''
                7  ''''
                8  '''''

        Returns string.
        """
        return str(self)

    @property
    def pitch_number(self):
        r'''Gets pitch number of first note in octave.

        ..  container:: example

            ::

                >>> pitchtools.Octave(4).pitch_number
                0

            ::

                >>> pitchtools.Octave(5).pitch_number
                12

            ::

                >>> pitchtools.Octave(3).pitch_number
                -12

        Returns integer.
        '''
        return (self.octave_number - 4) * 12

    @property
    def pitch_range(self):
        r'''Gets pitch range of octave.

        ..  container:: example

            ::

                >>> pitchtools.Octave(5).pitch_range
                PitchRange(range_string='[C5, C6)')

        Returns pitch range.
        '''
        from abjad.tools import pitchtools
        return pitchtools.PitchRange(
            '[C{}, C{})'.format(
                self.octave_number,
                self.octave_number + 1,
                ))
