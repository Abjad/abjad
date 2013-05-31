from abjad.tools import instrumenttools
from abjad.tools.instrumenttools.Instrument import Instrument
from experimental.tools.scoremanagertools import selectors
from experimental.tools.scoremanagertools.wizards.InstrumentCreationWizard import InstrumentCreationWizard
from experimental.tools.scoremanagertools.wizards.Wizard import Wizard


class InstrumentSelectionWizard(Wizard):

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def _breadcrumb(self):
        return 'instrument selection wizard'

    ### PUBLIC METHODS ###

    def _run(self, cache=False, clear=True, head=None, user_input=None):
        self._io.assign_user_input(user_input=user_input)
        self._session.cache_breadcrumbs(cache=cache)
        self._session.push_breadcrumb(self._breadcrumb)
        if self._session.is_in_score:
            selector = selectors.ScoreInstrumentSelector(session=self._session)
            with self.backtracking:
                result = selector._run(clear=clear)
            if self._session.backtrack():
                self._session.pop_breadcrumb()
                self._session.restore_breadcrumbs(cache=cache)
                return
            if isinstance(result, Instrument):
                self._session.pop_breadcrumb()
                self._session.restore_breadcrumbs(cache=cache)
                self.target = result
                return self.target
            elif not result == 'other':
                raise ValueError
        wizard = InstrumentCreationWizard(session=self._session)
        with self.backtracking:
            result = wizard._run()
        if self._session.backtrack():
            self._session.pop_breadcrumb()
            self._session.restore_breadcrumbs(cache=cache)
            return
        self._session.pop_breadcrumb()
        self._session.restore_breadcrumbs(cache=cache)
        self.target = result
        return self.target
