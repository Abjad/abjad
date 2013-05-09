def get_rhythm_maker_editor(target=None, session=None):
    from experimental.tools.scoremanagertools.wizards.RhythmMakerCreationWizard import RhythmMakerCreationWizard
    if target:
        wizard = RhythmMakerCreationWizard()
        rhythm_maker_editor = wizard.get_handler_editor(target._class_name, target=target)
        return rhythm_maker_editor
