# -*- encoding: utf-8 -*-
from abjad.tools import instrumenttools
from abjad.tools.topleveltools import new
from scoremanager import iotools
from scoremanager.core.Controller import Controller


class InstrumentCreationWizard(Controller):
    r'''Instrument creation wizard.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_is_ranged',
        '_target',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        is_ranged=False,
        session=None,
        target=None,
        ):
        Controller.__init__(self, session=session)
        self._is_ranged = is_ranged
        self_target = target

    ### PRIVATE METHODS ###

    @staticmethod
    def _change_instrument_name_to_instrument(instrument_name):
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

    def _name_untuned_percussion(self, instrument):
        from abjad.tools.instrumenttools import UntunedPercussion
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
                instrument = \
                    self._change_instrument_name_to_instrument(instrument_name)
                instrument = self._name_untuned_percussion(instrument)
                instruments.append(instrument)
            if self._is_ranged:
                result = instruments[:]
            else:
                result = instruments[0]
            self._target = result
            return self.target

    ### PUBLIC PROPERTIES ###

    @property
    def target(self):
        r'''Gets wizard target.

        Returns object or none.
        '''
        return self._target