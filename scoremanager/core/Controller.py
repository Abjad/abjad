# -*- encoding: utf -*-
from scoremanager.core.ScoreManagerObject import ScoreManagerObject


class Controller(ScoreManagerObject):
    r'''Controller.
    '''

    ### PRIVATE PROPERTIES ###

    @property
    def _user_input_to_action(self):
        result = {
            }
        return result

    ### PRIVATE METHODS ###

    def _make_directory_menu_section(self, menu, is_permanent=False):
        section = menu.make_command_section(
            is_hidden=True,
            name='directory',
            )
        section.append(('directory - list', 'ls'))
        section.append(('directory - list long', 'll'))
        section.append(('directory - pwd', 'pwd'))
        if not is_permanent:
            section.append(('directory - remove', 'rm'))
            section.append(('directory - rename', 'ren'))
        return section

    def _make_done_menu_section(self, menu):
        section = menu.make_command_section(
            name='done',
            )
        section.append(('done', 'done'))
        return section

    def _make_initializer_menu_section(self, menu, has_initializer=True):
        if not has_initializer:
            section = menu.make_command_section(name='initializer')
            section.title = "package has no initializer: use 'ins'."
        section = menu.make_command_section(
            is_hidden=True,
            match_on_display_string=False,
            name='initializer',
            )
        section.append(('initializer - boilerplate', 'inbp'))
        section.append(('initializer - remove', 'inrm'))
        section.append(('initializer - stub', 'ins'))
        section.append(('initializer - view', 'inv'))
        return section

    def _make_material_tour_menu_section(self, menu):
        section = menu.make_command_section(
            is_hidden=True,
            name='tour materials',
            )
        section.append(('materials - tour next', 'mtn'))
        section.append(('materials - tour previous', 'mtp'))
        return section

    def _make_metadata_menu_section(self, menu):
        section = menu.make_command_section(
            is_hidden=True,
            match_on_display_string=False,
            name='metadata',
            )
        section.append(('metadatum - add', 'mma'))
        section.append(('metadatum - get', 'mmg'))
        section.append(('metadatum - remove', 'mmrm'))
        return section

    def _make_metadata_module_menu_section(self, menu):
        section = menu.make_command_section(
            is_hidden=True,
            match_on_display_string=False,
            name='metadata module',
            )
        section.append(('metadata module - remove', 'mmmrm'))
        section.append(('metadata module - rewrite', 'mmmrw'))
        section.append(('metadata module - view', 'mmmv'))
        return section

    def _make_views_menu_section(self, menu):
        section = menu.make_command_section(
            is_hidden=True,
            match_on_display_string=False,
            name='views',
            )
        section.append(('views - list', 'vwl'))
        section.append(('views - new', 'vwn'))
        section.append(('views - select', 'vws'))
        return section

    def _make_views_module_menu_section(self, menu):
        section = menu.make_command_section(
            is_hidden=True,
            match_on_display_string=False,
            name='views module',
            )
        section.append(('views module - remove', 'vwmrm'))
        section.append(('views module - view', 'vwmv'))
        return section
