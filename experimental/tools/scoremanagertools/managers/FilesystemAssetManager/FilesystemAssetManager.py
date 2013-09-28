# -*- encoding: utf-8 -*-
import abc
import os
import shutil
import subprocess
from abjad.tools import stringtools
from experimental.tools.scoremanagertools.scoremanager.ScoreManagerObject \
    import ScoreManagerObject


class FilesystemAssetManager(ScoreManagerObject):
    r'''Filesystem asset manager.
    '''

    ### CLASS VARIABLES ###

    __metaclass__ = abc.ABCMeta

    _generic_class_name = 'filesystem asset'

    boilerplate_directory_path = os.path.join(
        ScoreManagerObject.configuration.score_manager_tools_directory_path,
        'boilerplate',
        )

    ### INITIALIZER ###

    def __init__(self, filesystem_path=None, session=None):
        assert filesystem_path is None or os.path.sep in filesystem_path
        self._filesystem_path = filesystem_path
        ScoreManagerObject.__init__(self, session=session)

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        r'''True when filesystem path properties are equal.
        Otherwise false.

        Return boolean.
        '''
        if isinstance(expr, type(self)):
            if self.filesystem_path == expr.filesystem_path:
                return True
        return False

    def __repr__(self):
        r'''Interpreter representation of filesystem assset manager.

        Return string.
        '''
        return '{}({!r})'.format(self._class_name, self.filesystem_path)

    ### PRIVATE PROPERTIES ###

    @property
    def _breadcrumb(self):
        if self.filesystem_path:
            return os.path.basename(self.filesystem_path)
        return self._space_delimited_lowercase_class_name

    @property
    def _plural_generic_class_name(self):
        return stringtools.pluralize_string(self._generic_class_name)

    @property
    def _space_delimited_lowercase_name(self):
        if self.filesystem_path:
            return os.path.basename(self.filesystem_path)

    @property
    def _repository_add_command(self):
        if self.filesystem_path:
            return 'svn add {}'.format(self.filesystem_path)

    ### PRIVATE METHODS ###

    def _initialize_file_name_getter(self):
        getter = self.session.io_manager.make_getter()
        getter.append_snake_case_file_name('new name')
        return getter

    def _get_score_package_directory_name(self):
        line = self.filesystem_path
        line = line.replace(
            self.configuration.built_in_score_packages_directory_path,
            '',
            )
        line = line.replace(
            self.configuration.user_score_packages_directory_path,
            '',
            )
        line = line.lstrip(os.path.sep)
        return line

    def _run(self, cache=False, clear=True, pending_user_input=None):
        self.session.io_manager.assign_user_input(pending_user_input)
        self.session.cache_breadcrumbs(cache=cache)
        while True:
            self.session.push_breadcrumb(self._breadcrumb)
            menu = self._make_main_menu()
            result = menu._run(clear=clear)
            if self.session.backtrack(source=self._backtracking_source):
                break
            elif not result:
                self.session.pop_breadcrumb()
                continue
            self._handle_main_menu_result(result)
            if self.session.backtrack(source=self._backtracking_source):
                break
            self.session.pop_breadcrumb()
        self.session.pop_breadcrumb()
        self.session.restore_breadcrumbs(cache=cache)

    def _space_delimited_lowercase_name_to_asset_name(
        self, space_delimited_lowercase_name):
        space_delimited_lowercase_name = space_delimited_lowercase_name.lower()
        asset_name = space_delimited_lowercase_name.replace(' ', '_')
        return asset_name

    ### PUBLIC PROPERTIES ###

    @property
    def filesystem_path(self):
        r'''Filesystem path of filesystem asset manager.

        Returns string.
        '''
        return self._filesystem_path

    ### PUBLIC METHODS ###

    def interactively_copy(
        self, 
        pending_user_input=None,
        ):
        r'''Interactively copies filesystem asset.

        Returns none.
        '''
        self.session.io_manager.assign_user_input(pending_user_input)
        getter = self._initialize_file_name_getter()
        result = getter._run()
        if self.session.backtrack():
            return
        new_asset_name = \
            self._space_delimited_lowercase_name_to_asset_name(result)
        parent_directory_path = os.path.dirname(self.filesystem_path)
        new_path = os.path.join(parent_directory_path, new_asset_name)
        message = 'new path will be {}'.format(new_path)
        self.session.io_manager.display(message)
        if not self.session.io_manager.confirm():
            return
        shutil.copyfile(self.filesystem_path, new_path)
        self.session.io_manager.proceed('asset copied.')

    def interactively_remove(
        self, 
        pending_user_input=None,
        ):
        r'''Interactively removes filesystem asset.

        Returns none.
        '''
        self.session.io_manager.assign_user_input(pending_user_input)
        message = '{} will be removed.'.format(self.filesystem_path)
        self.session.io_manager.display([message, ''])
        getter = self.session.io_manager.make_getter(where=self._where)
        getter.append_string("type 'remove' to proceed")
        result = getter._run()
        if self.session.backtrack():
            return
        if not result == 'remove':
            return
        if self.remove():
            message = '{} removed.'.format(self.filesystem_path)
            self.session.io_manager.proceed(message)

    def interactively_remove_and_backtrack_locally(self):
        r'''Interactively removes filesystem asset and backtracks locally.

        Returns none.
        '''
        self.interactively_remove()
        self.session.is_backtracking_locally = True

    def interactively_rename(
        self, 
        pending_user_input=None,
        ):
        r'''Interactively renames filesystem asset.

        Returns none.
        '''
        self.session.io_manager.assign_user_input(pending_user_input)
        getter = self._initialize_file_name_getter()
        getter.include_newlines = False
        result = getter._run()
        if self.session.backtrack():
            return
        parent_directory_path = os.path.dirname(self.filesystem_path)
        new_path = os.path.join(parent_directory_path, result)
        message = 'new path name will be: "{}"'.format(new_path)
        self.session.io_manager.display([message, ''])
        if not self.session.io_manager.confirm():
            return
        if self.rename(new_path):
            self.session.io_manager.proceed('asset renamed.')

    def interactively_write_boilerplate(
        self, 
        pending_user_input=None,
        ):
        r'''Interactively writes filesystem asset boilerplate.

        Returns none.
        '''
        self.session.io_manager.assign_user_input(pending_user_input)
        getter = self.session.io_manager.make_getter(where=self._where)
        getter.append_snake_case_file_name('name of boilerplate asset')
        with self.backtracking:
            boilerplate_file_built_in_asset_name = getter._run()
        if self.session.backtrack():
            return
        if self.write_boilerplate(boilerplate_file_built_in_asset_name):
            self.session.io_manager.proceed('boilerplate asset copied.')
        else:
            message = 'boilerplate asset {!r} does not exist.'
            message = message.format(boilerplate_file_built_in_asset_name)
            self.session.io_manager.proceed(message)

    def is_versioned(self):
        r'''True when filesystem asset is versioned.
        Otherwise false.

        Returns boolean.
        '''
        if self.filesystem_path is None:
            return False
        if not os.path.exists(self.filesystem_path):
            return False
        command = 'svn st {}'.format(self.filesystem_path)
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

    @abc.abstractmethod
    def make_empty_asset(self, is_interactive=False):
        r'''Makes empty filesystem asset.

        Returns none.
        '''
        pass

    def remove(self):
        r'''Removes filesystem asset.

        Returns none.
        '''
        if self.is_versioned():
            command = 'svn --force rm {}'.format(self.filesystem_path)
            process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                )
            process.stdout.readline()
            return True
        else:
            command = 'rm -rf {}'.format(self.filesystem_path)
            process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                )
            process.stdout.readline()
            return True

    def rename(self, new_path):
        r'''Renames filesystem asset.

        Returns none.
        '''
        if self.is_versioned():
            command = 'svn --force mv {} {}'.format(
                self.filesystem_path, new_path)
            process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                )
            process.stdout.readline()
            self._filesystem_path = new_path
        else:
            command = 'mv {} {}'.format(
                self.filesystem_path, new_path)
            process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                )
            process.stdout.readline()
            self._filesystem_path = new_path

    def repository_add(self, is_interactive=False):
        r'''Adds unversioned filesystem assets to repository.

        Returns none.
        '''
        line = self._get_score_package_directory_name()
        line = line + ' ...'
        self.session.io_manager.display(line, capitalize_first_character=False)
        process = subprocess.Popen(
            self._repository_add_command,
            shell=True,
            stdout=subprocess.PIPE,
            )
        lines = [line.strip() for line in process.stdout.readlines()]
        lines.append('')
        self.session.io_manager.display(lines)
        self.session.io_manager.proceed(is_interactive=is_interactive)

    def repository_ci(self, commit_message=None, is_interactive=True):
        r'''Commits unversioned filesystem assets to repository.

        Returns none.
        '''
        if commit_message is None:
            getter = self.session.io_manager.make_getter(where=self._where)
            getter.append_string('commit message')
            commit_message = getter._run(clear_terminal=False)
            if self.session.backtrack():
                return
            line = 'commit message will be: "{}"\n'.format(commit_message)
            self.session.io_manager.display(line)
            if not self.session.io_manager.confirm():
                return
        lines = []
        line = self._get_score_package_directory_name()
        line = line + ' ...'
        lines.append(line)
        command = 'svn commit -m "{}" {}'
        command = command.format(commit_message, self.filesystem_path)
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            )
        lines.extend([line.strip() for line in process.stdout.readlines()])
        lines.append('')
        self.session.io_manager.display(
            lines, 
            capitalize_first_character=False,
            )
        self.session.io_manager.proceed(is_interactive=is_interactive)

    def repository_st(self, is_interactive=True):
        r'''Displays repository status of filesystem assets.
    
        Returns none.
        '''
        line = self._get_score_package_directory_name()
        line = line + ' ...'
        self.session.io_manager.display(line, capitalize_first_character=False)
        command = 'svn st -u {}'.format(self.filesystem_path)
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            )
        path = self.filesystem_path
        path = path + os.path.sep
        clean_lines = []
        for line in process.stdout.readlines():
            clean_line = line.strip()
            clean_line = clean_line.replace(path, '')
            clean_lines.append(clean_line)
        clean_lines.append('')
        self.session.io_manager.display(clean_lines)
        self.session.io_manager.proceed(is_interactive=is_interactive)

    def repository_up(self, is_interactive=True):
        r'''Updates versioned filesystem assets.

        Returns none.
        '''
        line = self._get_score_package_directory_name()
        line = line + ' ...'
        self.session.io_manager.display(line, capitalize_first_character=False)
        command = 'svn up {}'.format(self.filesystem_path)
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            )
        lines = [line.strip() for line in process.stdout.readlines()]
        lines.append('')
        self.session.io_manager.display(lines)
        self.session.io_manager.proceed(is_interactive=is_interactive)

    def write_boilerplate(self, boilerplate_file_built_in_asset_name):
        r'''Writes filesystem asset boilerplate.

        Returns none.
        '''
        if not os.path.exists(boilerplate_file_built_in_asset_name):
            boilerplate_file_built_in_asset_name = os.path.join(
                self.boilerplate_directory_path,
                boilerplate_file_built_in_asset_name,
                )
        if os.path.exists(boilerplate_file_built_in_asset_name):
            shutil.copyfile(
                boilerplate_file_built_in_asset_name,
                self.filesystem_path,
                )
            return True

    ### UI MANIFEST ###

    user_input_to_action = {
        'cp': interactively_copy,
        'rm': interactively_remove_and_backtrack_locally,
        'ren': interactively_rename,
        }
