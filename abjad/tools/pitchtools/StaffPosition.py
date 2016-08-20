# -*- coding: utf-8 -*-
import numbers
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class StaffPosition(AbjadValueObject):
    r'''Staff position.

    ..  container:: example

        **Example 1.** Initializes staff position at middle line of staff:

        ::

            >>> pitchtools.StaffPosition(0)
            StaffPosition(number=0)

    ..  container:: example

        **Example 2.** Initializes staff position one space below middle line
        of staff:

        ::

            >>> pitchtools.StaffPosition(-1)
            StaffPosition(number=-1)

    ..  container:: example

        **Example 3.** Initializes staff position one line below middle line
        of staff:

        ::

            >>> pitchtools.StaffPosition(-2)
            StaffPosition(number=-2)

    Staff positions are immutable.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_number',
        )

    ### INITIALIZER ###

    def __init__(self, number=0):
        assert isinstance(number, numbers.Number), repr(number)
        self._number = number

    ### SPECIAL METHODS ###

    def __eq__(self, other):
        r'''Is true when `other` is a staff position with the same number as
        this staff position. Otherwise false.

        ..  container:: example

            ::

                >>> staff_position_1 = pitchtools.StaffPosition(-2)
                >>> staff_position_2 = pitchtools.StaffPosition(-2)
                >>> staff_position_3 = pitchtools.StaffPosition(0)

            ::

                >>> staff_position_1 == staff_position_1
                True
                >>> staff_position_1 == staff_position_2
                True
                >>> staff_position_1 == staff_position_3
                False

            ::

                >>> staff_position_1 == 'foo'
                False

        Returns true or false.
        '''
        if isinstance(other, type(self)):
            return self.number == other.number
        return False

    def __float__(self):
        r'''Casts staff position as floating point number.

        ..  container:: example

            ::

                >>> float(pitchtools.StaffPosition(-2))
                -2.0

        Returns floating-point number.
        '''
        return float(self.number)

    def __hash__(self):
        r'''Hashes staff position.

        Returns integer.
        '''
        return hash(repr(self))

    def __int__(self):
        r'''Changes staff position to integer.

        ..  container:: example

            ::

                >>> int(pitchtools.StaffPosition(-2))
                -2

        Returns integer.
        '''
        return int(self.number)

    def __str__(self):
        r'''Gets string representation of staff position.

        ..  container:: example

            ::

                >>> str(pitchtools.StaffPosition(-2))
                'StaffPosition(-2)'

        Returns string.
        '''
        return '{}({})'.format(type(self).__name__, self.number)

    ### PUBLIC PROPERTIES ###

    @property
    def number(self):
        r'''Gets staff position number.

        ..  container:: example

            ::

                >>> pitchtools.StaffPosition(-2).number
                -2 

        Returns number.
        '''
        return self._number
