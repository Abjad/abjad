from experimental.tools.scoremanagertools import getters
from experimental.tools.scoremanagertools import selectors
from experimental.tools.scoremanagertools.editors.ParameterSpecifierEditor import ParameterSpecifierEditor
from experimental.tools.scoremanagertools.editors.TargetManifest import TargetManifest
from experimental.tools.scoremanagertools.specifiers.DynamicSpecifier import DynamicSpecifier


class DynamicSpecifierEditor(ParameterSpecifierEditor):

    ### CLASS ATTRIBUTES ###

    target_manifest = TargetManifest(DynamicSpecifier,
        ('name', 'nm', getters.get_string),
        ('description', 'ds', getters.get_string),
        (),
        ('dynamic_handler_name', 'dynamic handler', 'dh', selectors.DynamicHandlerPackageSelector),
        )
