# -*- encoding: utf-8 -*-
from experimental.tools.scoremanagertools import getters
from experimental.tools.scoremanagertools import specifiers
from experimental.tools.scoremanagertools import wizards
from experimental.tools.scoremanagertools.editors.ObjectInventoryEditor \
    import ObjectInventoryEditor
from experimental.tools.scoremanagertools.editors.TargetManifest \
    import TargetManifest


class MusicContributionSpecifierEditor(ObjectInventoryEditor):

    ### CLASS VARIABLES ###

    item_class = specifiers.ParameterSpecifier

    item_creator_class = wizards.ParameterSpecifierCreationWizard

    @staticmethod
    def item_editor_class(target=None, session=None):
        from experimental.tools import scoremanagertools
        if target:
            wizard = \
                scoremanagertools.wizards.ParameterSpecifierCreationWizard()
            target_editor = wizard.get_target_editor(
                target._class_name, target=target)
            return target_editor

    item_identifier = 'parameter specifier'

    target_manifest = TargetManifest(
        specifiers.MusicContributionSpecifier,
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
