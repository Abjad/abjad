from scf import selectors
from scf.wizards.HandlerCreationWizard import HandlerCreationWizard


class RhythmMakerCreationWizard(HandlerCreationWizard):

    ### CLASS ATTRIBUTES ###

    handler_class_name_selector = selectors.RhythmMakerClassNameSelector
    handler_editor_class_name_suffix = 'Editor'

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def breadcrumb(self):
        return 'time-token maker creation wizard'
