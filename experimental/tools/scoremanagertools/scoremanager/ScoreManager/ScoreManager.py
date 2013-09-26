# -*- encoding: utf-8 -*-
import os
import subprocess
from experimental.tools.scoremanagertools.scoremanager.ScoreManagerObject \
    import ScoreManagerObject


class ScoreManager(ScoreManagerObject):
    r'''Score manager.

    ::

        >>> score_manager = scoremanagertools.scoremanager.ScoreManager()
        >>> score_manager
        ScoreManager()

    Return score manager.
    '''

    ### INITIALIZER ###

    def __init__(self, session=None):
        from experimental.tools import scoremanagertools
        ScoreManagerObject.__init__(self, session=session)
        self._segment_package_wrangler = \
            scoremanagertools.wranglers.SegmentPackageWrangler(
            session=self.session)
        self._material_package_maker_wrangler = \
            scoremanagertools.wranglers.MaterialPackageMakerWrangler(
            session=self.session)
        self._material_package_wrangler = \
            scoremanagertools.wranglers.MaterialPackageWrangler(
            session=self.session)
        self._score_package_wrangler = \
            scoremanagertools.wranglers.ScorePackageWrangler(
            session=self.session)
        self._stylesheet_file_wrangler = \
            scoremanagertools.wranglers.StylesheetFileWrangler(
            session=self.session)

    ### PRIVATE PROPERTIES ###

    @property
    def _breadcrumb(self):
        return 'score manager'

    @property
    def _score_status_string(self):
        return '{} scores'.format(self.session.scores_to_show)

    ### PRIVATE METHODS ###

    def _get_next_score_package_name(self):
        score_package_names = self.score_package_wrangler.list_asset_names()
        if self.session.snake_case_current_score_name is None:
            return score_package_names[0]
        index = score_package_names.index(
            self.session.snake_case_current_score_name)
        next_index = (index + 1) % len(score_package_names)
        return score_package_names[next_index]

    def _get_prev_score_package_name(self):
        score_package_names = self.score_package_wrangler.list_asset_names()
        if self.session.snake_case_current_score_name is None:
            return score_package_names[-1]
        index = score_package_names.index(
            self.session.snake_case_current_score_name)
        prev_index = (index - 1) % len(score_package_names)
        return score_package_names[prev_index]

    def _handle_main_menu_result(self, result):
        if result in self.user_input_to_action:
            self.user_input_to_action[result](self)
        else:
            wrangler = self.score_package_wrangler
            if result in wrangler.list_visible_asset_packagesystem_paths():
                self.interactively_edit_score(result)

    def _handle_svn_menu_result(self, result):
        r'''Return true to exit the svn menu.
        '''
        this_result = False
        if result == 'add':
            self.score_package_wrangler.svn_add_assets()
        elif result == 'ci':
            self.score_package_wrangler.svn_ci_assets()
        elif result == 'st':
            self.score_package_wrangler.svn_st_assets()
        elif result == 'up':
            self.score_package_wrangler.svn_up_assets()
            return True
        return this_result

    def _make_main_menu(self):
        menu = self._make_score_selection_menu()
        command_section = menu.make_command_section()
        command_section.append(('materials', 'm'))
        command_section.append(('stylesheets', 'y'))
        command_section.append(('new score', 'new'))
        hidden_section = menu.make_command_section(is_hidden=True)
        hidden_section.append(('show active scores only', 'active'))
        hidden_section.append(('show all scores', 'all'))
        hidden_section.append(('fix all score package structures', 'fix'))
        hidden_section.append(('show mothballed scores only', 'mb'))
        hidden_section.append(('profile packages', 'profile'))
        hidden_section.append(('run py.test on all scores', 'py.test'))
        hidden_section.append(('work with repository', 'svn'))
        hidden_section.append(('write cache', 'wc'))
        return menu

    def _make_score_selection_menu(self):
        if self.session.is_first_run:
            if hasattr(self, 'start_menu_entries'):
                menu_entries = self.start_menu_entries
            else:
                self.write_cache()
                menu_entries = \
                    self.score_package_wrangler._make_asset_menu_entries()
            self.session.is_first_run = False
        else:
            menu_entries = \
                self.score_package_wrangler._make_asset_menu_entries()
        menu = self.session.io_manager.make_menu(where=self._where)
        asset_section = menu.make_asset_section()
        asset_section.menu_entries = menu_entries
        return menu

    def _make_svn_menu(self):
        menu = self.session.io_manager.make_menu(where=self._where)
        command_section = menu.make_command_section()
        command_section.append(('svn add scores', 'add'))
        command_section.append(('svn commit scores', 'ci'))
        command_section.append(('svn status scores', 'st'))
        command_section.append(('svn update scores', 'up'))
        return menu

    def _run(self, 
        pending_user_input=None, 
        clear=True, 
        cache=False, 
        is_test=False, 
        dump_transcript=False):
        type(self).__init__(self)
        self.session.io_manager.assign_user_input(
            pending_user_input=pending_user_input)
        self.session.cache_breadcrumbs(cache=cache)
        self.session.push_breadcrumb(self._breadcrumb)
        if is_test:
            self.session.is_test = True
        self.session.dump_transcript = dump_transcript
        run_main_menu = True
        while True:
            self.session.push_breadcrumb(self._score_status_string)
            if run_main_menu:
                menu = self._make_main_menu()
                result = menu._run(clear=clear)
            else:
                run_main_menu = True
            if self.session.backtrack(source='home'):
                self.session.pop_breadcrumb()
                self.session.clean_up()
                break
            elif self.session.is_navigating_to_next_score:
                self.session.is_navigating_to_next_score = False
                self.session.is_backtracking_to_score_manager = False
                result = self._get_next_score_package_name()
            elif self.session.is_navigating_to_prev_score:
                self.session.is_navigating_to_prev_score = False
                self.session.is_backtracking_to_score_manager = False
                result = self._get_prev_score_package_name()
            elif not result:
                self.session.pop_breadcrumb()
                continue
            self._handle_main_menu_result(result)
            if self.session.backtrack(source='home'):
                self.session.pop_breadcrumb()
                self.session.clean_up()
                break
            elif self.session.is_navigating_to_sibling_score:
                run_main_menu = False
            self.session.pop_breadcrumb()
        self.session.pop_breadcrumb()
        self.session.restore_breadcrumbs(cache=cache)

    ### PUBLIC PROPERTIES ###

    @property
    def material_package_maker_wrangler(self):
        r'''Score manager material package maker wrangler:

        ::

            >>> score_manager.material_package_maker_wrangler
            MaterialPackageMakerWrangler()

        Return material package maker wrangler.
        '''
        return self._material_package_maker_wrangler

    @property
    def material_package_wrangler(self):
        r'''Score manager material package wrangler:

        ::

            >>> score_manager.material_package_wrangler
            MaterialPackageWrangler()

        Return material package wrangler.
        '''
        return self._material_package_wrangler

    @property
    def score_package_wrangler(self):
        r'''Score manager score package wrangler:

        ::

            >>> score_manager.score_package_wrangler
            ScorePackageWrangler()

        Return score package wrangler.
        '''
        return self._score_package_wrangler

    @property
    def segment_package_wrangler(self):
        r'''Score manager segment package wrangler:

        ::

            >>> score_manager.segment_package_wrangler
            SegmentPackageWrangler()

        Return segment package wrangler.
        '''
        return self._segment_package_wrangler

    @property
    def stylesheet_file_wrangler(self):
        r'''Score manager stylesheet file wrangler:

        ::

            >>> score_manager.stylesheet_file_wrangler
            StylesheetFileWrangler()

        Return stylesheet file wrangler.
        '''
        return self._stylesheet_file_wrangler

    ### PUBLIC METHODS ###

    def display_active_scores(self):
        self.session.display_active_scores()

    def display_all_scores(self):
        self.session.display_all_scores()

    def display_mothballed_scores(self):
        self.session.display_mothballed_scores()

    def fix_visible_scores(self):
        self.score_package_wrangler.fix_visible_assets()

    def interactively_edit_score(self, score_package_path):
        proxy = self.score_package_wrangler._initialize_asset_proxy(
            score_package_path)
        proxy.session.snake_case_current_score_name = \
            score_package_path
        proxy._run(cache=True)
        self.session.snake_case_current_score_name = None

    def interactively_make_new_score(self):
        self.score_package_wrangler.interactively_make_asset(rollback=True)

    def manage_materials(self):
        self.material_package_wrangler._run(
            rollback=True, 
            head=self.configuration.built_in_material_packages_package_path,
            )

    def manage_stylesheets(self):
        self.stylesheet_file_wrangler._run(
            rollback=True, 
            #head=self.configuration.built_in_stylesheets_directory_path,
            head='scoremanagertools.stylesheets',
            )

    def manage_svn(self, clear=True):
        while True:
            self.session.push_breadcrumb('repository commands')
            menu = self._make_svn_menu()
            result = menu._run(clear=clear)
            if self.session.is_backtracking_to_score:
                self.session.is_backtracking_to_score = False
                self.session.pop_breadcrumb()
                continue
            elif self.session.backtrack():
                break
            self._handle_svn_menu_result(result)
            if self.session.backtrack():
                break
            self.session.pop_breadcrumb()
        self.session.pop_breadcrumb()

    def profile_visible_scores(self):
        self.score_package_wrangler.profile_visible_assets()

    def run_py_test_on_all_user_scores(self, prompt=True):
        command = 'py.test {}'.format(
            self.configuration.user_score_packages_directory_path)
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        lines = [line.strip() for line in proc.stdout.readlines()]
        if lines:
            self.session.io_manager.display(
                lines, capitalize_first_character=False)
        line = 'tests complete.'
        self.session.io_manager.proceed(line, is_interactive=prompt)

    def write_cache(self):
        cache_file_path = os.path.join(
                self.configuration.configuration_directory_path, 'cache.py')
        cache_file_pointer = file(cache_file_path, 'w')
        cache_file_pointer.write('start_menu_entries = [\n')
        menu_entries = self.score_package_wrangler._make_asset_menu_entries()
        for menu_entry in menu_entries:
            cache_file_pointer.write('{},\n'.format(menu_entry))
        cache_file_pointer.write(']\n')
        cache_file_pointer.close()

    ### UI MANIFEST ###

    user_input_to_action = {
        'active':   display_active_scores,
        'all':      display_all_scores,
        'fix':      fix_visible_scores,
        'm':        manage_materials,
        'mb':       display_mothballed_scores,
        'new':      interactively_make_new_score,
        'profile':  profile_visible_scores,
        'py.test':  run_py_test_on_all_user_scores,
        'svn':      manage_svn,
        'y':        manage_stylesheets,
        'wc':       write_cache,
        }
