from scftools import getters
from scftools import selectors
from scftools.editors.ParameterSpecifierEditor import ParameterSpecifierEditor
from scftools.editors.TargetManifest import TargetManifest
from scftools.specifiers.RhythmSpecifier import RhythmSpecifier


class RhythmSpecifierEditor(ParameterSpecifierEditor):

    ### CLASS ATTRIBUTES ###

    target_manifest = TargetManifest(RhythmSpecifier,
        ('name', 'nm', getters.get_string),
        ('description', 'ds', getters.get_string),
        (),
        ('time_token_maker_package_importable_name', 'time-token', 'ttm', selectors.RhythmMakerPackageSelector),
        )
