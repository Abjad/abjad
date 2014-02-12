# -*- encoding: utf-8 -*-
from experimental.tools.scoremanagertools import getters
from experimental.tools.scoremanagertools import iotools
from experimental.tools.scoremanagertools import wizards
from experimental.tools.scoremanagertools.editors.ParameterSpecifierEditor \
    import ParameterSpecifierEditor
from experimental.tools.scoremanagertools.editors.TargetManifest \
    import TargetManifest


class PitchClassSpecifierEditor(ParameterSpecifierEditor):

    ### PUBLIC PROPERTIES ###

    @property
    def target_manifest(self):
        from scoremanagertools import specifiers
        return self.TargetManifest(
            PitchClassSpecifier,
            ('custom_identifier', 'id', getters.get_string),
            ('description', 'ds', getters.get_string),
            (),
            (
                'pitch_class_reservoir', 
                'pc', 
                iotools.Selector.make_pitch_class_reservoir_selector,
                ),
            (
                'pitch_class_transform', 
                'tr', 
                wizards.PitchClassTransformCreationWizard,
                ),
            (
                'reservoir_start_helper', 
                'hp', 
                wizards.ReservoirStartHelperCreationWizard,
                ),
            )

    @property
    def target_name(self):
        return self.target.name
