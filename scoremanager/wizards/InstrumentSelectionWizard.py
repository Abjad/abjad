# -*- encoding: utf-8 -*-
from abjad.tools import instrumenttools
from scoremanager import iotools
from scoremanager.wizards.Wizard import Wizard


class InstrumentSelectionWizard(Wizard):
    r'''Instrument selection wizard.
    '''

    ### PRIVATE PROPERTIES ###

    @property
    def _breadcrumb(self):
        return 'instrument selection wizard'

    ### PRIVATE METHODS ###

    def _run(
        self,
        clear=True,
        pending_user_input=None,
        ):
        from scoremanager import wizards
        self._io_manager._assign_user_input(pending_user_input)
        if self._session.is_in_score:
            selector = iotools.Selector.make_score_instrument_selector(
                session=self._session,
                )
            with self._backtrack:
                result = selector._run(clear=clear)
            if self._break_io_loop():
                return
            if isinstance(result, instrumenttools.Instrument):
                self.target = result
                return self.target
            elif not result == 'other':
                raise ValueError
        wizard = wizards.InstrumentCreationWizard(session=self._session)
        with self._backtrack:
            result = wizard._run()
        if self._break_io_loop():
            return
        self.target = result
        return self.target