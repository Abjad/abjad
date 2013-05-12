import os
import subprocess
from experimental.tools.scoremanagertools.proxies.FilesystemAssetProxy import FilesystemAssetProxy


class DirectoryProxy(FilesystemAssetProxy):

    ### INITIALIZER ###

    def __init__(self, directory_path=None, session=None):
        FilesystemAssetProxy.__init__(self, filesystem_path=directory_path, session=session)

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _svn_add_command(self):
        return 'cd {} && svn-add-all'.format(self.directory_path)

    ### PUBLIC METHODS ###

    def get_filesystem_path_interactively(self):
        getter = self._io.make_getter(where=self._where)
        getter.append_string('directory path')
        result = getter._run()
        if self._session.backtrack():
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
        if not self.exists:
            os.mkdir(self.filesystem_path)
        self._io.proceed(is_interactive=is_interactive)

    def print_directory_entries(self):
        self._io.display(self.list_directory(), capitalize_first_character=False)
        self._io.display('')
        self._session.hide_next_redraw = True

    def run_py_test(self, prompt=True):
        proc = subprocess.Popen('py.test {}'.format(self.filesystem_path), shell=True, stdout=subprocess.PIPE)
        lines = [line.strip() for line in proc.stdout.readlines()]
        if lines:
            self._io.display(lines)
        line = 'tests run.'
        self._io.proceed(line, is_interactive=prompt)
