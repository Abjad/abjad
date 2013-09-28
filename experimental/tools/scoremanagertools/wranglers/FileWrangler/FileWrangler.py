# -*- encoding: utf-8 -*-
from experimental.tools.scoremanagertools.wranglers.FilesystemAssetWrangler \
    import FilesystemAssetWrangler


class FileWrangler(FilesystemAssetWrangler):

    ### INITIALIZER ###

    def __init__(self, session=None):
        from experimental.tools import scoremanagertools
        superclass = super(FileWrangler, self)
        superclass.__init__(session=session)
        self._asset_manager_class = scoremanagertools.managers.FileManager
