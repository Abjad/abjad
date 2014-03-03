# -*- encoding: utf-8 -*-
import os
import shutil
import subprocess
from abjad.tools import stringtools
from scoremanager.core.ScoreManagerObject import ScoreManagerObject


class Manager(ScoreManagerObject):
    r'''Filesystem asset manager.
    '''

    ### INITIALIZER ###

    def __init__(self, filesystem_path=None, session=None):
        ScoreManagerObject.__init__(self, session=session)
        assert filesystem_path is None or os.path.sep in filesystem_path
        self._filesystem_path = filesystem_path
        self._generic_class_name = 'filesystem asset'

    ### SPECIAL METHODS ###

    def __repr__(self):
        r'''Gets interpreter representation of filesystem assset manager.

        Returns string.
        '''
        return '{}({!r})'.format(type(self).__name__, self._filesystem_path)

    ### PRIVATE PROPERTIES ###

    @property
    def _breadcrumb(self):
        if self._filesystem_path:
            return os.path.basename(self._filesystem_path)
        return self._space_delimited_lowercase_class_name

    @property
    def _plural_generic_class_name(self):
        return stringtools.pluralize_string(self._generic_class_name)

    @property
    def _repository_add_command(self):
        if not self._filesystem_path:
            return
        parent_directory_path = os.path.dirname(self._filesystem_path)
        if self._is_git_versioned(filesystem_path=parent_directory_path):
            return 'git add {}'.format(self._filesystem_path)
        elif self._is_svn_versioned(filesystem_path=parent_diretory_path):
            return 'svn add {}'.format(self._filesystem_path)

    @property
    def _space_delimited_lowercase_name(self):
        if self._filesystem_path:
            return os.path.basename(self._filesystem_path)

    @property
    def _user_input_to_action(self):
        _user_input_to_action = {
            'cp': self.copy,
            'rm': self.remove_and_backtrack_locally,
            'ren': self.rename,
            }
        return _user_input_to_action

    ### PRIVATE METHODS ###

    def _get_score_package_directory_name(self):
        line = self._filesystem_path
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
        getter.append_snake_case_file_name('new name')
        return getter

    def _is_populated_directory(self, directory_path):
        if os.path.exists(directory_path):
            if os.listdir(directory_path):
                return True
        return False

    def _is_git_added(self, filesystem_path=None):
        filesystem_path = filesystem_path or self._filesystem_path
        if filesystem_path is None:
            return False
        if not os.path.exists(filesystem_path):
            return False
        command = 'git st --short {}'
        command = command.format(filesystem_path)
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            )
        first_line = process.stdout.readline()
        if first_line.startswith('A'):
            return True
        return False

    def _is_git_versioned(self, filesystem_path=None):
        filesystem_path = filesystem_path or self._filesystem_path
        if filesystem_path is None:
            return False
        if not os.path.exists(filesystem_path):
            return False
        command = 'git st --short {}'
        command = command.format(filesystem_path)
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            )
        first_line = process.stdout.readline()
        if first_line.startswith(('fatal:', '??', 'A')):
            return False
        return True

    def _is_svn_versioned(self, filesystem_path=None):
        filesystem_path = filesystem_path or self._filesystem_path
        if filesystem_path is None:
            return False
        if not os.path.exists(filesystem_path):
            return False
        command = 'svn st -u {}'
        command = command.format(filesystem_path)
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            )
        first_line = process.stdout.readline()
        if first_line.startswith(('?', 'svn: warning:')):
            return False
        return True

    def _remove(self):
        if self._is_git_versioned():
            command = 'git rm --force {}'
        elif self._is_git_added():
            command = 'git rm --force {}'
        elif self._is_svn_versioned():
            command = 'svn --force rm {}'
        else:
            command = 'rm -rf {}'
        command = command.format(self._filesystem_path)
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            )
        process.stdout.readline()
        return True

    def _rename(self, new_path):
        if self._is_git_versioned():
            command = 'git mv --force {} {}'
        elif self._is_git_added():
            command = 'git mv --force {} {}'
        elif self._is_svn_versioned():
            command = 'svn --force mv {} {}'
        else:
            command = 'mv {} {}'
        command = command.format(self._filesystem_path, new_path)
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            )
        process.stdout.readline()
        self._filesystem_path = new_path

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
            self._session._last_material_package_path = self._package_path
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

    def _write_boilerplate(self, boilerplate_file_abjad_asset_name):
        if not os.path.exists(boilerplate_file_abjad_asset_name):
            boilerplate_file_abjad_asset_name = os.path.join(
                self._configuration.boilerplate_directory_path,
                boilerplate_file_abjad_asset_name,
                )
        if os.path.exists(boilerplate_file_abjad_asset_name):
            shutil.copyfile(
                boilerplate_file_abjad_asset_name,
                self._filesystem_path,
                )
            return True

    ### PUBLIC METHODS ###

    def add_assets_to_repository(self, prompt=False):
        r'''Adds unversioned filesystem assets to repository.

        Returns none.
        '''
        line = self._get_score_package_directory_name()
        line = line + ' ...'
        self._io_manager.display(line, capitalize_first_character=False)
        process = subprocess.Popen(
            self._repository_add_command,
            shell=True,
            stdout=subprocess.PIPE,
            )
        lines = [line.strip() for line in process.stdout.readlines()]
        lines.append('')
        self._io_manager.display(lines)
        self._io_manager.proceed(prompt=prompt)

    def commit_assets_to_repository(self, commit_message=None, prompt=True):
        r'''Commits unversioned filesystem assets to repository.

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
        command = command.format(commit_message, self._filesystem_path)
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
        r'''Copies filesystem asset.

        Returns none.
        '''
        self._io_manager._assign_user_input(pending_user_input)
        getter = self._initialize_file_name_getter()
        result = getter._run()
        if self._session._backtrack():
            return
        new_asset_name = \
            self._space_delimited_lowercase_name_to_asset_name(result)
        parent_directory_path = os.path.dirname(self._filesystem_path)
        new_path = os.path.join(parent_directory_path, new_asset_name)
        message = 'new path will be {}'
        message = message.format(new_path)
        self._io_manager.display(message)
        if not self._io_manager.confirm():
            return
        shutil.copyfile(self._filesystem_path, new_path)
        self._io_manager.proceed('asset copied.')

    def display_repository_status(self, prompt=True):
        r'''Intearctively displays repository status of filesystem assets.
    
        Returns none.
        '''
        line = self._get_score_package_directory_name()
        line = line + ' ...'
        self._io_manager.display(line, capitalize_first_character=False)
        command = 'svn st -u {}'.format(self._filesystem_path)
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            )
        path = self._filesystem_path
        path = path + os.path.sep
        clean_lines = []
        for line in process.stdout.readlines():
            clean_line = line.strip()
            clean_line = clean_line.replace(path, '')
            clean_lines.append(clean_line)
        clean_lines.append('')
        if clean_lines and 'svn: warning' in clean_lines[0]:
            command = 'git st {}'.format(self._filesystem_path)
            process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                )
            path = self._filesystem_path
            path = path + os.path.sep
            clean_lines = []
            for line in process.stdout.readlines():
                clean_line = line.strip()
                clean_line = clean_line.replace(path, '')
                clean_lines.append(clean_line)
            clean_lines.append('')
        if clean_lines and 'fatal:' in clean_lines[0]:
            clean_lines = []
            message = 'versioned by neither Subversion nor Git'
            clean_lines.append(message)
            clean_lines.append('')
        self._io_manager.display(
            clean_lines, 
            capitalize_first_character=False,
            )
        self._io_manager.proceed(prompt=prompt)

    def remove(
        self, 
        pending_user_input=None,
        prompt=True,
        ):
        r'''Removes filesystem asset.

        Returns none.
        '''
        self._io_manager._assign_user_input(pending_user_input)
        message = '{} will be removed.'
        message = message.format(self._filesystem_path)
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

    def remove_and_backtrack_locally(self):
        r'''Removes filesystem asset and backtracks locally.

        Returns none.
        '''
        self.remove()
        self._session._is_backtracking_locally = True

    def rename(
        self, 
        pending_user_input=None,
        ):
        r'''Renames filesystem asset.

        Returns none.
        '''
        self._io_manager._assign_user_input(pending_user_input)
        getter = self._initialize_file_name_getter()
        getter.include_newlines = False
        result = getter._run()
        if self._session._backtrack():
            return
        parent_directory_path = os.path.dirname(self._filesystem_path)
        new_path = os.path.join(parent_directory_path, result)
        message = 'new path name will be: {!r}.'
        message = message.format(new_path)
        self._io_manager.display([message, ''])
        if not self._io_manager.confirm():
            return
        if self._rename(new_path):
            self._io_manager.proceed('asset renamed.')

    def update_from_repository(self, prompt=True):
        r'''Updates versioned filesystem assets.

        Returns none.
        '''
        line = self._get_score_package_directory_name()
        line = line + ' ...'
        self._io_manager.display(line, capitalize_first_character=False)
        command = 'svn up {}'.format(self._filesystem_path)
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            )
        lines = [line.strip() for line in process.stdout.readlines()]
        lines.append('')
        self._io_manager.display(lines)
        self._io_manager.proceed(prompt=prompt)

    def write_boilerplate(
        self, 
        pending_user_input=None,
        prompt=True,
        ):
        r'''Writes filesystem asset boilerplate.

        Returns none.
        '''
        self._io_manager._assign_user_input(pending_user_input)
        getter = self._io_manager.make_getter(where=self._where)
        getter.append_snake_case_file_name('name of boilerplate asset')
        with self._backtracking:
            boilerplate_file_abjad_asset_name = getter._run()
        if self._session._backtrack():
            return
        if self._write_boilerplate(boilerplate_file_abjad_asset_name):
            self._io_manager.proceed('boilerplate asset copied.')
        else:
            message = 'boilerplate asset {!r} does not exist.'
            message = message.format(boilerplate_file_abjad_asset_name)
            self._io_manager.proceed(message)
