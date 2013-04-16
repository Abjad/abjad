from experimental.tools.scoremanagementtools import getters
from experimental.tools.scoremanagementtools import specifiers
from experimental.tools.scoremanagementtools import wizards
from experimental.tools.scoremanagementtools.editors.ObjectInventoryEditor import ObjectInventoryEditor
from experimental.tools.scoremanagementtools.editors.TargetManifest import TargetManifest
from experimental.tools.scoremanagementtools.editors.get_parameter_specifier_editor import get_parameter_specifier_editor


class MusicContributionSpecifierEditor(ObjectInventoryEditor):

    ### CLASS ATTRIBUTES ###

    item_class = specifiers.ParameterSpecifier
    item_creator_class = wizards.ParameterSpecifierCreationWizard
    item_editor_class = staticmethod(get_parameter_specifier_editor)
    item_identifier = 'parameter specifier'
    target_manifest = TargetManifest(specifiers.MusicContributionSpecifier,
        ('name', 'nm', getters.get_string),
        ('description', 'ds', getters.get_string),
        target_attribute_name='name',
        )

    ### PUBLIC READ-ONLY PROPERTIES ###

    @property
    def breadcrumb(self):
        if self.target:
            return self.target.one_line_menuing_summary
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
