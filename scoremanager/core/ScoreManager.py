# -*- encoding: utf-8 -*-
import os
import subprocess
from scoremanager.core.ScoreManagerObject import ScoreManagerObject


class ScoreManager(ScoreManagerObject):
    r'''Score manager.

    ..  container:: example

        ::

            >>> score_manager = scoremanager.core.ScoreManager()
            >>> score_manager
            ScoreManager()

    '''

    ### INITIALIZER ###

    def __init__(self, session=None):
        from scoremanager import wranglers
        ScoreManagerObject.__init__(self, session=session)
        self._session._score_manager = self
        wrangler = wranglers.SegmentPackageWrangler(session=self._session)
        self._segment_package_wrangler = wrangler
        wrangler = wranglers.MaterialPackageManagerWrangler(
            session=self._session)
        self._material_package_manager_wrangler = wrangler
        wrangler = wranglers.MaterialPackageWrangler(session=self._session)
        self._material_package_wrangler = wrangler
        wrangler = wranglers.ScorePackageWrangler(session=self._session)
        self._score_package_wrangler = wrangler
        wrangler = wranglers.StylesheetFileWrangler(session=self._session)
        self._stylesheet_file_wrangler = wrangler

    ### PRIVATE PROPERTIES ###

    @property
    def _breadcrumb(self):
        return 'score manager'

    @property
    def _score_status_string(self):
        return '{} scores'.format(self._session.scores_to_display)

    ### PRIVATE METHODS ###

    def _get_next_score_package_name(self):
        score_package_names = self._score_package_wrangler.list_asset_names()
        if self._session.current_score_snake_case_name is None:
            return score_package_names[0]
        index = score_package_names.index(
            self._session.current_score_snake_case_name)
        next_index = (index + 1) % len(score_package_names)
        return score_package_names[next_index]

    def _get_previous_score_package_name(self):
        score_package_names = self._score_package_wrangler.list_asset_names()
        if self._session.current_score_snake_case_name is None:
            return score_package_names[-1]
        index = score_package_names.index(
            self._session.current_score_snake_case_name)
        prev_index = (index - 1) % len(score_package_names)
        return score_package_names[prev_index]

    def _handle_main_menu_result(self, result):
        if result in self.user_input_to_action:
            self.user_input_to_action[result](self)
        else:
            wrangler = self._score_package_wrangler
            if result in wrangler.list_visible_asset_packagesystem_paths():
                self.manage_score(result)

    def _make_main_menu(self):
        menu = self._make_score_selection_menu()
        section = menu.make_command_section()
        section.append(('scores - new', 'new'))
        section = menu.make_command_section(is_secondary=True)
        section.append(('cache - view', 'cv'))
        section.append(('cache - write', 'cw'))
        section = menu.make_command_section(is_secondary=True)
        section.append(('library - manage materials', 'lmm'))
        section.append(('library - manage stylesheets', 'lmy'))
        section = menu.make_command_section(is_secondary=True)
        section.append(('scores - show all', 'ssl'))
        section.append(('scores - show active', 'ssv'))
        section.append(('scores - show examples', 'ssx'))
        section.append(('scores - show mothballed', 'ssmb'))
        menu._make_default_hidden_sections()
        return menu

    def _make_score_selection_menu(self):
        wrangler = self._score_package_wrangler
        if self._session.rewrite_cache:
            self._session.io_manager.write_cache(prompt=False)
            self._session.rewrite_cache = False
        menu_entries = self._session.io_manager._read_cache()
        if (self._session._scores_to_display == 'example' and
            not menu_entries[0][0] == 'Blue Example Score (2013)') or \
            not menu_entries:
            self._session.io_manager.write_cache(prompt=False)
            menu_entries = self._session.io_manager._read_cache()
        menu = self._session.io_manager.make_menu(
            where=self._where,
            include_default_hidden_sections=False,
            )
        asset_section = menu.make_asset_section()
        asset_section.menu_entries = menu_entries
        return menu

    def _run(
        self, 
        pending_user_input=None, 
        clear=True, 
        cache=False, 
        is_test=False, 
        display_active_scores=False,
        dump_transcript=False,
        ):
        type(self).__init__(self)
        self._session._push_controller(self)
        self._session.io_manager._assign_user_input(
            pending_user_input=pending_user_input,
            )
        self._session._cache_breadcrumbs(cache=cache)
        self._session._push_breadcrumb(self._breadcrumb)
        if is_test:
            self._session.is_test = True
        self._session.dump_transcript = dump_transcript
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
                self._session.is_navigating_to_next_score = False
                self._session.is_backtracking_to_score_manager = False
                result = self._get_next_score_package_name()
            elif self._session.is_navigating_to_previous_score:
                self._session.is_navigating_to_previous_score = False
                self._session.is_backtracking_to_score_manager = False
                result = self._get_previous_score_package_name()
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

    def add_assets_to_repository(self, prompt=True):
        r'''Adds assets to repository.

        Returns none.
        '''
        self._score_package_wrangler.add_assets_to_repository()

    def commit_assets_to_repository(self, prompt=True):
        r'''Commits assets to repository.

        Returns none.
        '''
        self._score_package_wrangler.commit_assets_to_repository()

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

    def display_repository_status(self, prompt=True):
        r'''Displays status of repository assets.
        
        Returns none.
        '''
        self._score_package_wrangler.display_repository_status()

    def make_new_score(self):
        r'''Makes new score.

        Returns none.
        '''
        self._score_package_wrangler.interactively_make_asset(rollback=True)

    def manage_material_library(self):
        r'''Manages material library.

        Returns none.
        '''
        self._material_package_wrangler._run(
            rollback=True, 
            head=self.configuration.built_in_material_packages_package_path,
            )

    def manage_score(self, score_package_path):
        r'''Manages score.

        Returns none.
        '''
        manager = self._score_package_wrangler._initialize_asset_manager(
            score_package_path)
        score_package_name = score_package_path.split('.')[-1]
        manager._session.current_score_snake_case_name = score_package_name
        manager._run(cache=True)
        self._session.current_score_snake_case_name = None

    def manage_stylesheet_library(self):
        r'''Manages stylesheet library.

        Returns none.
        '''
        self._stylesheet_file_wrangler._run(
            rollback=True, 
            )

    def run_doctest(self, prompt=True):
        r'''Runs doctest.

        Returns none.
        '''
        path = self.configuration.user_score_packages_directory_path
        command = 'ajv doctest {}'.format(path)
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        lines = [line.strip() for line in process.stdout.readlines()]
        if lines:
            lines.append('')
            self._session.io_manager.display(
                lines, 
                capitalize_first_character=False,
                )
        self._session.io_manager.proceed(prompt=prompt)

    def run_pytest(self, prompt=True):
        r'''Runs py.test.

        Returns none.
        '''
        path = self.configuration.user_score_packages_directory_path
        command = 'py.test -rf {}'.format(path)
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        lines = [line.strip() for line in process.stdout.readlines()]
        if lines:
            lines.append('')
            self._session.io_manager.display(
                lines, 
                capitalize_first_character=False,
                )
        self._session.io_manager.proceed(prompt=prompt)

    def update_from_repository(self, prompt=True):
        r'''Updates repository assets.

        Returns none.
        '''
        self._score_package_wrangler.update_from_repository()

    def view_cache(self):
        r'''Views cache.

        Returns none.
        '''
        file_path = self.configuration.cache_file_path
        self._session.io_manager.open_file(file_path)

    def write_cache(self, prompt=True):
        r'''Writes cache.

        Returns none.
        '''
        self._session.io_manager.write_cache(prompt=prompt)

    ### UI MANIFEST ###

    user_input_to_action = {
        'cv': view_cache,
        'cw': write_cache,
        'lmm': manage_material_library,
        'new': make_new_score,
        'radd': add_assets_to_repository,
        'rci': commit_assets_to_repository,
        'rst': display_repository_status,
        'rup': update_from_repository,
        'ssl': display_all_scores,
        'ssv': display_active_scores,
        'ssmb': display_mothballed_scores,
        'ssx': display_example_scores,
        'lmy': manage_stylesheet_library,
        }
