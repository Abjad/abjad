# -*- encoding: utf-8 -*-
from scoremanager import iotools
from scoremanager.editors.SpecifierEditor import SpecifierEditor


class ArticulationSpecifierEditor(SpecifierEditor):

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
