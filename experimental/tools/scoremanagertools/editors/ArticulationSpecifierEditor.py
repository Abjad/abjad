# -*- encoding: utf-8 -*-
from experimental.tools.scoremanagertools import iotools
from experimental.tools.scoremanagertools.editors.ParameterSpecifierEditor \
    import ParameterSpecifierEditor
from experimental.tools.scoremanagertools.editors.TargetManifest \
    import TargetManifest
from experimental.tools.scoremanagertools.specifiers.ArticulationSpecifier \
    import ArticulationSpecifier


class ArticulationSpecifierEditor(ParameterSpecifierEditor):

    ### PUBLIC PROPERTIES ###

    @property
    def target_manifest(self):
        return TargetManifest(
            ArticulationSpecifier,
            (
                'articulation_handler_name', 
                'articulation handler',
                'ah',
                iotools.Selector.make_articulation_handler_selector,
                ),
            )
