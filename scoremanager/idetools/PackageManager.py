# -*- encoding: utf-8 -*-
import os
from abjad.tools import stringtools
from abjad.tools import systemtools
from scoremanager.idetools.ScoreInternalAssetController import \
    ScoreInternalAssetController


class PackageManager(ScoreInternalAssetController):
    r'''Package manager.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_asset_identifier',
        '_main_menu',
        '_optional_directories',
        '_optional_files',
        '_package_name',
        '_path',
        '_required_directories',
        '_required_files',
        )

    ### INITIALIZER ###

    def __init__(self, path=None, session=None):
        assert session is not None
        assert path is not None and os.path.sep in path
        superclass = super(PackageManager, self)
        superclass.__init__(session=session)
        self._asset_identifier = None
        self._optional_directories = (
            '__pycache__',
            'test',
            )
        self._optional_files = ()
        self._required_directories = ()
        self._required_files = (
            '__init__.py',
            '__metadata__.py',
            )
        self._package_name = os.path.basename(path)
        self._path = path

    ### SPECIAL METHODS ###

    def __repr__(self):
        r'''Gets interpreter representation of manager.

        Returns string.
        '''
        return '{}({!r})'.format(type(self).__name__, self._path)

    ### PRIVATE PROPERTIES ###

    @property
    def _breadcrumb(self):
        if self._path:
            return os.path.basename(self._path)
        return self._spaced_class_name

    @property
    def _command_to_method(self):
        superclass = super(PackageManager, self)
        result = superclass._command_to_method
        result = result.copy()
        result.update({
            'ck': self.check_package,
            #
            'mda': self.add_metadatum,
            'mdg': self.get_metadatum,
            'mdr': self.remove_metadatum,
            #
            'ne': self.edit_init_py,
            'nl': self.list_init_py,
            'ns': self.write_stub_init_py,
            #
            'rad': self.add,
            'rci': self.commit,
            'rcn': self.remove_unadded_assets,
            'rrv': self.revert,
            'rst': self.display_status,
            'rup': self.update,
            })
        return result

    @property
    def _display_status_command(self):
        if not self._path:
            return
        if self._is_in_git_repository(path=self._path):
            return 'git status {}'.format(self._path)
        elif self._is_svn_versioned(path=self._path):
            return 'svn st {}'.format(self._path)
        else:
            return

    @property
    def _init_py_file_path(self):
        return os.path.join(self._path, '__init__.py')

    @property
    def _metadata_py_path(self):
        return os.path.join(self._path, '__metadata__.py')

    @property
    def _repository_add_command(self):
        if not self._path:
            return
        if self._is_in_git_repository(path=self._path):
            command = 'git add -A {}'.format(self._path)
        elif self._is_svn_versioned(path=self._path):
            paths = self._get_unadded_asset_paths()
            commands = []
            for path in paths:
                command = 'svn add {}'.format(path)
                commands.append(command)
            command = ' && '.join(commands)
        else:
            raise ValueError(self)
        return command

    @property
    def _repository_update_command(self):
        if not self._path:
            return
        if self._is_in_git_repository(path=self._path):
            root_directory = self._get_repository_root_directory()
            return 'git pull {}'.format(root_directory)
        elif self._is_svn_versioned(path=self._path):
            return 'svn update {}'.format(self._path)
        else:
            raise ValueError(self)

    @property
    def _shell_remove_command(self):
        paths = self._io_manager.find_executable('trash')
        if paths:
            return 'trash'
        return 'rm'

    @property
    def _space_delimited_lowercase_name(self):
        if self._path:
            base_name = os.path.basename(self._path)
            result = base_name.replace('_', ' ')
            return result

    @property
    def _views_py_path(self):
        return os.path.join(self._path, '__views__.py')

    ### PRIVATE METHODS ###

    def _add_metadatum(self, metadatum_name, metadatum_value):
        assert ' ' not in metadatum_name, repr(metadatum_name)
        metadata = self._get_metadata()
        metadata[metadatum_name] = metadatum_value
        with self._io_manager._silent():
            self._write_metadata_py(metadata)

    def _enter_run(self):
        self._session._is_navigating_to_next_asset = False
        self._session._is_navigating_to_previous_asset = False
        self._session._last_asset_path = self._path

    def _exit_run(self):
        return self._session.is_backtracking

    @staticmethod
    def _file_name_to_version_number(file_name):
        root, extension = os.path.splitext(file_name)
        assert 4 <= len(root), repr(file_name)
        version_number_string = root[-4:]
        try:
            version_number = int(version_number_string)
        except ValueError:
            version_number = None
        return version_number

    def _find_first_file_name(self):
        for directory_entry in sorted(os.listdir(self._path)):
            if not directory_entry.startswith('.'):
                path = os.path.join(self._path, directory_entry)
                if os.path.isfile(path):
                    return directory_entry

    def _format_counted_check_messages(
        self,
        paths,
        identifier,
        participal,
        ):
        messages = []
        if paths:
            tab = self._io_manager._tab
            count = len(paths)
            identifier = stringtools.pluralize(identifier, count)
            message = '{} {} {}:'
            message = message.format(count, identifier, participal)
            messages.append(message)
            for path in paths:
                message = tab + path
                messages.append(message)
        return messages

    def _format_ratio_check_messages(
        self,
        found_paths,
        total_paths,
        identifier,
        participal='found',
        ):
        messages = []
        denominator = len(total_paths)
        numerator = len(found_paths)
        identifier = stringtools.pluralize(identifier, denominator)
        if denominator:
            message = '{} of {} {} {}:'
        else:
            message = '{} of {} {} {}.'
        message = message.format(
            numerator, denominator, identifier, participal)
        messages.append(message)
        tab = self._io_manager._tab
        for path in sorted(found_paths):
            message = tab + path
            messages.append(message)
        return messages

    def _get_added_asset_paths(self):
        if self._is_in_git_repository():
            command = 'git status --porcelain {}'
            command = command.format(self._path)
            process = self._io_manager.make_subprocess(command)
            paths = []
            stdout_lines = self._io_manager._read_from_pipe(process.stdout)
            for line in stdout_lines.splitlines():
                line = str(line)
                if line.startswith('A'):
                    path = line.strip('A')
                    path = path.strip()
                    root_directory = self._get_repository_root_directory()
                    path = os.path.join(root_directory, path)
                    paths.append(path)
        elif self._is_svn_versioned():
            command = 'svn st {}'
            command = command.format(self._path)
            process = self._io_manager.make_subprocess(command)
            paths = []
            stdout_lines = self._io_manager._read_from_pipe(process.stdout)
            for line in stdout_lines.splitlines():
                line = str(line)
                if line.startswith('A'):
                    path = line.strip('A')
                    path = path.strip()
                    paths.append(path)
        else:
            raise ValueError(self)
        return paths

    def _get_current_directory(self):
        return self._path

    def _get_existing_version_numbers(self, file_name_prototype):
        root, extension = os.path.splitext(file_name_prototype)
        version_numbers = []
        for entry in sorted(os.listdir(self._versions_directory)):
            if entry.startswith(root) and entry.endswith(extension):
                version_number = self._file_name_to_version_number(entry)
                version_numbers.append(version_number)
        return version_numbers

    def _get_file_path_ending_with(self, string):
        for file_name in self._list():
            if file_name.endswith(string):
                file_path = os.path.join(self._path, file_name)
                return file_path

    def _get_last_version_number(self):
        versions_directory = self._versions_directory
        if not os.path.exists(versions_directory):
            return
        file_names = sorted(os.listdir(versions_directory))
        if not file_names:
            return
        return max(self._file_name_to_version_number(_) for _ in file_names)

    def _get_metadatum(self, metadatum_name, include_score=False):
        metadata = self._get_metadata()
        metadatum = metadata.get(metadatum_name, None)
        if metadatum is None:
            metadata = self._get_score_metadata()
            metadatum = metadata.get(metadatum_name, None)
        return metadatum

    def _get_modified_asset_paths(self):
        if self._is_in_git_repository():
            command = 'git status --porcelain {}'
            command = command.format(self._path)
            process = self._io_manager.make_subprocess(command)
            paths = []
            stdout_lines = self._io_manager._read_from_pipe(process.stdout)
            for line in stdout_lines.splitlines():
                line = str(line)
                if line.startswith(('M', ' M')):
                    path = line.strip('M ')
                    path = path.strip()
                    root_directory = self._get_repository_root_directory()
                    path = os.path.join(root_directory, path)
                    paths.append(path)
        elif self._is_svn_versioned():
            command = 'svn st {}'
            command = command.format(self._path)
            process = self._io_manager.make_subprocess(command)
            paths = []
            stdout_lines = self._io_manager._read_from_pipe(process.stdout)
            for line in stdout_lines.splitlines():
                line = str(line)
                if line.startswith('M'):
                    path = line.strip('M')
                    path = path.strip()
                    paths.append(path)
        else:
            raise ValueError(self._path)
        return paths

    def _get_next_version_string(self):
        last_version_number = self._get_last_version_number()
        last_version_number = last_version_number or 0
        next_version_number = last_version_number + 1
        next_version_string = '%04d' % next_version_number
        return next_version_string

    def _get_repository_root_directory(self):
        if self._is_in_git_repository():
            command = 'git rev-parse --show-toplevel'
            process = self._io_manager.make_subprocess(command)
            line = self._io_manager._read_one_line_from_pipe(process.stdout)
            return line
        elif self._is_svn_versioned():
            pass
        else:
            raise ValueError(self)

    def _get_score_package_directory_name(self):
        line = self._path
        path = self._configuration.example_score_packages_directory
        line = line.replace(path, '')
        path = self._configuration.user_score_packages_directory
        line = line.replace(path, '')
        line = line.lstrip(os.path.sep)
        return line

    def _get_top_level_wranglers(self):
        return ()

    def _get_unadded_asset_paths(self):
        if self._is_in_git_repository():
            command = 'git status --porcelain {}'
            command = command.format(self._path)
            process = self._io_manager.make_subprocess(command)
            paths = []
            stdout_lines = self._io_manager._read_from_pipe(process.stdout)
            for line in stdout_lines.splitlines():
                line = str(line)
                if line.startswith('?'):
                    path = line.strip('?')
                    path = path.strip()
                    root_directory = self._get_repository_root_directory()
                    path = os.path.join(root_directory, path)
                    paths.append(path)
        elif self._is_svn_versioned():
            command = 'svn st {}'
            command = command.format(self._path)
            process = self._io_manager.make_subprocess(command)
            paths = []
            stdout_lines = self._io_manager._read_from_pipe(process.stdout)
            for line in stdout_lines.splitlines():
                line = str(line)
                if line.startswith('?'):
                    path = line.strip('?')
                    path = path.strip()
                    paths.append(path)
        else:
            raise ValueError(self)
        return paths

    def _handle_numeric_user_input(self, result):
        if os.path.isfile(result):
            self._io_manager.open_file(result)
        elif os.path.isdir(result):
            entries = self._io_manager._list_directory(result)
            if not entries:
                message = 'Empty directory.'
                entries = [message]
            self._io_manager._display(entries, capitalize=False)
        else:
            message = 'neither file nor directory: {}?'.format(result)
            raise ValueError(message)

    def _initialize_file_name_getter(self):
        getter = self._io_manager._make_getter()
        asset_identifier = getattr(self, '_asset_identifier', None)
        if asset_identifier:
            prompt = 'new {} name'.format(asset_identifier)
        else:
            prompt = 'new name'
        getter.append_dash_case_file_name(prompt)
        return getter

    def _is_git_added(self, path=None):
        path = path or self._path
        if path is None:
            return False
        if not os.path.exists(path):
            return False
        command = 'git status --porcelain {}'
        command = command.format(path)
        process = self._io_manager.make_subprocess(command)
        first_line = self._io_manager._read_one_line_from_pipe(process.stdout)
        if first_line.startswith('A'):
            return True
        return False

    def _is_git_unknown(self, path=None):
        path = path or self._path
        if path is None:
            return False
        if not os.path.exists(path):
            return False
        command = 'git status --porcelain {}'
        command = command.format(path)
        process = self._io_manager.make_subprocess(command)
        first_line = self._io_manager._read_one_line_from_pipe(process.stdout)
        if first_line.startswith('??'):
            return True
        return False

    def _is_git_versioned(self, path=None):
        path = path or self._path
        if not self._is_in_git_repository(path=path):
            return False
        command = 'git status --porcelain {}'
        command = command.format(path)
        with systemtools.TemporaryDirectoryChange(directory=self._path):
            process = self._io_manager.make_subprocess(command)
        first_line = self._io_manager._read_one_line_from_pipe(process.stdout)
        if first_line.startswith('?'):
            return False
        return True

    def _is_in_git_repository(self, path=None):
        path = path or self._path
        if path is None:
            return False
        if not os.path.exists(path):
            return False
        command = 'git status --porcelain {}'
        command = command.format(path)
        with systemtools.TemporaryDirectoryChange(directory=path):
            process = self._io_manager.make_subprocess(command)
        first_line = self._io_manager._read_one_line_from_pipe(process.stdout)
        if first_line.startswith('fatal:'):
            return False
        return True

    def _is_populated_directory(self, directory):
        if os.path.exists(directory):
            if sorted(os.listdir(directory)):
                return True
        return False

    def _is_svn_versioned(self, path=None):
        path = path or self._path
        if path is None:
            return False
        if not os.path.exists(path):
            return False
        is_in_svn_versioned_tree = False
        path_to_check = path
        root_directory = os.path.sep
        while path_to_check:
            if os.path.isdir(path_to_check):
                if '.svn' in sorted(os.listdir(path_to_check)):
                    is_in_svn_versioned_tree = True
            path_to_check = os.path.dirname(path_to_check)
            if path_to_check == root_directory:
                break
        if not is_in_svn_versioned_tree:
            return False
        command = 'svn st {}'
        command = command.format(path)
        process = self._io_manager.make_subprocess(command)
        first_line = self._io_manager._read_one_line_from_pipe(process.stdout)
        if first_line.startswith('svn: warning:'):
            return False
        else:
            return True

    def _is_up_to_date(self):
        if self._is_in_git_repository():
            command = 'git status --porcelain {}'
        elif self._is_svn_versioned():
            command = 'svn st {}'
        else:
            raise ValueError(self)
        command = command.format(self._path)
        with systemtools.TemporaryDirectoryChange(directory=self._path):
            process = self._io_manager.make_subprocess(command)
        first_line = self._io_manager._read_one_line_from_pipe(process.stdout)
        return first_line == ''

    def _list(self, public_entries_only=False, smart_sort=False):
        entries = []
        if not os.path.exists(self._path):
            return entries
        if public_entries_only:
            for entry in sorted(os.listdir(self._path)):
                if entry == '__pycache__':
                    continue
                if entry[0].isalpha():
                    if not entry.endswith('.pyc'):
                        if not entry in ('test',):
                            entries.append(entry)
        else:
            for entry in sorted(os.listdir(self._path)):
                if entry == '__pycache__':
                    continue
                if not entry.startswith('.'):
                    if not entry.endswith('.pyc'):
                        entries.append(entry)
        if not smart_sort:
            return entries
        files, directories = [], []
        for entry in entries:
            path = os.path.join(self._path, entry)
            if os.path.isdir(path):
                directories.append(entry + '/')
            else:
                files.append(entry)
        result = files + directories
        return result

    def _list_visible_asset_paths(self):
        return [self._path]

    def _make_asset_menu_section(self, menu):
        directory_entries = self._list(smart_sort=True)
        menu_entries = []
        for directory_entry in directory_entries:
            clean_directory_entry = directory_entry
            if directory_entry.endswith('/'):
                clean_directory_entry = directory_entry[:-1]
            path = os.path.join(self._path, clean_directory_entry)
            menu_entry = (directory_entry, None, None, path)
            menu_entries.append(menu_entry)
        menu.make_asset_section(menu_entries=menu_entries)

    def _make_main_menu(self):
        superclass = super(PackageManager, self)
        menu = superclass._make_main_menu()
        self._make_asset_menu_section(menu)
        self._make_repository_menu_section(menu)
        return menu

    def _make_metadata_menu_entries(self):
        result = []
        metadata = self._get_metadata()
        for key in sorted(metadata):
            display_string = key.replace('_', ' ')
            result.append((display_string, None, metadata[key], key))
        return result

    def _make_package_menu_section(self, menu, commands_only=False):
        commands = []
        commands.append(('package - check', 'ck'))
        if commands_only:
            return commands
        if commands:
            menu.make_command_section(
                is_hidden=True,
                commands=commands,
                name='package',
                )

    def _make_repository_commit_command(self, message):
        if not self._path:
            return
        if self._is_in_git_repository(path=self._path):
            command = 'git commit -m "{}" {}; git push'
            command = command.format(message, self._path)
        elif self._is_svn_versioned(path=self._path):
            command =  'svn commit -m "{}" {}'
            command = command.format(message, self._path)
        else:
            raise ValueError(self)
        return command

    def _open_versioned_file(self, file_name_prototype):
        getter = self._io_manager._make_getter()
        version_numbers = self._get_existing_version_numbers(
            file_name_prototype)
        if not version_numbers:
            message = 'no {} files in versions directory.'
            message = message.format(file_name_prototype)
            self._io_manager._display(message)
            return
        prompt = 'version number ({})'
        prompt = prompt.format(version_numbers)
        getter.append_integer(prompt)
        version_number = getter._run()
        if self._session.is_backtracking or version_number is None:
            return
        if version_number < 0:
            version_number = version_numbers[version_number]
        version_string = str(version_number).zfill(4)
        root, extension = os.path.splitext(file_name_prototype)
        file_name = '{}_{}{}'.format(
            root,
            version_string,
            extension,
            )
        file_path = os.path.join(
            self._path,
            'versions',
            file_name,
            )
        if os.path.isfile(file_path):
            self._io_manager.open_file(file_path)
        else:
            message = 'file not found: {}'.format(file_path)
            self._io_manager._display(message)

    def _remove(self):
        message = '{} will be removed.'
        message = message.format(self._path)
        self._io_manager._display(message)
        getter = self._io_manager._make_getter()
        getter.append_string("type 'remove' to proceed")
        if self._session.confirm:
            result = getter._run()
            if self._session.is_backtracking or result is None:
                return
            if not result == 'remove':
                return
        cleanup_command = None
        if self._is_in_git_repository():
            if self._is_git_unknown():
                command = 'rm -rf {}'
            else:
                command = 'git rm --force -r {}'
                cleanup_command = 'rm -rf {}'
        elif self._is_svn_versioned():
            command = 'svn --force rm {}'
        else:
            command = 'rm -rf {}'
        path = self._path
        command = command.format(path)
        process = self._io_manager.make_subprocess(command)
        self._io_manager._read_one_line_from_pipe(process.stdout)
        if cleanup_command:
            cleanup_command = cleanup_command.format(path)
            process = self._io_manager.make_subprocess(cleanup_command)
            self._io_manager._read_one_line_from_pipe(process.stdout)
        return True

    def _remove_metadatum(self, metadatum_name):
        metadata = self._get_metadata()
        was_removed = False
        try:
            del(metadata[metadatum_name])
            was_removed = True
        except KeyError:
            pass
        if was_removed:
            with self._io_manager._silent():
                self._write_metadata_py(metadata)

    def _rename(self, new_path):
        if self._is_in_git_repository():
            if self._is_git_unknown():
                command = 'mv {} {}'
            else:
                command = 'git mv --force {} {}'
        elif self._is_svn_versioned():
            command = 'svn --force mv {} {}'
        else:
            command = 'mv {} {}'
        command = command.format(self._path, new_path)
        process = self._io_manager.make_subprocess(command)
        self._io_manager._read_from_pipe(process.stdout)
        self._path = new_path

    def _rename_interactively(
        self,
        extension=None,
        file_name_callback=None,
        force_lowercase=True,
        ):
        base_name = os.path.basename(self._path)
        line = 'current name: {}'.format(base_name)
        self._io_manager._display(line)
        getter = self._io_manager._make_getter()
        getter.append_string('new name')
        new_package_name = getter._run()
        if self._session.is_backtracking or new_package_name is None:
            return
        new_package_name = stringtools.strip_diacritics(new_package_name)
        if file_name_callback:
            new_package_name = file_name_callback(new_package_name)
        new_package_name = new_package_name.replace(' ', '_')
        if force_lowercase:
            new_package_name = new_package_name.lower()
        if extension and not new_package_name.endswith(extension):
            new_package_name = new_package_name + extension
        lines = []
        line = 'current name: {}'.format(base_name)
        lines.append(line)
        line = 'new name:     {}'.format(new_package_name)
        lines.append(line)
        self._io_manager._display(lines)
        result = self._io_manager._confirm()
        if self._session.is_backtracking or not result:
            return
        new_directory = os.path.join(
            os.path.dirname(self._path),
            new_package_name,
            )
        if self._is_svn_versioned():
            # rename package directory
            command = 'svn mv {} {}'
            command = command.format(self._path, new_directory)
            self._io_manager.spawn_subprocess(command)
            # commit
            commit_message = 'renamed {} to {}.'
            commit_message = commit_message.format(
                base_name,
                new_package_name,
                )
            commit_message = commit_message.replace('_', ' ')
            parent_directory = os.path.dirname(self._path)
            command = 'svn commit -m {!r} {}'
            command = command.format(
                commit_message,
                parent_directory,
                )
            self._io_manager.spawn_subprocess(command)
        else:
            command = 'mv {} {}'
            command = command.format(self._path, new_directory)
            self._io_manager.spawn_subprocess(command)
        # update path name to reflect change
        self._path = new_directory
        self._session._is_backtracking_locally = True

    def _run(self):
        controller = self._io_manager._controller(
            consume_local_backtrack=True,
            controller=self,
            )
        directory = systemtools.TemporaryDirectoryChange(self._path)
        with controller, directory:
                self._enter_run()
                self._session._pending_redraw = True
                while True:
                    result = self._session.wrangler_navigation_directive
                    if not result:
                        menu = self._make_main_menu()
                        result = menu._run()
                    if self._exit_run():
                        break
                    elif not result:
                        continue
                    self._handle_input(result)
                    if self._exit_run():
                        break

    def _run_asset_manager(self, path):
        manager = self._manager_class(path=path, session=self._session)
        manager._run()

    def _space_delimited_lowercase_name_to_asset_name(
        self, space_delimited_lowercase_name):
        space_delimited_lowercase_name = space_delimited_lowercase_name.lower()
        asset_name = space_delimited_lowercase_name.replace(' ', '_')
        return asset_name

    def _test_add(self):
        assert self._is_up_to_date()
        path_1 = os.path.join(self._path, 'tmp_1.py')
        path_2 = os.path.join(self._path, 'tmp_2.py')
        with systemtools.FilesystemState(remove=[path_1, path_2]):
            with open(path_1, 'w') as file_pointer:
                file_pointer.write('')
            with open(path_2, 'w') as file_pointer:
                file_pointer.write('')
            assert os.path.exists(path_1)
            assert os.path.exists(path_2)
            assert not self._is_up_to_date()
            assert self._get_unadded_asset_paths() == [path_1, path_2]
            assert self._get_added_asset_paths() == []
            with self._io_manager._silent():
                self.add()
            assert self._get_unadded_asset_paths() == []
            assert self._get_added_asset_paths() == [path_1, path_2]
            with self._io_manager._silent():
                self._unadd_added_assets()
            assert self._get_unadded_asset_paths() == [path_1, path_2]
            assert self._get_added_asset_paths() == []
        assert self._is_up_to_date()
        return True

    def _test_remove_unadded_assets(self):
        assert self._is_up_to_date()
        path_3 = os.path.join(self._path, 'tmp_3.py')
        path_4 = os.path.join(self._path, 'tmp_4.py')
        with systemtools.FilesystemState(remove=[path_3, path_4]):
            with open(path_3, 'w') as file_pointer:
                file_pointer.write('')
            with open(path_4, 'w') as file_pointer:
                file_pointer.write('')
            assert os.path.exists(path_3)
            assert os.path.exists(path_4)
            assert not self._is_up_to_date()
            assert self._get_unadded_asset_paths() == [path_3, path_4]
            with self._io_manager._silent():
                self.remove_unadded_assets()
        assert self._is_up_to_date()
        return True

    def _test_revert(self):
        assert self._is_up_to_date()
        assert self._get_modified_asset_paths() == []
        file_name = self._find_first_file_name()
        if not file_name:
            return
        file_path = os.path.join(self._path, file_name)
        with systemtools.FilesystemState(keep=[file_path]):
            with open(file_path, 'a') as file_pointer:
                string = '# extra text appended during testing'
                file_pointer.write(string)
            assert not self._is_up_to_date()
            assert self._get_modified_asset_paths() == [file_path]
            with self._io_manager._silent():
                self.revert()
        assert self._get_modified_asset_paths() == []
        assert self._is_up_to_date()
        return True

    def _unadd_added_assets(self):
        paths = []
        paths.extend(self._get_added_asset_paths())
        paths.extend(self._get_modified_asset_paths())
        commands = []
        if self._is_git_versioned():
            for path in paths:
                command = 'git reset -- {}'.format(path)
                commands.append(command)
        elif self._is_svn_versioned():
            for path in paths:
                command = 'svn revert {}'.format(path)
                commands.append(command)
        else:
            raise ValueError(self)
        command = ' && '.join(commands)
        self._io_manager.spawn_subprocess(command)

    ### PUBLIC METHODS ###

    def add(self, dry_run=False):
        r'''Adds files to repository.

        Returns none.
        '''
        change = systemtools.TemporaryDirectoryChange(directory=self._path)
        with change:
            inputs = self._get_unadded_asset_paths()
            outputs = []
            if dry_run:
                return inputs, outputs
            if not inputs:
                message = 'nothing to add.'
                self._io_manager._display(message)
                return
            messages = []
            messages.append('will add ...')
            for path in inputs:
                messages.append(self._tab + path)
            self._io_manager._display(messages)
            result = self._io_manager._confirm()
            if self._session.is_backtracking or not result:
                return
            command = self._repository_add_command
            assert isinstance(command, str)
            self._io_manager.run_command(command)

    def add_metadatum(self):
        r'''Adds metadatum to ``__metadata.py__``.

        Returns none.
        '''
        getter = self._io_manager._make_getter()
        getter.append_snake_case_string(
            'metadatum name',
            allow_empty=False,
            )
        getter.append_expr('metadatum value')
        result = getter._run()
        if self._session.is_backtracking or result is None:
            return
        if result:
            metadatum_name, metadatum_value = result
            self._add_metadatum(metadatum_name, metadatum_value)

    def check_package(
        self,
        problems_only=None,
        return_messages=False,
        return_supply_messages=False,
        supply_missing=None,
        ):
        r'''Checks package.

        Returns none.
        '''
        if problems_only is None:
            prompt = 'show problem assets only?'
            result = self._io_manager._confirm(prompt)
            if self._session.is_backtracking or result is None:
                return
            problems_only = bool(result)
        tab = self._io_manager._tab
        optional_directories, optional_files = [], []
        missing_directories, missing_files = [], []
        required_directories, required_files = [], []
        supplied_directories, supplied_files = [], []
        unrecognized_directories, unrecognized_files = [], []
        names = self._list()
        for name in names:
            path = os.path.join(self._path, name)
            if os.path.isdir(path):
                if name in self._required_directories:
                    required_directories.append(path)
                elif name in self._optional_directories:
                    optional_directories.append(path)
                else:
                    unrecognized_directories.append(path)
            elif os.path.isfile(path):
                if name in self._required_files:
                    required_files.append(path)
                elif name in self._optional_files:
                    optional_files.append(path)
                else:
                    unrecognized_files.append(path)
            else:
                raise TypeError(path)
        recognized_directories = required_directories + optional_directories
        recognized_files = required_files + optional_files
        for required_directory in self._required_directories:
            path = os.path.join(self._path, required_directory)
            if path not in recognized_directories:
                missing_directories.append(path)
        for required_file in self._required_files:
            path = os.path.join(self._path, required_file)
            if path not in recognized_files:
                missing_files.append(path)
        messages = []
        if not problems_only:
            messages_ = self._format_ratio_check_messages(
                required_directories,
                self._required_directories,
                'required directory',
                participal='found',
                )
            messages.extend(messages_)
        if missing_directories:
            messages_ = self._format_ratio_check_messages(
                missing_directories,
                self._required_directories,
                'required directory',
                'missing',
                )
            messages.extend(messages_)
        if not problems_only:
            messages_ = self._format_ratio_check_messages(
                required_files,
                self._required_files,
                'required file',
                'found',
                )
            messages.extend(messages_)
        if missing_files:
            messages_ = self._format_ratio_check_messages(
                missing_files,
                self._required_files,
                'required file',
                'missing',
                )
            messages.extend(messages_)
        if not problems_only:
            messages_ = self._format_counted_check_messages(
                optional_directories,
                'optional directory',
                participal='found',
                )
            messages.extend(messages_)
            messages_ = self._format_counted_check_messages(
                optional_files,
                'optional file',
                participal='found',
                )
            messages.extend(messages_)
        messages_ = self._format_counted_check_messages(
            unrecognized_directories,
            'unrecognized directory',
            participal='found',
            )
        messages.extend(messages_)
        messages_ = self._format_counted_check_messages(
            unrecognized_files,
            'unrecognized file',
            participal='found',
            )
        messages.extend(messages_)
        tab = self._io_manager._tab
        messages = [tab + _ for _ in messages]
        name = self._path_to_asset_menu_display_string(self._path)
        found_problems = missing_directories or \
            missing_files or \
            unrecognized_directories or \
            unrecognized_files
        count = len(names)
        wranglers = self._get_top_level_wranglers()
        if wranglers or not return_messages:
            message = 'top level ({} assets):'.format(count)
            if not found_problems:
                message = '{} OK'.format(message)
            messages.insert(0, message)
            messages = [stringtools.capitalize_start(_) for _ in messages]
            messages = [tab + _ for _ in messages]
        message = '{}:'.format(name)
        if not wranglers and not found_problems and return_messages:
            message = '{} OK'.format(message)
        messages.insert(0, message)
        if wranglers:
            controller = self._io_manager._controller(
                controller=self,
                current_score_directory=self._path,
                )
            silence = self._io_manager._silent()
            with controller, silence:
                tab = self._io_manager._tab
                for wrangler in wranglers:
                    if hasattr(wrangler, 'check_every_package'):
                        result = wrangler.check_every_package(
                            indent=1,
                            problems_only=problems_only,
                            supply_missing=False,
                            )
                    else:
                        result = wrangler.check_every_file()
                    messages_, missing_directories_, missing_files_ = result
                    missing_directories.extend(missing_directories_)
                    missing_files.extend(missing_files_)
                    messages_ = [
                        stringtools.capitalize_start(_) for _ in messages_]
                    messages_ = [tab + _ for _ in messages_]
                    messages.extend(messages_)
        if return_messages:
            return messages, missing_directories, missing_files
        else:
            self._io_manager._display(messages)
        if not missing_directories + missing_files:
            return messages, missing_directories, missing_files
        if supply_missing is None:
            directory_count = len(missing_directories)
            file_count = len(missing_files)
            directories = stringtools.pluralize('directory', directory_count)
            files = stringtools.pluralize('file', file_count)
            if missing_directories and missing_files:
                prompt = 'supply missing {} and {}?'.format(directories, files)
            elif missing_directories:
                prompt = 'supply missing {}?'.format(directories)
            elif missing_files:
                prompt = 'supply missing {}?'.format(files)
            else:
                raise ValueError
            result = self._io_manager._confirm(prompt)
            if self._session.is_backtracking or result is None:
                return
            supply_missing = bool(result)
        if not supply_missing:
            return messages, missing_directories, missing_files
        messages = []
        messages.append('Made:')
        for missing_directory in missing_directories:
            os.makedirs(missing_directory)
            gitignore_path = os.path.join(missing_directory, '.gitignore')
            with open(gitignore_path, 'w') as file_pointer:
                file_pointer.write('')
            message = tab + missing_directory
            messages.append(message)
            supplied_directories.append(missing_directory)
        for missing_file in missing_files:
            if missing_file.endswith('__init__.py'):
                lines = []
                lines.append(self._configuration.unicode_directive)
            elif missing_file.endswith('__metadata__.py'):
                lines = []
                lines.append(self._configuration.unicode_directive)
                lines.append('import collections')
                lines.append('')
                lines.append('')
                lines.append('metadata = collections.OrderedDict([])')
            elif missing_file.endswith('__views__.py'):
                lines = []
                lines.append(self._configuration.unicode_directive)
                lines.append(self._abjad_import_statement)
                lines.append('from scoremanager import idetools')
                lines.append('')
                lines.append('')
                line = 'view_inventory = idetools.ViewInventory([])'
                lines.append(line)
            elif missing_file.endswith('definition.py'):
                source_path = os.path.join(
                    self._configuration.score_manager_directory,
                    'boilerplate',
                    'definition.py',
                    )
                with open(source_path, 'r') as file_pointer:
                    lines = file_pointer.readlines()
                lines = [_.strip() for _ in lines]
            else:
                message = 'do not know how to make stub for {}.'
                message = message.format(missing_file)
                raise ValueError(message)
            contents = '\n'.join(lines)
            with open(missing_file, 'w') as file_pointer:
                file_pointer.write(contents)
            message = tab + missing_file
            messages.append(message)
            supplied_files.append(missing_file)
        if return_supply_messages:
            return messages, supplied_directories, supplied_files
        else:
            self._io_manager._display(messages)
        return messages, supplied_directories, supplied_files

    def commit(self, commit_message=None):
        r'''Commits files to repository.

        Returns none.
        '''
        change = systemtools.TemporaryDirectoryChange(directory=self._path)
        with change:
            self._session._attempted_to_commit = True
            if self._session.is_repository_test:
                return
            if commit_message is None:
                getter = self._io_manager._make_getter()
                getter.append_string('commit message')
                commit_message = getter._run()
                if self._session.is_backtracking or commit_message is None:
                    return
                message = 'commit message will be: "{}"'
                message = message.format(commit_message)
                self._io_manager._display(message)
                result = self._io_manager._confirm()
                if self._session.is_backtracking or not result:
                    return
            message = self._get_score_package_directory_name()
            message = message + ' ...'
            command = self._make_repository_commit_command(commit_message)
            self._io_manager.run_command(command, capitalize=False)

    def display_status(self):
        r'''Displays repository status.

        Returns none.
        '''
        change = systemtools.TemporaryDirectoryChange(directory=self._path)
        with change:
            command = self._display_status_command
            if not command:
                message = 'path not in repository: {}.'
                message = message.format(self._path)
                self._io_manager._display(message)
                return
            messages = []
            self._session._attempted_display_status = True
            message = 'Repository status for {} ...'
            message = message.format(self._path)
            messages.append(message)
            process = self._io_manager.make_subprocess(command)
            path = self._path
            path = path + os.path.sep
            clean_lines = []
            stdout_lines = self._io_manager._read_from_pipe(process.stdout)
            for line in stdout_lines.splitlines():
                line = str(line)
                clean_line = line.strip()
                clean_line = clean_line.replace(path, '')
                clean_lines.append(clean_line)
            everything_ok = False
            for line in clean_lines:
                if 'nothing to commit' in line:
                    everything_ok = True
                    break
            if clean_lines and not everything_ok:
                messages.extend(clean_lines)
            else:
                first_message = messages[0]
                first_message = first_message + ' OK'
                messages[0] = first_message
                clean_lines.append(message)
            self._io_manager._display(messages, capitalize=False)

    def edit_init_py(self):
        r'''Edits ``__init__.py``.

        Returns none.
        '''
        self._open_file(self._init_py_file_path)

    def get_metadatum(self):
        r'''Gets metadatum from ``__metadata.py__``.

        Returns none.
        '''
        getter = self._io_manager._make_getter()
        getter.append_string('metadatum name')
        result = getter._run()
        if self._session.is_backtracking or result is None:
            return
        metadatum = self._get_metadatum(result)
        message = '{!r}'.format(metadatum)
        self._io_manager._display(message)

    def list_init_py(self):
        r'''Lists ``__init__.py``.

        Returns none.
        '''
        self._io_manager._display(self._init_py_file_path)

    def remove_metadatum(self):
        r'''Removes metadatum from ``__metadata__.py``.

        Returns none.
        '''
        getter = self._io_manager._make_getter()
        getter.append_string('metadatum name')
        result = getter._run()
        if self._session.is_backtracking or not result:
            return
        metadatum_name = result
        self._remove_metadatum(metadatum_name)

    def remove_unadded_assets(self, dry_run=False):
        r'''Removes files not yet added to repository.

        Returns none.
        '''
        return self._remove_unadded_assets(dry_run=dry_run)

    def revert(self):
        r'''Reverts files to repository.

        Returns none.
        '''
        change = systemtools.TemporaryDirectoryChange(directory=self._path)
        with change:
            self._session._attempted_to_revert = True
            if self._session.is_repository_test:
                return
            paths = []
            paths.extend(self._get_added_asset_paths())
            paths.extend(self._get_modified_asset_paths())
            messages = []
            messages.append('will revert ...')
            for path in paths:
                messages.append(self._io_manager._tab + path)
            self._io_manager._display(messages)
            result = self._io_manager._confirm()
            if self._session.is_backtracking or not result:
                return
            commands = []
            if self._is_in_git_repository():
                for path in paths:
                    command = 'git checkout {}'.format(path)
                    commands.append(command)
            elif self._is_svn_versioned():
                for path in paths:
                    command = 'svn revert {}'.format(path)
                    commands.append(command)
            else:
                raise ValueError(self)
            command = ' && '.join(commands)
            self._io_manager.spawn_subprocess(command)

    def update(self, messages_only=False):
        r'''Updates files from repository.

        Returns none.
        '''
        messages = []
        change = systemtools.TemporaryDirectoryChange(directory=self._path)
        with change:
            self._session._attempted_to_update = True
            if self._session.is_repository_test:
                return messages
            command = self._repository_update_command
            messages = self._io_manager.run_command(
                command,
                messages_only=True,
                )
        if messages and messages[-1].startswith('At revision'):
            messages = messages[-1:]
        elif messages and 'Already up-to-date' in messages[-1]:
            messages = messages[-1:]
        if messages_only:
            return messages
        self._io_manager._display(messages)

    def write_stub_init_py(self):
        r'''Writes stub ``__init__.py``.

        Returns none.
        '''
        path = self._init_py_file_path
        message = 'will write stub to {}.'
        message = message.format(path)
        self._io_manager._display(message)
        result = self._io_manager._confirm()
        if self._session.is_backtracking or not result:
            return
        self._io_manager.write_stub(self._init_py_file_path)