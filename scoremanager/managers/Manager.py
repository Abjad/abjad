# -*- encoding: utf-8 -*-
import copy
import os
import shutil
import subprocess
from abjad.tools import stringtools
from scoremanager.core.Controller import Controller


class Manager(Controller):
    r'''Manager.
    '''

    ### INITIALIZER ###

    def __init__(self, path=None, session=None):
        assert session is not None
        Controller.__init__(self, session=session)
        assert path is None or os.path.sep in path, repr(path)
        self._path = path
        self._generic_class_name = 'asset'

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
    def _plural_generic_class_name(self):
        return stringtools.pluralize_string(self._generic_class_name)

    @property
    def _repository_add_command(self):
        if not self._path:
            return
        if self._is_in_git_repository(path=self._path):
            return 'git add {}'.format(self._path)
        elif self._is_svn_versioned(path=self._path):
            return 'svn add {}'.format(self._path)
        else:
            raise ValueError(self)

    @property
    def _repository_status_command(self):
        if not self._path:
            return
        if self._is_in_git_repository(path=self._path):
            return 'git status {}'.format(self._path)
        elif self._is_svn_versioned(path=self._path):
            return 'svn st -u {}'.format(self._path)
        else:
            raise ValueError(self)

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
            'radd': self.add,
            'rci': self.commit,
            'ren': self.rename,
            'rup': self.update,
            'rst': self.status,
            })
        return result

    ### PRIVATE METHODS ###

    def _get_score_package_directory_name(self):
        line = self._path
        line = line.replace(
            self._configuration.abjad_score_packages_directory_path,
            '',
            )
        line = line.replace(
            self._configuration.user_score_packages_directory_path,
            '',
            )
        line = line.lstrip(os.path.sep)
        return line

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
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            )
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
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            )
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
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            )
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
        process = subprocess.Popen(
            command,
            shell=True,
            stderr=subprocess.PIPE,
            )
        first_line = process.stderr.readline()
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
        command = 'svn st -u {}'
        command = command.format(path)
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            )
        first_line = process.stdout.readline()
        if first_line.startswith('svn: warning:'):
            return False
        else:
            return True

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
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            )
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
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            )
        process.stdout.readline()
        self._path = new_path

    def _run(self, cache=False, clear=True, pending_user_input=None):
        from scoremanager import managers
        self._session._push_controller(self)
        self._io_manager._assign_user_input(pending_user_input)
        self._session._cache_breadcrumbs(cache=cache)
        if type(self) is managers.BuildDirectoryManager:
            self._session._is_navigating_to_build_directory = False
        if isinstance(self, managers.MaterialManager):
            self._session._is_navigating_to_next_material = False
            self._session._is_navigating_to_previous_material = False
            self._session._last_material_path = self._path
        while True:
            self._session._push_breadcrumb(self._breadcrumb)
            if self._session.is_navigating_to_build_directory and \
                type(self) is managers.ScorePackageManager:
                result = 'u'
            elif self._session.is_navigating_to_score_materials and \
                type(self) is managers.ScorePackageManager:
                result = 'm'
            elif self._session.is_navigating_to_score_segments and \
                type(self) is managers.ScorePackageManager:
                result = 'g'
            else:
                menu = self._make_main_menu()
                result = menu._run(clear=clear)
            if self._session._backtrack(source=self._backtracking_source):
                break
            elif not result:
                self._session._pop_breadcrumb()
                continue
            self._handle_main_menu_result(result)
            if self._session._backtrack(source=self._backtracking_source):
                break
            self._session._pop_breadcrumb()
        self._session._pop_controller()
        self._session._pop_breadcrumb()
        self._session._restore_breadcrumbs(cache=cache)

    def _space_delimited_lowercase_name_to_asset_name(
        self, space_delimited_lowercase_name):
        space_delimited_lowercase_name = space_delimited_lowercase_name.lower()
        asset_name = space_delimited_lowercase_name.replace(' ', '_')
        return asset_name

    ### PUBLIC METHODS ###

    def add(self, prompt=False):
        r'''Adds unversioned assets to repository.

        Returns none.
        '''
        line = self._get_score_package_directory_name()
        line = line + ' ...'
        self._io_manager.display(line, capitalize_first_character=False)
        command = self._repository_add_command,
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            )
        lines = [line.strip() for line in process.stdout.readlines()]
        lines.append('')
        self._io_manager.display(lines)
        self._io_manager.proceed(prompt=prompt)

    def commit(self, commit_message=None, prompt=True):
        r'''Commits unversioned assets to repository.

        Returns none.
        '''
        if commit_message is None:
            getter = self._io_manager.make_getter(where=self._where)
            getter.append_string('commit message')
            commit_message = getter._run(clear_terminal=False)
            if self._session._backtrack():
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
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            )
        lines.extend([line.strip() for line in process.stdout.readlines()])
        lines.append('')
        self._io_manager.display(
            lines, 
            capitalize_first_character=False,
            )
        self._io_manager.proceed(prompt=prompt)

    def copy(
        self, 
        pending_user_input=None,
        ):
        r'''Copies asset.

        Returns none.
        '''
        self._io_manager._assign_user_input(pending_user_input)
        getter = self._initialize_file_name_getter()
        result = getter._run()
        if self._session._backtrack():
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
        command = 'ajv doctest {}'.format(self._path)
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
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
        command = 'ls -l {}'
        command = command.format(self._path)
        lines = []
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
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
        command = 'py.test -rf {}'.format(self._path)
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        lines = [line.strip() for line in process.stdout.readlines()]
        if lines:
            lines.append('')
            self._io_manager.display(lines)
        self._io_manager.proceed(prompt=prompt)

    def remove(
        self, 
        pending_user_input=None,
        prompt=True,
        ):
        r'''Removes asset.

        Backtracks up one level from previous location of asset.

        Returns none.
        '''
        self._io_manager._assign_user_input(pending_user_input)
        message = '{} will be removed.'
        message = message.format(self._path)
        if prompt:
            self._io_manager.display([message, ''])
            getter = self._io_manager.make_getter(where=self._where)
            getter.append_string("type 'remove' to proceed")
            result = getter._run()
        else:
            result = True
        if self._session._backtrack():
            return
        if not result == 'remove':
            return
        self._remove()
        self._session._is_backtracking_locally = True

    def rename(
        self, 
        pending_user_input=None,
        ):
        r'''Renames asset.

        Returns none.
        '''
        self._io_manager._assign_user_input(pending_user_input)
        getter = self._initialize_file_name_getter()
        result = getter._run()
        if self._session._backtrack():
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

    def status(self, prompt=True):
        r'''Displays repository status of assets.
    
        Returns none.
        '''
        line = self._get_score_package_directory_name()
        line = line + ' ...'
        self._io_manager.display(line, capitalize_first_character=False)
        command = self._repository_status_command
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            )
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
        self._io_manager.proceed(prompt=prompt)

    def update(self, prompt=True):
        r'''Updates versioned assets.

        Returns none.
        '''
        line = self._get_score_package_directory_name()
        line = line + ' ...'
        self._io_manager.display(line, capitalize_first_character=False)
        command = 'svn up {}'.format(self._path)
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            )
        lines = [line.strip() for line in process.stdout.readlines()]
        lines.append('')
        self._io_manager.display(lines)
        self._io_manager.proceed(prompt=prompt)
