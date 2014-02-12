# -*- encoding: utf-8 -*-
from scoremanager import getters
from scoremanager import specifiers
from scoremanager import wizards
from scoremanager.editors.ObjectInventoryEditor \
    import ObjectInventoryEditor


class MusicContributionSpecifierEditor(ObjectInventoryEditor):

    ### CLASS VARIABLES ###

    item_class = specifiers.ParameterSpecifier

    item_creator_class = wizards.ParameterSpecifierCreationWizard

    item_identifier = 'parameter specifier'

    ### PRIVATE PROPERTIES ###

    @property
    def _breadcrumb(self):
        if self.target:
            return self.target._one_line_menuing_summary
        return 'unknown contribution'

    ### PUBLIC PROPERTIES ###

    @property
    def target_manifest(self):
        from scoremanager import specifiers
        return self.TargetManifest(
            specifiers.MusicContributionSpecifier,
            ('custom_identifier', 'custom_identifier', 'id', getters.get_string),
            ('description', 'ds', getters.get_string),
            target_attribute_name='name',
            )

    ### PUBLIC METHODS ###

    @staticmethod
    def item_editor_class(target=None, session=None):
        from experimental.tools import scoremanager
        if target:
            wizard = \
                scoremanager.wizards.ParameterSpecifierCreationWizard()
            target_editor = wizard.get_target_editor(
                target.__class__.__name__, target=target)
            return target_editor

    def menu_key_to_delegated_editor_kwargs(self, menu_key):
        kwargs = {}
        if menu_key == 'str':
            try:
                kwargs['instruments'] = \
                    self.target.performer_specifier.performer.instruments[:]
            except AttributeError:
                pass
        return kwargs
