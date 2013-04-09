def get_articulation_handler_editor(target=None, session=None):
    from scftools.wizards.ArticulationHandlerCreationWizard import ArticulationHandlerCreationWizard
    if target:
        wizard = ArticulationHandlerCreationWizard()
        articulation_handler_editor = wizard.get_handler_editor(target._class_name, target=target)
        return articulation_handler_editor
