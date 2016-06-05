# -*- coding: utf-8 -*-
from abjad.tools.abctools import AbjadObject


class ChordExtent(AbjadObject):
    '''A chord extent, such as triad, seventh chord, ninth chord, etc.

    Value object that can not be changed after instantiation.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_number',
        )

    _acceptable_number = (
        5,
        7,
        9,
        )

    _extent_number_to_extent_name = {
        5: 'triad',
        7: 'seventh',
        9: 'ninth',
        }

    ### INITIALIZER ###

    def __init__(self, number=5):
        if isinstance(number, int):
            if number not in self._acceptable_number:
                message = 'can not initialize extent: {}.'
                raise ValueError(message.format(number))
            number = number
        elif isinstance(number, type(self)):
            number = number.number
        self._number = number

    ### SPECIAL METHODS ###

    def __eq__(self, arg):
        r'''Is true when `arg` is a chord extent with number equal to that of
        this chord extent. Otherwise false.

        Returns true or false.
        '''
        if isinstance(arg, type(self)):
            if self.number == arg.number:
                return True
        return False

    def __hash__(self):
        r'''Hashes chord extent.

        Required to be explicitly redefined on Python 3 if __eq__ changes.

        Returns integer.
        '''
        return super(ChordExtent, self).__hash__()

    def __ne__(self, arg):
        r'''Is true when chord extent does not equal `arg`. Otherwise false.

        Returns true or false.
        '''
        return not self == arg

    ### PUBLIC PROPERTIES ###

    @property
    def name(self):
        r'''Name of chord extent.

        Returns string.
        '''
        return self._extent_number_to_extent_name[self.number]

    @property
    def number(self):
        r'''Number of chord extent.

        Returns nonnegative integer.
        '''
        return self._number
