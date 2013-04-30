import abc
import os
import shutil
import subprocess
from abjad.tools import stringtools
from experimental.tools.scoremanagertools.core.ScoreManagerObject import ScoreManagerObject
from experimental.tools.scoremanagertools.menuing.UserInputGetter import UserInputGetter


class AssetProxy(ScoreManagerObject):
    '''Asset proxy.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta
    generic_class_name = 'asset'

    ### INITIALIZER ###

    def __init__(self, asset_path=None, session=None):
        assert isinstance(asset_path, (str, type(None))), repr(asset_path)
        ScoreManagerObject.__init__(self, session=session)
        self._asset_path = asset_path

    ### SPECIAL METHODS ###

    def __repr__(self):
        if self.asset_path:
            return '{}({!r})'.format(self._class_name, self.asset_path)
        else:
            return '{}()'.format(self._class_name)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def asset_path(self):
        return self._asset_path

    @property
    def breadcrumb(self):
        return self.name or self._human_readable_class_name

    @property
    def exists(self):
        if self.asset_path:
            return os.path.exists(self.asset_path)
        return False

    @property
    def human_readable_name(self):
        return self.name

    @property
    def is_versioned(self):
        if self.asset_path is None:
            return False
        if not os.path.exists(self.asset_path):
            return False
        command = 'svn st {}'.format(self.asset_path)
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        first_line = proc.stdout.readline()
        if first_line.startswith(('?', 'svn: warning:')):
            return False
        else:
            return True

    @property
    def name(self):
        if self.asset_path:
            return self.asset_path.split(os.path.sep)[-1]

    @property
    def name_without_extension(self):
        if self.name:
            if '.' in self.name:
                return self.name[:self.name.rindex('.')]
            else:
                return self.name

    @property
    def parent_directory_path(self):
        if self.asset_path:
            return os.path.dirname(self.asset_path)

    @property
    def plural_generic_class_name(self):
        return stringtools.pluralize_string(self.generic_class_name)

    @property
    def svn_add_command(self):
        if self.asset_path:
            return 'svn add {}'.format(self.asset_path)

    ### PUBLIC METHODS ###

    @abc.abstractmethod
    def conditionally_make_empty_asset(self, is_interactive=False):
        pass

    def copy(self, new_asset_path):
        shutil.copyfile(self.asset_path, new_asset_path)

    def copy_interactively(self, user_input=None):
        self.assign_user_input(user_input=user_input)
        getter = self.make_getter()
        getter.append_underscore_delimited_lowercase_file_name('new name')
        result = getter.run()
        if self.session.backtrack():
            return
        new_asset_name = self.human_readable_name_to_asset_name(result)
        new_path = os.path.join(self.parent_directory_path, new_asset_name)
        self.display('new path will be {}'.format(new_path))
        if not self.confirm():
            return
        self.copy(new_path)
        self.proceed('asset copied.')

    @abc.abstractmethod
    def fix(self):
        pass

    def human_readable_name_to_asset_name(self, human_readable_name):
        asset_name = human_readable_name.lower()
        asset_name = asset_name.replace(' ', '_')
        return asset_name

    @abc.abstractmethod
    def profile(self):
        pass

    def remove(self):
        if self.is_versioned:
            return self.remove_versioned_asset()
        else:
            return self.remove_nonversioned_asset()

    def remove_interactively(self, user_input=None):
        self.assign_user_input(user_input=user_input)
        self.display(['{} will be removed.'.format(self.asset_path), ''])
        getter = self.make_getter(where=self.where())
        getter.append_string("type 'remove' to proceed")
        result = getter.run()
        if self.session.backtrack():
            return
        if not result == 'remove':
            return
        if self.remove():
            self.proceed('{} removed.'.format(self.asset_path))

    def remove_nonversioned_asset(self):
        command = 'rm -rf {}'.format(self.asset_path)
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        proc.stdout.readline()
        return True

    def remove_versioned_asset(self, is_interactive=False):
        command = 'svn --force rm {}'.format(self.asset_path)
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        proc.stdout.readline()
        return True

    def rename(self, new_path):
        if self.is_versioned:
            result = self.rename_versioned_asset(new_path)
        else:
            result = self.rename_nonversioned_asset(new_path)

    def rename_interactively(self, user_input=None):
        self.assign_user_input(user_input=user_input)
        getter = self.make_getter(where=self.where())
        getter.append_underscore_delimited_lowercase_file_name('new human-readable name')
        getter.include_newlines = False
        result = getter.run()
        if self.session.backtrack():
            return
        new_path = os.path.join(self.parent_directory_path, result)
        self.display(['new path name will be: "{}"'.format(new_path), ''])
        if not self.confirm():
            return
        if self.rename(new_path):
            self.proceed('asset renamed.')

    def rename_nonversioned_asset(self, new_path):
        command = 'mv {} {}'.format(self.asset_path, new_path)
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        proc.stdout.readline()
        self._asset_path = new_path

    def rename_versioned_asset(self, new_path):
        command = 'svn --force mv {} {}'.format(self.asset_path, new_path)
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        proc.stdout.readline()
        self._asset_path = new_path

    def run(self, cache=False, clear=True, user_input=None):
        self.assign_user_input(user_input=user_input)
        self.session.cache_breadcrumbs(cache=cache)
        while True:
            self.session.push_breadcrumb(self.breadcrumb)
            menu = self.make_main_menu()
            result = menu.run(clear=clear)
            if self.session.backtrack(source=self._backtracking_source):
                break
            elif not result:
                self.session.pop_breadcrumb()
                continue
            self.handle_main_menu_result(result)
            if self.session.backtrack(source=self._backtracking_source):
                break
            self.session.pop_breadcrumb()
        self.session.pop_breadcrumb()
        self.session.restore_breadcrumbs(cache=cache)

    def run_first_time(self, **kwargs):
        self.run(**kwargs)

    def run_py_test(self, prompt=True):
        proc = subprocess.Popen('py.test {}'.format(self.asset_path), shell=True, stdout=subprocess.PIPE)
        lines = [line.strip() for line in proc.stdout.readlines()]
        if lines:
            self.display(lines)
        line = 'tests run.'
        self.proceed(line, is_interactive=prompt)

    def svn_add(self, is_interactive=False):
        if is_interactive:
            self.display(self.asset_path)
        proc = subprocess.Popen(self.svn_add_command, shell=True, stdout=subprocess.PIPE)
        lines = [line.strip() for line in proc.stdout.readlines()]
        lines.append('')
        if is_interactive:
            self.display(lines)
        self.proceed(is_interactive=is_interactive)

    def svn_ci(self, commit_message=None, is_interactive=True):
        if commit_message is None:
            getter = self.make_getter(where=self.where())
            getter.append_string('commit message')
            commit_message = getter.run()
            if self.session.backtrack():
                return
            line = 'commit message will be: "{}"\n'.format(commit_message)
            self.display(line)
            if not self.confirm():
                return
        lines = []
        lines.append(self.asset_path)
        command = 'svn commit -m "{}" {}'.format(commit_message, self.asset_path)
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        lines.extend([line.strip() for line in proc.stdout.readlines()])
        lines.append('')
        self.display(lines)
        self.proceed(is_interactive=is_interactive)

    def svn_st(self, is_interactive=True):
        if is_interactive:
            self.display(self.asset_path)
        command = 'svn st -u {}'.format(self.asset_path)
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        lines = [line.strip() for line in proc.stdout.readlines()]
        lines.append('')
        self.display(lines)
        self.proceed(is_interactive=is_interactive)

    def svn_up(self, is_interactive=True):
        if is_interactive:
            self.display(self.asset_path)
        command = 'svn up {}'.format(self.asset_path)
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        lines = [line.strip() for line in proc.stdout.readlines()]
        lines.append('')
        self.display(lines)
        self.proceed(is_interactive=is_interactive)

    def touch(self):
        os.system('touch {}'.format(self.asset_path))

    def write_boilerplate_asset_to_disk(self, boilerplate_asset_name):
        if not os.path.exists(boilerplate_asset_name):
            boilerplate_asset_name = os.path.join(
                self.configuration.boilerplate_directory_path, boilerplate_asset_name)
        if os.path.exists(boilerplate_asset_name):
            shutil.copyfile(boilerplate_asset_name, self.asset_path)
            return True

    def write_boilerplate_asset_to_disk_interactively(self, user_input=None):
        self.assign_user_input(user_input=user_input)
        getter = self.make_getter(where=self.where())
        getter.append_underscore_delimited_lowercase_file_name('name of boilerplate asset')
        self.session.push_backtrack()
        boilerplate_asset_name = getter.run()
        self.session.pop_backtrack()
        if self.session.backtrack():
            return
        if self.write_boilerplate_asset_to_disk(boilerplate_asset_name):
            self.proceed('boilerplate asset copied.')
        else:
            self.proceed('boilerplate asset {!r} does not exist.'.format(boilerplate_asset_name))
