# -*- encoding: utf-8 -*-
import os
import shutil
import subprocess
from abjad.tools import stringtools
from scoremanager.core.ScoreManagerObject import ScoreManagerObject


class Manager(ScoreManagerObject):
    r'''Filesystem asset manager.
    '''

    ### CLASS VARIABLES ###

    _generic_class_name = 'filesystem asset'

    boilerplate_directory_path = os.path.join(
        ScoreManagerObject.configuration.score_manager_directory_path,
        'boilerplate',
        )

    ### INITIALIZER ###

    def __init__(self, filesystem_path=None, session=None):
        assert filesystem_path is None or os.path.sep in filesystem_path
        self._filesystem_path = filesystem_path
        ScoreManagerObject.__init__(self, session=session)

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
        if self._filesystem_path:
            if self._is_in_svn_parent_directory():
                command = 'svn add {}'
            else:
                command = 'git add {}'
            command = command.format(self._filesystem_path)
            return command

    @property
    def _space_delimited_lowercase_name(self):
        if self._filesystem_path:
            return os.path.basename(self._filesystem_path)

    ### PRIVATE METHODS ###

    def _get_score_package_directory_name(self):
        line = self._filesystem_path
        line = line.replace(
            self.configuration.abjad_score_packages_directory_path,
            '',
            )
        line = line.replace(
            self.configuration.user_score_packages_directory_path,
            '',
            )
        line = line.lstrip(os.path.sep)
        return line

    def _initialize_file_name_getter(self):
        getter = self._session.io_manager.make_getter()
        getter.append_snake_case_file_name('new name')
        return getter

    def _is_in_svn_parent_directory(self):
        directory_path = os.path.dirname(self._filesystem_path)
        return '.svn' in os.listdir(directory_path)

    def _is_populated_directory(self, directory_path):
        if os.path.exists(directory_path):
            if os.listdir(directory_path):
                return True
        return False

    def _is_versioned(self):
        if self._filesystem_path is None:
            return False
        if not os.path.exists(self._filesystem_path):
            return False
        if self._is_in_svn_parent_directory():
            command = 'svn st {}'
        # if enclosing directory isn't svn then assume git.
        # then just return true.
        # because we don't know how to tell if git is managing a file or not
        else:
            return True
        command = command.format(self._filesystem_path)
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            )
        first_line = process.stdout.readline()
        if first_line.startswith(('?', 'svn: warning:')):
            return False
        else:
            return True

    def _remove(self):
        if self._is_in_svn_parent_directory():
            if self._is_versioned():
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
        else:
            command = 'git rm --force {}'
            command = command.format(self._filesystem_path)
            process = subprocess.Popen(
                command,
                shell=True,
                stderr=subprocess.PIPE,
                stdout=subprocess.PIPE,
                )
            process.stdout.readline()
            first_error_line = process.stderr.readline() or ''
            if first_error_line.startswith('fatal:'):
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
        if self._is_in_svn_parent_directory():
            if self._is_versioned():
                command = 'svn --force mv {} {}'
                command = command.format(self._filesystem_path, new_path)
                process = subprocess.Popen(
                    command,
                    shell=True,
                    stdout=subprocess.PIPE,
                    )
                process.stdout.readline()
            else:
                command = 'mv {} {}'
                command = command.format(self._filesystem_path, new_path)
                process = subprocess.Popen(
                    command,
                    shell=True,
                    stdout=subprocess.PIPE,
                    )
                process.stdout.readline()
        else:
            command = 'git mv --force {} {}'
            command = command.format(self._filesystem_path, new_path)
            process = subprocess.Popen(
                command,
                shell=True,
                stderr=subprocess.PIPE,
                stdout=subprocess.PIPE,
                )
            process.stdout.readline()
            first_error_line = process.stderr.readline() or ''
            if first_error_line.startswith('fatal:'):
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
        self._session._push_controller(self)
        self._session.io_manager._assign_user_input(pending_user_input)
        self._session._cache_breadcrumbs(cache=cache)
        while True:
            self._session._push_breadcrumb(self._breadcrumb)
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
                self.boilerplate_directory_path,
                boilerplate_file_abjad_asset_name,
                )
        if os.path.exists(boilerplate_file_abjad_asset_name):
            shutil.copyfile(
                boilerplate_file_abjad_asset_name,
                self._filesystem_path,
                )
            return True

    ### PUBLIC METHODS ###

    def interactively_copy(
        self, 
        pending_user_input=None,
        ):
        r'''Interactively copies filesystem asset.

        Returns none.
        '''
        self._session.io_manager._assign_user_input(pending_user_input)
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
        self._session.io_manager.display(message)
        if not self._session.io_manager.confirm():
            return
        shutil.copyfile(self._filesystem_path, new_path)
        self._session.io_manager.proceed('asset copied.')

    def remove(
        self, 
        pending_user_input=None,
        ):
        r'''Interactively removes filesystem asset.

        Returns none.
        '''
        self._session.io_manager._assign_user_input(pending_user_input)
        message = '{} will be removed.'
        message = message.format(self._filesystem_path)
        self._session.io_manager.display([message, ''])
        getter = self._session.io_manager.make_getter(where=self._where)
        getter.append_string("type 'remove' to proceed")
        result = getter._run()
        if self._session._backtrack():
            return
        if not result == 'remove':
            return
        if self._remove():
            message = '{} removed.'
            message = message.format(self._filesystem_path)
            self._session.io_manager.proceed(message)

    def remove_and_backtrack_locally(self):
        r'''Interactively removes filesystem asset and backtracks locally.

        Returns none.
        '''
        self.remove()
        self._session.is_backtracking_locally = True

    def interactively_rename(
        self, 
        pending_user_input=None,
        ):
        r'''Interactively renames filesystem asset.

        Returns none.
        '''
        self._session.io_manager._assign_user_input(pending_user_input)
        getter = self._initialize_file_name_getter()
        getter.include_newlines = False
        result = getter._run()
        if self._session._backtrack():
            return
        parent_directory_path = os.path.dirname(self._filesystem_path)
        new_path = os.path.join(parent_directory_path, result)
        message = 'new path name will be: {!r}.'
        message = message.format(new_path)
        self._session.io_manager.display([message, ''])
        if not self._session.io_manager.confirm():
            return
        if self._rename(new_path):
            self._session.io_manager.proceed('asset renamed.')

    def write_boilerplate(
        self, 
        pending_user_input=None,
        ):
        r'''Interactively writes filesystem asset boilerplate.

        Returns none.
        '''
        self._session.io_manager._assign_user_input(pending_user_input)
        getter = self._session.io_manager.make_getter(where=self._where)
        getter.append_snake_case_file_name('name of boilerplate asset')
        with self.backtracking:
            boilerplate_file_abjad_asset_name = getter._run()
        if self._session._backtrack():
            return
        if self._write_boilerplate(boilerplate_file_abjad_asset_name):
            self._session.io_manager.proceed('boilerplate asset copied.')
        else:
            message = 'boilerplate asset {!r} does not exist.'
            message = message.format(boilerplate_file_abjad_asset_name)
            self._session.io_manager.proceed(message)

    def add_assets_to_repository(self, prompt=False):
        r'''Interactively adds unversioned filesystem assets to repository.

        Returns none.
        '''
        line = self._get_score_package_directory_name()
        line = line + ' ...'
        self._session.io_manager.display(line, capitalize_first_character=False)
        process = subprocess.Popen(
            self._repository_add_command,
            shell=True,
            stdout=subprocess.PIPE,
            )
        lines = [line.strip() for line in process.stdout.readlines()]
        lines.append('')
        self._session.io_manager.display(lines)
        self._session.io_manager.proceed(prompt=prompt)

    def commit_assets_to_repository(self, commit_message=None, prompt=True):
        r'''Interactively commits unversioned filesystem assets to repository.

        Returns none.
        '''
        if commit_message is None:
            getter = self._session.io_manager.make_getter(where=self._where)
            getter.append_string('commit message')
            commit_message = getter._run(clear_terminal=False)
            if self._session._backtrack():
                return
            line = 'commit message will be: "{}"\n'.format(commit_message)
            self._session.io_manager.display(line)
            if not self._session.io_manager.confirm():
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
        self._session.io_manager.display(
            lines, 
            capitalize_first_character=False,
            )
        self._session.io_manager.proceed(prompt=prompt)

    def display_repository_status(self, prompt=True):
        r'''Intearctively displays repository status of filesystem assets.
    
        Returns none.
        '''
        line = self._get_score_package_directory_name()
        line = line + ' ...'
        self._session.io_manager.display(line, capitalize_first_character=False)
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
        self._session.io_manager.display(
            clean_lines, 
            capitalize_first_character=False,
            )
        self._session.io_manager.proceed(prompt=prompt)

    def update_from_repository(self, prompt=True):
        r'''Interactively updates versioned filesystem assets.

        Returns none.
        '''
        line = self._get_score_package_directory_name()
        line = line + ' ...'
        self._session.io_manager.display(line, capitalize_first_character=False)
        command = 'svn up {}'.format(self._filesystem_path)
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            )
        lines = [line.strip() for line in process.stdout.readlines()]
        lines.append('')
        self._session.io_manager.display(lines)
        self._session.io_manager.proceed(prompt=prompt)

    ### UI MANIFEST ###

    _user_input_to_action = {
        'cp': interactively_copy,
        'rm': remove_and_backtrack_locally,
        'ren': interactively_rename,
        }
