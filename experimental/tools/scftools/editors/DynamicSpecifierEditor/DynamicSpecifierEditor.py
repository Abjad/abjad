from experimental.tools.scftools import getters
from experimental.tools.scftools import selectors
from experimental.tools.scftools.editors.ParameterSpecifierEditor import ParameterSpecifierEditor
from experimental.tools.scftools.editors.TargetManifest import TargetManifest
from experimental.tools.scftools.specifiers.DynamicSpecifier import DynamicSpecifier


class DynamicSpecifierEditor(ParameterSpecifierEditor):

    ### CLASS ATTRIBUTES ###

    target_manifest = TargetManifest(DynamicSpecifier,
        ('name', 'nm', getters.get_string),
        ('description', 'ds', getters.get_string),
        (),
        ('dynamic_handler_name', 'dynamic handler', 'dh', selectors.DynamicHandlerPackageSelector),
        )
