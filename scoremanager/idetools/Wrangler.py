# -*- encoding: utf-8 -*-
import copy
import doctest
import os
import shutil
import subprocess
import traceback
from abjad.tools import datastructuretools
from abjad.tools import developerscripttools
from abjad.tools import sequencetools
from abjad.tools import stringtools
from abjad.tools import systemtools
from scoremanager.idetools.ScoreInternalAssetController import \
    ScoreInternalAssetController


class Wrangler(ScoreInternalAssetController):
    r'''Wrangler.

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_abjad_storehouse_path',
        '_allow_depot',
        '_asset_identifier',
        '_basic_breadcrumb',
        '_force_lowercase',
        '_in_library',
        '_main_menu',
        '_manager_class',
        '_score_storehouse_path_infix_parts',
        '_sort_by_annotation',
        '_user_storehouse_path',
        )

    ### INITIALIZER ###

    def __init__(self, session=None):
        from scoremanager import idetools
        assert session is not None
        superclass = super(Wrangler, self)
        superclass.__init__(session=session)
        self._abjad_storehouse_path = None
        self._allow_depot = True
        self._asset_identifier = None
        self._basic_breadcrumb = None
        self._force_lowercase = True
        self._in_library = False
        self._manager_class = idetools.PackageManager
        self._score_storehouse_path_infix_parts = ()
        self._sort_by_annotation = True
        self._user_storehouse_path = None

    ### PRIVATE PROPERTIES ###

    @property
    def _breadcrumb(self):
        breadcrumb = self._basic_breadcrumb
        if not self._allow_depot:
            pass
        elif self._session.is_in_score:
            breadcrumb = '{} directory'.format(breadcrumb)
        else:
            breadcrumb = '{} depot'.format(breadcrumb)
        view_name = self._read_view_name()
        if not view_name:
            return breadcrumb
        view_inventory = self._read_view_inventory()
        if view_inventory is not None and view_name in view_inventory:
            breadcrumb = '{} [{}]'.format(breadcrumb, view_name)
        return breadcrumb

    @property
    def _command_to_method(self):
        superclass = super(Wrangler, self)
        result = superclass._command_to_method
        result = result.copy()
        result.update({
            'rad*': self.add_every_asset,
            'rci*': self.commit_every_asset,
            'rcn*': self.remove_every_unadded_asset,
            'rst*': self.display_every_asset_status,
            'rrv*': self.revert_every_asset,
            'rup*': self.update_every_asset,
            #
            'wa': self.autoedit_views,
            'ws': self.set_view,
            #
            'we': self.edit_views_py,
            'ww': self.write_views_py,
            })
        return result

    @property
    def _current_package_manager(self):
        path = self._get_current_directory()
        if path is None:
            return
        return self._io_manager._make_package_manager(path)

    @property
    def _current_storehouse_path(self):
        if self._session.is_in_score:
            parts = []
            parts.append(self._session.current_score_directory)
            parts.extend(self._score_storehouse_path_infix_parts)
            return os.path.join(*parts)
        else:
            return self._abjad_storehouse_path

    @property
    def _init_py_file_path(self):
        path = self._get_current_directory()
        if path:
            return os.path.join(path, '__init__.py')

    @property
    def _metadata_py_path(self):
        if self._session.is_in_score:
            manager = self._current_package_manager
        else:
            manager = self._views_package_manager
        return manager._metadata_py_path

    @property
    def _views_py_path(self):
        if self._session.is_in_score:
            directory = self._get_current_directory()
            return os.path.join(directory, '__views__.py')
        else:
            directory = self._configuration.wrangler_views_directory
            class_name = type(self).__name__
            file_name = '__{}_views__.py'.format(class_name)
            return os.path.join(directory, file_name)

    ### PRIVATE METHODS ###

    def _clear_view(self):
        if self._session.is_in_score:
            manager = self._current_package_manager
            metadatum_name = 'view_name'
        else:
            manager = self._views_package_manager
            metadatum_name = '{}_view_name'.format(type(self).__name__)
        manager._add_metadatum(metadatum_name, None)

    def _copy_asset(
        self, 
        extension=None,
        new_storehouse=None
        ):
        visible_asset_paths = self._list_visible_asset_paths()
        if not visible_asset_paths:
            messages = ['nothing to copy.']
            messages.append('')
            self._io_manager._display(messages)
            return
        extension = extension or getattr(self, '_extension', '')
        old_path = self._select_visible_asset_path(infinitive_phrase='to copy')
        if not old_path:
            return
        old_name = os.path.basename(old_path)
        if new_storehouse:
            pass
        elif self._session.is_in_score:
            new_storehouse = self._get_current_directory()
        else:
            new_storehouse = self._select_storehouse_path()
            if self._session.is_backtracking or new_storehouse is None:
                return
        message = 'existing {} name> {}'
        message = message.format(self._asset_identifier, old_name)
        self._io_manager._display(message)
        message = 'new {} name'
        message = message.format(self._asset_identifier)
        getter = self._io_manager._make_getter()
        getter.append_string(message)
        help_template = getter.prompts[0].help_template
        string = 'Press <return> to preserve existing name.'
        help_template = help_template + ' ' + string
        getter.prompts[0]._help_template = help_template
        new_name = getter._run()
        new_name = new_name or old_name
        if self._session.is_backtracking or new_name is None:
            return
        new_name = stringtools.strip_diacritics(new_name)
        if hasattr(self, '_file_name_callback'):
            new_name = self._file_name_callback(new_name)
        new_name = new_name.replace(' ', '_')
        if self._force_lowercase:
            new_name = new_name.lower()
        if extension and not new_name.endswith(extension):
            new_name = new_name + extension
        new_path = os.path.join(new_storehouse, new_name)
        if os.path.exists(new_path):
            message = 'already exists: {}'.format(new_path)
            self._io_manager._display(message)
            self._io_manager._acknowledge()
            return
        messages = []
        messages.append('will copy ...')
        messages.append(' FROM: {}'.format(old_path))
        messages.append('   TO: {}'.format(new_path))
        self._io_manager._display(messages)
        result = self._io_manager._confirm()
        if self._session.is_backtracking or not result:
            return
        if os.path.isfile(old_path):
            shutil.copyfile(old_path, new_path)
        elif os.path.isdir(old_path):
            shutil.copytree(old_path, new_path)
        else:
            raise TypeError(old_path)
        if os.path.isdir(new_path):
            for directory_entry in sorted(os.listdir(new_path)):
                if not directory_entry.endswith('.py'):
                    continue
                path = os.path.join(new_path, directory_entry)
                self._replace_in_file(
                    path,
                    old_name,
                    new_name,
                    )

    def _enter_run(self):
        pass

    def _extract_common_parent_directories(self, paths):
        parent_directories = []
        example_score_packages_directory = \
            self._configuration.example_score_packages_directory
        user_score_packages_directory = \
            self._configuration.user_score_packages_directory
        for path in paths:
            parent_directory = os.path.dirname(path)
            if parent_directory == user_score_packages_directory:
                parent_directories.append(path)
            elif parent_directory == example_score_packages_directory:
                parent_directories.append(path)
            elif parent_directory not in parent_directories:
                parent_directories.append(parent_directory)
        return parent_directories

    def _find_git_manager(self, inside_score=True, must_have_file=False):
        manager = self._find_up_to_date_manager(
            inside_score=inside_score,
            must_have_file=must_have_file,
            system=True,
            repository='git',
            )
        return manager

    def _find_svn_manager(self, inside_score=True, must_have_file=False):
        manager = self._find_up_to_date_manager(
            inside_score=inside_score,
            must_have_file=must_have_file,
            system=False,
            repository='svn',
            )
        return manager

    def _find_up_to_date_manager(
        self,
        inside_score=True,
        must_have_file=False,
        system=True,
        repository='git',
        ):
        from scoremanager import idetools
        from scoremanager import idetools
        abjad_material_packages_and_stylesheets = False
        example_score_packages = False
        library = False
        user_score_packages = False
        if system and inside_score:
            example_score_packages = True
        elif system and not inside_score:
            abjad_material_packages_and_stylesheets = True
        elif not system and inside_score:
            user_score_packages = True
        elif not system and not inside_score:
            library = True
        else:
            Exception
        asset_paths = self._list_asset_paths(
            abjad_material_packages_and_stylesheets=abjad_material_packages_and_stylesheets,
            example_score_packages=example_score_packages,
            library=library,
            user_score_packages=user_score_packages,
            )
        if type(self) is idetools.ScorePackageWrangler:
            if system:
                scores_directory = \
                    self._configuration.example_score_packages_directory
            else:
                scores_directory = \
                    self._configuration.user_score_packages_directory
            asset_paths = []
            for directory_entry in sorted(os.listdir(scores_directory)):
                if not directory_entry[0].isalpha():
                    continue
                path = os.path.join(scores_directory, directory_entry)
                if os.path.isdir(path):
                    asset_paths.append(path)
        session = idetools.Session()
        for asset_path in asset_paths:
            manager = self._manager_class(
                path=asset_path,
                session=session,
                )
            if (repository == 'git' and
                manager._is_git_versioned() and
                manager._is_up_to_date() and
                (not must_have_file or manager._find_first_file_name())):
                return manager
            elif (repository == 'svn' and
                manager._is_svn_versioned() and
                manager._is_up_to_date() and
                (not must_have_file or manager._find_first_file_name())):
                return manager

    def _get_available_path(
        self,
        message=None,
        storehouse_path=None,
        ):
        storehouse_path = storehouse_path or self._current_storehouse_path
        while True:
            default_prompt = 'enter {} name'.format(self._asset_identifier)
            message = message or default_prompt
            getter = self._io_manager._make_getter()
            getter.append_string(message)
            name = getter._run()
            if self._session.is_backtracking or not name:
                return
            name = stringtools.strip_diacritics(name)
            words = stringtools.delimit_words(name)
            words = [_.lower() for _ in words]
            name = '_'.join(words)
            if not stringtools.is_snake_case_package_name(name):
                continue
            path = os.path.join(storehouse_path, name)
            if os.path.exists(path):
                line = 'path already exists: {!r}.'
                line = line.format(path)
                self._io_manager._display(line)
            else:
                return path

    def _get_file_path_ending_with(self, string):
        path = self._get_current_directory()
        for file_name in self._list():
            if file_name.endswith(string):
                file_path = os.path.join(path, file_name)
                return file_path

    def _get_manager(self, path):
        manager = self._manager_class(
            path=path,
            session=self._session,
            )
        return manager

    def _get_next_asset_path(self):
        last_path = self._session.last_asset_path
        menu_entries = self._make_asset_menu_entries()
        paths = [x[-1] for x in menu_entries]
        if self._session.is_in_score:
            score_directory = self._session.current_score_directory
            paths = [x for x in paths if x.startswith(score_directory)]
        if last_path is None:
            return paths[0]
        if last_path not in paths:
            return paths[0]
        index = paths.index(last_path)
        next_index = (index + 1) % len(paths)
        next_path = paths[next_index]
        return next_path

    def _get_previous_asset_path(self):
        last_path = self._session.last_asset_path
        menu_entries = self._make_asset_menu_entries()
        paths = [x[-1] for x in menu_entries]
        if self._session.is_in_score:
            score_directory = self._session.current_score_directory
            paths = [x for x in paths if x.startswith(score_directory)]
        if last_path is None:
            return paths[-1]
        if last_path not in paths:
            return paths[-1]
        index = paths.index(last_path)
        previous_index = (index - 1) % len(paths)
        previous_path = paths[previous_index]
        return previous_path

    def _get_sibling_asset_path(self):
        if self._session.is_navigating_to_next_asset:
            return self._get_next_asset_path()
        if self._session.is_navigating_to_previous_asset:
            return self._get_previous_asset_path()

    def _get_visible_storehouses(self):
        menu = self._make_asset_selection_menu()
        asset_section = menu['assets']
        storehouses = set()
        for menu_entry in asset_section:
            path = menu_entry.return_value
            storehouse = self._configuration._path_to_storehouse(path)
            storehouses.add(storehouse)
        storehouses = list(sorted(storehouses))
        return storehouses

    def _handle_numeric_user_input(self, result):
        self._io_manager.open_file(result)

    def _initialize_manager(self, path, asset_identifier=None):
        assert os.path.sep in path, repr(path)
        manager = self._manager_class(
            path=path,
            session=self._session,
            )
        if asset_identifier:
            manager._asset_identifier = asset_identifier
        return manager

    def _list(self, public_entries_only=False):
        result = []
        path = self._get_current_directory()
        result = self._io_manager._list_directory(
            path, 
            public_entries_only=public_entries_only,
            )
        return result

    def _list_all_directories_with_metadata_pys(self):
        directories = []
        paths = self._list_visible_asset_paths()
        for path in paths:
            result = self._list_directories_with_metadata_pys(path)
            directories.extend(result)
        return directories

    def _list_asset_paths(
        self,
        abjad_material_packages_and_stylesheets=True,
        example_score_packages=True,
        library=True,
        user_score_packages=True,
        valid_only=True,
        ):
        result = []
        directories = self._list_storehouse_paths(
            abjad_material_packages_and_stylesheets=abjad_material_packages_and_stylesheets,
            example_score_packages=example_score_packages,
            library=library,
            user_score_packages=user_score_packages,
            )
        for directory in directories:
            if not directory:
                continue
            if not os.path.exists(directory):
                continue
            directory_entries = sorted(os.listdir(directory))
            for directory_entry in directory_entries:
                if valid_only:
                    if not self._is_valid_directory_entry(directory_entry):
                        continue
                path = os.path.join(directory, directory_entry)
                result.append(path)
        return result

    def _list_storehouse_paths(
        self,
        abjad_material_packages_and_stylesheets=True,
        example_score_packages=True,
        library=True,
        user_score_packages=True,
        ):
        result = []
        if (abjad_material_packages_and_stylesheets and
            self._abjad_storehouse_path is not None):
            result.append(self._abjad_storehouse_path)
        if library and self._user_storehouse_path is not None:
            result.append(self._user_storehouse_path)
        if (example_score_packages and
            self._score_storehouse_path_infix_parts):
            for score_directory in \
                self._configuration.list_score_directories(abjad=True):
                parts = [score_directory]
                if self._score_storehouse_path_infix_parts:
                    parts.extend(self._score_storehouse_path_infix_parts)
                storehouse_path = os.path.join(*parts)
                result.append(storehouse_path)
        elif (example_score_packages and
            not self._score_storehouse_path_infix_parts):
            result.append(self._configuration.example_score_packages_directory)
        if user_score_packages and self._score_storehouse_path_infix_parts:
            for directory in \
                self._configuration.list_score_directories(user=True):
                parts = [directory]
                if self._score_storehouse_path_infix_parts:
                    parts.extend(self._score_storehouse_path_infix_parts)
                path = os.path.join(*parts)
                result.append(path)
        return result

    def _list_visible_asset_managers(self):
        paths = self._list_visible_asset_paths()
        managers = []
        for path in paths:
            manager = self._initialize_manager(path=path)
            managers.append(manager)
        return managers

    def _list_visible_asset_paths(self):
        entries = self._make_asset_menu_entries()
        paths = [_[-1] for _ in entries]
        return paths

    def _make_asset(self, asset_name):
        if os.path.sep in asset_name:
            asset_name = os.path.basename(asset_name)
        assert stringtools.is_snake_case(asset_name)
        path = os.path.join(
            self._current_storehouse_path,
            asset_name,
            )
        manager = self._initialize_manager(path)
        if hasattr(manager, '_write_stub'):
            self._io_manager.write_stub(path)
        else:
            with self._io_manager._silent():
                manager.check_package(
                    return_supply_messages=True,
                    supply_missing=True,
                    )
        paths = self._list_visible_asset_paths()
        if path not in paths:
            with self._io_manager._silent():
                self._clear_view()
        self._session._pending_redraw = True

    def _make_asset_selection_breadcrumb(
        self,
        human_readable_target_name=None,
        infinitival_phrase=None,
        is_storehouse=False,
        ):
        if human_readable_target_name is None:
            name = self._manager_class.__name__
            name = stringtools.to_space_delimited_lowercase(name)
            human_readable_target_name = name
        if infinitival_phrase:
            return 'select {} {}:'.format(
                human_readable_target_name,
                infinitival_phrase,
                )
        elif is_storehouse:
            return 'select storehouse'
        else:
            return 'select {}:'.format(human_readable_target_name)

    def _make_asset_selection_menu(self):
        menu = self._io_manager._make_menu(name='asset selection')
        menu_entries = self._make_asset_menu_entries()
        menu.make_asset_section(menu_entries=menu_entries)
        return menu

    def _make_file(
        self, 
        extension=None, 
        message='file name', 
        ):
        from scoremanager import idetools
        extension = extension or getattr(self, '_extension', '')
        if self._session.is_in_score:
            path = self._get_current_directory()
        else:
            path = self._select_storehouse_path()
            if self._session.is_backtracking or path is None:
                return
        getter = self._io_manager._make_getter()
        getter.append_string(message)
        name = getter._run()
        if self._session.is_backtracking or name is None:
            return
        name = stringtools.strip_diacritics(name)
        if hasattr(self, '_file_name_callback'):
            name = self._file_name_callback(name)
        name = name.replace(' ', '_')
        if self._force_lowercase:
            name = name.lower()
        if not name.endswith(extension):
            name = name + extension
        path = os.path.join(path, name)
        self._io_manager.write(path, '')
        self._io_manager.edit(path)

    def _make_main_menu(self):
        superclass = super(Wrangler, self)
        menu = superclass._make_main_menu()
        self._make_asset_menu_section(menu)
        self._make_metadata_menu_section(menu)
        self._make_views_menu_section(menu)
        return menu

    def _make_storehouse_menu_entries(
        self,
        abjad_material_packages_and_stylesheets=True,
        example_score_packages=True,
        library=True,
        user_score_packages=True,
        ):
        from scoremanager import idetools
        display_strings, keys = [], []
        keys.append(self._user_storehouse_path)
        if self._in_library:
            display_string = 'My {} library'.format(self._asset_identifier)
            display_strings.append(display_string)
        wrangler = idetools.ScorePackageWrangler(session=self._session)
        paths = wrangler._list_asset_paths(
            abjad_material_packages_and_stylesheets=abjad_material_packages_and_stylesheets,
            example_score_packages=example_score_packages,
            library=library,
            user_score_packages=user_score_packages,
            )
        for path in paths:
            manager = wrangler._initialize_manager(path)
            display_strings.append(manager._get_title())
            path_parts = (manager._path,)
            path_parts = path_parts + self._score_storehouse_path_infix_parts
            key = os.path.join(*path_parts)
            keys.append(key)
        sequences = [display_strings, [None], [None], keys]
        return sequencetools.zip_sequences(sequences, cyclic=True)

    def _make_views_menu_section(self, menu):
        commands = []
        commands.append(('__views.py__ - edit', 'we'))
        commands.append(('__views.py__ - write', 'ww'))
        commands.append(('views - autoedit', 'wa'))
        commands.append(('views - set', 'ws'))
        menu.make_command_section(
            is_hidden=True,
            commands=commands,
            name='views',
            )

    def _match_display_string_view_pattern(self, pattern, entry):
        display_string, _, _, path = entry
        token = ':ds:'
        assert token in pattern, repr(pattern)
        pattern = pattern.replace(token, repr(display_string))
        try:
            result = eval(pattern)
        except:
            traceback.print_exc()
            return False
        return result

    def _match_metadata_view_pattern(self, pattern, entry):
        display_string, _, _, path = entry
        manager = self._io_manager._make_package_manager(path)
        count = pattern.count('md:')
        for _ in range(count+1):
            parts = pattern.split()
            for part in parts:
                if part.startswith('md:'):
                    metadatum_name = part[3:]
                    metadatum = manager._get_metadatum(
                        metadatum_name,
                        include_score=True,
                        )
                    metadatum = repr(metadatum)
                    pattern = pattern.replace(part, metadatum)
        try:
            result = eval(pattern)
        except:
            traceback.print_exc()
            return False
        return result

    def _match_path_view_pattern(self, pattern, entry):
        display_string, _, _, path = entry
        token = ':path:'
        assert token in pattern, repr(pattern)
        pattern = pattern.replace(token, repr(path))
        try:
            result = eval(pattern)
        except:
            traceback.print_exc()
            return False
        return result

    def _open_file_ending_with(self, string):
        path = self._get_file_path_ending_with(string)
        if path:
            self._io_manager.open_file(path)
        else:
            message = 'file ending in {!r} not found.'
            message = message.format(string)
            self._io_manager._display(message)

    def _open_in_every_package(self, file_name, verb='open'):
        paths = []
        for path in self._list_visible_asset_paths():
            path = os.path.join(path, file_name)
            if os.path.isfile(path):
                paths.append(path)
        if not paths:
            message = 'no {} files found.'
            message = message.format(file_name)
            self._io_manager._display(message)
            return
        messages = []
        message = 'will {} ...'.format(verb)
        messages.append(message)
        for path in paths:
            message = '   ' + path
            messages.append(message)
        self._io_manager._display(messages)
        result = self._io_manager._confirm()
        if self._session.is_backtracking or not result:
            return
        self._io_manager.open_file(paths)

    def _remove_assets(self):
        from scoremanager import idetools
        self._session._attempted_to_remove = True
        if self._session.is_repository_test:
            return
        paths = self._select_visible_asset_paths()
        if not paths:
            return
        count = len(paths)
        messages = []
        if count == 1:
            message = 'will remove {}'.format(paths[0])
            messages.append(message)
        else:
            messages.append('will remove ...')
            for path in paths:
                message = '    {}'.format(path)
                messages.append(message)
        self._io_manager._display(messages)
        if count == 1:
            confirmation_string = 'remove'
        else:
            confirmation_string = 'remove {}'
            confirmation_string = confirmation_string.format(count)
        message = "type {!r} to proceed"
        message = message.format(confirmation_string)
        getter = self._io_manager._make_getter()
        getter.append_string(message)
        if self._session.confirm:
            result = getter._run()
            if self._session.is_backtracking or result is None:
                return
            if not result == confirmation_string:
                return
        for path in paths:
            manager = idetools.PackageManager(path=path, session=self._session)
            with self._io_manager._silent():
                manager._remove()
        self._session._pending_redraw = True

    def _rename_asset(
        self,
        extension=None,
        file_name_callback=None, 
        ):
        extension = extension or getattr(self, '_extension', '')
        path = self._select_visible_asset_path(infinitive_phrase='to rename')
        if not path:
            return
        file_name = os.path.basename(path)
        message = 'existing file name> {}'
        message = message.format(file_name)
        self._io_manager._display(message)
        manager = self._initialize_manager(
            path,
            asset_identifier=self._asset_identifier,
            )
        manager._rename_interactively(
            extension=extension,
            file_name_callback=file_name_callback,
            force_lowercase=self._force_lowercase,
            )
        self._session._is_backtracking_locally = False

    def _run(self):
        controller = self._io_manager._controller(
            consume_local_backtrack=True,
            controller=self,
            on_enter_callbacks=(self._enter_run,),
            )
        directory = systemtools.NullContextManager()
        if self._session.is_in_score:
            path = self._get_current_directory()
            directory = systemtools.TemporaryDirectoryChange(path)
        with controller, directory:
            result = None
            self._session._pending_redraw = True
            while True:
                result = self._get_sibling_asset_path()
                if not result:
                    menu = self._make_main_menu()
                    result = menu._run()
                if self._session.is_backtracking:
                    return
                if result:
                    self._handle_input(result)
                    if self._session.is_backtracking:
                        return

    def _select_asset_path(self):
        menu = self._make_asset_selection_menu()
        while True:
            result = menu._run()
            if self._session.is_backtracking:
                return
            elif not result:
                continue
            elif result == '<return>':
                return
            else:
                break
        return result

    def _select_storehouse_path(self):
        from scoremanager import idetools
        menu_entries = self._make_storehouse_menu_entries(
            abjad_material_packages_and_stylesheets=False,
            example_score_packages=False,
            library=True,
            user_score_packages=False,
            )
        selector = idetools.Selector(
            breadcrumb='storehouse',
            menu_entries=menu_entries,
            session=self._session,
            )
        result = selector._run()
        if self._session.is_backtracking or result is None:
            return
        return result

    def _select_view(self, infinitive_phrase=None, is_ranged=False):
        from scoremanager import idetools
        view_inventory = self._read_view_inventory()
        if view_inventory is None:
            message = 'no views found.'
            self._io_manager._display(message)
            return
        view_names = list(view_inventory.keys())
        view_names.append('none')
        if is_ranged:
            breadcrumb = 'view(s)'
        else:
            breadcrumb = 'view'
        if infinitive_phrase:
            breadcrumb = '{} {}'.format(breadcrumb, infinitive_phrase)
        selector = self._io_manager._make_selector(
            breadcrumb=breadcrumb,
            is_ranged=is_ranged,
            items=view_names,
            )
        result = selector._run()
        if self._session.is_backtracking or result is None:
            return
        return result

    def _select_visible_asset_path(self, infinitive_phrase=None):
        getter = self._io_manager._make_getter()
        message = 'enter {}'.format(self._asset_identifier)
        if infinitive_phrase:
            message = message + ' ' + infinitive_phrase
        if hasattr(self, '_make_asset_menu_section'):
            dummy_menu = self._io_manager._make_menu()
            self._make_asset_menu_section(dummy_menu)
            asset_section = dummy_menu._asset_section
        else:
            menu = self._make_asset_selection_menu()
            asset_section = menu['assets']
        getter.append_menu_section_item(
            message, 
            asset_section,
            )
        numbers = getter._run()
        if self._session.is_backtracking or numbers is None:
            return
        if not len(numbers) == 1:
            return
        number = numbers[0]
        index = number - 1
        paths = [_.return_value for _ in asset_section.menu_entries]
        path = paths[index]
        return path

    def _select_visible_asset_paths(self):
        getter = self._io_manager._make_getter()
        plural_identifier = stringtools.pluralize(self._asset_identifier)
        message = 'enter {}(s) to remove'
        message = message.format(plural_identifier)
        menu = self._make_asset_selection_menu()
        asset_section = menu['assets']
        getter.append_menu_section_range(
            message, 
            asset_section,
            )
        numbers = getter._run()
        if self._session.is_backtracking or numbers is None:
            return
        indices = [_ - 1 for _ in numbers]
        paths = [_.return_value for _ in asset_section.menu_entries]
        paths = sequencetools.retain_elements(paths, indices)
        return paths

    def _set_is_navigating_to_sibling_asset(self):
        message = 'implement on concrete wrangler classes.'
        raise Exception(message)

    @staticmethod
    def _strip_annotation(display_string):
        if not display_string.endswith(')'):
            return display_string
        index = display_string.find('(')
        result = display_string[:index]
        result = result.strip()
        return result

    def _write_view_inventory(self, view_inventory):
        lines = []
        lines.append(self._configuration.unicode_directive)
        lines.append(self._abjad_import_statement)
        lines.append('from scoremanager import idetools')
        lines.append('')
        lines.append('')
        view_inventory = self._sort_ordered_dictionary(view_inventory)
        line = 'view_inventory={}'.format(format(view_inventory))
        lines.append(line)
        contents = '\n'.join(lines)
        self._io_manager.write(self._views_py_path, contents)
        message = 'view inventory written to disk.'
        self._io_manager._display(message)

    ### PUBLIC METHODS ###

    def add_every_asset(self):
        r'''Adds every asset to repository.

        Returns none.
        '''
        self._session._attempted_to_add = True
        if self._session.is_repository_test:
            return
        managers = self._list_visible_asset_managers()
        inputs, outputs = [], []
        method_name = 'add'
        for manager in managers:
            method = getattr(manager, method_name)
            inputs_, outputs_ = method(dry_run=True)
            inputs.extend(inputs_)
            outputs.extend(outputs_)
        messages = self._format_messaging(inputs, outputs, verb='add')
        self._io_manager._display(messages)
        if not inputs:
            return
        result = self._io_manager._confirm()
        if self._session.is_backtracking or not result:
            return
        with self._io_manager._silent():
            for manager in managers:
                method = getattr(manager, method_name)
                method()
        count = len(inputs)
        identifier = stringtools.pluralize('file', count)
        message = 'added {} {} to repository.'
        message = message.format(count, identifier)
        self._io_manager._display(message)
        
    def autoedit_views(self):
        r'''Autoedits views.

        Returns none.
        '''
        from scoremanager import idetools
        inventory = self._read_view_inventory()
        if inventory is None:
            inventory = idetools.ViewInventory()
        old_inventory = inventory.copy()
        autoeditor = self._io_manager._make_autoeditor(
            breadcrumb='views',
            target=inventory,
            )
        autoeditor._run()
        inventory = autoeditor.target
        if old_inventory != inventory:
            self._write_view_inventory(inventory)
        self._session._pending_redraw = True

    def commit_every_asset(self):
        r'''Commits every asset to repository.

        Returns none.
        '''
        self._session._attempted_to_commit = True
        if self._session.is_repository_test:
            return
        getter = self._io_manager._make_getter()
        getter.append_string('commit message')
        commit_message = getter._run()
        if self._session.is_backtracking or commit_message is None:
            return
        line = 'commit message will be: "{}"'.format(commit_message)
        self._io_manager._display(line)
        result = self._io_manager._confirm()
        if self._session.is_backtracking or not result:
            return
        paths = self._list_visible_asset_paths()
        for path in paths:
            manager = self._initialize_manager(path)
            with self._io_manager._silent():
                manager.commit(commit_message=commit_message)

    def display_every_asset_status(self):
        r'''Displays repository status of every asset.

        Returns none.
        '''
        self._session._attempted_display_status = True
        paths = self._list_visible_asset_paths()
        paths = self._extract_common_parent_directories(paths)
        paths.sort()
        for path in paths:
            manager = self._io_manager._make_package_manager(path)
            manager.display_status()
        if not paths:
            message = 'Repository status for {} ... OK'
            directory = self._get_current_directory()
            message = message.format(directory)
            self._io_manager._display(message)

    def edit_views_py(self):
        r'''Opens ``__views__.py``.

        Returns none.
        '''
        if os.path.exists(self._views_py_path):
            self._io_manager.open_file(self._views_py_path)
        else:
            message = 'no __views.py__ found.'
            self._io_manager._display(message)

    def remove_every_unadded_asset(self):
        r'''Removes files not yet added to repository of every asset.

        Returns none.
        '''
        self._session._attempted_remove_unadded_assets = True
        if self._session.is_test and not self._session.is_in_score:
            return
        paths = self._list_visible_asset_paths()
        paths = self._extract_common_parent_directories(paths)
        paths.sort()
        inputs, outputs = [], []
        managers = []
        method_name = 'remove_unadded_assets'
        for path in paths:
            manager = self._io_manager._make_package_manager(path)
            managers.append(manager)
            method = getattr(manager, method_name)
            inputs_, outputs_ = method(dry_run=True)
            inputs.extend(inputs_)
            outputs.extend(outputs_)
        messages = self._format_messaging(inputs, outputs, verb='remove')
        self._io_manager._display(messages)
        if not inputs:
            return
        result = self._io_manager._confirm()
        if self._session.is_backtracking or not result:
            return
        with self._io_manager._silent():
            for manager in managers:
                method = getattr(manager, method_name)
                method()
        count = len(inputs)
        identifier = stringtools.pluralize('asset', count)
        message = 'removed {} unadded {}.'
        message = message.format(count, identifier)
        self._io_manager._display(message)

    def revert_every_asset(self):
        r'''Reverts every asset to repository.

        Returns none.
        '''
        self._session._attempted_to_revert = True
        if self._session.is_repository_test:
            return
        paths = self._list_visible_asset_paths()
        for path in paths:
            manager = self._io_manager._make_package_manager(path)
            manager.revert()

    def set_view(self):
        r'''Applies view.

        Writes view name to ``__metadata.py__``.

        Returns none.
        '''
        infinitive_phrase = 'to apply'
        view_name = self._select_view(infinitive_phrase=infinitive_phrase)
        if self._session.is_backtracking or view_name is None:
            return
        if view_name == 'none':
            view_name = None
        if self._session.is_in_score:
            manager = self._current_package_manager
            metadatum_name = 'view_name'
        else:
            manager = self._views_package_manager
            metadatum_name = '{}_view_name'.format(type(self).__name__)
        manager._add_metadatum(metadatum_name, view_name)

    def update_every_asset(self):
        r'''Updates every asset from repository.

        Returns none.
        '''
        tab = self._io_manager._tab
        managers = self._list_visible_asset_managers()
        for manager in managers:
            messages = []
            message = self._path_to_asset_menu_display_string(manager._path)
            message = self._strip_annotation(message)
            message = message + ':'
            messages_ = manager.update(messages_only=True)
            if len(messages_) == 1:
                message = message + ' ' + messages_[0]
                messages.append(message)
            else:
                messages_ = [tab + _ for _ in messages_]
                messages.extend(messages_)
            self._io_manager._display(messages, capitalize=False)

    def write_views_py(self):
        r'''Rewrites ``__views__.py``.

        Returns none.
        '''
        from scoremanager import idetools
        inputs, outputs = [], []
        inputs.append(self._views_py_path)
        messages = self._format_messaging(inputs, outputs, verb='write')
        self._io_manager._display(messages)
        result = self._io_manager._confirm()
        if self._session.is_backtracking or not result:
            return
        view_inventory = self._read_view_inventory()
        view_inventory = view_inventory or idetools.ViewInventory()
        with self._io_manager._silent():
            self._write_view_inventory(view_inventory)
        message = 'wrote {}.'.format(self._views_py_path)
        self._io_manager._display(message)