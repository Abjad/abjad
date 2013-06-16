from experimental.tools.scoremanagertools import selectors
from experimental.tools.scoremanagertools.wizards.HandlerCreationWizard import HandlerCreationWizard


class RhythmMakerCreationWizard(HandlerCreationWizard):

    ### CLASS VARIABLES ###

    handler_class_name_selector = selectors.RhythmMakerClassNameSelector
    handler_editor_class_name_suffix = 'Editor'

    ### PUBLIC PROPERTIES ###

    @property
    def _breadcrumb(self):
        return 'time-menu_entry maker creation wizard'
