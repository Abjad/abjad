from experimental.tools.scoremanagementtools import getters
from experimental.tools.scoremanagementtools import selectors
from experimental.tools.scoremanagementtools.editors.ParameterSpecifierEditor import ParameterSpecifierEditor
from experimental.tools.scoremanagementtools.editors.TargetManifest import TargetManifest
from experimental.tools.scoremanagementtools.specifiers.ClefSpecifier import ClefSpecifier


class ClefSpecifierEditor(ParameterSpecifierEditor):

    ### CLASS ATTRIBUTES ###

    target_manifest = TargetManifest(ClefSpecifier,
        #('name', 'nm', getters.get_string),
        #('description', 'ds', getters.get_string),
        #(),
        ('clef_name', 'cf', selectors.ClefNameSelector),
        )
