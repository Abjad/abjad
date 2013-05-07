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

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def directory_path(self):
        return self.filesystem_path

    @property
    def public_content_names(self):
        result = []
        #for name in os.listdir(self.directory_path):
        for name in os.listdir(self.filesystem_path):
            if name[0].isalpha():
                if not name.endswith('.pyc'):
                    result.append(name)
        return result

    ### PUBLIC METHODS ###

    def conditionally_make_empty_asset(self, is_interactive=False):
        self.print_not_yet_implemented()

    def fix(self, is_interactive=False):
        pass

    #def get_directory_path_interactively(self):
    def get_filesystem_path_interactively(self):
        getter = self.io.make_getter(where=self.where())
        getter.append_string('directory path')
        result = getter.run()
        if self.session.backtrack():
            return
        #self.directory_path = result
        self.filesystem_path = result

    def list_directory(self):
        result = []
        #for file_name in os.listdir(self.directory_path):
        for file_name in os.listdir(self.filesystem_path):
            if file_name.endswith('.pyc'):
                #file_path = os.path.join(self.directory_path, file_name)
                file_path = os.path.join(self.filesystem_path, file_name)
                os.remove(file_path)
        #for name in os.listdir(self.directory_path):
        for name in os.listdir(self.filesystem_path):
            if not name.startswith('.'):
                result.append(name)
        return result

    def make_directory(self):
        #os.mkdir(self.directory_path)
        os.mkdir(self.filesystem_path)

    def print_directory_contents(self):
        self.io.display(self.list_directory(), capitalize_first_character=False)
        self.io.display('')
        self.session.hide_next_redraw = True

    def profile(self):
        pass
