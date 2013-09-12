# -*- encoding: utf-8 -*-
import os
from experimental.tools.scoremanagertools.proxies.FilesystemAssetProxy \
    import FilesystemAssetProxy


class FileProxy(FilesystemAssetProxy):
    r'''File proxy.
    '''

    ### CLASS VARIABLES ###

    _generic_class_name = 'file'

    _temporary_asset_name = 'temporary_file.txt'

    extension = ''

    ### PUBLIC METHODS ###

    def interactively_edit(self):
        r'''Interactively edits file.

        Returns none.
        '''
        os.system('vim + {}'.format(self.filesystem_path))

    def interactively_view(self):
        r'''Interactively views file.

        Returns none.
        '''
        os.system('vim -R {}'.format(self.filesystem_path))

    def make_empty_asset(self, is_interactive=False):
        r'''Makes emtpy file.

        Returns none.
        '''
        if not self.exists():
            file_reference = file(self.filesystem_path, 'w')
            file_reference.write('')
            file_reference.close()
        self.session.io_manager.proceed(is_interactive=is_interactive)

    def read_lines(self):
        r'''Reads lines in file.

        Returns list.
        '''
        result = []
        if self.filesystem_path:
            if os.path.exists(self.filesystem_path):
                file_pointer = file(self.filesystem_path)
                result.extend(file_pointer.readlines())
                file_pointer.close()
        return result

    ### UI MANIFEST ###

    user_input_to_action = FilesystemAssetProxy.user_input_to_action.copy()
    user_input_to_action.update({
        'vim': interactively_edit,
        'vw': interactively_view,
        })
