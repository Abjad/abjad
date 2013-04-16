from experimental.tools.scoremanagementtools import getters
from experimental.tools.scoremanagementtools import selectors
from experimental.tools.scoremanagementtools import wizards
from experimental.tools.scoremanagementtools.editors.ParameterSpecifierEditor import ParameterSpecifierEditor
from experimental.tools.scoremanagementtools.editors.TargetManifest import TargetManifest
from experimental.tools.scoremanagementtools.specifiers.PitchClassSpecifier import PitchClassSpecifier


class PitchClassSpecifierEditor(ParameterSpecifierEditor):

    ### CLASS ATTRIBUTES ###

    target_manifest = TargetManifest(PitchClassSpecifier,
        ('name', 'nm', getters.get_string),
        ('description', 'ds', getters.get_string),
        (),
        ('pitch_class_reservoir', 'pc', selectors.PitchClassReservoirSelector),
        ('pitch_class_transform', 'tr', wizards.PitchClassTransformCreationWizard),
        ('reservoir_start_helper', 'hp', wizards.ReservoirStartHelperCreationWizard),
        )

    ### READ-ONLY PROPERTIES ###

    @property
    def target_name(self):
        return self.target.name
