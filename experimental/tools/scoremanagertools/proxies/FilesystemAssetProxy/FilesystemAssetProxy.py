import abc
import os
import shutil
import subprocess
from abjad.tools import stringtools
from experimental.tools.scoremanagertools.core.ScoreManagerObject import ScoreManagerObject


class FilesystemAssetProxy(ScoreManagerObject):
    '''Asset proxy.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta
    _generic_class_name = 'filesystem asset'

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

    def _space_delimited_lowercase_name_to_asset_name(self, space_delimited_lowercase_name):
        space_delimited_lowercase_name = space_delimited_lowercase_name.lower()
        asset_name = space_delimited_lowercase_name.replace(' ', '_')
        return asset_name

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def breadcrumb(self):
        return self.filesystem_basename or self._space_delimited_lowercase_class_name

    @property
    def exists(self):
        if self.filesystem_path:
            return os.path.exists(self.filesystem_path)
        return False

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

    @property
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

    ### PUBLIC METHODS ###

    def copy(self, new_filesystem_path):
        shutil.copyfile(self.filesystem_path, new_filesystem_path)

    def copy_interactively(self, user_input=None):
        self.io.assign_user_input(user_input=user_input)
        getter = self.io.make_getter()
        getter.append_underscore_delimited_lowercase_file_name('new name')
        result = getter.run()
        if self.session.backtrack():
            return
        new_asset_name = self._space_delimited_lowercase_name_to_asset_name(result)
        new_path = os.path.join(self.filesystem_directory_name, new_asset_name)
        self.io.display('new path will be {}'.format(new_path))
        if not self.io.confirm():
            return
        self.copy(new_path)
        self.io.proceed('asset copied.')

    @abc.abstractmethod
    def fix(self):
        pass

    @abc.abstractmethod
    def make_empty_asset(self, is_interactive=False):
        pass

    @abc.abstractmethod
    def profile(self):
        pass

    def remove(self):
        if self.is_versioned:
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
        self.io.assign_user_input(user_input=user_input)
        self.io.display(['{} will be removed.'.format(self.filesystem_path), ''])
        getter = self.io.make_getter(where=self.where())
        getter.append_string("type 'remove' to proceed")
        result = getter.run()
        if self.session.backtrack():
            return
        if not result == 'remove':
            return
        if self.remove():
            self.io.proceed('{} removed.'.format(self.filesystem_path))

    def rename(self, new_path):
        if self.is_versioned:
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
        self.io.assign_user_input(user_input=user_input)
        getter = self.io.make_getter(where=self.where())
        getter.append_underscore_delimited_lowercase_file_name('new name')
        getter.include_newlines = False
        result = getter.run()
        if self.session.backtrack():
            return
        new_path = os.path.join(self.filesystem_directory_name, result)
        self.io.display(['new path name will be: "{}"'.format(new_path), ''])
        if not self.io.confirm():
            return
        if self.rename(new_path):
            self.io.proceed('asset renamed.')

    def svn_add(self, is_interactive=False):
        if is_interactive:
            self.io.display(self.filesystem_path)
        proc = subprocess.Popen(self._svn_add_command, shell=True, stdout=subprocess.PIPE)
        lines = [line.strip() for line in proc.stdout.readlines()]
        lines.append('')
        if is_interactive:
            self.io.display(lines)
        self.io.proceed(is_interactive=is_interactive)

    def svn_ci(self, commit_message=None, is_interactive=True):
        if commit_message is None:
            getter = self.io.make_getter(where=self.where())
            getter.append_string('commit message')
            commit_message = getter.run()
            if self.session.backtrack():
                return
            line = 'commit message will be: "{}"\n'.format(commit_message)
            self.io.display(line)
            if not self.io.confirm():
                return
        lines = []
        lines.append(self.filesystem_path)
        command = 'svn commit -m "{}" {}'.format(commit_message, self.filesystem_path)
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        lines.extend([line.strip() for line in proc.stdout.readlines()])
        lines.append('')
        self.io.display(lines)
        self.io.proceed(is_interactive=is_interactive)

    def svn_st(self, is_interactive=True):
        if is_interactive:
            self.io.display(self.filesystem_path)
        command = 'svn st -u {}'.format(self.filesystem_path)
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        lines = [line.strip() for line in proc.stdout.readlines()]
        lines.append('')
        self.io.display(lines)
        self.io.proceed(is_interactive=is_interactive)

    def svn_up(self, is_interactive=True):
        if is_interactive:
            self.io.display(self.filesystem_path)
        command = 'svn up {}'.format(self.filesystem_path)
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        lines = [line.strip() for line in proc.stdout.readlines()]
        lines.append('')
        self.io.display(lines)
        self.io.proceed(is_interactive=is_interactive)

    def touch(self):
        os.system('touch {}'.format(self.filesystem_path))

    def write_boilerplate_asset_to_disk(self, boilerplate_asset_name):
        if not os.path.exists(boilerplate_asset_name):
            boilerplate_asset_name = os.path.join(
                self.configuration.boilerplate_directory_path, boilerplate_asset_name)
        if os.path.exists(boilerplate_asset_name):
            shutil.copyfile(boilerplate_asset_name, self.filesystem_path)
            return True

    def write_boilerplate_asset_to_disk_interactively(self, user_input=None):
        self.io.assign_user_input(user_input=user_input)
        getter = self.io.make_getter(where=self.where())
        getter.append_underscore_delimited_lowercase_file_name('name of boilerplate asset')
        self.session.push_backtrack()
        boilerplate_asset_name = getter.run()
        self.session.pop_backtrack()
        if self.session.backtrack():
            return
        if self.write_boilerplate_asset_to_disk(boilerplate_asset_name):
            self.io.proceed('boilerplate asset copied.')
        else:
            self.io.proceed('boilerplate asset {!r} does not exist.'.format(boilerplate_asset_name))
