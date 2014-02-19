# -*- encoding: utf-8 -*-
from abjad.tools import instrumenttools
from scoremanager import iotools
from scoremanager.wizards.Wizard import Wizard


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
        from scoremanager import wizards
        self.session.io_manager._assign_user_input(pending_user_input)
        self.session._cache_breadcrumbs(cache=cache)
        self.session._push_breadcrumb(self._breadcrumb)
        if self.session.is_in_score:
            selector = iotools.Selector.make_score_instrument_selector(
                session=self.session,
                )
            with self.backtracking:
                result = selector._run(clear=clear)
            if self.session._backtrack():
                self.session._pop_breadcrumb()
                self.session._restore_breadcrumbs(cache=cache)
                return
            if isinstance(result, instrumenttools.Instrument):
                self.session._pop_breadcrumb()
                self.session._restore_breadcrumbs(cache=cache)
                self.target = result
                return self.target
            elif not result == 'other':
                raise ValueError
        wizard = wizards.InstrumentCreationWizard(session=self.session)
        with self.backtracking:
            result = wizard._run()
        if self.session._backtrack():
            self.session._pop_breadcrumb()
            self.session._restore_breadcrumbs(cache=cache)
            return
        self.session._pop_breadcrumb()
        self.session._restore_breadcrumbs(cache=cache)
        self.target = result
        return self.target
