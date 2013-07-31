# -*- encoding: utf-8 -*-
import os
import subprocess
from experimental.tools.scoremanagertools.proxies.FilesystemAssetProxy \
    import FilesystemAssetProxy


class DirectoryProxy(FilesystemAssetProxy):

    ### PRIVATE PROPERTIES ###

    @property
    def _svn_add_command(self):
        return 'cd {} && svn-add-all'.format(self.filesystem_path)

    ### PUBLIC METHODS ###

    def interactively_get_filesystem_path(self):
        getter = self.session.io_manager.make_getter(where=self._where)
        getter.append_string('directory path')
        result = getter._run()
        if self.session.backtrack():
            return
        self.filesystem_path = result

    def list_directory(self, public_entries_only=False):
        result = []
        if public_entries_only:
            for directory_entry in os.listdir(self.filesystem_path):
                if directory_entry[0].isalpha() and \
                    not directory_entry.endswith('.pyc'):
                    result.append(directory_entry)
        else:
            for directory_entry in os.listdir(self.filesystem_path):
                if not directory_entry.startswith('.') and \
                    not directory_entry.endswith('.pyc'):
                    result.append(directory_entry)
        return result

    def make_empty_asset(self, is_interactive=False):
        if not self.exists():
            os.mkdir(self.filesystem_path)
        self.session.io_manager.proceed(is_interactive=is_interactive)

    def print_directory_entries(self):
        self.session.io_manager.display(
            self.list_directory(), capitalize_first_character=False)
        self.session.io_manager.display('')
        self.session.hide_next_redraw = True

    def run_py_test(self, prompt=True):
        command = 'py.test {}'.format(self.filesystem_path)
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        lines = [line.strip() for line in proc.stdout.readlines()]
        if lines:
            self.session.io_manager.display(lines)
        line = 'tests run.'
        self.session.io_manager.proceed(line, is_interactive=prompt)

    ### UI MANIFEST ###

    user_input_to_action = {
        'ls': print_directory_entries,
        'py.test': run_py_test,
        }
