# -*- encoding: utf-8 -*-
from abjad.tools import instrumenttools
from abjad.tools.topleveltools import new
from scoremanager import iotools
from scoremanager.wizards.Wizard import Wizard


class InstrumentCreationWizard(Wizard):

    ### INITIALIZER ###

    def __init__(
        self,
        is_ranged=False,
        _session=None,
        target=None,
        ):
        Wizard.__init__(self, _session=_session, target=target)
        self.is_ranged = is_ranged

    ### PRIVATE PROPERTIES ###

    @property
    def _breadcrumb(self):
        return 'instrument creation wiard'

    ### PRIVATE METHODS ###

    def _run(
        self,
        cache=False,
        clear=True,
        head=None,
        pending_user_input=None,
        ):
        self._session.io_manager._assign_user_input(pending_user_input)
        self._session._cache_breadcrumbs(cache=cache)
        self._session._push_breadcrumb(self._breadcrumb)
        selector = iotools.Selector(_session=self._session)
        items = instrumenttools.Instrument._list_instrument_names()
        selector.items = items
        selector.is_ranged = self.is_ranged
        with self.backtracking:
            result = selector._run()
        if self._session._backtrack():
            self._session._pop_breadcrumb()
            self._session._restore_breadcrumbs(cache=cache)
            return
        if isinstance(result, list):
            instrument_names = result
        else:
            instrument_names = [result]
        instruments = []
        for instrument_name in instrument_names:
            instrument = \
                self.change_instrument_name_to_instrument(instrument_name)
            instrument = self.name_untuned_percussion(instrument)
            instruments.append(instrument)
        if self.is_ranged:
            result = instruments[:]
        else:
            result = instruments[0]
        self._session._pop_breadcrumb()
        self._session._restore_breadcrumbs(cache=cache)
        self.target = result
        return self.target

    ### PUBLIC METHODS ###

    def change_instrument_name_to_instrument(self, instrument_name):
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

    def name_untuned_percussion(self, instrument):
        from abjad.tools.instrumenttools import UntunedPercussion
        if isinstance(instrument, instrumenttools.UntunedPercussion):
            selector = iotools.Selector(_session=self._session)
            items = UntunedPercussion.known_untuned_percussion[:]
            selector.items = items
            with self.backtracking:
                instrument_name = selector._run()
            if self._session._backtrack():
                return
            instrument = new(
                instrument,
                instrument_name=instrument_name,
                short_instrument_name=instrument_name,
                )
        return instrument
