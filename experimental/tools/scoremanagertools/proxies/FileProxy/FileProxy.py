import os
from experimental.tools.scoremanagertools.proxies.FilesystemAssetProxy import FilesystemAssetProxy


class FileProxy(FilesystemAssetProxy):

    ### CLASS ATTRIBUTES ###

    _generic_class_name = 'file'
    _temporary_asset_name = 'temporary_file.txt'
    extension = ''

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def file_lines(self):
        result = []
        if self.filesystem_path:
            if os.path.exists(self.filesystem_path):
                file_pointer = file(self.filesystem_path)
                result.extend(file_pointer.readlines())
                file_pointer.close()
        return result

    ### PUBLIC METHODS ###

    def display_formatted_lines(self):
        self._io.display(self.formatted_lines)

    def edit(self):
        os.system('vi + {}'.format(self.filesystem_path))

    def has_line(self, line):
        file_reference = open(self.filesystem_path, 'r')
        for file_line in file_reference.readlines():
            if file_line == line:
                file_reference.close()
                return True
        file_reference.close()
        return False

    def make_empty_asset(self, is_interactive=False):
        if not self.exists():
            file_reference = file(self.filesystem_path, 'w')
            file_reference.write('')
            file_reference.close()
        self._io.proceed(is_interactive=is_interactive)

    def view(self):
        os.system('vi -R {}'.format(self.filesystem_path))
