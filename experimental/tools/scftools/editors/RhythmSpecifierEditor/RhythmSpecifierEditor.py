from experimental.tools.scftools import getters
from experimental.tools.scftools import selectors
from experimental.tools.scftools.editors.ParameterSpecifierEditor import ParameterSpecifierEditor
from experimental.tools.scftools.editors.TargetManifest import TargetManifest
from experimental.tools.scftools.specifiers.RhythmSpecifier import RhythmSpecifier


class RhythmSpecifierEditor(ParameterSpecifierEditor):

    ### CLASS ATTRIBUTES ###

    target_manifest = TargetManifest(RhythmSpecifier,
        ('name', 'nm', getters.get_string),
        ('description', 'ds', getters.get_string),
        (),
        ('time_token_maker_package_importable_name', 'time-token', 'ttm', selectors.RhythmMakerPackageSelector),
        )
