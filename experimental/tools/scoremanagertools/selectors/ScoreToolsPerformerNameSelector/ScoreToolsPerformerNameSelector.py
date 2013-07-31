# -*- encoding: utf-8 -*-
from abjad.tools import scoretools
from experimental.tools.scoremanagertools.selectors.Selector import Selector


class ScoreToolsPerformerNameSelector(Selector):

    ### CLASS VARIABLES ###

    space_delimited_lowercase_target_name = 'performer'

    ### PUBLIC METHODS ###

    def _make_main_menu(self, head=None):
        main_menu = self.session.io_manager.make_menu(where=self._where)
        menu_section = main_menu._make_section(
            return_value_attribute='display_string',
            is_numbered=self.is_numbered,
            is_ranged=self.is_ranged,
            )
        menu_section.menu_entries = self.make_menu_entries()
        return main_menu

    def make_menu_entries(self):
        performer_pairs = scoretools.Performer.list_primary_performer_names()
        performer_pairs.append(('percussionist', 'perc.'))
        performer_pairs.sort()
        menu_entries = []
        for performer_pair in performer_pairs:
            performer_name, performer_abbreviation = performer_pair
            performer_abbreviation = performer_abbreviation.split()[-1]
            performer_abbreviation = performer_abbreviation.strip('.')
            menu_entries.append((performer_name, performer_abbreviation)) 
        return menu_entries
