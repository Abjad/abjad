from experimental.tools.scoremanagertools import getters
from experimental.tools.scoremanagertools import selectors
from experimental.tools.scoremanagertools.editors.ParameterSpecifierEditor import ParameterSpecifierEditor
from experimental.tools.scoremanagertools.editors.TargetManifest import TargetManifest
from experimental.tools.scoremanagertools.specifiers.ArticulationSpecifier import ArticulationSpecifier


class ArticulationSpecifierEditor(ParameterSpecifierEditor):

    ### CLASS ATTRIBUTES ###

    target_manifest = TargetManifest(ArticulationSpecifier,
        #('name', 'nm', getters.get_string),
        #('description', 'ds', getters.get_string),
        #(),
        ('articulation_handler_name', 'articulation handler', 'ah', selectors.ArticulationHandlerSelector),
        )
