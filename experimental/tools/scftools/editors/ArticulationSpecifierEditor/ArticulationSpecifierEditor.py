from experimental.tools.scftools import getters
from experimental.tools.scftools import selectors
from experimental.tools.scftools.editors.ParameterSpecifierEditor import ParameterSpecifierEditor
from experimental.tools.scftools.editors.TargetManifest import TargetManifest
from experimental.tools.scftools.specifiers.ArticulationSpecifier import ArticulationSpecifier


class ArticulationSpecifierEditor(ParameterSpecifierEditor):

    ### CLASS ATTRIBUTES ###

    target_manifest = TargetManifest(ArticulationSpecifier,
        #('name', 'nm', getters.get_string),
        #('description', 'ds', getters.get_string),
        #(),
        ('articulation_handler_name', 'articulation handler', 'ah', selectors.ArticulationHandlerSelector),
        )
