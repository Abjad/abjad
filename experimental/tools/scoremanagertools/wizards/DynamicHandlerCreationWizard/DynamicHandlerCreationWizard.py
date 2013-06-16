from experimental.tools.scoremanagertools import selectors
from experimental.tools.scoremanagertools.wizards.HandlerCreationWizard \
    import HandlerCreationWizard


class DynamicHandlerCreationWizard(HandlerCreationWizard):

    ### CLASS VARIABLES ###

    handler_class_name_selector = selectors.DynamicHandlerClassNameSelector
    handler_editor_class_name_suffix = 'Editor'

    ### PRIVATE PROPERTIES ###

    @property
    def _breadcrumb(self):
        return 'dynamic handler creation wizard'
