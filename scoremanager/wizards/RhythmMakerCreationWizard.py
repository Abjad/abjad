# -*- encoding: utf-8 -*-
from scoremanager.wizards.HandlerCreationWizard \
    import HandlerCreationWizard


class RhythmMakerCreationWizard(HandlerCreationWizard):

    ### CLASS VARIABLES ###

    handler_editor_class_name_suffix = 'Editor'

    ### INITIALIZER ###

    def __init__(self, session=None, target=None):
        from scoremanager.iotools import Selector
        HandlerCreationWizard.__init__(
            self,
            session=session,
            target=target,
            )

        selector = Selector.make_rhythm_maker_class_name_selector(
            session=self.session,
            )
        self.selector = selector

    ### PUBLIC PROPERTIES ###

    @property
    def _breadcrumb(self):
        return 'rhythm-maker creation wizard'
