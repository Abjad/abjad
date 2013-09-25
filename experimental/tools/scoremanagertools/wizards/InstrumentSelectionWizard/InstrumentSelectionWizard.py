# -*- encoding: utf-8 -*-
from abjad.tools import instrumenttools
from abjad.tools.instrumenttools.Instrument import Instrument
from experimental.tools.scoremanagertools import io
from experimental.tools.scoremanagertools.wizards.InstrumentCreationWizard \
    import InstrumentCreationWizard
from experimental.tools.scoremanagertools.wizards.Wizard import Wizard


class InstrumentSelectionWizard(Wizard):

    ### PRIVATE PROPERTIES ###

    @property
    def _breadcrumb(self):
        return 'instrument selection wizard'

    ### PRIVATE METHODS ###

    def _run(
        self,
        cache=False,
        clear=True,
        head=None,
        pending_user_input=None,
        ):
        self.session.io_manager.assign_user_input(pending_user_input)
        self.session.cache_breadcrumbs(cache=cache)
        self.session.push_breadcrumb(self._breadcrumb)
        if self.session.is_in_score:
            selector = io.Selector.make_score_instrument_selector(
                session=self.session,
                )
            with self.backtracking:
                result = selector._run(clear=clear)
            if self.session.backtrack():
                self.session.pop_breadcrumb()
                self.session.restore_breadcrumbs(cache=cache)
                return
            if isinstance(result, Instrument):
                self.session.pop_breadcrumb()
                self.session.restore_breadcrumbs(cache=cache)
                self.target = result
                return self.target
            elif not result == 'other':
                raise ValueError
        wizard = InstrumentCreationWizard(session=self.session)
        with self.backtracking:
            result = wizard._run()
        if self.session.backtrack():
            self.session.pop_breadcrumb()
            self.session.restore_breadcrumbs(cache=cache)
            return
        self.session.pop_breadcrumb()
        self.session.restore_breadcrumbs(cache=cache)
        self.target = result
        return self.target
