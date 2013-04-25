def get_dynamic_handler_editor(target=None, session=None):
    from experimental.tools.scoremanagertools.wizards.DynamicHandlerCreationWizard import DynamicHandlerCreationWizard
    if target:
        wizard = DynamicHandlerCreationWizard()
        # TODO: generalize get_handler_editor to get_target_editor?
        dynamic_handler_editor = wizard.get_handler_editor(target._class_name, target=target)
        return dynamic_handler_editor
