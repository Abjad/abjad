# -*- encoding: utf-8 -*-
from scoremanager.wizards.Wizard import Wizard


class RhythmMakerCreationWizard(Wizard):
    r'''Rhythm-maker creation wizard.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(self, session=None, target=None):
        from scoremanager.iotools import Selector
        Wizard.__init__(
            self,
            session=session,
            target=target,
            )
        selector = Selector.make_rhythm_maker_class_name_selector(
            session=self._session,
            )
        self.selector = selector
        self.handler_editor_class_name_suffix = 'Editor'

    ### PUBLIC PROPERTIES ###

    @property
    def _breadcrumb(self):
        return 'rhythm-maker creation wizard'