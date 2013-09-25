# -*- encoding: utf-8 -*-
from experimental.tools.scoremanagertools import io
from experimental.tools.scoremanagertools.editors.ParameterSpecifierEditor \
    import ParameterSpecifierEditor
from experimental.tools.scoremanagertools.editors.TargetManifest \
    import TargetManifest
from experimental.tools.scoremanagertools.specifiers.ArticulationSpecifier \
    import ArticulationSpecifier


class ArticulationSpecifierEditor(ParameterSpecifierEditor):

    ### CLASS VARIABLES ###

    target_manifest = TargetManifest(
        ArticulationSpecifier,
        (
            'articulation_handler_name', 
            'articulation handler',
            'ah',
            io.Selector.make_articulation_handler_selector,
            ),
        )
