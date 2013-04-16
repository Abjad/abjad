from experimental.tools.scoremanagementtools import getters
from experimental.tools.scoremanagementtools import selectors
from experimental.tools.scoremanagementtools.editors.ParameterSpecifierEditor import ParameterSpecifierEditor
from experimental.tools.scoremanagementtools.editors.TargetManifest import TargetManifest
from experimental.tools.scoremanagementtools.specifiers.ArticulationSpecifier import ArticulationSpecifier


class ArticulationSpecifierEditor(ParameterSpecifierEditor):

    ### CLASS ATTRIBUTES ###

    target_manifest = TargetManifest(ArticulationSpecifier,
        #('name', 'nm', getters.get_string),
        #('description', 'ds', getters.get_string),
        #(),
        ('articulation_handler_name', 'articulation handler', 'ah', selectors.ArticulationHandlerSelector),
        )
