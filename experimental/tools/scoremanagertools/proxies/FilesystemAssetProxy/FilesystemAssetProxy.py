import abc
import os
import shutil
import subprocess
from abjad.tools import stringtools
from experimental.tools.scoremanagertools.core.ScoreManagerObject import ScoreManagerObject


class FilesystemAssetProxy(ScoreManagerObject):
    '''Asset proxy.
    '''

    ### CLASS VARIABLES ###

    __metaclass__ = abc.ABCMeta
    _generic_class_name = 'filesystem asset'
    boilerplate_directory_path = os.path.join(
        ScoreManagerObject.configuration.score_manager_tools_directory_path, 'boilerplate')

    ### INITIALIZER ###

    def __init__(self, filesystem_path=None, session=None):
        assert filesystem_path is None or os.path.sep in filesystem_path
        self._filesystem_path = filesystem_path
        ScoreManagerObject.__init__(self, session=session)

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        '''True when filesystem path properties are equal.
        Otherwise false.

        Return boolean.
        '''
        if isinstance(expr, type(self)):
            if self.filesystem_path == expr.filesystem_path:
                return True
        return False

    def __repr__(self):
        '''Filesystem asset proxy repr.
    
        Return string.
        '''
        return '{}({!r})'.format(self._class_name, self.filesystem_path)

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _breadcrumb(self):
        return self.filesystem_basename or self._space_delimited_lowercase_class_name

    @property
    def _plural_generic_class_name(self):
        return stringtools.pluralize_string(self._generic_class_name)

    @property
    def _space_delimited_lowercase_name(self):
        return self.filesystem_basename

    @property
    def _svn_add_command(self):
        if self.filesystem_path:
            return 'svn add {}'.format(self.filesystem_path)

    ### PRIVATE METHODS ###

    def _initialize_file_name_getter(self):
        getter = self._io.make_getter()
        getter.append_underscore_delimited_lowercase_file_name('new name')
        return getter

    @staticmethod
    def _safe_import(target_namespace, source_module_name, source_attribute_name,
        source_parent_package_path=None):

        #print repr(target_namespace.keys())
        #print repr(source_module_name)
        #print repr(source_attribute_name)
        #print repr(source_parent_package_path)

        if source_parent_package_path is None:
            try:
                source_parent_package_path = target_namespace['__name__']
            except KeyError:
                pass

        if source_parent_package_path:
            source_module_path = '{}.{}'.format(
                source_parent_package_path, source_module_name)
        else:
            source_module_path = source_module_name

        try:
            source_module = __import__(source_module_path, fromlist=['*'])
        except:
            message = 'Error importing {!r}.'.format(source_module_path)
            print message
            return

        try:
            source_attribute_value = source_module.__dict__[source_attribute_name]
        except:
            message = 'Can not import {!r} from {!r}.'.format(source_attribute_name, source_module_path)
            print message
            return

        target_namespace[source_attribute_name] = source_attribute_value
        return source_attribute_value

    def _space_delimited_lowercase_name_to_asset_name(self, space_delimited_lowercase_name):
        space_delimited_lowercase_name = space_delimited_lowercase_name.lower()
        asset_name = space_delimited_lowercase_name.replace(' ', '_')
        return asset_name

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def filesystem_basename(self):
        if self.filesystem_path:
            return os.path.basename(self.filesystem_path)

    @property
    def filesystem_directory_name(self):
        if self.filesystem_path:
            return os.path.dirname(self.filesystem_path)

    @property
    def filesystem_path(self):
        return self._filesystem_path

    ### PUBLIC METHODS ###

    def copy(self, new_filesystem_path):
        shutil.copyfile(self.filesystem_path, new_filesystem_path)

    def copy_interactively(self, user_input=None):
        self._io.assign_user_input(user_input=user_input)
        getter = self._initialize_file_name_getter()
        result = getter._run()
        if self._session.backtrack():
            return
        new_asset_name = self._space_delimited_lowercase_name_to_asset_name(result)
        new_path = os.path.join(self.filesystem_directory_name, new_asset_name)
        self._io.display('new path will be {}'.format(new_path))
        if not self._io.confirm():
            return
        self.copy(new_path)
        self._io.proceed('asset copied.')

    def exists(self):
        if self.filesystem_path:
            return os.path.exists(self.filesystem_path)
        return False

    def is_versioned(self):
        if self.filesystem_path is None:
            return False
        if not os.path.exists(self.filesystem_path):
            return False
        command = 'svn st {}'.format(self.filesystem_path)
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        first_line = proc.stdout.readline()
        if first_line.startswith(('?', 'svn: warning:')):
            return False
        else:
            return True

    @abc.abstractmethod
    def make_empty_asset(self, is_interactive=False):
        pass

    def remove(self):
        if self.is_versioned():
            command = 'svn --force rm {}'.format(self.filesystem_path)
            proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
            proc.stdout.readline()
            return True
        else:
            command = 'rm -rf {}'.format(self.filesystem_path)
            proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            proc.stdout.readline()
            return True

    def remove_interactively(self, user_input=None):
        self._io.assign_user_input(user_input=user_input)
        self._io.display(['{} will be removed.'.format(self.filesystem_path), ''])
        getter = self._io.make_getter(where=self._where)
        getter.append_string("type 'remove' to proceed")
        result = getter._run()
        if self._session.backtrack():
            return
        if not result == 'remove':
            return
        if self.remove():
            self._io.proceed('{} removed.'.format(self.filesystem_path))

    def remove_interactively_and_backtrack_locally(self):
        self.remove_interactively()
        self._session.is_backtracking_locally = True

    def rename(self, new_path):
        if self.is_versioned():
            command = 'svn --force mv {} {}'.format(self.filesystem_path, new_path)
            proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
            proc.stdout.readline()
            self._filesystem_path = new_path
        else:
            command = 'mv {} {}'.format(self.filesystem_path, new_path)
            proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
            proc.stdout.readline()
            self._filesystem_path = new_path

    def rename_interactively(self, user_input=None):
        self._io.assign_user_input(user_input=user_input)
        getter = self._initialize_file_name_getter()
        getter.include_newlines = False
        result = getter._run()
        if self._session.backtrack():
            return
        new_path = os.path.join(self.filesystem_directory_name, result)
        self._io.display(['new path name will be: "{}"'.format(new_path), ''])
        if not self._io.confirm():
            return
        if self.rename(new_path):
            self._io.proceed('asset renamed.')

    def svn_add(self, is_interactive=False):
        if is_interactive:
            self._io.display(self.filesystem_path)
        proc = subprocess.Popen(self._svn_add_command, shell=True, stdout=subprocess.PIPE)
        lines = [line.strip() for line in proc.stdout.readlines()]
        lines.append('')
        if is_interactive:
            self._io.display(lines)
        self._io.proceed(is_interactive=is_interactive)

    def svn_ci(self, commit_message=None, is_interactive=True):
        if commit_message is None:
            getter = self._io.make_getter(where=self._where)
            getter.append_string('commit message')
            commit_message = getter._run()
            if self._session.backtrack():
                return
            line = 'commit message will be: "{}"\n'.format(commit_message)
            self._io.display(line)
            if not self._io.confirm():
                return
        lines = []
        lines.append(self.filesystem_path)
        command = 'svn commit -m "{}" {}'.format(commit_message, self.filesystem_path)
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        lines.extend([line.strip() for line in proc.stdout.readlines()])
        lines.append('')
        self._io.display(lines)
        self._io.proceed(is_interactive=is_interactive)

    def svn_st(self, is_interactive=True):
        if is_interactive:
            self._io.display(self.filesystem_path)
        command = 'svn st -u {}'.format(self.filesystem_path)
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        lines = [line.strip() for line in proc.stdout.readlines()]
        lines.append('')
        self._io.display(lines)
        self._io.proceed(is_interactive=is_interactive)

    def svn_up(self, is_interactive=True):
        if is_interactive:
            self._io.display(self.filesystem_path)
        command = 'svn up {}'.format(self.filesystem_path)
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        lines = [line.strip() for line in proc.stdout.readlines()]
        lines.append('')
        self._io.display(lines)
        self._io.proceed(is_interactive=is_interactive)

    def write_boilerplate(self, boilerplate_filebuilt_in_asset_name):
        if not os.path.exists(boilerplate_filebuilt_in_asset_name):
            boilerplate_filebuilt_in_asset_name = os.path.join(
                self.boilerplate_directory_path, boilerplate_filebuilt_in_asset_name)
        if os.path.exists(boilerplate_filebuilt_in_asset_name):
            shutil.copyfile(boilerplate_filebuilt_in_asset_name, self.filesystem_path)
            return True

    def write_boilerplate_interactively(self, user_input=None):
        self._io.assign_user_input(user_input=user_input)
        getter = self._io.make_getter(where=self._where)
        getter.append_underscore_delimited_lowercase_file_name('name of boilerplate asset')
        self._session.push_backtrack()
        boilerplate_filebuilt_in_asset_name = getter._run()
        self._session.pop_backtrack()
        if self._session.backtrack():
            return
        if self.write_boilerplate(boilerplate_filebuilt_in_asset_name):
            self._io.proceed('boilerplate asset copied.')
        else:
            self._io.proceed('boilerplate asset {!r} does not exist.'.format(
                boilerplate_filebuilt_in_asset_name))

    ### UI MANIFEST ###

    user_input_to_action = {
        'cp': copy_interactively,
        'rm': remove_interactively_and_backtrack_locally,
        'ren': rename_interactively,
        }
