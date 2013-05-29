import os
from experimental.tools.scoremanagertools.proxies.FilesystemAssetProxy import FilesystemAssetProxy


class FileProxy(FilesystemAssetProxy):

    ### CLASS VARIABLES ###

    _generic_class_name = 'file'
    _temporary_asset_name = 'temporary_file.txt'
    extension = ''

    ### PUBLIC METHODS ###

    def edit(self):
        os.system('vi + {}'.format(self.filesystem_path))

    def make_empty_asset(self, is_interactive=False):
        if not self.exists():
            file_reference = file(self.filesystem_path, 'w')
            file_reference.write('')
            file_reference.close()
        self._io.proceed(is_interactive=is_interactive)

    def read_lines(self):
        result = []
        if self.filesystem_path:
            if os.path.exists(self.filesystem_path):
                file_pointer = file(self.filesystem_path)
                result.extend(file_pointer.readlines())
                file_pointer.close()
        return result

    def view(self):
        os.system('vi -R {}'.format(self.filesystem_path))

    ### UI MANIFEST ###

    user_input_to_action = FilesystemAssetProxy.user_input_to_action.copy()
    user_input_to_action.update({
        'vi': edit,
        })
