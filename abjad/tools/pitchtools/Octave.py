# -*- encoding: utf-8 -*-
import math
import numbers
import re
from abjad.tools.abctools.AbjadObject import AbjadObject


class Octave(AbjadObject):
    r'''An octave.

    ::

        >>> pitchtools.Octave(4)
        Octave(4)

    ::

        >>> pitchtools.Octave(",,")
        Octave(1)

    ::

        >>> pitchtools.Octave(NamedPitch("cs''"))
        Octave(5)

    ::

        >>> pitchtools.Octave(pitchtools.Octave(2))
        Octave(2)

    Returns octave.
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
                message = 'can not instantiate octave: {!r}.'.format(expr)
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
        r'''True if `other` is octave with same octave number, otherwise False.

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

        Returns boolean.
        '''
        try:
            other = type(self)(other)
            return self.octave_number == other.octave_number
        except: 
            return False

    def __float__(self):
        r'''Cast octave as floating-point number.

        ::

            >>> float(pitchtools.Octave(3))
            3.0

        Returns floating-point number.
        '''
        return float(self.octave_number)

    def __hash__(self):
        return hash(repr(self))

    def __int__(self):
        r'''Cast octave as integer.

        ::

            >>> int(pitchtools.Octave(3))
            3

        Returns integer.
        '''
        return self.octave_number

    def __str__(self):
        r'''LilyPond octave tick representation of octave.

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

    ### PRIVATE PROPERTIES ###

    @property
    def _storage_format_specification(self):
        from abjad.tools import systemtools
        return systemtools.StorageFormatSpecification(
            self,
            is_indented=False,
            keyword_argument_names=(),
            positional_argument_values=(
                self.octave_number,
                )
            )

    ### PUBLIC PROPERTIES ###

    @property
    def octave_number(self):
        r'''Octave number of octave.

        ::

            >>> pitchtools.Octave(5).octave_number
            5

        Returns integer.
        '''
        return self._octave_number

    @property
    def octave_tick_string(self):
        r"""LilyPond octave tick representation of octave.

        ::

            >>> for i in range(-1, 9):
            ...     print i, pitchtools.Octave(i).octave_tick_string
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
        r'''Pitch number of first note in octave.

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
        r'''Pitch range of octave.

        ::

            >>> pitchtools.Octave(5).pitch_range
            PitchRange('[C5, C6)')

        Returns pitch range.
        '''
        from abjad.tools import pitchtools
        return pitchtools.PitchRange(
            '[C{}, C{})'.format(
                self.octave_number,
                self.octave_number + 1,
                ))

    ### PUBLIC METHODS ###

    @classmethod
    def from_pitch_name(cls, pitch_name):
        '''Change `pitch_name` to octave.

        ::

            >>> pitchtools.Octave.from_pitch_name('cs')
            Octave(3)

        Returns integer.
        '''
        from abjad.tools import pitchtools
        if not isinstance(pitch_name, str):
            message = 'must be string: {!r}.'.format(pitch_name)
            raise TypeError(message)
        match = re.match('^([a-z]+)(\,*|\'*)$', pitch_name)
        if match is None:
            message = 'incorrect pitch string format.'
            raise TypeError(message)
        name, tick_string = match.groups()
        return cls(tick_string)

    @classmethod
    def from_pitch_number(cls, pitch_number):
        r'''Change `pitch_number` to octave.

        ::

            >>> pitchtools.Octave.from_pitch_number(13)
            Octave(5)

        Returns octave.
        '''
        octave_number = int(math.floor(pitch_number / 12)) + 4
        return cls(octave_number)

    @classmethod
    def is_octave_tick_string(cls, expr):
        '''True when `expr` is an octave tick string, otherwise false.

        ::

            >>> pitchtools.Octave.is_octave_tick_string(',,,')
            True

        The regex ``^,+|'+|$`` underlies this predicate.

        Returns boolean.
        '''
        if not isinstance(expr, str):
            return False
        return bool(cls._octave_tick_regex.match(expr))
