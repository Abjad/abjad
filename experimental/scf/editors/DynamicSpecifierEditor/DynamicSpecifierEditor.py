from scf import getters
from scf import selectors
from scf.editors.ParameterSpecifierEditor import ParameterSpecifierEditor
from scf.editors.TargetManifest import TargetManifest
from scf.specifiers.DynamicSpecifier import DynamicSpecifier


class DynamicSpecifierEditor(ParameterSpecifierEditor):

    ### CLASS ATTRIBUTES ###

    target_manifest = TargetManifest(DynamicSpecifier,
        ('name', 'nm', getters.get_string),
        ('description', 'ds', getters.get_string),
        (),
        ('dynamic_handler_name', 'dynamic handler', 'dh', selectors.DynamicHandlerPackageSelector),
        )
