from experimental.tools.scoremanagertools import getters
from experimental.tools.scoremanagertools import specifiers
from experimental.tools.scoremanagertools import wizards
from experimental.tools.scoremanagertools.editors.ObjectInventoryEditor \
    import ObjectInventoryEditor
from experimental.tools.scoremanagertools.editors.TargetManifest \
    import TargetManifest
from experimental.tools.scoremanagertools.editors.get_parameter_specifier_editor \
    import get_parameter_specifier_editor


class MusicContributionSpecifierEditor(ObjectInventoryEditor):

    ### CLASS VARIABLES ###

    item_class = specifiers.ParameterSpecifier
    item_creator_class = wizards.ParameterSpecifierCreationWizard
    item_editor_class = staticmethod(get_parameter_specifier_editor)
    item_identifier = 'parameter specifier'
    target_manifest = TargetManifest(specifiers.MusicContributionSpecifier,
        ('name', 'nm', getters.get_string),
        ('description', 'ds', getters.get_string),
        target_attribute_name='name',
        )

    ### PRIVATE PROPERTIES ###

    @property
    def _breadcrumb(self):
        if self.target:
            return self.target._one_line_menuing_summary
        return 'unknown contribution'

    ### PUBLIC METHODS ###

    def menu_key_to_delegated_editor_kwargs(self, menu_key):
        kwargs = {}
        if menu_key == 'str':
            try:
                kwargs['instruments'] = \
                    self.target.performer_specifier.performer.instruments[:]
            except AttributeError:
                pass
        return kwargs
