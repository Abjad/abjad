from experimental.tools.scoremanagertools import getters
from experimental.tools.scoremanagertools import selectors
from experimental.tools.scoremanagertools.editors.ParameterSpecifierEditor import ParameterSpecifierEditor
from experimental.tools.scoremanagertools.editors.TargetManifest import TargetManifest
from experimental.tools.scoremanagertools.specifiers.ClefSpecifier import ClefSpecifier


class ClefSpecifierEditor(ParameterSpecifierEditor):

    ### CLASS ATTRIBUTES ###

    target_manifest = TargetManifest(ClefSpecifier,
        #('name', 'nm', getters.get_string),
        #('description', 'ds', getters.get_string),
        #(),
        ('clef_name', 'cf', selectors.ClefNameSelector),
        )
