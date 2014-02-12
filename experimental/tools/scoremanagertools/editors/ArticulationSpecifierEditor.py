# -*- encoding: utf-8 -*-
from experimental.tools.scoremanagertools import iotools
from experimental.tools.scoremanagertools.editors.ParameterSpecifierEditor \
    import ParameterSpecifierEditor


class ArticulationSpecifierEditor(ParameterSpecifierEditor):

    ### PUBLIC PROPERTIES ###

    @property
    def target_manifest(self):
        from scoremanagertools import specifiers
        return self.TargetManifest(
            specifiers.ArticulationSpecifier,
            (
                'articulation_handler_name', 
                'articulation handler',
                'ah',
                iotools.Selector.make_articulation_handler_selector,
                ),
            )
