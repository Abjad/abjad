def get_parameter_specifier_editor(target=None, session=None):
    from experimental.tools.scftools.wizards.ParameterSpecifierCreationWizard import ParameterSpecifierCreationWizard
    if target:
        wizard = ParameterSpecifierCreationWizard()
        target_editor = wizard.get_target_editor(target._class_name, target=target)
        return target_editor
