# -*- encoding: utf-8 -*-
from scoremanager import getters
from scoremanager import iotools
from scoremanager.editors.SpecifierEditor \
    import SpecifierEditor
from scoremanager.specifiers.RhythmSpecifier \
    import RhythmSpecifier


class RhythmSpecifierEditor(SpecifierEditor):

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
