# -*- encoding: utf-8 -*-
import os
from abjad.tools import sequencetools
from abjad.tools import stringtools
from scoremanager.wranglers.Wrangler import Wrangler


class ScorePackageWrangler(Wrangler):
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
        path = self._configuration.example_score_packages_directory_path
        self._abjad_storehouse_path = path
        self._asset_identifier = 'score package'
        self._basic_breadcrumb = 'scores'
        self._include_asset_name = False
        self._annotate_year = True
        self._manager_class = managers.ScorePackageManager
        self._only_example_scores_during_test = True
        self._sort_by_annotation = False
        path = self._configuration.user_score_packages_directory_path
        self._user_storehouse_path = path

    ### PRIVATE PROPERTIES ###

    @property
    def _current_storehouse_path(self):
        if self._session.is_in_score:
            path = self._configuration.example_score_packages_directory_path
            directory_entries = sorted(os.listdir(path))
            manager = self._session.current_score_package_manager
            score_name = manager._package_name
            if score_name in directory_entries:
                return path
            else:
                return self._configuration.user_score_packages_directory_path
        else:
            return self._configuration.user_score_packages_directory_path

    @property
    def _input_to_action(self):
        superclass = super(ScorePackageWrangler, self)
        result = superclass._input_to_action
        result = result.copy()
        result.update({
            'cp': self.copy_package,
            'co': self.open_cache,
            'cw': self.write_cache,
            'd': self._session._score_manager._distribution_file_wrangler._run,
            'fix': self.fix_packages,
            'g': self._session._score_manager._segment_package_wrangler._run,
            'k': self._session._score_manager._maker_module_wrangler._run,
            'm': self._session._score_manager._material_package_wrangler._run,
            'mdmls': self.list_metadata_pys,
            'mdmo': self.open_metadata_pys,
            'mdmrw': self.rewrite_metadata_pys,
            'new': self.make_package,
            'rad': self.add_to_repository,
            'rci': self.commit_to_repository,
            'ren': self.rename_package,
            'rm': self.remove_packages,
            'rrv': self.revert_to_repository,
            'rst': self.repository_status,
            'rup': self.update_from_repository,
            'u': self._session._score_manager._build_file_wrangler._run,
            'y': self._session._score_manager._stylesheet_wrangler._run,
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
            managers.ScorePackageManager,
            repository='svn',
            system=False,
            )
        if manager:
            title = manager._get_title()
            title = stringtools.to_accent_free_snake_case(title)
            return title

    def _get_scores_to_display_string(self):
        if self._session.is_test:
            return 'example scores'
        view = self._read_view()
        if view:
            view_name = self._read_view_name()
            return 'scores ({})'.format(view_name)
        return 'scores'

    def _get_sibling_score_directory_path(self, next_=True):
        paths = self._list_visible_asset_paths()
        if self._session.last_asset_path is None:
            if next_:
                return paths[0]
            else:
                return paths[-1]
        score_path = self._session.last_asset_path
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
            return self._get_sibling_score_directory_path(next_=True)
        if self._session.is_navigating_to_previous_score:
            self._session._is_navigating_to_previous_score = False
            self._session._is_backtracking_to_score_manager = False
            return self._get_sibling_score_directory_path(next_=False)

    def _handle_main_menu_result(self, result):
        if result in self._input_to_action:
            self._input_to_action[result]()
        elif result == 'user entered lone return':
            pass
        else:
            paths = self._list_visible_asset_paths()
            if result in paths:
                path = result
                manager = self._initialize_manager(path)
                package_name = os.path.basename(path)
                manager.fix_package(confirm=False, display=False)
                if self._should_backtrack():
                    return
                manager._run()

    def _is_valid_directory_entry(self, expr):
        superclass = super(ScorePackageWrangler, self)
        if superclass._is_valid_directory_entry(expr):
            if '.' not in expr:
                return True
        return False

    def _list_all_directories_with_metadata_pys(self):
        directories = []
        paths = self._list_visible_asset_paths()
        for path in paths:
            result = self._list_directories_with_metadata_pys(path)
            directories.extend(result)
        return directories

    def _make_all_score_packages_menu_section(self, menu):
        commands = []
        commands.append(('all - metadata modules - edit', 'mdmo'))
        commands.append(('all - metadata modules - list', 'mdmls'))
        commands.append(('all - metadata modules - rewrite', 'mdmrw'))
        commands.append(('all - score packages - fix', 'fix'))
        commands.append(('all - unadded assets - remove', 'uar'))
        menu.make_command_section(
            is_hidden=True,
            commands=commands,
            name='all score packages',
            )

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
        menu = self._make_score_selection_menu()
        self._make_all_score_packages_menu_section(menu)
        self._make_scores_menu_section(menu)
        self._make_cache_menu_section(menu)
        self._make_views_menu_section(menu)
        return menu

    def _make_score_selection_menu(self):
        menu = self._io_manager.make_menu(
            name='main',
            breadcrumb_callback=self._get_scores_to_display_string,
            )
        entries = self._io_manager._read_cache()
        if self._session.is_test:
            entries = [_ for _ in entries if 'Example Score' in _[0]]
        else:
            entries = self._filter_asset_menu_entries_by_view(entries)
        if entries:
            menu.make_asset_section(menu_entries=entries)
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

    ### PUBLIC METHODS ###

    def copy_package(self):
        r'''Copies score package.

        Returns none.
        '''
        path = self._configuration.user_score_packages_directory_path
        self._copy_asset(new_storehouse=path)
        self.write_cache(confirm=False, display=False)

    def fix_packages(self, confirm=True, display=True):
        r'''Fixes visible score packages.

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
        messages.append('')
        message = '{} score packages checked.'
        message = message.format(len(paths))
        messages.append(message)
        messages.append('')
        self._io_manager.display(messages)
        self._session._hide_next_redraw = True

    def list_metadata_pys(self):
        r'''Lists metadata modules in all visible score packages.

        Returns none.
        '''
        directories = self._list_all_directories_with_metadata_pys()
        paths = [os.path.join(_, '__metadata__.py') for _ in directories]
        messages = paths[:]
        messages.append('')
        self._io_manager.display(messages)
        message = '{} metadata modules found.'
        message = message.format(len(paths))
        self._io_manager.display([message, ''])
        self._session._hide_next_redraw = True

    def make_package(self):
        r'''Makes score package.

        Returns none.
        '''
        path = self._get_available_path()
        if self._should_backtrack():
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
        self._session._hide_next_redraw = True

    def open_metadata_pys(self):
        r'''Edits metadata modules in all visible score packages.

        Returns none.
        '''
        directories = self._list_all_directories_with_metadata_pys()
        paths = [os.path.join(_, '__metadata__.py') for _ in directories]
        self._io_manager.open_file(paths)

    def remove_packages(self):
        r'''Removes one or more score packages.
        
        Returns none.
        '''
        self._remove_assets()

    def rename_package(self):
        r'''Renames score package.

        Returns none.
        '''
        self._rename_asset()

    def rewrite_metadata_pys(self, confirm=True, display=True):
        r'''Rewrites metadata modules in all visible score packages.

        Returns none.
        '''
        directories = self._list_all_directories_with_metadata_pys()
        messages = []
        for directory in directories:
            path = os.path.join(directory, '__metadata__.py')
            message = 'rewriting {} ...'.format(path)
            messages.append(message)
            manager = self._io_manager.make_package_manager(directory)
            manager.rewrite_metadata_py(confirm=False, display=False)
        if display:
            messages.append('')
            message = '{} metadata modules rewritten.'
            message = message.format(len(directories))
            messages.append(message)
            messages.append('')
            self._io_manager.display(messages)
            self._session._hide_next_redraw = True

    def write_cache(self, confirm=True, display=True):
        r'''Writes cache.

        Returns none.
        '''
        lines = []
        lines.append(self._unicode_directive)
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
            self._io_manager.display([message, ''])
            self._session._hide_next_redraw = True