# -*- encoding: utf-8 -*-
from abjad.tools.abctools import AbjadObject


class ChordExtent(AbjadObject):
    '''A chord extent, such as triad, seventh chord, ninth chord,
    etc.

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

    _default_positional_input_arguments = (
        7,
        )

    _extent_number_to_extent_name = {
        5: 'triad',
        7: 'seventh',
        9: 'ninth',
        }

    ### INITIALIZER ###

    def __init__(self, arg):
        if isinstance(arg, (int, long)):
            if arg not in self._acceptable_number:
                message = 'can not initialize extent: {}.'
                raise ValueError(message.format(arg))
            number = arg
        elif isinstance(arg, type(self)):
            number = arg.number
        self._number = number

    ### SPECIAL METHODS ###

    def __eq__(self, arg):
        if isinstance(arg, type(self)):
            if self.number == arg.number:
                return True
        return False

    def __ne__(self, arg):
        return not self == arg

    ### PRIVATE PROPERTIES ###

    @property
    def _storage_format_specification(self):
        from abjad.tools import systemtools
        return systemtools.StorageFormatSpecification(
            self,
            positional_argument_values=(
                self.number,
                )
            )

    ### PUBLIC PROPERTIES ###

    @property
    def name(self):
        return self._extent_number_to_extent_name[self.number]

    @property
    def number(self):
        return self._number
