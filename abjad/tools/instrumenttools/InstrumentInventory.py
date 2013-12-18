# -*- encoding: utf-8 -*-
from abjad.tools.datastructuretools.TypedList import TypedList


class InstrumentInventory(TypedList):
    r'''An ordered list of instruments.

    ::

        >>> inventory = instrumenttools.InstrumentInventory([
        ...     instrumenttools.Flute(), 
        ...     instrumenttools.Guitar()
        ...     ])

    Instrument inventories implement list interface and are mutable.
    '''

    ### SPECIAL METHODS ###

    def __format__(self, format_specification=''):
        r'''Formats instrument inventory.

        Set `format_specification` to `''` or `'storage'`.
        Interprets `''` equal to `'storage'`.

        Returns string.
        '''
        superclass = super(InstrumentInventory, self)
        return superclass.__format__(format_specification=format_specification)

    def __repr__(self):
        r'''Gets interpreter representation of instrument inventory.

        ::

            >>> inventory
            InstrumentInventory([Flute(), Guitar()])

        Returns string.
        '''
        contents = [repr(x) for x in self]
        contents = ', '.join(contents)
        return '{}([{}])'.format(type(self).__name__, contents)
