# -*- encoding: utf-8 -*-
from abjad.tools import instrumenttools
from experimental.tools.scoremanagertools import selectors
from experimental.tools.scoremanagertools.wizards.Wizard import Wizard


class InstrumentCreationWizard(Wizard):

    ### INITIALIZER ###

    def __init__(
        self,
        is_ranged=False,
        session=None,
        target=None,
        ):
        Wizard.__init__(self, session=session, target=target)
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
        self.session.io_manager.assign_user_input(
            pending_user_input=pending_user_input)
        self.session.cache_breadcrumbs(cache=cache)
        self.session.push_breadcrumb(self._breadcrumb)
        selector = selectors.Selector(session=self.session)
        items = instrumenttools.Instrument.list_instrument_names()
        selector.items = items
        selector.is_ranged = self.is_ranged
        with self.backtracking:
            result = selector._run()
        if self.session.backtrack():
            self.session.pop_breadcrumb()
            self.session.restore_breadcrumbs(cache=cache)
            return
        if isinstance(result, list):
            instrument_names = result
        else:
            instrument_names = [result]
        instruments = []
        for instrument_name in instrument_names:
            instrument = \
                self.change_instrument_name_to_instrument(instrument_name)
            self.name_untuned_percussion(instrument)
            instruments.append(instrument)
        if self.is_ranged:
            result = instruments[:]
        else:
            result = instruments[0]
        self.session.pop_breadcrumb()
        self.session.restore_breadcrumbs(cache=cache)
        self.target = result
        return self.target

    ### PUBLIC METHODS ###

    def change_instrument_name_to_instrument(self, instrument_name):
        instrument_name = instrument_name.title()
        instrument_name = instrument_name.replace(' ', '')
        command = 'instrument = instrumenttools.{}()'.format(instrument_name)
        exec(command)
        return instrument

    def name_untuned_percussion(self, instrument):
        from abjad.tools.instrumenttools import UntunedPercussion
        if isinstance(instrument, instrumenttools.UntunedPercussion):
            selector = selectors.Selector(session=self.session)
            items = UntunedPercussion.known_untuned_percussion[:]
            selector.items = items
            with self.backtracking:
                instrument_name = selector._run()
            if self.session.backtrack():
                return
            instrument.instrument_name = instrument_name
            instrument.short_instrument_name = instrument_name
