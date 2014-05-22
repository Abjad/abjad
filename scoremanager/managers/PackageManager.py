# -*- encoding: utf-8 -*-
import collections
import itertools
import os
import shutil
from abjad.tools import stringtools
from abjad.tools import systemtools
from scoremanager.core.AssetController import AssetController


class PackageManager(AssetController):
    r'''Package manager.

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_asset_identifier',
        '_main_menu',
        '_package_name',
        '_path',
        )

    ### INITIALIZER ###

    def __init__(self, path=None, session=None):
        assert session is not None
        assert path is not None and os.path.sep in path
        superclass = super(PackageManager, self)
        superclass.__init__(session=session)
        self._asset_identifier = None
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
    def _init_py_file_path(self):
        return os.path.join(self._path, '__init__.py')

    @property
    def _input_to_method(self):
        superclass = super(PackageManager, self)
        result = superclass._input_to_method
        result = result.copy()
        result.update({
            'mda': self.add_metadatum,
            'mdg': self.get_metadatum,
            'mdrm': self.remove_metadatum,
            #
            'mdls': self.list_metadata_py,
            'mdo': self.open_metadata_py,
            'mdw': self.rewrite_metadata_py,
            #
            'no': self.open_init_py,
            'ns': self.write_stub_init_py,
            })
        return result

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
    def _repository_status_command(self):
        if not self._path:
            return
        if self._is_in_git_repository(path=self._path):
            return 'git status {}'.format(self._path)
        elif self._is_svn_versioned(path=self._path):
            return 'svn st {}'.format(self._path)
        else:
            return

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
        self.rewrite_metadata_py(
            metadata=metadata,
            confirm=False,
            display=False,
            )

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
        version_number = int(version_number_string)
        return version_number

    def _find_first_file_name(self):
        for directory_entry in os.listdir(self._path):
            if not directory_entry.startswith('.'):
                path = os.path.join(self._path, directory_entry)
                if os.path.isfile(path):
                    return directory_entry

    def _get_added_asset_paths(self):
        if self._is_in_git_repository():
            command = 'git status --porcelain {}'
            command = command.format(self._path)
            process = self._io_manager.make_subprocess(command)
            paths = []
            for line in process.stdout.readlines():
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
            for line in process.stdout.readlines():
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
        for entry in os.listdir(self._versions_directory):
            if entry.startswith(root) and entry.endswith(extension):
                version_number = self._file_name_to_version_number(entry)
                version_numbers.append(version_number)
        return version_numbers

    def _get_last_version_number(self):
        versions_directory = self._versions_directory
        if not os.path.exists(versions_directory):
            return
        file_names = os.listdir(versions_directory)
        if not file_names:
            return
        return max(self._file_name_to_version_number(_) for _ in file_names)

    def _get_metadata(self):
        metadata = None
        if os.path.isfile(self._metadata_py_path):
            with open(self._metadata_py_path, 'r') as file_pointer:
                file_contents_string = file_pointer.read()
            try:
                local_dict = {}
                exec(file_contents_string, globals(), local_dict)
                metadata = local_dict.get('metadata')
            except:
                message = 'can not interpret metadata py: {!r}.'
                message = message.format(self)
                print(message)
        metadata = metadata or collections.OrderedDict()
        return metadata

    def _get_metadatum(self, metadatum_name):
        metadata = self._get_metadata()
        metadatum = metadata.get(metadatum_name, None)
        return metadatum

    def _get_modified_asset_paths(self):
        if self._is_git_versioned():
            command = 'git status --porcelain {}'
            command = command.format(self._path)
            process = self._io_manager.make_subprocess(command)
            paths = []
            for line in process.stdout.readlines():
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
            for line in process.stdout.readlines():
                line = str(line)
                if line.startswith('M'):
                    path = line.strip('M')
                    path = path.strip()
                    paths.append(path)
        else:
            raise ValueError(self)
        return paths

    def _get_next_version_string(self):
        last_version_number = self._get_last_version_number()
        next_version_number = last_version_number + 1
        next_version_string = '%04d' % next_version_number
        return next_version_string

    def _get_repository_root_directory(self):
        if self._is_in_git_repository():
            command = 'git rev-parse --show-toplevel'
            process = self._io_manager.make_subprocess(command)
            line = str(process.stdout.readline())
            line = line.strip()
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

    def _get_unadded_asset_paths(self):
        if self._is_in_git_repository():
            command = 'git status --porcelain {}'
            command = command.format(self._path)
            process = self._io_manager.make_subprocess(command)
            paths = []
            for line in process.stdout.readlines():
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
            for line in process.stdout.readlines():
                line = str(line)
                if line.startswith('?'):
                    path = line.strip('?')
                    path = path.strip()
                    paths.append(path)
        else:
            raise ValueError(self)
        return paths

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
        first_line = str(process.stdout.readline())
        first_line = first_line.strip()
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
        first_line = str(process.stdout.readline())
        first_line = first_line.strip()
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
        first_line = str(process.stdout.readline())
        first_line = first_line.strip()
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
        first_line = str(process.stdout.readline())
        if first_line.startswith('fatal:'):
            return False
        else:
            return True

    def _is_populated_directory(self, directory):
        if os.path.exists(directory):
            if os.listdir(directory):
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
                if '.svn' in os.listdir(path_to_check):
                    is_in_svn_versioned_tree = True
            path_to_check = os.path.dirname(path_to_check)
            if path_to_check == root_directory:
                break
        if not is_in_svn_versioned_tree:
            return False
        command = 'svn st {}'
        command = command.format(path)
        process = self._io_manager.make_subprocess(command)
        first_line = str(process.stdout.readline())
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
        first_line = str(process.stdout.readline())
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
        dunder_files, files, directories = [], [], []
        for entry in entries:
            path = os.path.join(self._path, entry)
            if entry.startswith('_'):
                dunder_files.append(entry)
            elif os.path.isdir(path):
                directories.append(entry + '/')
            else:
                files.append(entry)
        result = files + dunder_files + directories
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
        menu.make_information_section(menu_entries=menu_entries)

    def _make_main_menu(self):
        superclass = super(PackageManager, self)
        menu = superclass._make_main_menu()
        self._make_asset_menu_section(menu)
        return menu

    @staticmethod
    def _make_metadata_lines(metadata):
        if metadata:
            lines = []
            for key, value in sorted(metadata.items()):
                key = repr(key)
                if hasattr(value, '_get_multiline_repr'):
                    repr_lines = \
                        value._get_multiline_repr(include_tools_package=True)
                    value = '\n    '.join(repr_lines)
                    lines.append('({}, {})'.format(key, value))
                else:
                    if hasattr(value, '_storage_format_specification'):
                        string = format(value)
                    else:
                        string = repr(value)
                    lines.append('({}, {})'.format(key, string))
            lines = ',\n    '.join(lines)
            result = 'metadata = collections.OrderedDict([\n    {},\n    ])'
            result = result.format(lines)
        else:
            result = 'metadata = collections.OrderedDict([])'
        return result

    def _make_metadata_menu_entries(self):
        result = []
        metadata = self._get_metadata()
        for key in sorted(metadata):
            display_string = key.replace('_', ' ')
            result.append((display_string, None, metadata[key], key))
        return result

    def _make_package_menu_section(self, menu):
        commands = []
        commands.append(('package - version', 'vr'))
        commands.append(('package - versions list', 'vrls'))
        if commands:
            menu.make_command_section(
                is_hidden=True,
                commands=commands,
                name='package',
                )

    def _open_versioned_file(self, file_name_prototype):
        with self._io_manager._make_interaction():
            getter = self._io_manager._make_getter()
            version_numbers = self._get_existing_version_numbers(
                file_name_prototype)
            if not version_numbers:
                message = 'no {} files in versions directory.'
                message = message.format(file_name_prototype)
                self._io_manager._display([message, ''])
                self._session._hide_next_redraw = True
                return
            prompt = 'version number ({})'
            prompt = prompt.format(version_numbers)
            getter.append_integer(prompt)
            version_number = getter._run()
            if self._session.is_backtracking:
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

    def _remove(self, confirm=True, display=True):
        if confirm:
            message = '{} will be removed.'
            message = message.format(self._path)
            self._io_manager._display([message, ''])
            getter = self._io_manager._make_getter()
            getter.append_string("type 'remove' to proceed")
            result = getter._run()
            if self._session.is_backtracking:
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
        line = str(process.stdout.readline())
        if cleanup_command:
            cleanup_command = cleanup_command.format(path)
            process = self._io_manager.make_subprocess(cleanup_command)
            line = str(process.stdout.readline())
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
            self.rewrite_metadata_py(
                metadata=metadata,
                confirm=False,
                display=False,
                )

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
        process.stdout.readline()
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
        if self._session.is_backtracking:
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
        lines.append('')
        self._io_manager._display(lines)
        result = self._io_manager._confirm()
        if self._session.is_backtracking:
            return
        if not result:
            return
        new_directory = self._path.replace(
            base_name,
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

    def _revert_from_repository(self):
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
        self._io_manager._display('')

    def _run(self, pending_input=None):
        from scoremanager import iotools
        if pending_input:
            self._session._pending_input = pending_input
        context = iotools.ControllerContext(
            consume_local_backtrack=True,
            controller=self,
            )
        directory_change = systemtools.TemporaryDirectoryChange(self._path)
        with context, directory_change:
                self._enter_run()
                while True:
                    result = self._session.wrangler_navigation_directive
                    if not result:
                        menu = self._make_main_menu()
                        result = menu._run()
                    if self._exit_run():
                        break
                    elif not result:
                        continue
                    self._handle_main_menu_result(result)
                    if self._exit_run():
                        break

    def _run_asset_manager(
        self,
        path,
        ):
        manager = self._manager_class(
            path=path,
            session=self._session,
            )
        manager._run()

    def _run_first_time(self, **kwargs):
        self._run(**kwargs)

    def _space_delimited_lowercase_name_to_asset_name(
        self, space_delimited_lowercase_name):
        space_delimited_lowercase_name = space_delimited_lowercase_name.lower()
        asset_name = space_delimited_lowercase_name.replace(' ', '_')
        return asset_name

    def _test_add_to_repository(self):
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
            self.add_to_repository(confirm=False, display=False)
            assert self._get_unadded_asset_paths() == []
            assert self._get_added_asset_paths() == [path_1, path_2]
            self.revert_to_repository(confirm=False, display=False)
            assert self._get_unadded_asset_paths() == [path_1, path_2]
            assert self._get_added_asset_paths() == []
        assert self._is_up_to_date()
        return True

    def _test_repository_clean(self):
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
            self.repository_clean(confirm=False, display=False)
        assert self._is_up_to_date()
        return True

    def _test_revert_to_repository(self):
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
            self.revert_to_repository(confirm=False, display=False)
        assert self._get_modified_asset_paths() == []
        assert self._is_up_to_date()
        return True

    def _write_metadata_py(self, metadata):
        lines = []
        lines.append(self._configuration.unicode_directive)
        lines.append('import collections')
        lines.append('')
        lines.append('')
        contents = '\n'.join(lines)
        metadata_lines = self._make_metadata_lines(metadata)
        contents = contents + '\n' + metadata_lines
        with open(self._metadata_py_path, 'w') as file_pointer:
            file_pointer.write(contents)

    ### PUBLIC METHODS ###

    def add_metadatum(self):
        r'''Adds metadatum to ``__metadata.py__``.

        Returns none.
        '''
        with self._io_manager._make_interaction():
            getter = self._io_manager._make_getter()
            getter.append_snake_case_string(
                'metadatum name',
                allow_empty=False,
                )
            getter.append_expr('metadatum value')
            result = getter._run()
            if self._session.is_backtracking:
                return
            if result:
                metadatum_name, metadatum_value = result
                self._add_metadatum(metadatum_name, metadatum_value)

    def add_to_repository(self, confirm=True, display=True):
        r'''Adds files to repository.

        Returns none.
        '''
        change = systemtools.TemporaryDirectoryChange(directory=self._path)
        interaction = self._io_manager._make_interaction(display=display)
        with change, interaction:
            self._session._attempted_to_add_to_repository = True
            if self._session.is_repository_test:
                return
            message = self._get_score_package_directory_name()
            message = message + ' ...'
            self._io_manager._display(message, capitalize=False)
            command = self._repository_add_command
            assert isinstance(command, str)
            self._io_manager.run_command(command)

    def commit_to_repository(
        self,
        commit_message=None,
        confirm=True,
        display=True,
        ):
        r'''Commits files to repository.

        Returns none.
        '''
        change = systemtools.TemporaryDirectoryChange(directory=self._path)
        interaction = self._io_manager._make_interaction(display=display)
        with change, interaction:
            self._session._attempted_to_commit_to_repository = True
            if self._session.is_repository_test:
                return
            if commit_message is None:
                getter = self._io_manager._make_getter()
                getter.append_string('commit message')
                commit_message = getter._run()
                if self._session.is_backtracking:
                    return
                if confirm:
                    message = 'commit message will be: "{}"\n'
                    message = message.format(commit_message)
                    self._io_manager._display(message)
                    result = self._io_manager._confirm()
                    if self._session.is_backtracking:
                        return
                    if not result:
                        return
            message = self._get_score_package_directory_name()
            message = message + ' ...'
            command = 'svn commit -m "{}" {}'
            command = command.format(commit_message, self._path)
            self._io_manager.run_command(command, capitalize=False)

    def get_metadatum(self):
        r'''Gets metadatum from ``__metadata.py__``.

        Returns none.
        '''
        with self._io_manager._make_interaction():
            getter = self._io_manager._make_getter()
            getter.append_string('metadatum name')
            result = getter._run()
            if self._session.is_backtracking:
                return
            metadatum = self._get_metadatum(result)
            message = '{!r}'.format(metadatum)
            self._io_manager._display(message)

    def list_metadata_py(self):
        r'''Lists ``__metadata__.py``.

        Returns none.
        '''
        with self._io_manager._make_interaction():
            self._io_manager._display(self._metadata_py_path)

    def open_init_py(self):
        r'''Opens ``__init__.py``.

        Returns none.
        '''
        self._open_file(self._init_py_file_path)

    def open_metadata_py(self):
        r'''Opens ``__metadata__.py``.

        Returns none.
        '''
        self._open_file(self._metadata_py_path)

    def remove_metadatum(self):
        r'''Removes metadatum from ``__metadata__.py``.

        Returns none.
        '''
        with self._io_manager._make_interaction():
            getter = self._io_manager._make_getter()
            getter.append_string('metadatum name')
            result = getter._run()
            if self._session.is_backtracking:
                return
            if result:
                metadatum_name = result
                self._remove_metadatum(metadatum_name)

    def repository_clean(self, confirm=True, display=True):
        r'''Removes files not yet added to repository.

        Returns none.
        '''
        self._repository_clean(confirm=confirm, display=display)

    def repository_status(self):
        r'''Displays repository status.

        Returns none.
        '''
        change = systemtools.TemporaryDirectoryChange(directory=self._path)
        interaction = self._io_manager._make_interaction()
        with change, interaction:
            self._session._attempted_repository_status = True
            message = self._path + '...'
            self._io_manager._display(message, capitalize=False)
            command = self._repository_status_command
            if not command:
                message = 'path not in repository: {}.'
                message = message.format(self._path)
                self._io_manager._display(message)
                return
            process = self._io_manager.make_subprocess(command)
            path = self._path
            path = path + os.path.sep
            clean_lines = []
            for line in process.stdout.readlines():
                line = str(line)
                clean_line = line.strip()
                clean_line = clean_line.replace(path, '')
                clean_lines.append(clean_line)
            self._io_manager._display(
                clean_lines,
                capitalize=False,
                )

    def revert_to_repository(self, confirm=True, display=True):
        r'''Reverts files to repository.

        Returns none.
        '''
        change = systemtools.TemporaryDirectoryChange(directory=self._path)
        interaction = self._io_manager._make_interaction()
        with change, interaction:
            self._session._attempted_to_revert_to_repository = True
            if self._session.is_repository_test:
                return
            if display:
                message = 'reverting {} ...'
                message = message.format(self._path)
                self._io_manager._display(message)
            self._revert_from_repository()

    def rewrite_metadata_py(
        self,
        confirm=True,
        metadata=None,
        display=True,
        ):
        r'''Rewrites ``__metadata.py__``.

        Returns none.
        '''
        with self._io_manager._make_interaction(display=display):
            if display:
                message = 'will rewrite {}.'
                message = message.format(self._metadata_py_path)
                self._io_manager._display(message)
            if confirm:
                result = self._io_manager._confirm()
                if self._session.is_backtracking:
                    return
                if not result:
                    return
            if metadata is None:
                metadata = self._get_metadata()
            self._write_metadata_py(metadata)

    def update_from_repository(self, confirm=True, display=True):
        r'''Updates files from repository.

        Returns none.
        '''
        change = systemtools.TemporaryDirectoryChange(directory=self._path)
        interaction = self._io_manager._make_interaction(display=display)
        with change, interaction:
            self._session._attempted_to_update_from_repository = True
            if self._session.is_repository_test:
                return
            line = self._get_score_package_directory_name()
            if display:
                line = line + ' ...'
                self._io_manager._display(line, capitalize=False)
            command = self._repository_update_command
            self._io_manager.run_command(command)

    def write_stub_init_py(self, confirm=True, display=True):
        r'''Writes stub ``__init__.py``.

        Returns none.
        '''
        with self._io_manager._make_interaction(display=display):
            path = self._init_py_file_path
            if display:
                message = 'will write stub to {}.'
                message = message.format(path)
                self._io_manager._display(message)
            if confirm:
                result = self._io_manager._confirm()
                if self._session.is_backtracking:
                    return
                if not result:
                    return
            self._io_manager.write_stub(self._init_py_file_path)