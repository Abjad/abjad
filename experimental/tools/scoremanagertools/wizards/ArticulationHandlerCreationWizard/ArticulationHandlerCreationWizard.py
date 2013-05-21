from experimental.tools.scoremanagertools import selectors
from experimental.tools.scoremanagertools.wizards.HandlerCreationWizard import HandlerCreationWizard


class ArticulationHandlerCreationWizard(HandlerCreationWizard):

    ### CLASS VARIABLES ###

    handler_class_name_selector = selectors.ArticulationHandlerClassNameSelector
    handler_editor_class_name_suffix = 'Editor'

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def _breadcrumb(self):
        return 'articulation handler creation wizard'
