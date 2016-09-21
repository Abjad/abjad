# -*- coding: utf-8 -*-
from abjad.tools.datastructuretools.TypedList import TypedList
from abjad.tools.topleveltools import new


class InstrumentInventory(TypedList):
    r'''An ordered list of instruments.

    ::

        >>> inventory = instrumenttools.InstrumentInventory([
        ...     instrumenttools.Flute(),
        ...     instrumenttools.Guitar()
        ...     ])

    Instrument inventories implement list interface and are mutable.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

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

    ### PRIVATE METHODS ###

    @staticmethod
    def _change_instrument_name_to_instrument(instrument_name):
        from abjad.tools import instrumenttools
        if instrument_name in (
            'alto',
            'baritone',
            'bass',
            'soprano',
            'tenor',
            ):
            instrument_name = instrument_name + ' Voice'
        instrument_name = instrument_name.title()
        instrument_name = instrument_name.replace(' ', '')
        instrument_name = instrument_name.replace('-', '')
        instrument_class = instrumenttools.__dict__[instrument_name]
        instrument = instrument_class()
        return instrument

    @staticmethod
    def _name_percussion(instrument, session):
        from abjad.tools import instrumenttools
        from ide import idetools
        if isinstance(instrument, instrumenttools.Percussion):
            Percussion = instrumenttools.Percussion
            items = Percussion.known_percussion[:]
            selector = idetools.Selector(session=session, items=items)
            instrument_name = selector._run()
            if selector._session.is_backtracking or instrument_name is None:
                return
            instrument = new(
                instrument,
                instrument_name=instrument_name,
                short_instrument_name=instrument_name,
                )
        return instrument

    ### ITEM CREATOR ###

    @staticmethod
    def _make_item_creator_class():
        from ide.idetools.Controller import Controller
        class ItemCreator(Controller):
            ### CLASS VARIABLES ###
            __slots__ = ('_is_ranged', '_target',)
            ### INITIALIZER ###
            def __init__(self, is_ranged=False, session=None, target=None):
                Controller.__init__(self, session=session)
                self._is_ranged = is_ranged
                self._target = target
            ### PRIVATE METHODS ###
            def _run(self):
                from abjad.tools import instrumenttools
                from ide import idetools
                controller = idetools.ControllerContext(controller=self)
                with controller:
                    items = instrumenttools.Instrument._list_instrument_names()
                    selector = idetools.Selector(
                        session=self._session,
                        items=items,
                        is_ranged=self._is_ranged,
                        )
                    result = selector._run()
                    if self._session.is_backtracking or not result:
                        return
                    if isinstance(result, list):
                        instrument_names = result
                    else:
                        instrument_names = [result]
                    instruments = []
                    class_ = InstrumentInventory
                    to_instrument = \
                        class_._change_instrument_name_to_instrument
                    name_percussion = class_._name_percussion
                    for instrument_name in instrument_names:
                        instrument = to_instrument(instrument_name)
                        instrument = name_percussion(instrument, self._session)
                        if instrument is not None:
                            instruments.append(instrument)
                    if self._is_ranged:
                        result = instruments[:]
                    else:
                        result = instruments[0]
                    self._target = result
                    return self.target
            @property
            def target(self):
                return self._target
        return ItemCreator

    ### PRIVATE PROPERTIES ###

    @property
    def _item_creator_class(self):
        item_creator_class = self._make_item_creator_class()
        return item_creator_class

    @property
    def _item_creator_class_kwargs(self):
        return {'is_ranged': True}
