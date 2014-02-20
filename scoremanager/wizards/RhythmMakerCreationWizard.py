# -*- encoding: utf-8 -*-
from scoremanager.wizards.Wizard import Wizard


class RhythmMakerCreationWizard(Wizard):

    ### CLASS VARIABLES ###

    handler_editor_class_name_suffix = 'Editor'

    ### INITIALIZER ###

    def __init__(self, _session=None, target=None):
        from scoremanager.iotools import Selector
        Wizard.__init__(
            self,
            _session=_session,
            target=target,
            )
        selector = Selector.make_rhythm_maker_class_name_selector(
            _session=self._session,
            )
        self.selector = selector

    ### PUBLIC PROPERTIES ###

    @property
    def _breadcrumb(self):
        return 'rhythm-maker creation wizard'
