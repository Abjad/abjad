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
        cache=False,
        clear=True,
        pending_user_input=None,
        ):
        from scoremanager import wizards
        self._io_manager._assign_user_input(pending_user_input)
        self._session._push_breadcrumb(self._breadcrumb)
        if self._session.is_in_score:
            selector = iotools.Selector.make_score_instrument_selector(
                session=self._session,
                )
            with self._backtracking:
                result = selector._run(clear=clear)
            if self._session._backtrack():
                self._session._pop_breadcrumb()
                return
            if isinstance(result, instrumenttools.Instrument):
                self._session._pop_breadcrumb()
                self.target = result
                return self.target
            elif not result == 'other':
                raise ValueError
        wizard = wizards.InstrumentCreationWizard(session=self._session)
        with self._backtracking:
            result = wizard._run()
        if self._session._backtrack():
            self._session._pop_breadcrumb()
            return
        self._session._pop_breadcrumb()
        self.target = result
        return self.target