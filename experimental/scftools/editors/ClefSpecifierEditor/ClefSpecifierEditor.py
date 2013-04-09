from scftools import getters
from scftools import selectors
from scftools.editors.ParameterSpecifierEditor import ParameterSpecifierEditor
from scftools.editors.TargetManifest import TargetManifest
from scftools.specifiers.ClefSpecifier import ClefSpecifier


class ClefSpecifierEditor(ParameterSpecifierEditor):

    ### CLASS ATTRIBUTES ###

    target_manifest = TargetManifest(ClefSpecifier,
        #('name', 'nm', getters.get_string),
        #('description', 'ds', getters.get_string),
        #(),
        ('clef_name', 'cf', selectors.ClefNameSelector),
        )
