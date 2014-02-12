# -*- encoding: utf-8 -*-
from scoremanagertools import getters
from scoremanagertools import iotools
from scoremanagertools.editors.ParameterSpecifierEditor \
    import ParameterSpecifierEditor
from scoremanagertools.specifiers.RhythmSpecifier \
    import RhythmSpecifier


class RhythmSpecifierEditor(ParameterSpecifierEditor):

    ### PUBLIC PROPERTIES ###

    @property
    def target_manifest(self):
        return self.TargetManifest(
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
