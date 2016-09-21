# -*- coding: utf-8 -*-
from abjad.tools.abctools import AbjadObject


class ChordInversion(AbjadObject):
    '''A chord inversion for tertian chords: 5, 63, 64 and
    also 7, 65, 43, 42, etc.

    Also root position, first, second, third
    inversions, etc.

    Value object that can not be changed once initialized.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_number',
        )

    _inversion_name_to_inversion_number = {
        'root': 0,
        'root position': 0,
        'first': 1,
        'second': 2,
        'third': 3,
        'fourth': 4,
        }

    _inversion_number_to_inversion_name = {
        0: 'root position',
        1: 'first',
        2: 'second',
        3: 'third',
        4: 'fourth',
        }

    _seventh_chord_inversion_to_figured_bass_string = {
        0: '7',
        1: '6/5',
        2: '4/3',
        3: '4/2',
        }

    _triadic_inversion_to_figured_bass_string = {
        0: '',
        1: '6',
        2: '6/4',
        }

    ### INITIALIZER ###

    def __init__(self, number=0):
        arg = number
        if isinstance(arg, int):
            number = arg
        elif isinstance(arg, str):
            number = self._inversion_name_to_inversion_number[arg]
        else:
            message = 'can not initialize chord inversion.'
            raise ValueError(message)
        self._number = number

    ### SPECIAL METHODS ###

    def __eq__(self, arg):
        r'''Is true when `arg` is a chord inversion with number equal to that
        of this chord inversion. Otherwise false.

        Returns true or false.
        '''
        if isinstance(arg, type(self)):
            if self.number == arg.number:
                return True
        return False

    def __hash__(self):
        r'''Hashes chord inversion.

        Required to be explicitly redefined on Python 3 if __eq__ changes.

        Returns integer.
        '''
        return super(ChordInversion, self).__hash__()

    def __ne__(self, arg):
        r'''Is true when chord inversion does not equal `arg`. Otherise false.

        Returns true or false.
        '''
        return not self == arg

    ### PUBLIC METHODS ###

    def extent_to_figured_bass_string(self, extent):
        r'''Changes `extent` to figured bass string.

        Returns string.
        '''
        if extent == 5:
            return self._triadic_inversion_to_figured_bass_string[self.number]
        elif extent == 7:
            return self._seventh_chord_inversion_to_figured_bass_string[
                self.number]
        else:
            raise NotImplementedError

    ### PUBLIC PROPERTIES ###

    @property
    def name(self):
        r'''Name of chord inversion.

        Returns string.
        '''
        return self._inversion_number_to_inversion_name[self.number]

    @property
    def number(self):
        r'''Number of chord inversion.

        Returns nonnegative integer.
        '''
        return self._number

    @property
    def title(self):
        r'''Title of chord inversion.

        Returns string.
        '''
        name = self._inversion_number_to_inversion_name[self.number]
        if name == 'root position':
            return 'RootPosition'
        return '{}Inversion'.format(name.title())
