# -*- encoding: utf-8 -*-
from scoremanager import getters
from scoremanager import iotools
from scoremanager.editors.ParameterSpecifierEditor \
    import ParameterSpecifierEditor


class DynamicSpecifierEditor(ParameterSpecifierEditor):

    ### PUBLIC PROPERTIES ###

    @property
    def target_manifest(self):
        from scoremanager import specifiers
        return self.TargetManifest(
            specifiers.DynamicSpecifier,
            ('custom_identifier', 'id', getters.get_string),
            ('description', 'ds', getters.get_string),
            (),
            (
                'dynamic_handler_name', 
                'dynamic handler', 
                'dh', 
                iotools.Selector.make_dynamic_handler_package_selector,
                ),
            )
