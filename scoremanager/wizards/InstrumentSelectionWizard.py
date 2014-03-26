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

    def _run(self, pending_user_input=None):
        from scoremanager import iotools
        from scoremanager import wizards
        if pending_user_input:
            self._session._pending_user_input = pending_user_input
        context = iotools.ControllerContext(self)
        with context:
            if self._session.is_in_score:
                selector = iotools.Selector.make_score_instrument_selector(
                    session=self._session,
                    )
                result = selector._run()
                if self._should_backtrack():
                    return
                if isinstance(result, instrumenttools.Instrument):
                    self.target = result
                    return self.target
                elif not result == 'other':
                    raise ValueError
            wizard = wizards.InstrumentCreationWizard(session=self._session)
            result = wizard._run()
            if self._should_backtrack():
                return
            self.target = result
            return self.target