# -*- encoding: utf-8 -*-
from scoremanager.wranglers.FilesystemAssetWrangler \
    import FilesystemAssetWrangler


class FileWrangler(FilesystemAssetWrangler):

    ### INITIALIZER ###

    def __init__(self, session=None):
        from scoremanager import managers
        superclass = super(FileWrangler, self)
        superclass.__init__(session=session)
        self._asset_manager_class = managers.FileManager
