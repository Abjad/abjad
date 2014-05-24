# -*- encoding: utf-8 -*-
import os
from abjad.tools import sequencetools
from abjad.tools import stringtools
from scoremanager.wranglers.PackageWrangler import PackageWrangler


class ScorePackageWrangler(PackageWrangler):
    r'''Score package wrangler.

    ..  container:: example

        ::

            >>> session = scoremanager.core.Session()
            >>> wrangler = scoremanager.wranglers.ScorePackageWrangler(
            ...     session=session,
            ...     )
            >>> wrangler
            ScorePackageWrangler()

    ..  container:: example

        ::

            >>> session = scoremanager.core.Session()
            >>> session._set_test_score('red_example_score')
            >>> wrangler_in_score = scoremanager.wranglers.ScorePackageWrangler(
            ...     session=session,
            ...     )
            >>> wrangler_in_score
            ScorePackageWrangler()

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_only_example_scores_during_test',
        )

    ### INITIALIZER ###

    def __init__(self, session=None):
        from scoremanager import managers
        superclass = super(ScorePackageWrangler, self)
        superclass.__init__(session=session)
        path = self._configuration.example_score_packages_directory
        self._abjad_storehouse_path = path
        self._asset_identifier = 'score package'
        self._basic_breadcrumb = 'scores'
        self._include_asset_name = False
        self._annotate_year = True
        self._manager_class = managers.ScorePackageManager
        self._only_example_scores_during_test = True
        self._sort_by_annotation = False
        path = self._configuration.user_score_packages_directory
        self._user_storehouse_path = path

    ### PRIVATE PROPERTIES ###

    @property
    def _breadcrumb(self):
        return

    @property
    def _current_storehouse_path(self):
        if self._session.is_in_score:
            path = self._configuration.example_score_packages_directory
            directory_entries = sorted(os.listdir(path))
            manager = self._session.current_score_package_manager
            score_name = manager._package_name
            if score_name in directory_entries:
                return path
            else:
                return self._configuration.user_score_packages_directory
        else:
            return self._configuration.user_score_packages_directory

    @property
    def _input_to_method(self):
        superclass = super(ScorePackageWrangler, self)
        result = superclass._input_to_method
        result = result.copy()
        result.update({
            'co': self.open_cache,
            'cw': self.write_cache,
            #
            'fix*': self.fix_every_package,
            'spo*': self.open_every_score_pdf,
            })
        return result

    ### PRIVATE METHODS ###

    def _find_git_manager(self, must_have_file=False):
        superclass = super(ScorePackageWrangler, self)
        manager = superclass._find_git_manager(
            inside_score=False,
            must_have_file=must_have_file,
            )
        return manager

    def _find_svn_manager(self, must_have_file=False):
        superclass = super(ScorePackageWrangler, self)
        manager = superclass._find_svn_manager(
            inside_score=False,
            must_have_file=must_have_file,
            )
        return manager

    def _find_svn_score_name(self):
        from scoremanager import managers
        manager = self._find_up_to_date_manager(
            repository='svn',
            system=False,
            )
        if manager:
            title = manager._get_title()
            title = stringtools.to_accent_free_snake_case(title)
            return title

    def _get_scores_to_display_string(self):
        view = self._read_view()
        if view:
            view_name = self._read_view_name()
            return 'scores ({})'.format(view_name)
        return 'scores'

    def _get_sibling_score_directory(self, next_=True):
        paths = self._list_visible_asset_paths()
        if self._session.last_asset_path is None:
            if next_:
                return paths[0]
            else:
                return paths[-1]
        score_path = self._session.last_score_package_path
        index = paths.index(score_path)
        if next_:
            sibling_index = (index + 1) % len(paths)
        else:
            sibling_index = (index - 1) % len(paths)
        sibling_path = paths[sibling_index]
        return sibling_path
        
    def _get_sibling_score_path(self):
        if self._session.is_navigating_to_next_score:
            self._session._is_navigating_to_next_score = False
            self._session._is_backtracking_to_score_manager = False
            return self._get_sibling_score_directory(next_=True)
        if self._session.is_navigating_to_previous_score:
            self._session._is_navigating_to_previous_score = False
            self._session._is_backtracking_to_score_manager = False
            return self._get_sibling_score_directory(next_=False)

    def _handle_numeric_user_input(self, result):
        paths = self._list_visible_asset_paths()
        if result in paths:
            path = result
            manager = self._initialize_manager(path)
            package_name = os.path.basename(path)
            manager.fix_package(confirm=False, display=False)
            if self._session.is_backtracking:
                return
            manager._run()

    def _is_valid_directory_entry(self, expr):
        superclass = super(ScorePackageWrangler, self)
        if superclass._is_valid_directory_entry(expr):
            if '.' not in expr:
                return True
        return False

    def _make_all_packages_menu_section(self, menu):
        commands = []
        commands.append(('all packages - __init__.py - list', 'nls*'))
        commands.append(('all packages - __init__.py - open', 'no*'))
        commands.append(('all packages - __init__.py - stub', 'ns*'))
        commands.append(('all packages - __metadata__.py - list', 'mdls*'))
        commands.append(('all packages - __metadata__.py - open', 'mdo*'))
        commands.append(('all packages - __metadata__.py - rewrite', 'mdw*'))
        commands.append(('all packages - fix', 'fix*'))
        commands.append(('all packages - score.pdf - open', 'spo*'))
        menu.make_command_section(
            is_hidden=True,
            commands=commands,
            name='zzz',
            )

    def _make_asset_menu_section(self, menu):
        entries = self._read_cache()
        if self._session.is_test:
            entries = [_ for _ in entries if 'Example Score' in _[0]]
        else:
            entries = self._filter_asset_menu_entries_by_view(entries)
        if entries:
            menu.make_asset_section(menu_entries=entries)

    def _make_cache_menu_section(self, menu):
        commands = []
        commands.append(('cache - open', 'co'))
        commands.append(('cache - write', 'cw'))
        menu.make_command_section(
            is_hidden=True,
            commands=commands,
            name='cache',
            )

    def _make_main_menu(self):
        superclass = super(ScorePackageWrangler, self)
        menu = superclass._make_main_menu()
        breadcrumb_callback=self._get_scores_to_display_string
        menu._breadcrumb_callback = breadcrumb_callback
        self._make_all_packages_menu_section(menu)
        self._make_scores_menu_section(menu)
        self._make_cache_menu_section(menu)
        return menu

    def _make_scores_menu_section(self, menu):
        commands = []
        commands.append(('scores - copy', 'cp'))
        commands.append(('scores - new', 'new'))
        commands.append(('scores - remove', 'rm'))
        commands.append(('scores - rename', 'ren'))
        menu.make_command_section(
            commands=commands,
            name='scores',
            )

    def _read_cache(self):
        start_menu_entries = []
        if os.path.exists(self._configuration.cache_file_path):
            path = self._configuration.cache_file_path
            with open(path, 'r') as file_pointer:
                cache_lines = file_pointer.read()
            try:
                local_dict = {}
                exec(cache_lines, globals(), local_dict)
                start_menu_entries = local_dict.get('start_menu_entries', [])
            except SyntaxError:
                pass
        return start_menu_entries

    ### PUBLIC METHODS ###

    def copy_package(self):
        r'''Copies package.

        Returns none.
        '''
        path = self._configuration.user_score_packages_directory
        self._copy_asset(new_storehouse=path)
        self.write_cache(confirm=False, display=False)

    def fix_every_package(self, confirm=True, display=True):
        r'''Fixes every package.

        Returns none.
        '''
        from scoremanager import managers
        paths = self._list_visible_asset_paths()
        messages = []
        for path in paths:
            manager = self._initialize_manager(path)
            needed_to_be_fixed = manager.fix_package(
                confirm=confirm,
                display=display,
                )
            if not needed_to_be_fixed:
                title = manager._get_title()
                message = '{} OK.'
                message = message.format(title)
                messages.append(message)
        message = '{} score packages checked.'
        message = message.format(len(paths))
        messages.append(message)
        self._io_manager._display(messages)

    def make_package(self):
        r'''Makes package.

        Returns none.
        '''
        path = self._get_available_path()
        if self._session.is_backtracking:
            return
        if not path:
            return
        self._make_asset(path)
        self.write_cache(confirm=False, display=False)

    def open_cache(self):
        r'''Opens cache.

        Returns none.
        '''
        file_path = self._configuration.cache_file_path
        self._io_manager.open_file(file_path)

    def open_every_score_pdf(self, confirm=True, display=True):
        r'''Opens ``score.pdf`` in every package.

        Returns none.
        '''
        with self._io_manager._make_interaction(display=display):
            managers = self._list_visible_asset_managers()
            paths = []
            for manager in managers:
                inputs, outputs = manager.open_score_pdf(dry_run=True)
                paths.extend(inputs)
            if display:
                messages = ['will open ...']
                tab = self._io_manager._make_tab()
                paths = [tab + _ for _ in paths]
                messages.extend(paths)
                self._io_manager._display(messages)
            if confirm:
                result = self._io_manager._confirm()
                if self._session.is_backtracking:
                    return
                if not result:
                    return
            if paths:
                self._io_manager.open_file(paths)

    def remove_packages(self):
        r'''Removes one or more packages.
        
        Returns none.
        '''
        self._remove_assets()

    def rename_package(self):
        r'''Renames package.

        Returns none.
        '''
        self._rename_asset()

    def write_cache(self, confirm=True, display=True):
        r'''Writes cache.

        Returns none.
        '''
        lines = []
        lines.append(self._configuration.unicode_directive)
        lines.append('')
        lines.append('')
        lines.append('start_menu_entries = [')
        menu_entries = self._make_asset_menu_entries(
            apply_current_directory=False,
            apply_view=False,
            )
        for menu_entry in menu_entries:
            lines.append('{},'.format(menu_entry))
        lines.append(']')
        contents = '\n'.join(lines)
        cache_file_path = self._configuration.cache_file_path
        self._io_manager.write(cache_file_path, contents)
        if display:
            message = 'wrote {}.'.format(cache_file_path)
            self._io_manager._display(message)