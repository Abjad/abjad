# -*- encoding: utf-8 -*-
import math
import numbers
import re
from abjad.tools.abctools.AbjadObject import AbjadObject


class OctaveIndication(AbjadObject):
    r'''Abjad model of an octave indication:

    ::

        >>> pitchtools.OctaveIndication(4)
        OctaveIndication(4)

    ::

        >>> pitchtools.OctaveIndication(",,")
        OctaveIndication(1)

    ::

        >>> pitchtools.OctaveIndication(pitchtools.NamedPitch("cs''"))
        OctaveIndication(5)

    ::

        >>> pitchtools.OctaveIndication(pitchtools.OctaveIndication(2))
        OctaveIndication(2)

    Return octave indication.
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

    def __init__(self, expr):
        from abjad.tools import pitchtools
        if isinstance(expr, numbers.Number):
            octave_number = int(expr)
        elif isinstance(expr, str):
            match = self._octave_tick_regex.match(expr)
            if match is None:
                raise Exception('Cannot instantiate octave indication from '
                    '{!r}'.format(expr))
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
        else:
            raise Exception('Cannot instantiate octave indication from '
                '{!r}'.format(expr))
        self._octave_number = octave_number

    ### SPECIAL METHODS ###

    def __eq__(self, other):
        r'''True if `other` is octave indication with same octave number:

        ::

            >>> octave_indication = pitchtools.OctaveIndication(4)
            >>> octave_indication == pitchtools.OctaveIndication(4)
            True

        ::

            >>> octave_indication == pitchtools.OctaveIndication(3)
            False

        ::

            >>> octave_indication == 'foo'
            False

        Return boolean.
        '''
        try:
            other = type(self)(other)
            return self.octave_number == other.octave_number
        except: 
            return False

    def __float__(self):
        r'''Case octave indication as floating-point number:

        ::

            >>> float(pitchtools.OctaveIndication(3))
            3.0

        Return floating-point number.
        '''
        return float(self.octave_number)

    def __hash__(self):
        return hash(repr(self))

    def __int__(self):
        r'''Cast octave indication as integer:

        ::

            >>> int(pitchtools.OctaveIndication(3))
            3

        Return integer.
        '''
        return self.octave_number

    def __repr__(self):
        return '{}({})'.format(self._class_name, self.octave_number)

    def __str__(self):
        r'''LilyPond octave tick representation of octave indication:

        ::

            >>> str(pitchtools.OctaveIndication(4))
            "'"

        ::

            >>> str(pitchtools.OctaveIndication(1))
            ',,'

        ::

            >>> str(pitchtools.OctaveIndication(3))
            ''

        Return string.
        '''
        if 3 < self.octave_number:
            return "'" * (self.octave_number - 3)
        elif self.octave_number < 3:
            return ',' * abs(3 - self.octave_number)
        return ''

    ### PUBLIC METHODS ###

    @classmethod
    def from_pitch_name(cls, pitch_name):
        '''Change `pitch_name` to octave indication:

        ::

            >>> pitchtools.OctaveIndication.from_pitch_name('cs')
            OctaveIndication(3)

        Return integer.
        '''
        from abjad.tools import pitchtools
        if not isinstance(pitch_name, str):
            raise TypeError('pitch string must be string.')
        match = re.match('^([a-z]+)(\,*|\'*)$', pitch_name)
        if match is None:
            raise PitchError('incorrect pitch string format.')
        name, tick_string = match.groups()
        return cls(tick_string)

    @classmethod
    def from_pitch_number(cls, pitch_number):
        r'''Change `pitch_number` to octave indication:

        ::

            >>> pitchtools.OctaveIndication.from_pitch_number(13)
            OctaveIndication(5)

        Return octave indication.
        '''
        octave_number = int(math.floor(pitch_number / 12)) + 4
        return cls(octave_number)

    @classmethod
    def is_octave_tick_string(cls, expr):
        '''True when `expr` is an octave tick string. Otherwise false:

        ::

            >>> pitchtools.OctaveIndication.is_octave_tick_string(',,,')
            True

        The regex ``^,+|'+|$`` underlies this predicate.

        Return boolean.
        '''
        if not isinstance(expr, str):
            return False
        return bool(cls._octave_tick_regex.match(expr))

    ### PUBLIC PROPERTIES ###

    @property
    def octave_number(self):
        r'''Octave number of octave indication:

        ::

            >>> pitchtools.OctaveIndication(5).octave_number
            5

        Return integer.
        '''
        return self._octave_number

    @property
    def octave_tick_string(self):
        r"""LilyPond octave tick representation of octave indication:

        ::

            >>> for i in range(-1, 9):
            ...     print i, pitchtools.OctaveIndication(i).octave_tick_string
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

        Return string.
        """
        return str(self)

    @property
    def pitch_number(self):
        r'''Pitch number of first note in octave:

        ::

            >>> pitchtools.OctaveIndication(4).pitch_number
            0

        ::

            >>> pitchtools.OctaveIndication(5).pitch_number
            12

        ::

            >>> pitchtools.OctaveIndication(3).pitch_number
            -12

        Return integer.
        '''
        return (self.octave_number - 4) * 12

    @property
    def pitch_range(self):
        r'''Pitch range of octave:

        ::

            >>> pitchtools.OctaveIndication(5).pitch_range
            PitchRange('[C5, C6)')

        Return pitch range.
        '''
        from abjad.tools import pitchtools
        return pitchtools.PitchRange(
            '[C{}, C{})'.format(
                self.octave_number,
                self.octave_number + 1,
                ))
