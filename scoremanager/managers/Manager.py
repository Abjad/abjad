# -*- encoding: utf-8 -*-
import copy
import filecmp
import os
import shutil
import subprocess
from abjad.tools import stringtools
from abjad.tools import systemtools
from scoremanager.core.Controller import Controller


class Manager(Controller):
    r'''Manager.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_main_menu',
        '_path',
        )

    ### INITIALIZER ###

    def __init__(self, path=None, session=None):
        assert session is not None
        Controller.__init__(self, session=session)
        assert path is None or os.path.sep in path, repr(path)
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
        return self._space_delimited_lowercase_class_name

    @property
    def _is_visible(self):
        raise NotImplementedError

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
            raise ValueError(self)

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
            return os.path.basename(self._path)

    @property
    def _user_input_to_action(self):
        superclass = super(Manager, self)
        result = superclass._user_input_to_action
        result = copy.deepcopy(result)
        result.update({
            'cp': self.copy,
            'ls': self.list,
            'll': self.list_long,
            'rm': self.remove,
            'rad': self.add_to_repository,
            'rci': self.commit_to_repository,
            'ren': self.rename,
            'rst': self.repository_status,
            'rrv': self.revert_to_repository,
            'rua': self.remove_unadded_assets,
            'rup': self.update_from_repository,
            })
        return result

    ### PRIVATE METHODS ###

    def _enter_run(self):
        pass

    def _exit_run(self):
        return self._should_backtrack()

    def _find_first_file_name(self):
        for directory_entry in os.listdir(self._path):
            if not directory_entry.startswith('.'):
                path = os.path.join(self._path, directory_entry)
                if os.path.isfile(path):
                    return directory_entry

    def _get_added_asset_paths(self):
        if self._is_git_versioned():
            command = 'git status --porcelain {}'
            command = command.format(self._path)
            process = self._io_manager.make_subprocess(command)
            paths = []
            for line in process.stdout.readlines():
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
                if line.startswith('A'):
                    path = line.strip('A')
                    path = path.strip()
                    paths.append(path)
        else:
            raise ValueError(self)
        return paths

    def _get_modified_asset_paths(self):
        if self._is_git_versioned():
            command = 'git status --porcelain {}'
            command = command.format(self._path)
            process = self._io_manager.make_subprocess(command)
            paths = []
            for line in process.stdout.readlines():
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
                if line.startswith('M'):
                    path = line.strip('M')
                    path = path.strip()
                    paths.append(path)
        else:
            raise ValueError(self)
        return paths

    def _get_repository_root_directory(self):
        if self._is_git_versioned():
            command = 'git rev-parse --show-toplevel'
            process = self._io_manager.make_subprocess(command)
            line = process.stdout.readline()
            line = line.strip()
            return line
        elif self._is_svn_versioned():
            pass
        else:
            raise ValueError(self)

    def _get_score_package_directory_name(self):
        line = self._path
        path = self._configuration.abjad_score_packages_directory_path
        line = line.replace(path, '')
        path = self._configuration.user_score_packages_directory_path
        line = line.replace(path, '')
        line = line.lstrip(os.path.sep)
        return line

    def _get_unadded_asset_paths(self):
        if self._is_git_versioned():
            command = 'git status --porcelain {}'
            command = command.format(self._path)
            process = self._io_manager.make_subprocess(command)
            paths = []
            for line in process.stdout.readlines():
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
                if line.startswith('?'):
                    path = line.strip('?')
                    path = path.strip()
                    paths.append(path)
        else:
            raise ValueError(self)
        return paths

    def _get_wrangler_navigation_directive(self):
        pass

    def _initialize_file_name_getter(self):
        getter = self._io_manager.make_getter()
        getter.append_dash_case_file_name('new name')
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
        first_line = process.stdout.readline()
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
        first_line = process.stdout.readline()
        first_line = first_line.strip()
        if first_line.startswith('??'):
            return True
        return False

    def _is_git_versioned(self, path=None):
        if not self._is_in_git_repository(path=path):
            return False
        command = 'git status --porcelain {}'
        command = command.format(path)
        process = self._io_manager.make_subprocess(command)
        first_line = process.stdout.readline()
        first_line = first_line.strip()
        if first_line == '':
            return True
        elif first_line.startswith('M'):
            return True
        else:
            return False

    def _is_in_git_repository(self, path=None):
        path = path or self._path
        if path is None:
            return False
        if not os.path.exists(path):
            return False
        command = 'git status --porcelain {}'
        command = command.format(path)
        process = self._io_manager.make_subprocess(command)
        first_line = process.stdout.readline()
        if first_line.startswith('fatal:'):
            return False
        else:
            return True

    def _is_populated_directory(self, directory_path):
        if os.path.exists(directory_path):
            if os.listdir(directory_path):
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
        first_line = process.stdout.readline()
        if first_line.startswith('svn: warning:'):
            return False
        else:
            return True

    def _is_up_to_date(self):
        if self._is_git_versioned():
            command = 'git status --porcelain {}'
        elif self._is_svn_versioned():
            command = 'svn st {}'
        else:
            raise ValueError(self)
        command = command.format(self._path)
        process = self._io_manager.make_subprocess(command)
        first_line = process.stdout.readline()
        return first_line == ''

    def _list(self, public_entries_only=False):
        result = []
        if not os.path.exists(self._path):
            return result
        if public_entries_only:
            for directory_entry in sorted(os.listdir(self._path)):
                if directory_entry[0].isalpha():
                    if not directory_entry.endswith('.pyc'):
                        if not directory_entry in ('test',):
                            result.append(directory_entry)
        else:
            for directory_entry in sorted(os.listdir(self._path)):
                if not directory_entry.startswith('.'):
                    if not directory_entry.endswith('.pyc'):
                        result.append(directory_entry)
        return result

    def _remove(self):
        if self._is_in_git_repository():
            if self._is_git_unknown():
                command = 'rm -rf {}'
            else:
                command = 'git rm --force {}'
        elif self._is_svn_versioned():
            command = 'svn --force rm {}'
        else:
            command = 'rm -rf {}'
        command = command.format(self._path)
        process = self._io_manager.make_subprocess(command)
        process.stdout.readline()
        return True

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
        self._io_manager.display('')

    def _run(self, pending_user_input=None):
        from scoremanager import iotools
        if pending_user_input:
            self._session._pending_user_input = pending_user_input
        context = iotools.ControllerContext(self)
        directory_change = systemtools.TemporaryDirectoryChange(self._path)
        with context, directory_change:
                self._enter_run()
                while True:
                    result = self._get_wrangler_navigation_directive()
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

    def _space_delimited_lowercase_name_to_asset_name(
        self, space_delimited_lowercase_name):
        space_delimited_lowercase_name = space_delimited_lowercase_name.lower()
        asset_name = space_delimited_lowercase_name.replace(' ', '_')
        return asset_name

    def _test_add_to_repository(self):
        assert self._is_up_to_date()
        path_1 = os.path.join(self._path, 'tmp_1.py')
        path_2 = os.path.join(self._path, 'tmp_2.py')
        assert not os.path.exists(path_1)
        assert not os.path.exists(path_2)
        with file(path_1, 'w') as file_pointer:
            file_pointer.write('')
        with file(path_2, 'w') as file_pointer:
            file_pointer.write('')
        assert os.path.exists(path_1)
        assert os.path.exists(path_2)
        assert not self._is_up_to_date()
        assert self._get_unadded_asset_paths() == [path_1, path_2]
        assert self._get_added_asset_paths() == []
        self.add_to_repository(prompt=False)
        assert self._get_unadded_asset_paths() == []
        assert self._get_added_asset_paths() == [path_1, path_2]
        self.revert_to_repository(prompt=False)
        assert self._get_unadded_asset_paths() == [path_1, path_2]
        assert self._get_added_asset_paths() == []
        os.remove(path_1)
        os.remove(path_2)
        assert not os.path.exists(path_1)
        assert not os.path.exists(path_2)
        assert self._is_up_to_date()
        return True

    def _test_remove_unadded_assets(self):
        assert self._is_up_to_date()
        path_3 = os.path.join(self._path, 'tmp_3.py')
        path_4 = os.path.join(self._path, 'tmp_4.py')
        assert not os.path.exists(path_3)
        assert not os.path.exists(path_4)
        with file(path_3, 'w') as file_pointer:
            file_pointer.write('')
        with file(path_4, 'w') as file_pointer:
            file_pointer.write('')
        assert os.path.exists(path_3)
        assert os.path.exists(path_4)
        assert not self._is_up_to_date()
        assert self._get_unadded_asset_paths() == [path_3, path_4]
        try:
            self.remove_unadded_assets(prompt=False)
        finally:
            if os.path.exists(path_3):
                os.remove(path_3)
            if os.path.exists(path_4):
                os.remove(path_4)
        assert not os.path.exists(path_3)
        assert not os.path.exists(path_4)
        assert self._is_up_to_date()
        return True

    def _test_revert_to_repository(self):
        assert self._is_up_to_date()
        assert self._get_modified_asset_paths() == []
        file_name = self._find_first_file_name()
        if not file_name:
            return
        file_path = os.path.join(self._path, file_name)
        home_directory = self._configuration.home_directory_path
        backup_copy = os.path.join(home_directory, file_name + '.back')
        shutil.copyfile(file_path, backup_copy)
        assert filecmp.cmp(file_path, backup_copy)
        try:
            with file(file_path, 'a') as file_pointer:
                string = '# extra text appended during testing'
                file_pointer.write(string)
            assert not self._is_up_to_date()
            assert self._get_modified_asset_paths() == [file_path]
            self.revert_to_repository(prompt=False)
        finally:
            shutil.copyfile(backup_copy, file_path)
        assert self._get_modified_asset_paths() == []
        assert self._is_up_to_date()
        return True

    ### PUBLIC METHODS ###

    def add_to_repository(self, prompt=True):
        r'''Adds unversioned assets to repository.

        Returns none.
        '''
        self._session._attempted_to_add_to_repository = True
        if self._session.is_repository_test:
            return
        line = self._get_score_package_directory_name()
        line = line + ' ...'
        self._io_manager.display(line, capitalize_first_character=False)
        command = self._repository_add_command
        assert isinstance(command, str)
        process = self._io_manager.make_subprocess(command)
        lines = [line.strip() for line in process.stdout.readlines()]
        lines.append('')
        self._io_manager.display(lines)
        self._io_manager.proceed(prompt=prompt)

    def commit_to_repository(self, commit_message=None, prompt=True):
        r'''Commits unversioned assets to repository.

        Returns none.
        '''
        self._session._attempted_to_commit_to_repository = True
        if self._session.is_repository_test:
            return
        if commit_message is None:
            getter = self._io_manager.make_getter()
            getter.append_string('commit message')
            commit_message = getter._run()
            if self._should_backtrack():
                return
            line = 'commit message will be: "{}"\n'.format(commit_message)
            self._io_manager.display(line)
            if not self._io_manager.confirm():
                return
        lines = []
        line = self._get_score_package_directory_name()
        line = line + ' ...'
        lines.append(line)
        command = 'svn commit -m "{}" {}'
        command = command.format(commit_message, self._path)
        process = self._io_manager.make_subprocess(command)
        lines.extend([line.strip() for line in process.stdout.readlines()])
        lines.append('')
        self._io_manager.display(
            lines,
            capitalize_first_character=False,
            )
        self._io_manager.proceed(prompt=prompt)

    def copy(self):
        r'''Copies asset.

        Returns none.
        '''
        getter = self._initialize_file_name_getter()
        result = getter._run()
        if self._should_backtrack():
            return
        new_asset_name = \
            self._space_delimited_lowercase_name_to_asset_name(result)
        parent_directory_path = os.path.dirname(self._path)
        new_path = os.path.join(parent_directory_path, new_asset_name)
        message = 'new path will be {}'
        message = message.format(new_path)
        self._io_manager.display(message)
        if not self._io_manager.confirm():
            return
        shutil.copyfile(self._path, new_path)
        self._io_manager.proceed('asset copied.')

    def doctest(self, prompt=True):
        r'''Runs doctest on asset.

        Returns none.
        '''
        if self._session.is_test:
            return
        command = 'ajv doctest {}'.format(self._path)
        process = self._io_manager.make_subprocess(command)
        lines = [line.strip() for line in process.stdout.readlines()]
        if lines:
            if lines[0] == '':
                lines.remove('')
            lines.append('')
            self._io_manager.display(lines)
        self._io_manager.proceed(prompt=prompt)

    def list(self):
        r'''Lists directory.

        Returns none.
        '''
        lines = []
        for directory_entry in self._list():
            path = os.path.join(self._path, directory_entry)
            if os.path.isdir(path):
                line = directory_entry + '/'
            elif os.path.isfile(path):
                line = directory_entry
            else:
                raise TypeError(directory_entry)
            lines.append(line)
        lines.append('')
        self._io_manager.display(
            lines,
            capitalize_first_character=False,
            )
        self._session._hide_next_redraw = True

    def list_long(self):
        r'''Lists directory with ``ls -l``.

        Returns none.
        '''
        command = 'ls -l {} | grep -v .pyc'
        command = command.format(self._path)
        lines = []
        process = self._io_manager.make_subprocess(command)
        lines = [line.strip() for line in process.stdout.readlines()]
        lines.append('')
        self._io_manager.display(
            lines,
            capitalize_first_character=False,
            )
        self._session._hide_next_redraw = True

    def pytest(self, prompt=True):
        r'''Runs py.test on asset.

        Returns none.
        '''
        if self._session.is_test:
            return
        command = 'py.test -rf {}'.format(self._path)
        process = self._io_manager.make_subprocess(command)
        lines = [line.strip() for line in process.stdout.readlines()]
        if lines:
            lines.append('')
            self._io_manager.display(lines)
        self._io_manager.proceed(prompt=prompt)

    def remove(self, prompt=True):
        r'''Removes asset.

        Backtracks up one level from previous location of asset.

        Returns none.
        '''
        message = '{} will be removed.'
        message = message.format(self._path)
        if prompt:
            self._io_manager.display([message, ''])
            getter = self._io_manager.make_getter()
            getter.append_string("type 'remove' to proceed")
            result = getter._run()
            if self._should_backtrack():
                return
        # TODO: remove this branch?
        else:
            result = True
        if not result == 'remove':
            return
        self._remove()
        self._session._is_backtracking_locally = True

    def remove_unadded_assets(self, prompt=True):
        r'''Removes assets not yet added to repository.

        Returns none.
        '''
        paths = self._get_unadded_asset_paths()
        if not paths:
            return
        remove_command = self._shell_remove_command
        paths = ' '.join(paths)
        command = '{} {}'
        command = command.format(remove_command, paths)
        process = self._io_manager.make_subprocess(command)
        clean_lines = []
        for line in process.stdout.readlines():
            clean_line = line.strip()
            clean_lines.append(clean_line)
        clean_lines.append('')
        self._io_manager.display(
            clean_lines,
            capitalize_first_character=False,
            )
        self._io_manager.proceed(prompt=prompt)

    def rename(self):
        r'''Renames asset.

        Returns none.
        '''
        getter = self._initialize_file_name_getter()
        result = getter._run()
        if self._should_backtrack():
            return
        parent_directory_path = os.path.dirname(self._path)
        new_path = os.path.join(parent_directory_path, result)
        message = 'new path name will be: {!r}.'
        message = message.format(new_path)
        self._io_manager.display([message, ''])
        if not self._io_manager.confirm():
            return
        if self._rename(new_path):
            self._io_manager.proceed('asset renamed.')

    def repository_status(self, prompt=True):
        r'''Displays repository status of assets.

        Returns none.
        '''
        line = self._get_score_package_directory_name()
        line = line + ' ...'
        self._io_manager.display(line, capitalize_first_character=False)
        command = self._repository_status_command
        process = self._io_manager.make_subprocess(command)
        path = self._path
        path = path + os.path.sep
        clean_lines = []
        for line in process.stdout.readlines():
            clean_line = line.strip()
            clean_line = clean_line.replace(path, '')
            clean_lines.append(clean_line)
        clean_lines.append('')
        self._io_manager.display(
            clean_lines,
            capitalize_first_character=False,
            )
        self._session._hide_next_redraw = True

    def revert_to_repository(self, prompt=True):
        r'''Reverts assets from repository.

        Returns none.
        '''
        self._session._attempted_to_revert_to_repository = True
        if self._session.is_repository_test:
            return
        message = 'reverting {} ...'
        message = message.format(self._path)
        self._io_manager.display(message)
        self._revert_from_repository()
        self._io_manager.proceed(prompt=prompt)

    def update_from_repository(self, prompt=True):
        r'''Updates versioned assets.

        Returns none.
        '''
        self._session._attempted_to_update_from_repository = True
        if self._session.is_repository_test:
            return
        line = self._get_score_package_directory_name()
        line = line + ' ...'
        self._io_manager.display(line, capitalize_first_character=False)
        command = self._repository_update_command
        process = self._io_manager.make_subprocess(command)
        lines = [line.strip() for line in process.stdout.readlines()]
        lines.append('')
        self._io_manager.display(lines)
        self._io_manager.proceed(prompt=prompt)