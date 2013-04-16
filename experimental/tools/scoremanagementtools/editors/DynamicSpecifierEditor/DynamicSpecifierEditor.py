from experimental.tools.scoremanagementtools import getters
from experimental.tools.scoremanagementtools import selectors
from experimental.tools.scoremanagementtools.editors.ParameterSpecifierEditor import ParameterSpecifierEditor
from experimental.tools.scoremanagementtools.editors.TargetManifest import TargetManifest
from experimental.tools.scoremanagementtools.specifiers.DynamicSpecifier import DynamicSpecifier


class DynamicSpecifierEditor(ParameterSpecifierEditor):

    ### CLASS ATTRIBUTES ###

    target_manifest = TargetManifest(DynamicSpecifier,
        ('name', 'nm', getters.get_string),
        ('description', 'ds', getters.get_string),
        (),
        ('dynamic_handler_name', 'dynamic handler', 'dh', selectors.DynamicHandlerPackageSelector),
        )
