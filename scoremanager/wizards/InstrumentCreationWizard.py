# -*- encoding: utf-8 -*-
from abjad.tools import instrumenttools
from abjad.tools.topleveltools import new
from scoremanager import iotools
from scoremanager.wizards.Wizard import Wizard


class InstrumentCreationWizard(Wizard):
    r'''Instrument creation wizard.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_is_ranged',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        is_ranged=False,
        session=None,
        target=None,
        ):
        Wizard.__init__(self, session=session, target=target)
        self._is_ranged = is_ranged

    ### PRIVATE PROPERTIES ###

    @property
    def _breadcrumb(self):
        return 'instrument creation wizard'

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
            if self._session._should_backtrack():
                return
            instrument = new(
                instrument,
                instrument_name=instrument_name,
                short_instrument_name=instrument_name,
                )
        return instrument

    def _run(self, pending_input=None):
        from scoremanager import iotools
        if pending_input:
            self._session._pending_input = pending_input
        context = iotools.ControllerContext(controller=self)
        with context:
            items = instrumenttools.Instrument._list_instrument_names()
            selector = iotools.Selector(
                session=self._session,
                items=items,
                is_ranged=self._is_ranged,
                )
            result = selector._run()
            if self._session._should_backtrack():
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