# -*- encoding: utf-8 -*-
from experimental.tools.scoremanagertools import getters
from experimental.tools.scoremanagertools import iotools
from experimental.tools.scoremanagertools.editors.ParameterSpecifierEditor \
    import ParameterSpecifierEditor
from experimental.tools.scoremanagertools.editors.TargetManifest \
    import TargetManifest
from experimental.tools.scoremanagertools.specifiers.RhythmSpecifier \
    import RhythmSpecifier


class RhythmSpecifierEditor(ParameterSpecifierEditor):

    ### PUBLIC PROPERTIES ###

    @property
    def target_manifest(self):
        return TargetManifest(
            RhythmSpecifier,
            ('custom_identifier', 'id', getters.get_string),
            ('description', 'ds', getters.get_string),
            (),
            (
                'rhythm_maker_package_path', 
                'time-menu_entry', 
                'ttm', 
                iotools.Selector.make_rhythm_maker_package_selector,
                ),
            )
