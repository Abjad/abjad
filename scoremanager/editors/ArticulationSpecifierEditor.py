# -*- encoding: utf-8 -*-
from scoremanager import iotools
from scoremanager.editors.ParameterSpecifierEditor \
    import ParameterSpecifierEditor


class ArticulationSpecifierEditor(ParameterSpecifierEditor):

    ### PUBLIC PROPERTIES ###

    @property
    def target_manifest(self):
        from scoremanager import specifiers
        return self.TargetManifest(
            specifiers.ArticulationSpecifier,
            (
                'articulation_handler_name', 
                'articulation handler',
                'ah',
                iotools.Selector.make_articulation_handler_selector,
                ),
            )
