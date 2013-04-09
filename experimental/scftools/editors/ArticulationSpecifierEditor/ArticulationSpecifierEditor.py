from scftools import getters
from scftools import selectors
from scftools.editors.ParameterSpecifierEditor import ParameterSpecifierEditor
from scftools.editors.TargetManifest import TargetManifest
from scftools.specifiers.ArticulationSpecifier import ArticulationSpecifier


class ArticulationSpecifierEditor(ParameterSpecifierEditor):

    ### CLASS ATTRIBUTES ###

    target_manifest = TargetManifest(ArticulationSpecifier,
        #('name', 'nm', getters.get_string),
        #('description', 'ds', getters.get_string),
        #(),
        ('articulation_handler_name', 'articulation handler', 'ah', selectors.ArticulationHandlerSelector),
        )
