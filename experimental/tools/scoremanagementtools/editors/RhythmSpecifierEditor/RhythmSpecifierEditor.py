from experimental.tools.scoremanagementtools import getters
from experimental.tools.scoremanagementtools import selectors
from experimental.tools.scoremanagementtools.editors.ParameterSpecifierEditor import ParameterSpecifierEditor
from experimental.tools.scoremanagementtools.editors.TargetManifest import TargetManifest
from experimental.tools.scoremanagementtools.specifiers.RhythmSpecifier import RhythmSpecifier


class RhythmSpecifierEditor(ParameterSpecifierEditor):

    ### CLASS ATTRIBUTES ###

    target_manifest = TargetManifest(RhythmSpecifier,
        ('name', 'nm', getters.get_string),
        ('description', 'ds', getters.get_string),
        (),
        ('time_token_maker_package_importable_name', 'time-token', 'ttm', selectors.RhythmMakerPackageSelector),
        )
