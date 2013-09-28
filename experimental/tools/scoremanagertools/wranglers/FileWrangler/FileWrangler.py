# -*- encoding: utf-8 -*-
from experimental.tools.scoremanagertools.wranglers.FilesystemAssetWrangler \
    import FilesystemAssetWrangler


class FileWrangler(FilesystemAssetWrangler):

    ### PUBLIC PROPERTIES ###

    @property
    def asset_manager_class(self):
        r'''File wrangler asset manager class.

        Returns class.
        '''
        from experimental.tools import scoremanagertools
        return scoremanagertools.managers.FileManager
