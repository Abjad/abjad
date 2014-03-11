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

    def _make_default_hidden_sections(self, menu):
        sections = []
        sections.append(self._make_navigation_menu_section(menu))
        sections.append(self._make_command_display_menu_section(menu))
        sections.append(self._make_lilypond_menu_section(menu))
        sections.append(self._make_python_menu_section(menu))
        sections.append(self._make_repository_menu_section(menu))
        if self._session.is_in_score:
            sections.append(self._make_score_navigation_menu_section(menu))
        sections.append(self._make_scores_tour_menu_section(menu))
        sections.append(self._make_session_menu_section(menu))
        sections.append(self._make_source_code_menu_section(menu))
        sections.append(self._make_system_menu_section(menu))
        return sections

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

    ### ALPHABETIZE ME LATER ###

    def _make_command_display_menu_section(self, menu):
        section = menu._make_section(
            is_hidden=True,
            name='command display',
            return_value_attribute='key',
            )
        section.append(('commands - hidden', 'n'))
        section.append(('commands - secondary', 'o'))
        return section

    def _make_lilypond_menu_section(self, menu):
        section = menu._make_section(
            is_hidden=True,
            match_on_display_string=False,
            name='lilypond',
            return_value_attribute='key',
            )
        section.append(('LilyPond - view log', 'lvl'))
        return section

    def _make_navigation_menu_section(self, menu):
        section = menu._make_section(
            is_hidden=True,
            name='navigation',
            return_value_attribute='key',
            )
        section.append(('back - go', 'b'))
        section.append(('home - go', 'h'))
        section.append(('score - go', 's'))
        return section

    def _make_python_menu_section(self, menu):
        section = menu._make_section(
            is_hidden=True,
            match_on_display_string=False,
            name='python',
            return_value_attribute='key',
            )
        section.append(('Python - doctest', 'pyd'))
        section.append(('Python - interact', 'pyi'))
        section.append(('Python - test', 'pyt'))
        return section

    def _make_repository_menu_section(self, menu):
        section = menu._make_section(
            is_hidden=True,
            match_on_display_string=False,
            name='repository',
            return_value_attribute='key',
            )
        section.append(('repository - add', 'radd'))
        section.append(('repository - commit', 'rci'))
        section.append(('repository - status', 'rst'))
        section.append(('repository - update', 'rup'))
        return section

    def _make_score_navigation_menu_section(self, menu):
        section = menu._make_section(
            is_hidden=True,
            name='score navigation',
            return_value_attribute='key',
            )
        section.append(('score - build', 'u'))
        section.append(('score - materials', 'm'))
        section.append(('score - segments', 'g'))
        return section

    def _make_scores_tour_menu_section(self, menu):
        section = menu._make_section(
            is_hidden=True,
            match_on_display_string=False,
            name='tour',
            return_value_attribute='key',
            )
        section.append(('scores - tour next', 'stn'))
        section.append(('scores - tour prev', 'stp'))
        return section

    def _make_session_menu_section(self, menu):
        section = menu._make_section(
            is_hidden=True,
            match_on_display_string=False,
            name='session',
            return_value_attribute='key',
            )
        section.append(('session - display variables', 'sdv'))
        return section

    def _make_source_code_menu_section(self, menu):
        section = menu._make_section(
            is_hidden=True,
            match_on_display_string=False,
            name='source code',
            return_value_attribute='key',
            )
        section.append(('source code - edit', 'sce'))
        section.append(('source code - location', 'scl'))
        section.append(('source code - track', 'sct'))
        return section

    def _make_system_menu_section(self, menu):
        section = menu._make_section(
            is_hidden=True,
            match_on_display_string=False,
            name='system',
            return_value_attribute='key',
            )
        section.append(('system - quit', 'q'))
        return section
