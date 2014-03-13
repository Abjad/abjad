# -*- encoding: utf-8 -*-
import os
import subprocess
from scoremanager.core.Controller import Controller


class ScoreManager(Controller):
    r'''Score manager.

    ..  container:: example

        ::

            >>> score_manager = scoremanager.core.ScoreManager()
            >>> score_manager
            ScoreManager()

    '''

    ### INITIALIZER ###

    def __init__(self, session=None):
        from scoremanager import core
        from scoremanager import wranglers
        if session is None:
            session = core.Session()
        Controller.__init__(self, session=session)
        self._session._score_manager = self
        wrangler = wranglers.SegmentPackageWrangler(session=self._session)
        self._segment_package_wrangler = wrangler
        wrangler = wranglers.MaterialManagerWrangler(session=self._session)
        self._material_manager_wrangler = wrangler
        wrangler = wranglers.MaterialPackageWrangler(session=self._session)
        self._material_package_wrangler = wrangler
        wrangler = wranglers.ScorePackageWrangler(session=self._session)
        self._score_package_wrangler = wrangler
        wrangler = wranglers.StylesheetWrangler(session=self._session)
        self._stylesheet_wrangler = wrangler

    ### PRIVATE PROPERTIES ###

    @property
    def _breadcrumb(self):
        return 'score manager'

    @property
    def _score_status_string(self):
        return '{} scores'.format(self._session.scores_to_display)

    @property
    def _user_input_to_action(self):
        result = {
            'cv': self.view_cache,
            'cw': self.write_cache,
            'lmm': self.manage_material_library,
            'new': self.make_new_score,
            'radd': self.add,
            'rci': self.commit,
            'rst': self.status,
            'rup': self.update,
            'ssl': self.display_all_scores,
            'ssv': self.display_active_scores,
            'ssmb': self.display_mothballed_scores,
            'ssx': self.display_example_scores,
            'ssu': self.display_user_scores,
            'lmy': self.manage_stylesheet_library,
            }
        return result

    ### PRIVATE METHODS ###

    def _get_next_score_directory_path(self):
        wrangler = self._score_package_wrangler
        paths = wrangler._list_visible_asset_paths()
        if self._session.current_score_directory_path is None:
            return paths[0]
        score_path = self._session.current_score_directory_path
        index = paths.index(score_path)
        next_index = (index + 1) % len(paths)
        next_path = paths[next_index]
        return next_path

    def _get_previous_score_directory_path(self):
        wrangler = self._score_package_wrangler
        paths = wrangler._list_visible_asset_paths()
        if self._session.current_score_directory_path is None:
            return paths[-1]
        path = self._session.current_score_directory_path
        index = paths.index(path)
        previous_index = (index - 1) % len(paths)
        previous_path = paths[previous_index]
        return previous_path

    def _handle_main_menu_result(self, result):
        if result in self._user_input_to_action:
            self._user_input_to_action[result]()
        elif result == 'user entered lone return':
            pass
        else:
            wrangler = self._score_package_wrangler
            score_package_paths = wrangler._list_visible_asset_paths()
            if result in score_package_paths:
                self.manage_score(result)

    def _make_cache_menu_section(self, menu):
        section = menu.make_command_section(
            name='cache',
            is_hidden=True,
            )
        section.append(('cache - view', 'cv'))
        section.append(('cache - write', 'cw'))
        return menu

    def _make_library_menu_section(self, menu):
        section = menu.make_command_section(
            name='library',
            is_hidden=True,
            )
        section.append(('library - manage materials', 'lmm'))
        section.append(('library - manage stylesheets', 'lmy'))
        return section

    def _make_main_menu(self):
        menu = self._make_score_selection_menu()
        self._make_library_menu_section(menu)
        self._make_scores_menu_section(menu)
        self._make_scores_show_menu_section(menu)
        self._make_cache_menu_section(menu)
        menu._make_default_hidden_sections()
        return menu

    def _make_score_selection_menu(self):
        wrangler = self._score_package_wrangler
        if self._session.rewrite_cache:
            self._io_manager.write_cache(prompt=False)
            self._session._rewrite_cache = False
        menu_entries = self._io_manager._read_cache()
        if not menu_entries or \
            (self._session._scores_to_display == 'example' and
            not menu_entries[0][0] == 'Blue Example Score (2013)'):
            self._io_manager.write_cache(prompt=False)
            menu_entries = self._io_manager._read_cache()
        menu = self._io_manager.make_menu(
            where=self._where,
            include_default_hidden_sections=False,
            )
        asset_section = menu.make_asset_section()
        for menu_entry in menu_entries:
            asset_section.append(menu_entry)
        return menu

    def _make_scores_menu_section(self, menu):
        section = menu.make_command_section(
            name='scores - new',
            )
        section.append(('scores - new', 'new'))
        return section

    def _make_scores_show_menu_section(self, menu):
        section = menu.make_command_section(
            name='scores - show',
            is_hidden=True,
            )
        section.append(('scores - show all', 'ssl'))
        section.append(('scores - show active', 'ssv'))
        section.append(('scores - show examples', 'ssx'))
        section.append(('scores - show mothballed', 'ssmb'))
        section.append(('scores - show user', 'ssu'))
        return section

    def _run(
        self, 
        pending_user_input=None, 
        clear=True, 
        cache=False, 
        is_test=False, 
        display_active_scores=False,
        write_transcript=False,
        ):
        type(self).__init__(self)
        self._session._push_controller(self)
        self._io_manager._assign_user_input(
            pending_user_input=pending_user_input,
            )
        self._session._cache_breadcrumbs(cache=cache)
        self._session._push_breadcrumb(self._breadcrumb)
        if is_test:
            self._session._is_test = True
        self._session._write_transcript = write_transcript
        if display_active_scores:
            self._session.display_active_scores()
        run_main_menu = True
        while True:
            self._session._push_breadcrumb(self._score_status_string)
            if run_main_menu:
                menu = self._make_main_menu()
                result = menu._run(clear=clear)
            else:
                run_main_menu = True
            if self._session._backtrack(source='home'):
                self._session._pop_breadcrumb()
                self._session._clean_up()
                break
            elif self._session.is_navigating_to_next_score:
                self._session._is_navigating_to_next_score = False
                self._session._is_backtracking_to_score_manager = False
                result = self._get_next_score_directory_path()
            elif self._session.is_navigating_to_previous_score:
                self._session._is_navigating_to_previous_score = False
                self._session._is_backtracking_to_score_manager = False
                result = self._get_previous_score_directory_path()
            elif not result:
                self._session._pop_breadcrumb()
                continue
            self._handle_main_menu_result(result)
            if self._session._backtrack(source='home'):
                self._session._pop_breadcrumb()
                self._session._clean_up()
                break
            elif self._session.is_navigating_to_sibling_score:
                run_main_menu = False
            self._session._pop_breadcrumb()
        self._session._pop_controller()
        self._session._pop_breadcrumb()
        self._session._restore_breadcrumbs(cache=cache)

    ### PUBLIC METHODS ###

    def add(self, prompt=True):
        r'''Adds assets to repository.

        Returns none.
        '''
        self._score_package_wrangler.add()

    def commit(self, prompt=True):
        r'''Commits assets to repository.

        Returns none.
        '''
        self._score_package_wrangler.commit()

    def display_active_scores(self):
        r'''Displays active scores.

        Returns none.
        '''
        self._session.display_active_scores()

    def display_all_scores(self):
        r'''Displays all scores.

        Returns none.
        '''
        self._session.display_all_scores()

    def display_example_scores(self):
        r'''Displays example scores.

        Returns none.
        '''
        self._session.display_example_scores()

    def display_mothballed_scores(self):
        r'''Displays mothballed scores.

        Returns none.
        '''
        self._session.display_mothballed_scores()

    def display_user_scores(self):
        r'''Displays user scores.

        Returns none.
        '''
        self._session.display_user_scores()

    def doctest(self, prompt=True):
        r'''Runs doctest.

        Returns none.
        '''
        path = self._configuration.user_score_packages_directory_path
        command = 'ajv doctest {}'.format(path)
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        lines = [line.strip() for line in process.stdout.readlines()]
        if lines:
            lines.append('')
            self._io_manager.display(
                lines, 
                capitalize_first_character=False,
                )
        self._io_manager.proceed(prompt=prompt)

    def make_new_score(self):
        r'''Makes new score.

        Returns none.
        '''
        self._score_package_wrangler.make_asset(rollback=True)

    def manage_material_library(self):
        r'''Manages material library.

        Returns none.
        '''
        self._material_package_wrangler._run(
            rollback=True, 
            )

    def manage_score(self, score_package_path):
        r'''Manages score.

        Returns none.
        '''
        manager = self._score_package_wrangler._initialize_asset_manager(
            score_package_path)
        score_package_name = score_package_path.split('.')[-1]
        manager._session._current_score_snake_case_name = score_package_name
        manager._run(cache=True)

    def manage_stylesheet_library(self):
        r'''Manages stylesheet library.

        Returns none.
        '''
        self._stylesheet_wrangler._run(
            rollback=True, 
            )

    def pytest(self, prompt=True):
        r'''Runs py.test.

        Returns none.
        '''
        path = self._configuration.user_score_packages_directory_path
        command = 'py.test -rf {}'.format(path)
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        lines = [line.strip() for line in process.stdout.readlines()]
        if lines:
            lines.append('')
            self._io_manager.display(
                lines, 
                capitalize_first_character=False,
                )
        self._io_manager.proceed(prompt=prompt)

    def status(self, prompt=True):
        r'''Displays status of repository assets.
        
        Returns none.
        '''
        self._score_package_wrangler.status()

    def update(self, prompt=True):
        r'''Updates repository assets.

        Returns none.
        '''
        self._score_package_wrangler.update()

    def view_cache(self):
        r'''Views cache.

        Returns none.
        '''
        file_path = self._configuration.cache_file_path
        self._io_manager.open_file(file_path)
        self._session._hide_next_redraw = True

    def write_cache(self, prompt=True):
        r'''Writes cache.

        Returns none.
        '''
        self._io_manager.write_cache(prompt=prompt)
