import os
import subprocess
from experimental.tools.scoremanagertools.proxies.AssetProxy import AssetProxy


class DirectoryProxy(AssetProxy):

    ### INITIALIZER ###

    def __init__(self, directory_path=None, session=None):
        AssetProxy.__init__(self, asset_path=directory_path, session=session)

    ### SPECIAL METHODS ###

    def __eq__(self, other):
        if isinstance(other, type(self)):
            if self.directory_path == other.directory_path:
                return True
        return False

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        return '{}({!r})'.format(self._class_name, self.directory_path)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def directory_contents(self):
        result = []
        for file_name in os.listdir(self.directory_path):
            if file_name.endswith('.pyc'):
                file_path = os.path.join(self.directory_path, file_name)
                os.remove(file_path)
        for name in os.listdir(self.directory_path):
            if not name.startswith('.'):
                result.append(name)
        return result

    @property
    def directory_path(self):
        return self.asset_path

    @property
    def public_content_names(self):
        result = []
        for name in os.listdir(self.directory_path):
            if name[0].isalpha():
                if not name.endswith('.pyc'):
                    result.append(name)
        return result

    @property
    def svn_add_command(self):
        return 'cd {} && svn-add-all'.format(self.directory_path)

    ### PUBLIC METHODS ###

    def conditionally_make_empty_asset(self, is_interactive=False):
        self.print_not_yet_implemented()

    def fix(self, is_interactive=False):
        pass

    def get_directory_path_interactively(self):
        getter = self.make_getter(where=self.where())
        getter.append_string('directory name')
        result = getter.run()
        if self.backtrack():
            return
        self.directory_path = result

    def make_directory(self):
        os.mkdir(self.directory_path)

    def print_directory_contents(self):
        self.display(self.directory_contents, capitalize_first_character=False)
        self.display('')
        self.session.hide_next_redraw = True

    def profile(self):
        pass
