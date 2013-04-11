from experimental.tools.scftools import getters
from experimental.tools.scftools import selectors
from experimental.tools.scftools.editors.ParameterSpecifierEditor import ParameterSpecifierEditor
from experimental.tools.scftools.editors.TargetManifest import TargetManifest
from experimental.tools.scftools.specifiers.ClefSpecifier import ClefSpecifier


class ClefSpecifierEditor(ParameterSpecifierEditor):

    ### CLASS ATTRIBUTES ###

    target_manifest = TargetManifest(ClefSpecifier,
        #('name', 'nm', getters.get_string),
        #('description', 'ds', getters.get_string),
        #(),
        ('clef_name', 'cf', selectors.ClefNameSelector),
        )
