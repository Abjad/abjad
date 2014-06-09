# -*- encoding: utf-8 -*-
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
        command = 'instrument = instrumenttools.{}()'.format(instrument_name)
        exec(command)
        return instrument

    ### WIZARD ###

    def _make_wizard(self):
        from scoremanager.core.Controller import Controller
        class InstrumentCreationWizard(Controller):
            ### CLASS VARIABLES ###
            __slots__ = ('_is_ranged', '_target',)
            ### INITIALIZER ###
            def __init__(
                self,
                is_ranged=False,
                session=None,
                target=None,
                ):
                Controller.__init__(self, session=session)
                self._is_ranged = is_ranged
                self._target = target
            ### PRIVATE METHODS ###
#            @staticmethod
#            def _change_instrument_name_to_instrument(instrument_name):
#                if instrument_name in (
#                    'alto',
#                    'baritone',
#                    'bass',
#                    'soprano',
#                    'tenor',
#                    ):
#                    instrument_name = instrument_name + ' Voice'
#                instrument_name = instrument_name.title()
#                instrument_name = instrument_name.replace(' ', '')
#                command = 'instrument = instrumenttools.{}()'.format(instrument_name)
#                exec(command)
#                return instrument
            def _name_untuned_percussion(self, instrument):
                from abjad.tools import instrumenttools
                from abjad.tools.instrumenttools import UntunedPercussion
                from scoremanager import iotools
                if isinstance(instrument, instrumenttools.UntunedPercussion):
                    items = UntunedPercussion.known_untuned_percussion[:]
                    selector = iotools.Selector(
                        session=self._session,
                        items=items,
                        )
                    instrument_name = selector._run()
                    if self._session.is_backtracking:
                        return
                    instrument = new(
                        instrument,
                        instrument_name=instrument_name,
                        short_instrument_name=instrument_name,
                        )
                return instrument
            def _run(self, input_=None):
                from abjad.tools import instrumenttools
                from scoremanager import iotools
                if input_:
                    self._session._pending_input = input_
                controller = iotools.ControllerContext(controller=self)
                with controller:
                    items = instrumenttools.Instrument._list_instrument_names()
                    selector = iotools.Selector(
                        session=self._session,
                        items=items,
                        is_ranged=self._is_ranged,
                        )
                    result = selector._run()
                    if self._session.is_backtracking:
                        return
                    if isinstance(result, list):
                        instrument_names = result
                    else:
                        instrument_names = [result]
                    instruments = []
                    for instrument_name in instrument_names:
                        #instrument = \
                        #    self._change_instrument_name_to_instrument(instrument_name)
                        instrument = \
                            InstrumentInventory._change_instrument_name_to_instrument(instrument_name)
                        instrument = self._name_untuned_percussion(instrument)
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
        return InstrumentCreationWizard

    ### PRIVATE PROPERTIES ###

    @property
    def _item_creator_class(self):
        #from scoremanager import wizards
        #return wizards.InstrumentCreationWizard
        wizard = self._make_wizard()
        return wizard

    @property
    def _item_creator_class_kwargs(self):
        return {'is_ranged': True}