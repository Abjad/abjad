from scftools import getters
from scftools import selectors
from scftools.editors.ParameterSpecifierEditor import ParameterSpecifierEditor
from scftools.editors.TargetManifest import TargetManifest
from scftools.specifiers.DynamicSpecifier import DynamicSpecifier


class DynamicSpecifierEditor(ParameterSpecifierEditor):

    ### CLASS ATTRIBUTES ###

    target_manifest = TargetManifest(DynamicSpecifier,
        ('name', 'nm', getters.get_string),
        ('description', 'ds', getters.get_string),
        (),
        ('dynamic_handler_name', 'dynamic handler', 'dh', selectors.DynamicHandlerPackageSelector),
        )
