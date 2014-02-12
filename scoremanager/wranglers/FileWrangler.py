# -*- encoding: utf-8 -*-
from scoremanager.wranglers.FilesystemAssetWrangler \
    import FilesystemAssetWrangler


class FileWrangler(FilesystemAssetWrangler):

    ### INITIALIZER ###

    def __init__(self, session=None):
        from experimental.tools import scoremanager
        superclass = super(FileWrangler, self)
        superclass.__init__(session=session)
        self._asset_manager_class = scoremanager.managers.FileManager
