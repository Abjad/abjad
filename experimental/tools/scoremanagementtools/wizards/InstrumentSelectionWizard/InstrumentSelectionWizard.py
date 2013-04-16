from abjad.tools import instrumenttools
from abjad.tools.instrumenttools.Instrument import Instrument
from experimental.tools.scoremanagementtools import selectors
from experimental.tools.scoremanagementtools.wizards.InstrumentCreationWizard import InstrumentCreationWizard
from experimental.tools.scoremanagementtools.wizards.Wizard import Wizard


class InstrumentSelectionWizard(Wizard):

    ### PUBLIC READ-ONLY PROPERTIES ###

    @property
    def breadcrumb(self):
        return 'instrument selection wizard'

    ### PUBLIC METHODS ###

    def run(self, cache=False, clear=True, head=None, user_input=None):
        self.assign_user_input(user_input=user_input)
        self.cache_breadcrumbs(cache=cache)
        self.push_breadcrumb()
        if self.session.is_in_score:
            selector = selectors.ScoreInstrumentSelector(session=self.session)
            self.push_backtrack()
            result = selector.run(clear=clear)
            self.pop_backtrack()
            if self.backtrack():
                self.pop_breadcrumb()
                self.restore_breadcrumbs(cache=cache)
                return
            if isinstance(result, Instrument):
                self.pop_breadcrumb()
                self.restore_breadcrumbs(cache=cache)
                self.target = result
                return self.target
            elif not result == 'other':
                raise ValueError
        wizard = InstrumentCreationWizard(session=self.session)
        self.push_backtrack()
        result = wizard.run()
        self.pop_backtrack()
        if self.backtrack():
            self.pop_breadcrumb()
            self.restore_breadcrumbs(cache=cache)
            return
        self.pop_breadcrumb()
        self.restore_breadcrumbs(cache=cache)
        self.target = result
        return self.target
